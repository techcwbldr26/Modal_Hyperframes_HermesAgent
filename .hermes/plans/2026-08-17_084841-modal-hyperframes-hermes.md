# Modal + HyperFrames + Hermes Agent Project — Implementation Plan

> **For Hermes:** Execute task-by-task with `delegate_task` (subagent-driven development), one task per subagent where practical, two-stage review (spec compliance, then code quality) after each task. All GPU/long-running jobs must run with `background=true, notify_on_complete=true` and be logged to `logs/` — never polled.

**Goal:** Build a production-grade project that serves **Qwen3.8-27B** (BF16, thinking mode) on **Modal H200** (141 GB SXM, FP8-capable), drives it through **Hermes Agent** via a registered **Modal MCP server** (`techcwbldr26/modal-mcp-server`, already cloned locally), and uses **HyperFrames** as the video/render layer — with all dependencies verified against live sources and Xet-based model transfers (Git LFS deprecated). The **first official full test** is a **5–7 minute client-demo video** built from the `harness-engineering/` technical course (10 sections, 10 diagram PNGs, 10 animated HTML slides), with Qwen3.8-27B providing vision analysis of the diagrams at **`reasoning_effort=xhigh`** (per the model card: lower effort causes insufficient analysis, more failures, and repeated retries — increasing total latency and token consumption), a **custom voiceover script paced for a beginner at human reading speed** (user records with their own voice), and the composition following the `hot-tips-08-17-2026-hyperframes.txt` authoring contract.

**Architecture:** One Modal app (`qwen38_serve.py`) exposing an OpenAI-compatible vLLM endpoint on an H200, weights + vLLM JIT artifacts cached on persistent Modal Volumes (auto-scaling storage — Modal Volumes scale to TB, ~$0.09/GiB/mo with 1 TiB free). Hermes talks to Modal through the MCP server (stdio transport) and to the endpoint via OpenAI-compatible HTTP. HyperFrames composes/renders the harness-engineering course video locally (or via `hyperframes cloud render`); the Qwen endpoint is the vision/video-intelligence layer that analyzes the course diagrams into scene descriptions.

**Tech Stack:** Modal SDK 1.5.2 (already installed via `uv tool install modal`), vLLM ≥ 0.17.0 (official Qwen3.8 recipe; latest line as of Aug 2026), huggingface_hub ≥ 0.32.0 (hf_xet / Xet by default), HyperFrames CLI (Node 22+, FFmpeg), Hermes Agent (installed), modal-mcp-server 0.1.0 (local checkout).

---

**Date researched:** 2026-08-17

**Sources verified (live web):**
- Qwen3.8-27B model card + exact generation parameters (thinking mode: `temperature=1.0, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0, repetition_penalty=1.0`; `reasoning_effort` levels `xhigh` (default) / `medium` / `low`; `preserve_thinking` on by default; 262,144-token native context): <https://huggingface.co/Qwen/Qwen3.8-27B>
- Qwen3.8-27B vLLM recipe (vLLM ≥ 0.17.0; `--reasoning-parser qwen3`, `--tool-call-parser qwen3_coder`, `--enable-auto-tool-choice`, `--mm-encoder-tp-mode data`; NVFP4 quant `Inferact/Qwen3.8-27B-NVFP4`): <https://recipes.vllm.ai/Qwen/Qwen3.8-27B>
- vLLM BF16 sizing: 51.7 GB checkpoint → single 80 GB GPU (H100/H200) fits BF16: <https://www.orcarouter.ai/blog/qwen-3-8-27b-vllm>
- Modal GPU docs — H200 (SXM, 141 GB, 4.8 TB/s, FP8), H100 → H200 automatic upgrade, `gpu="H200"`: <https://modal.com/docs/guide/gpu>
- Modal pricing — H200 SXM $0.001261/sec (~$4.54/hr); Volumes $0.09/GiB/mo, **1 TiB free**; $30/mo free compute: <https://modal.com/pricing>
- Modal official vLLM examples — `@app.server` + volumes pattern, `HF_XET_HIGH_PERFORMANCE=1`, HF cache volume at `/root/.cache/huggingface`: <https://github.com/modal-labs/modal-examples/blob/main/06_gpu_and_ml/llm-serving/vllm_inference.py> and `lfm_snapshot.py`
- HF Xet backend — Xet is the Hub's standard storage backend; Git LFS remains only for legacy/backwards compatibility; `hf_xet` bundled with huggingface_hub ≥ 0.32.0; adaptive concurrency default, `HF_XET_HIGH_PERFORMANCE=1` for high-bandwidth machines (≥ 64 GB RAM); `HF_HUB_ENABLE_HF_TRANSFER` deprecated: <https://huggingface.co/docs/hub/en/xet/index>, <https://huggingface.co/docs/hub/xet/using-xet-storage>, <https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables>
- Hermes Agent CLI (MCP add/list/test, config, skills): <https://hermes-agent.nousresearch.com/docs>

