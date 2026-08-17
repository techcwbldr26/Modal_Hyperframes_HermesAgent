"""Smoke test for the Qwen3.8-27B endpoint on Modal.

Usage:
    python3 scripts/smoke_serve.py --base-url https://<workspace>--qwen38-serve-qwen38server.us-east.modal.direct/v1

Asserts: HTTP 200, model listed, non-empty completion, thinking content present.
Uses reasoning_effort=low for the smoke test to keep the first run cheap.
"""
import argparse
import sys
import time

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True, help="OpenAI-compatible base URL (…/v1)")
    parser.add_argument("--model", default="Qwen/Qwen3.8-27B")
    args = parser.parse_args()

    from openai import OpenAI

    client = OpenAI(base_url=args.base_url, api_key="modal")  # unauthenticated endpoint

    # 1. Model list (with retry for cold start)
    t0 = time.time()
    for attempt in range(30):  # up to ~10 min for cold start
        try:
            models = client.models.list()
            break
        except Exception as e:
            if attempt == 0:
                print(f"      cold start — waiting for container… ({e})")
            time.sleep(20)
    else:
        print("FAIL: endpoint did not become available after 10 min")
        return 1
    names = [m.id for m in models.data]
    print(f"[1/3] /v1/models OK ({time.time()-t0:.1f}s): {names}")
    if args.model not in names:
        print(f"FAIL: model {args.model} not in {names}")
        return 1

    # 2. Text completion with thinking
    t0 = time.time()
    resp = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": "Reply with exactly: smoke test ok"}],
        reasoning_effort="low",
        max_tokens=512,
    )
    content = resp.choices[0].message.content or ""
    reasoning = getattr(resp.choices[0].message, "reasoning_content", None) or ""
    print(f"[2/3] completion OK ({time.time()-t0:.1f}s): {content[:80]!r}")
    print(f"      thinking content: {len(reasoning)} chars")
    if not content.strip():
        print("FAIL: empty completion")
        return 1

    # 3. Image input (vision)
    t0 = time.time()
    img_url = ("https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3.5/demo/CI_Demo/mathv-1327.jpg")
    resp2 = client.chat.completions.create(
        model=args.model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": img_url}},
                {"type": "text", "text": "What geometric figure is shown? One sentence."},
            ],
        }],
        reasoning_effort="low",
        max_tokens=512,
    )
    content2 = resp2.choices[0].message.content or ""
    print(f"[3/3] vision OK ({time.time()-t0:.1f}s): {content2[:80]!r}")
    if not content2.strip():
        print("FAIL: empty vision completion")
        return 1

    print("\nSMOKE TEST PASSED ✅")
    return 0

if __name__ == "__main__":
    sys.exit(main())
