# AGENTS.md

## Project Overview

Serverless Qwen3.8-27B (BF16, thinking mode) served on Modal H200 via vLLM, driven by Hermes Agent through the Modal MCP server, rendering HyperFrames videos. The first full test is a 5-7 minute client-demo course video built from `harness-engineering/` (10 sections, 10 diagram PNGs, 10 HTML slides), with a beginner-paced voiceover script the user records with their own voice.

## Build / Install Commands

```bash
# Local dev deps (project venv)
uv venv .venv
uv pip install "modal>=1.5.2,<1.6" "openai>=1.x" "pytest>=8"

# Deploy the Modal vLLM server (first build 10-15 min)
modal deploy qwen38_serve.py > logs/deploy.log 2>&1

# Run tests
uv run pytest tests/ -v
```

## Test Commands

```bash
uv run pytest tests/ -v          # client unit tests
python3 scripts/smoke_serve.py --base-url <QWEN_BASE_URL>   # endpoint smoke test
npx hyperframes check            # composition gate (includes lint)
ffprobe -v error -show_format out_harness.mp4   # verify render
```

## Lint / Type Check

```bash
npx hyperframes lint              # HyperFrames compositions
python3 -c "import ast; ast.parse(open('qwen38_serve.py').read())"  # Modal app parse check
```

## Project Structure

```
qwen38_serve.py          # Modal vLLM server (H200, Xet, volumes)
client/                  # OpenAI-compatible Qwen client + CLI
scripts/                 # smoke_serve.py, analyze_scene.py
hyperframes/             # HyperFrames project (HYPERFRAMES_HOT_TIPS.md = authoring contract)
harness-engineering/    # READ-ONLY input for the full test (course, diagrams, slides)
tests/                   # client unit tests
logs/                    # gitignored; modal run output
```

## Code Style

- Python: stdlib-first; heavy imports (torch, vllm) INSIDE functions, never module top-level (Modal parses locally).
- Only `import modal` and `import os` at module top level in Modal apps.
- Sampling params: official Qwen3.8-27B thinking-mode defaults (temp=1.0, top_p=0.95, top_k=20, min_p=0.0, presence_penalty=0.0, repetition_penalty=1.0), reasoning_effort=xhigh.
- HyperFrames: follow `hyperframes/HYPERFRAMES_HOT_TIPS.md` (Rule of Three, pacing standards, quality protocol).

## Key Conventions

- Never commit `.env` or any token; CLI auth via `~/.modal.toml`.
- GPU jobs: `background=true, notify_on_complete=true`, log to `logs/`, never poll.
- `harness-engineering/` is read-only input — never modify.
- Xet is the HF transfer backend (LFS deprecated): `HF_XET_HIGH_PERFORMANCE=1`.
- Lock vLLM/huggingface_hub versions after first successful deploy (image-layer stability).

## Git Workflow

- Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
- Commit after every task; verify with `git status` before committing.

## Boundaries

- ✅ Always do: follow the plan in `.hermes/plans/`; verify against live sources before pinning versions; run `npx hyperframes check` before renders.
- ⚠️ Ask first: any GPU spend beyond smoke tests; changing `harness-engineering/`; making the endpoint private; creating `.env` with real tokens; switching reasoning_effort from xhigh.
- 🚫 Never do: commit secrets; poll background jobs; modify `harness-engineering/`; render without user approval of the preview; use Git LFS or `HF_HUB_ENABLE_HF_TRANSFER`.