**Environment audit performed (local, 2026-08-17):**
- `hermes mcp list` → only `krea-ai` and `microsoft_learn`. **Modal MCP is NOT registered.** The skill reference config for Modal MCP is confirmed correct for this project.
- `modal --version` → 1.5.2; `modal profile current` → `tamazightdev`; `modal secret list` → `huggingface-token` (created 2026-07-25, last used 2026-08-04). Modal CLI auth works.
- `~/Desktop/modal-mcp-server` exists (git origin `https://github.com/techcwbldr26/modal-mcp-server.git`, v0.1.0, deps `modal>=1.5.2,<1.6`, `mcp[cli]>=1.28,<2`, `cbor2`, `python-dotenv`; `.env.example` present; README confirms it reads `~/.modal.toml` automatically — no env tokens needed).
- `~/.hermes/config.yaml` `mcp_servers:` block contains only krea-ai and microsoft_learn; terminal backend is `local`; `modal_mode: auto`.
- Workspace contains: empty root (fresh project), plus **`hot-tips-08-17-2026-hyperframes.txt`** (HyperFrames agent authoring guide) and **`harness-engineering/`** (first full test content: `agent_harness_technical_course.md` 10 sections, `implementation_plan.md`, `minimal_harness.py`, 2 reference PDFs, 10 section diagram PNGs in `images/diagrams/`, 2 Figma export zips).
- **Missing files noted in `harness-engineering/README.md`:** `slides/` (10 animated HTML slides) and `v3_Youtube_Technical_Course_System_Prompt.md` are referenced but **not present** in the repo. Flag to user; do not fabricate them.

---

## Corrections to assumptions in the brief (verified against live sources)

| Brief claim | Verified fact | Impact |
|---|---|---|
| Model needs ~100 GB on Modal | **~52 GB** total: two ~25.9 GB safetensors (BF16 27B ≈ 51.7 GB) + small files. `unsloth/Qwen3.8-27B-NVFP4` quant is ~23.4 GB if a lighter option is ever needed | Saves ~50 GB volume cost; H200's 141 GB is ample |
| "Qwen 3.8, 28B parameters" | Model card: **27B** params, 64 layers, hidden 5120, context 262,144 (extensible to 1M via YaRN) | Use `Qwen/Qwen3.8-27B` everywhere |
| LFS deprecated → must use Xet | Xet is already the **default** Hub transfer backend; `hf_xet` ships with huggingface_hub ≥ 0.32.0; `HF_HUB_ENABLE_HF_TRANSFER` is deprecated | No LFS anywhere; set `HF_XET_HIGH_PERFORMANCE=1` in image + volume-cached downloads |
| Reasoning params | Confirmed exactly as stated: thinking mode `temp=1.0, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0, repetition_penalty=1.0`; `reasoning_effort` `xhigh` default | Encode these as endpoint defaults so all Hermes/MCP calls inherit them |
| H200 on Modal | Confirmed: `gpu="H200"` (SXM 141 GB, 4.8 TB/s, FP8); $0.001261/s; H100 requests auto-upgrade to H200 | Use `gpu="H200"` |
| Modal auto-scales storage | Volumes are the storage primitive: scale to TB, **1 TiB free** then $0.09/GiB/mo; vLLM server auto-scales containers (`target_concurrency`, `scaledown_window`) | Verified pattern from modal-examples; documented in plan |

---

## Execution gotchas discovered (2026-08-17)

| Gotcha | Fix |
|---|---|
| `@app.server()` must decorate a **class** in Modal 1.5.2 (function form raises `TypeError: The @app.server() decorator must be used on a class.`) | Class-based pattern with `@modal.enter()` starting the vLLM subprocess (see `qwen38_serve.py`) |
| `modal app validate` does not exist in CLI 1.5.2 | Local validation: `uv run --with "modal>=1.5.2,<1.6" python -c "import qwen38_serve"` — catches decorator/import errors with zero GPU spend |
| `modal quota show` does not exist in CLI 1.5.2 | Use `modal billing report --for "this month" --show-resources` |
| `hermes mcp add` interactive tool-enable prompt cancels in non-TTY shells | Pipe the answer: `echo "Y" \| hermes mcp add ...` |
| `hermes mcp add --env` places values into `args` instead of an `env:` block | Fix `~/.hermes/config.yaml` with a Python yaml script (never `patch` tool) |
| `timeout` command missing on macOS | Use Python deadline loops (`urllib` + `time.time()`) or `gtimeout` (coreutils) |

---

## Inputs for the first full test (already in workspace)

