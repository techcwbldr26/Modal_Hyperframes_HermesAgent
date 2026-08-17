"""CLI for the Qwen3.8-27B endpoint.

Usage:
    python client/cli.py ask "What is an agent harness?"
    python client/cli.py ask "Describe this diagram" --image path/to/diagram.png
    python client/cli.py ask "Analyze this video" --video path/to/clip.mp4
    python client/cli.py models
    python client/cli.py verify
"""
import argparse
import json
import os
import sys
import time

# Add parent dir to path for qwen_client import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.qwen_client import QwenClient, QWEN_MODEL, QWEN_BASE_URL


def cmd_models(client: QwenClient):
    """List available models."""
    models = client.client.models.list()
    for m in models.data:
        print(f"  {m.id} (max_len={m.max_model_len})")


def cmd_verify(client: QwenClient):
    """Quick health check: models + a tiny completion."""
    t0 = time.time()
    models = client.client.models.list()
    names = [m.id for m in models.data]
    print(f"[1/2] /v1/models OK ({time.time()-t0:.1f}s): {names}")
    if QWEN_MODEL not in names:
        print(f"FAIL: {QWEN_MODEL} not found")
        sys.exit(1)
    t0 = time.time()
    resp = client.ask_text("Reply with exactly: ok", reasoning_effort="low", max_tokens=64)
    print(f"[2/2] completion OK ({time.time()-t0:.1f}s): {resp!r}")
    print("Endpoint verified ✅")


def cmd_ask(client: QwenClient, args):
    """Send a prompt with optional image/video input."""
    if args.image:
        resp = client.ask_image(
            args.image, args.prompt,
            reasoning_effort=args.reasoning_effort,
            max_tokens=args.max_tokens,
        )
    elif args.video:
        resp = client.ask_video(
            args.video, args.prompt,
            reasoning_effort=args.reasoning_effort,
            max_tokens=args.max_tokens,
        )
    else:
        resp = client.ask_text(
            args.prompt,
            reasoning_effort=args.reasoning_effort,
            max_tokens=args.max_tokens,
        )
    print(resp)


def main():
    parser = argparse.ArgumentParser(description="Qwen3.8-27B CLI")
    parser.add_argument("--base-url", default=os.environ.get("QWEN_BASE_URL", QWEN_BASE_URL))
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("models", help="List available models")
    sub.add_parser("verify", help="Health check")

    ask = sub.add_parser("ask", help="Send a prompt")
    ask.add_argument("prompt", help="Text prompt")
    ask.add_argument("--image", help="Image file path or URL")
    ask.add_argument("--video", help="Video file path or URL")
    ask.add_argument("--reasoning-effort", default="xhigh",
                     choices=["xhigh", "medium", "low"])
    ask.add_argument("--max-tokens", type=int, default=8192)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = QwenClient(base_url=args.base_url)

    if args.command == "models":
        cmd_models(client)
    elif args.command == "verify":
        cmd_verify(client)
    elif args.command == "ask":
        cmd_ask(client, args)


if __name__ == "__main__":
    main()