1. **`hot-tips-08-17-2026-hyperframes.txt`** — the HyperFrames authoring contract for this project. It defines:
   - **Rule of Three:** root element (`data-composition-id`, `data-width="1920"`, `data-height="1080"`, `data-start`, `data-duration`), timed clip elements (`class="clip"`, `data-start`, `data-duration`, `data-track-index`), and GSAP timeline registration under `window.__timelines["<composition-id>"]` initialized with `{ paused: true }`.
   - **Design system:** dark tech theme `#090d16` slate gradient, ambient glow + grid overlays; Inter (headers/body) + JetBrains Mono (badges/code/metrics); glassmorphism cards (`rgba(22,27,38,0.85)`, `backdrop-filter: blur(12px)`, `1px rgba(255,255,255,0.1)` border); electric accents Cyan `#38bdf8`, Emerald `#3fb950`, Amber `#d29922`, Ruby `#f85149`, Purple `#a371f7`; brick-snapping diagram nodes, glowing SVG connectors, kinetic text reveals, syntax-highlighted code, timeline progress bars.
   - **Pacing standards (non-negotiable):** badge/title 0.7s after clip fade-in; subtitle 1.8s after title; first card 3.0s after subtitle; second card 8–10s after first card (Two-Card Rule — never same stagger call); bullets 1.5s min stagger; diagram nodes 5s between; code lines 0.8s; callout in last 10–12s of clip.
   - **Gotchas:** render with project dir (`.`) not `index.html`; FFmpeg/FFprobe on PATH (static binaries in project root if missing); blank-screen fallback `if (!window.location.search.includes('hyperframes') && !window.__HYPERFRAMES__) { tl.play(); }`; audio lint (no untimed `<audio>`, files must exist in `assets/`).
   - **Quality check protocol:** composition-id matches `window.__timelines` key exactly; timeline `{ paused: true }`; root `data-duration` = sum of clip durations; `body`/`#root` `width: 1920px; height: 1080px; overflow: hidden;`.
   - **Action:** copy this file into the project as `hyperframes/HYPERFRAMES_HOT_TIPS.md` (versioned with the repo) and treat it as the composition contract for Tasks 7–8.

2. **`harness-engineering/`** — the first full test subject matter:
   - `agent_harness_technical_course.md` (1,139 lines): complete 10-section course (OS analogy, framework vs harness, execution loop, context compaction, tools/skills, subagent delegation, persistence/prompt assembly, hooks/permissions, NLAH/Meta-Harness research, minimal harness synthesis).
   - `images/diagrams/sec-1 … sec-10` PNGs: one architecture diagram per section — these are the Qwen vision inputs.
   - **`slides/section_1 … section_10` HTML files (10, now present):** high-fidelity animated slides with the exact visual design per section — the authoritative visual reference for each clip's layout, callout positions, and animation timing.
   - `minimal_harness.py`: zero-dependency 9-component reference implementation (used in Section 10 content).
   - `implementation_plan.md`: per-section granular breakdown with timestamps.
   - 2 reference PDFs (Muhammad Farooq essays).

---

## Project layout (all paths relative to workspace root)

```
modal-hyperframes-hermes/
├── AGENTS.md                          # Agent instructions (8-section spec, Boundaries)
├── .env.example                       # Non-secret template; .env gitignored
├── .gitignore
├── README.md
├── qwen38_serve.py                    # Modal vLLM server (H200, Xet, volumes)
├── requirements.txt                   # Local dev deps (modal, openai, pytest)
├── client/
│   ├── qwen_client.py                 # OpenAI-compatible client w/ official sampling params
│   └── cli.py                         # CLI: ask / image / video / verify-endpoint
├── scripts/
│   ├── smoke_serve.py                 # Endpoint health + first-completion smoke test
│   └── analyze_scene.py               # Qwen vision analysis of diagrams → scene JSON
├── hyperframes/                       # HyperFrames project (init in Task 7)
│   ├── HYPERFRAMES_HOT_TIPS.md        # Copy of the hot-tips authoring contract
│   └── (init-generated files + compositions/)
├── harness-engineering/               # EXISTING — first full test input (do not modify)
├── tests/
│   └── test_qwen_client.py            # Unit tests for client params/serialization
└── logs/                              # gitignored; modal run output lives here
```

---

## Task 1: Scaffold project (git init, AGENTS.md, .env.example, .gitignore, README skeleton)

**Objective:** Create the repo skeleton with security hygiene (no secrets ever committed) and agent instructions.

**Files:**
- Create: `AGENTS.md` (plain Markdown, no YAML frontmatter; ~100–150 lines; write via `execute_code`/Python `open()`, not `write_file` — AGENTS.md is a protected file for the `write_file` tool)
- Create: `.env.example` — `MODAL_TOKEN_ID=`, `MODAL_TOKEN_SECRET=` (optional, CLI uses `~/.modal.toml`), `MODAL_ENVIRONMENT=` (main), `HF_TOKEN=` (optional local mirror of Modal secret), `MODAL_MCP_READ_ONLY=false`, `MODAL_MCP_ENABLED_TOOLSETS=discovery,apps,functions,volumes,storage,secrets,servers,containers,workspace`, `MODEL_REPO=Qwen/Qwen3.8-27B`, `QWEN_BASE_URL=https://<your-workspace>--qwen38-serve.modal.run/v1` (fill after Task 5), `TEMPERATURE=1.0`, `TOP_P=0.95`, `TOP_K=20`, `MIN_P=0.0`, `PRESENCE_PENALTY=0.0`, `REPETITION_PENALTY=1.0`, `REASONING_EFFORT=xhigh`
- Create: `.gitignore` — `.env`, `.venv/`, `logs/`, `__pycache__/`, `*.pyc`, `.DS_Store`, `out*.mp4`
- Create: `README.md` skeleton (title, one-paragraph architecture, status placeholders)
- Create: `logs/.gitkeep`

**Step 1:** `git init` in workspace root; create files above.

**Step 2:** Verify: `git status` shows only intended files; `.env` absent; `AGENTS.md` readable.

**Step 3:** Commit: `feat: scaffold project skeleton (AGENTS.md, env template, gitignore)`.

**Note:** Do NOT create a `.env` with real tokens. Per the credentials rule, ask the user before writing any real token into `.env`; CLI auth already works via `~/.modal.toml`.

---

## Task 2: Register & verify Modal MCP server in Hermes

**Objective:** Wire `~/Desktop/modal-mcp-server` into Hermes so Modal platform tools appear as first-class Hermes tools.

**Step 1:** Configure via CLI (the `patch` tool refuses to edit `~/.hermes/config.yaml`; CLI also avoids the `--env`-into-`args` pitfall by using the `env` block):

```bash
hermes mcp add modal \
  --command "uv" \
  --args "--directory" "/Users/gregorykennedy-salemi/Desktop/modal-mcp-server" "run" "modal-mcp-server" "--transport" "stdio"
```

**Step 2:** Verify the saved config and fix any env/args misplacement with a small Python yaml edit (as the modal skill prescribes):

```bash
grep -A 25 "modal:" ~/.hermes/config.yaml
```

Ensure the `modal` entry looks like:

```yaml
modal:
  command: "uv"
  args: ["--directory", "/Users/gregorykennedy-salemi/Desktop/modal-mcp-server", "run", "modal-mcp-server", "--transport", "stdio"]
  env:
    MODAL_MCP_READ_ONLY: "false"
    MODAL_MCP_ENABLED_TOOLSETS: "discovery,apps,functions,volumes,storage,secrets,servers,containers,workspace"
  tools:
    exclude: []
```

(If `hermes mcp add` placed `--env` values into `args`, fix with a Python `yaml.safe_load`/`yaml.dump` script — never with `patch`.)

**Step 3:** Test:

```bash
hermes mcp test modal
```

Expected: connection succeeds and tools are discovered (volumes, apps, functions, secrets, servers, storage toolsets).

**Step 4:** Verify Hermes sees the tools: `hermes mcp list` shows `modal ... ✓ enabled`.

**Step 5:** Record result in `README.md` ("Modal MCP: registered & verified").

> **Note:** MCP tools only load at session start. New tools appear after `/reset` or a new session — so Task 2 should be done early; the next session will have Modal tools for the full test.

---

## Task 3: Verify Modal account state (workspace, volume quota, HF secret)

**Objective:** Confirm billing/workspace state and HF secret before spending any GPU time (the Krea lesson: verify actual state before quoting budget).

**Step 1:**

```bash
modal profile current          # tamazightdev (expected)
modal secret list              # huggingface-token present (expected)
modal volume list              # expected empty; create in Task 4
modal quota show               # GPU concurrency / spend headroom on plan
```

**Step 2:** Record results in `README.md` (a "Verified environment" table). No commit of any credential.

**Step 3:** Ask the user for the go-ahead on spend only if quota looks tight; otherwise proceed.

---

## Task 4: Write `qwen38_serve.py` — Modal vLLM server on H200

**Objective:** Modal app that serves Qwen3.8-27B (BF16) with vLLM on `gpu="H200"`, weights and JIT artifacts cached on Modal Volumes, Xet-accelerated downloads, official Qwen sampling defaults.

**Files:**
- Create: `qwen38_serve.py`

**Step 1: Write the app** (complete, copy-pasteable):

```python
"""Serverless Qwen3.8-27B (BF16, thinking mode) on Modal H200 via vLLM.

OpenAI-compatible endpoint: https://<workspace>--qwen38-serve.modal.run/v1
Model weights + vLLM JIT artifacts persist on Modal Volumes (Xet downloads).
Sampling defaults follow the official Qwen3.8 model card:
  thinking mode: temperature=1.0, top_p=0.95, top_k=20, min_p=0.0,
                 presence_penalty=0.0, repetition_penalty=1.0
  reasoning_effort: xhigh (default) | medium | low
"""
import os
import subprocess
import time

import modal

MODEL_REPO = os.environ.get("MODEL_REPO", "Qwen/Qwen3.8-27B")
# Official model-card defaults for thinking mode
TEMPERATURE = float(os.environ.get("TEMPERATURE", "1.0"))
TOP_P = float(os.environ.get("TOP_P", "0.95"))
TOP_K = int(os.environ.get("TOP_K", "20"))
MIN_P = float(os.environ.get("MIN_P", "0.0"))
PRESENCE_PENALTY = float(os.environ.get("PRESENCE_PENALTY", "0.0"))
REPETITION_PENALTY = float(os.environ.get("REPETITION_PENALTY", "1.0"))
REASONING_EFFORT = os.environ.get("REASONING_EFFORT", "xhigh")

VLLM_PORT = 8000
GPU = os.environ.get("GPU", "H200")           # SXM 141 GB, 4.8 TB/s, FP8
MINUTES = 60

app = modal.App("qwen38-serve")

# Persistent, auto-scaling storage: 1 TiB free, then $0.09/GiB/mo.
hf_cache_vol = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)

# Existing secret in this workspace (created 2026-07-25).
hf_secret = modal.Secret.from_name("huggingface-token")

vllm_image = (
    modal.Image.from_registry("nvidia/cuda:12.9.0-devel-ubuntu22.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install(
        "vllm>=0.17.0",            # official Qwen3.8 recipe line (Aug 2026)
        "huggingface_hub>=0.32.0", # ships hf_xet (Xet) by default
    )
    .env(
        {
            "HF_HUB_CACHE": "/root/.cache/huggingface",
            # Xet: saturate bandwidth (LFS is deprecated on the Hub)
            "HF_XET_HIGH_PERFORMANCE": "1",
            "VLLM_USE_V1": "1",
        }
    )
)


def _wait_ready(proc, port: int, timeout_s: int = 600) -> None:
    import urllib.request

    url = f"http://127.0.0.1:{port}/health"
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"vLLM exited early: {proc.returncode}")
        try:
            with urllib.request.urlopen(url, timeout=5):
                return
        except Exception:
            time.sleep(2)
    raise TimeoutError("vLLM did not become healthy in time")


@app.server(
    image=vllm_image,
    gpu=GPU,
    scaledown_window=15 * MINUTES,      # auto-scale: containers spin down when idle
    startup_timeout=15 * MINUTES,
    volumes={
        "/root/.cache/huggingface": hf_cache_vol,
        "/root/.cache/vllm": vllm_cache_vol,
    },
    secrets=[hf_secret],
    port=VLLM_PORT,
    target_concurrency=100,
    unauthenticated=True,               # public OpenAI-compatible endpoint
)
def serve():
    cmd = [
        "vllm", "serve", MODEL_REPO,
        "--served-model-name", "Qwen/Qwen3.8-27B",
        "--host", "0.0.0.0",
        "--port", str(VLLM_PORT),
        "--dtype", "bfloat16",
        "--gpu-memory-utilization", "0.92",
        "--max-model-len", "262144",    # native context; YaRN only if 1M needed
        "--reasoning-parser", "qwen3",
        "--enable-auto-tool-choice",
        "--tool-call-parser", "qwen3_coder",
        "--mm-encoder-tp-mode", "data", # vision encoder (image/video input)
        "--temperature", str(TEMPERATURE),
        "--top-p", str(TOP_P),
        "--top-k", str(TOP_K),
        "--min-p", str(MIN_P),
        "--presence-penalty", str(PRESENCE_PENALTY),
        "--repetition-penalty", str(REPETITION_PENALTY),
        "--reasoning-effort", REASONING_EFFORT,
    ]
    proc = subprocess.Popen(cmd)
    _wait_ready(proc, VLLM_PORT)
    proc.wait()
```

**Step 2: Local parse check** (Modal parses the file locally before shipping; only `modal`/`os` at top level — heavy imports inside functions):

```bash
python3 -c "import ast; ast.parse(open('qwen38_serve.py').read())"
modal app validate qwen38_serve.py
```

**Step 3:** Commit: `feat: Modal H200 vLLM server for Qwen3.8-27B (Xet, volumes, official sampling)`.

---

## Task 5: Deploy the server and smoke-test the endpoint

**Objective:** First real GPU run; confirm the endpoint serves completions with thinking output.

**Step 1:** Deploy (this builds the image and warms the endpoint — first build 10–15 min):

```bash
modal deploy qwen38_serve.py > logs/deploy.log 2>&1
```

Run with `background=true, notify_on_complete=true`. The deploy output prints the endpoint URL (`https://<workspace>--qwen38-serve.modal.run`).

**Step 2:** Health + first completion:

```bash
curl -s https://<workspace>--qwen38-serve.modal.run/health
python3 scripts/smoke_serve.py --base-url https://<workspace>--qwen38-serve.modal.run/v1
```

`scripts/smoke_serve.py` (OpenAI client, `model="Qwen/Qwen3.8-27B"`, `reasoning_effort="low"` for the smoke test to save tokens) asserts: HTTP 200, `choices[0].message.content` non-empty, and (optionally) `reasoning_content` present when `enable_thinking` is on.

**Step 3:** Record the endpoint URL in `.env.example` (`QWEN_BASE_URL`) and `README.md`. Do NOT write secrets to `.env` without user confirmation.

**Step 4:** Commit: `feat: deploy qwen38-serve on H200 and verify endpoint`.

**Pitfalls (from skill + live docs):**
- First cold start downloads ~52 GB weights over Xet into the volume — allow 10–15 min; subsequent starts load from the volume at 1–2 GB/s.
- `ConflictError: function ... is stopped` during model download → weights are volume-cached, so re-deploy resumes without re-download.
- Image builds have a 900s heartbeat limit; if the pip list ever changes the cache layer invalidates — lock `vllm>=0.17.0` and `huggingface_hub>=0.32.0` once verified.

---

## Task 6: Client library + CLI with official Qwen parameters

**Objective:** `client/qwen_client.py` + `client/cli.py` — a typed OpenAI-compatible client that encodes the official sampling parameters and supports text/image/video prompts; unit-tested.

**Files:**
- Create: `client/qwen_client.py`
- Create: `client/cli.py`
- Create: `tests/test_qwen_client.py`
- Create: `requirements.txt` — `modal>=1.5.2,<1.6`, `openai>=1.x`, `pytest>=8`

**Step 1: `client/qwen_client.py`** — constants:

```python
QWEN_MODEL = "Qwen/Qwen3.8-27B"
QWEN_SAMPLING_DEFAULTS = {
    "temperature": 1.0, "top_p": 0.95, "top_k": 20, "min_p": 0.0,
    "presence_penalty": 0.0, "repetition_penalty": 1.0,
}
QWEN_REASONING_EFFORT = "xhigh"  # official default; "medium" | "low" allowed
```

Functions: `chat(messages, ...)` with `extra_body={"chat_template_kwargs": {"enable_thinking": True, "preserve_thinking": True}}` and `reasoning_effort=...`; `ask_text(prompt)`; `ask_image(image_path_or_url, prompt)` (content parts `image_url`); `ask_video(video_path_or_url, prompt)` (content parts `video_url`; note `fps=2`, `do_sample_frames=True` defaults from the model card).

**Step 2: `client/cli.py`** — `python client/cli.py ask "..."`, `--image path`, `--video path`, `--reasoning-effort {xhigh,medium,low}`, `--no-thinking`, `--base-url` (defaults to `QWEN_BASE_URL` env).

**Step 3: `tests/test_qwen_client.py`** — assert the request payload carries exactly the official params; assert thinking disabled path sets `enable_thinking: False`; assert image/video content-part serialization. Run: `uv run pytest tests/ -v` (or `.venv/bin/python -m pytest`).

**Step 4:** Commit: `feat: Qwen client + CLI with official sampling defaults and tests`.

---

## Task 7: HyperFrames scaffold + hot-tips authoring contract

**Objective:** A working HyperFrames project in `hyperframes/` whose authoring rules are pinned to the hot-tips doc, ready for the harness-engineering full test.

**Step 1:** Copy the authoring contract into the project (versioned, survives future sessions):

```bash
cp hot-tips-08-17-2026-hyperframes.txt hyperframes/HYPERFRAMES_HOT_TIPS.md
```

**Step 2:** Scaffold (Node 22+ and FFmpeg required):

```bash
npx hyperframes init hyperframes --non-interactive --example=basic
```

**Step 3:** Verify CLI health: `npx hyperframes doctor --json | jq -e '.ok'`.

**Step 4:** Author a minimal smoke composition (per `hyperframes-core` + hot-tips Rule of Three): root element with `data-composition-id`, `data-width="1920"`, `data-height="1080"`, `data-start="0"`, `data-duration`; one `class="clip"` scene; GSAP timeline registered under `window.__timelines["<id>"]` with `{ paused: true }`; include the blank-screen fallback snippet from hot-tips. Keep it under 10s.

**Step 5:** Run the gates: `npx hyperframes lint` → `npx hyperframes check` → `npx hyperframes preview` (hand URL to user; do NOT render before approval).

**Step 6:** After user approval: `npx hyperframes render --quality draft --output out.mp4`; verify non-empty + plausible duration (`ffprobe`). For a zero-local-infra alternative: `npx hyperframes cloud render`.

**Step 7:** Commit: `feat: scaffold HyperFrames project with hot-tips authoring contract`.

**Gotchas to honor (from hot-tips):** render with project dir (`.`) never `index.html`; FFmpeg/FFprobe on PATH (static binaries in project root if missing); no untimed `<audio>` elements; quality protocol before declaring ready (composition-id match, `paused: true`, root duration = sum of clips, `1920x1080 overflow: hidden`).

---

## Task 8: First full test — "Harness Engineering" course video (Qwen vision + HyperFrames)

**Objective:** The end-to-end stack test: Hermes orchestrates → Modal MCP manages the endpoint → Qwen3.8-27B (H200) analyzes the 10 course diagrams at **`reasoning_effort=xhigh`** → a **5–7 minute, 10-clip course video** follows the hot-tips design system and pacing standards, with a **beginner-paced voiceover script** the user records with their own voice.

**Inputs (read-only, do not modify `harness-engineering/`):**
- `harness-engineering/agent_harness_technical_course.md` (10 sections)
- `harness-engineering/images/diagrams/sec-1 … sec-10` PNGs
- `harness-engineering/slides/section_1 … section_10` HTML (authoritative visual reference per section)
- `harness-engineering/implementation_plan.md` (per-section timestamps)
- `hyperframes/HYPERFRAMES_HOT_TIPS.md` (authoring contract)

**Step 1: Qwen vision analysis of the 10 diagrams** (the Modal integration) — **`reasoning_effort="xhigh"`** per the model card (lower effort → insufficient analysis, more failures, repeated retries → higher total latency and token consumption):

```bash
python3 scripts/analyze_scene.py \
  --diagram harness-engineering/images/diagrams/sec-1-AI-Agent-System-Architecture.png \
  --section 1 --out harness-engineering-analysis/scene_descriptions.json
```

`scripts/analyze_scene.py` calls `client/qwen_client.ask_image(diagram, prompt)` with `reasoning_effort="xhigh"` and a prompt like: *"Describe this diagram in detail: title, components, relationships, and 3–5 key visual elements to reproduce in a video scene."* Run for all 10 sections (batch via a loop script; each call is seconds on the warm endpoint). Output: `harness-engineering-analysis/scene_descriptions.json` (one entry per section: title, key points, visual elements, suggested clip length).

**Step 2: Storyboard** — 10 clips (one per section), each **30–42s** per the hot-tips clip-duration budget, totaling **5–7 minutes** (client-demo requirement). Map each section's key points to clip content (badge/title, subtitle, left card + bullets, right card + bullets, callout) using the course markdown + Qwen's diagram descriptions + the section's HTML slide as the visual reference. Write `hyperframes/STORYBOARD.md` with per-clip timing tables.

**Step 3: Voiceover script** — `hyperframes/VOICEOVER_SCRIPT.md`:
- Written for a **beginner audience** (no jargon without explanation; each concept introduced before it's used).
- **Paced at human reading speed: ~130–150 words per minute** (comfortable instructional pace). Each clip's script section must fit its clip duration at that pace (e.g., a 35s clip ≈ 75–90 words).
- One section per clip, numbered to match `data-start`/`data-duration`; includes natural pauses between sections.
- The user records this with their own voice; the recording's actual timestamps then drive the final `data-start`/`data-duration` sync (hot-tips Audio Sync Workflow).

**Step 4: Author the composition** per hot-tips Rule of Three:
- Root: `data-composition-id="harness-engineering"`, `data-width="1920"`, `data-height="1080"`, `data-start="0"`, `data-duration=<sum of clips>`.
- 10 clip divs: `class="clip"`, sequential `data-start`/`data-duration`, `data-track-index="1"`.
- GSAP timelines registered under `window.__timelines["harness-engineering"]` with `{ paused: true }` + blank-screen fallback.
- Design system from hot-tips: `#090d16` slate gradient, Inter + JetBrains Mono, glassmorphism cards, electric accents (Cyan/Emerald/Amber/Ruby/Purple), brick-snapping nodes, glowing SVG connectors, timeline progress bars.
- Pacing per hot-tips minimums: badge 0.7s, subtitle 1.8s, Two-Card Rule (8–10s gap, separate `tl.from()` calls), bullets 1.5s stagger, diagram nodes 5s, code lines 0.8s, callout in last 10–12s.
- Each clip's layout mirrors its section's HTML slide (callout positions, element hierarchy) as the visual ground truth.

**Step 5: Gates:** `npx hyperframes lint` → `npx hyperframes check` → `npx hyperframes preview` (hand URL to user; render only after approval).

**Step 6: Render:** `npx hyperframes render --quality draft --output out_harness_draft.mp4` → review → `--quality high --output out_harness.mp4`. Verify with `ffprobe` (non-empty, **duration between 5:00 and 7:00**).

**Step 7: Voiceover sync (after user records):** per hot-tips Audio Sync Workflow — note actual timestamps from the recording, update `data-start`/`data-duration` on clips, update `setupClip()` calls, add `<audio id="bg-audio" src="assets/voiceover.mp3" data-start="0" data-duration="<total>" preload="auto">`, re-render.

**Step 8: Hot-tips quality protocol** before declaring done: composition-id matches `window.__timelines` key; `paused: true`; root duration = sum of clips; `1920x1080 overflow: hidden`; no untimed audio; no render errors.

**Step 9:** Commit: `feat: harness-engineering course video (Qwen vision analysis + 10-clip HyperFrames composition + voiceover script)`.

**Cost note:** 10 image analyses at `reasoning_effort=xhigh` on the warm H200 endpoint ≈ a few minutes of GPU ≈ **well under $2** (xhigh uses more tokens than medium, but 10 single-image calls remain small). The render is local (free) unless `hyperframes cloud render` is chosen.

---

## Task 9: README polish + verification pass + handoff

**Objective:** Document the full workflow so any future session (or collaborator) can run everything.

**Step 1:** `README.md` final content:
- Architecture diagram (Mermaid), quickstart (deploy → endpoint → client → hyperframes), env table, cost table (H200 $4.54/hr; volume 1 TiB free), troubleshooting (cold start, volume reload, image rebuild), the "Verified environment" table from Task 3, and the harness-engineering full-test results.

**Step 2:** Final verification sweep:
- `hermes mcp list` (modal ✓), `hermes mcp test modal`
- `modal app list` (qwen38-serve deployed)
- `curl <endpoint>/v1/models`
- `npx hyperframes check` passes
- `uv run pytest tests/ -v` green

**Step 3:** Commit: `docs: finalize README with architecture, costs, and verified-environment table`.

---

## Validation & acceptance criteria

1. `hermes mcp list` shows `modal` enabled; `hermes mcp test modal` succeeds (Task 2).
2. `modal deploy qwen38_serve.py` succeeds; endpoint returns `/v1/models` with `Qwen/Qwen3.8-27B` (Task 5).
3. A text completion and one image question return non-empty answers with `reasoning_content` present in thinking mode (Task 5/6).
4. `uv run pytest tests/ -v` green; payloads carry exactly the official sampling params (Task 6).
5. `npx hyperframes check` passes and a draft render exists with plausible duration (Task 7).
6. **Full test:** `harness-engineering-analysis/scene_descriptions.json` contains 10 Qwen vision analyses; the 10-clip composition passes the hot-tips quality protocol; `out_harness.mp4` renders with plausible duration (Task 8).
7. README documents deploy → client → HyperFrames flow with costs (Task 9).

## Risks & open questions

- **MCP tools appear only at session start.** After Task 2, the Modal MCP tools become available in the *next* Hermes session (or via `/reload-mcp`). Verification of tool *calls* happens then.
- **`~/.modal.toml` vs `.env`:** CLI auth already works (`tamazightdev`). The plan does not create a workspace `.env` with real tokens; user confirmation is required first (credentials boundary).
- **Public endpoint:** `unauthenticated=True` exposes the OpenAI-compatible endpoint publicly (standard for Modal examples). Anyone with the URL can burn GPU credits. Decision required from user (see discussion); mitigation options: workspace spend limits, API-key middleware, or Modal built-in auth.
- **H200 capacity:** Modal has seen H200 scheduling degradation (status page). Fallback: `gpu="H100"` (auto-upgrades to H200 when capacity allows) — one-line change.
- **vLLM version pin:** `vllm>=0.17.0` is the verified recipe floor; the plan recommends locking the exact version after the first successful deploy (image-layer stability rule).
- **1M context:** Native 262K is default; YaRN to 1M requires config overrides (documented in the model card) — only if a use case needs it.
- **Missing harness-engineering files:** `slides/` (10 HTML) and `v3_Youtube_Technical_Course_System_Prompt.md` are referenced in `harness-engineering/README.md` but absent. The full test does not need them (course md + diagrams suffice); ask the user whether to add them.
- **HyperFrames cloud render** is HeyGen-hosted and may require `npx hyperframes auth` — alternative is local render (Node 22 + FFmpeg required locally).
