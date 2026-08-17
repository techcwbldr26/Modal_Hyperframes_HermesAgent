# CONTINUATION PROMPT — Modal-HyperFrames-Hermes Project

> **Paste this entire prompt as your first message in a new Hermes session.**
> Set the workspace to `/Users/gregorykennedy-salemi/Desktop/modal-hyperframes-hermes`.

---

You are continuing a Modal + HyperFrames + Hermes Agent project. Tasks 1-8 are complete; Task 9 remains. Before doing anything, read these files in the workspace for full context:

1. **`AGENTS.md`** — project overview, build commands, code style, boundaries
2. **`.hermes/plans/2026-08-17_084841-modal-hyperframes-hermes.md`** — the full implementation plan with all gotchas
3. **`README.md`** — current status, endpoint info, troubleshooting table
4. **`hyperframes/HYPERFRAMES_HOT_TIPS.md`** — the HyperFrames authoring contract (Rule of Three, pacing, gotchas)
5. **`hyperframes/STORYBOARD.md`** — 10-clip storyboard with timing tables
6. **`hyperframes/VOICEOVER_SCRIPT.md`** — beginner-paced voiceover script (130-150 wpm, all verified)

## What's been done (Tasks 1-8, all committed)

- **Task 1:** Project scaffolded (git, AGENTS.md, .env.example, .gitignore, README)
- **Task 2:** Modal MCP server registered in Hermes (`hermes mcp list` shows `modal ✓ enabled`, 57 tools). Note: MCP tools load at session start — they may need `/reload-mcp` or a session restart to appear.
- **Task 3:** Modal account verified (profile `tamazightdev`, secret `huggingface-token`, $30 balance)
- **Task 4:** `qwen38_serve.py` written — class-based `@app.server()` on `vllm/vllm-openai:qwen38` image, H200, Xet, volumes. Sampling params are request-time (NOT vLLM CLI flags).
- **Task 5:** Deployed and smoke-tested. Endpoint is live at:
  `https://tamazightdev--qwen38-serve-qwen38server.us-east.modal.direct`
  Smoke test passed: text completion (0.8s), vision (2.7s), `/v1/models` returns `Qwen/Qwen3.8-27B` with 262,144 context.
- **Task 6:** Client library (`client/qwen_client.py`) + CLI (`client/cli.py`) + 17 unit tests (all passing). Official xhigh sampling defaults baked in. vLLM-only params (top_k, min_p, repetition_penalty) are in `extra_body`, not direct API params.
- **Task 7:** HyperFrames project scaffolded (`hyperframes/`), hot-tips contract copied, `check` passes.
- **Task 8:** Full integration test completed:
  - Qwen3.8-27B vision analysis of 12 diagrams at `reasoning_effort=xhigh` → `harness-engineering-analysis/scene_descriptions.json`
  - Storyboard: 10 clips, 382s (6:22) total, within 5-7 min target
  - Voiceover script: beginner-paced, all clips 130-150 wpm
  - HyperFrames composition authored: `hyperframes/index.html` (525 lines), `hyperframes/styles/main.css`, `hyperframes/anim.js`
  - `npx hyperframes@0.7.109 check` passes: 0 errors, 0 warnings, 61/61 WCAG AA

## Critical gotchas already discovered and documented (DO NOT repeat these mistakes)

1. **`@app.server()` must be class-based** in Modal 1.5.2 (function form raises TypeError)
2. **`proc.wait()` blocks container readiness** — don't call it in `@modal.enter()`; vLLM runs in background
3. **Use `vllm/vllm-openai:qwen38` pre-built image** — pip-installing vLLM on a bare CUDA image causes torch/torchvision version mismatch
4. **Sampling params are request-time, NOT vLLM CLI flags** — `--temperature`, `--top-p`, `--top-k`, `--min-p`, `--presence-penalty`, `--repetition-penalty`, `--reasoning-effort` are ALL invalid as `vllm serve` CLI args. The model's `generation_config.json` carries server defaults; the client sets them per-request.
5. **`top_k`, `min_p`, `repetition_penalty` go in `extra_body`** — the OpenAI Python SDK doesn't accept them as direct params; vLLM reads them from extra_body.
6. **Cold start takes ~8 min** (52 GB Xet download + torch.compile + CUDA graphs). Set `startup_timeout=20*MINUTES` and `_wait_ready` timeout=900s.
7. **`modal app stop <name> -y` before redeploying** to force a fresh container (old containers with stale code persist)
8. **`modal app validate` and `modal quota show` don't exist** in CLI 1.5.2 — use `uv run --with "modal>=1.5.2,<1.6" python -c "import <app>"` for local validation, `modal billing report --for "this month"` for spend
9. **`hermes mcp add` interactive prompt** — pipe `Y` in non-TTY: `echo "Y" | hermes mcp add ...`; `--env` values land in `args` not `env:` block — fix with a Python yaml script
10. **`uv run --with "openai>=1.x"` fails** — use `openai>=1.0` (PEP 440 doesn't accept `1.x`)
11. **HyperFrames CLI is pinned** at `hyperframes@0.7.109` — always use `npx --yes hyperframes@0.7.109 <command>` or the npm scripts in `hyperframes/package.json`

## Step 0: Check if the Modal endpoint is still running

```bash
curl -s -m 10 https://tamazightdev--qwen38-serve-qwen38server.us-east.modal.direct/v1/models
```

- If it returns JSON with `"Qwen/Qwen3.8-27B"`: endpoint is warm, proceed to Task 9.
- If it returns `{"error":"no upstreams available"}`: the container scaled down (idle for 15+ min). The first request will trigger a cold start (~3-4 min since weights are volume-cached). Wait for it with a retry loop, or check `modal app logs` for progress.
- If the app is stopped: `modal app list | grep qwen38` — if stopped, `modal deploy qwen38_serve.py` to redeploy (image is cached, takes ~2s).

## Task 9: README polish + final verification pass

### Step 1: Final verification sweep

Run ALL of these and record results in the README:

```bash
# Modal MCP
hermes mcp list                    # modal should show ✓ enabled
hermes mcp test modal              # should connect and discover tools

# Modal endpoint
curl -s https://tamazightdev--qwen38-serve-qwen38server.us-east.modal.direct/v1/models
# Should return Qwen/Qwen3.8-27B with 262144 max_model_len

# Client tests
uv run --with "openai>=1.0" --with "pytest>=8" python -m pytest tests/ -v
# Should show 17 passed

# HyperFrames check
cd hyperframes && npx --yes hyperframes@0.7.109 check
# Should show 0 errors, 0 warnings, 61/61 WCAG AA
```

### Step 2: Finalize README

Update `README.md` with:
- Final architecture diagram (Mermaid)
- Complete quickstart (deploy → endpoint → client → hyperframes → render)
- Final status table (all 9 tasks ✅)
- Cost summary (H200 $4.54/hr, volume 1 TiB free, ~$2-3 spent on deploys + vision analysis)
- Troubleshooting table (all gotchas from the plan)
- Harness-engineering full test results section

### Step 3: Commit

```bash
git add README.md
git commit -m "docs: finalize README with architecture, costs, and verified-environment table"
```

## After Task 9: Preview + Render (requires user approval)

Once Task 9 is done, the next steps are:

1. **Preview the composition** for user visual review:
   ```bash
   cd hyperframes && npx --yes hyperframes@0.7.109 preview
   ```
   Hand the URL to the user. Do NOT render without explicit approval.

2. **User records voiceover** using `hyperframes/VOICEOVER_SCRIPT.md` with their own voice.

3. **Audio sync** (after recording): per hot-tips Audio Sync Workflow — note actual timestamps from the recording, update `data-start`/`data-duration` on clips, add `<audio>` element, re-render.

4. **Render to MP4** (after user approval):
   ```bash
   cd hyperframes && npx --yes hyperframes@0.7.109 render --quality draft --output ../out_harness_draft.mp4
   ```
   Verify with `ffprobe -v error -show_format out_harness_draft.mp4` — duration should be 5:00-7:00.

   Then high quality:
   ```bash
   npx --yes hyperframes@0.7.109 render --quality high --output ../out_harness.mp4
   ```

## Key files and paths

- Endpoint: `https://tamazightdev--qwen38-serve-qwen38server.us-east.modal.direct`
- Modal profile: `tamazightdev` (auth via `~/.modal.toml`)
- Modal secret: `huggingface-token` (already created)
- Modal MCP server: `~/Desktop/modal-mcp-server` (registered in Hermes config)
- vLLM image: `vllm/vllm-openai:qwen38`
- Model: `Qwen/Qwen3.8-27B` (BF16, 27B, ~52 GB, 262K context)
- GPU: H200 SXM (141 GB, $4.54/hr)
- Firecrawl MCP: installed (25 tools, API key `fc-0eb3c7ad9e304b46961f1f1d25b35b6a`) — available next session
- HyperFrames CLI: pinned at `0.7.109`
- Node: v24.16.0, FFmpeg: 8.1.1

## Skills to load

Before starting, load these skills:
- `skill_view(name='hyperframes-cli')` — for render/preview commands
- `skill_view(name='modal-gpu-pipeline-development')` — for Modal gotchas (already updated with all discovered issues)
- `skill_view(name='hermes-agent')` — for MCP config verification

## Rules

- Never poll background jobs — use `background=true, notify_on_complete=true`
- GPU jobs log to `logs/`, never to stdout
- `harness-engineering/` is READ-ONLY — never modify
- Don't commit `.env` or secrets
- Verify with live sources before pinning versions
- `reasoning_effort=xhigh` for all Qwen calls (user's explicit requirement)
- Use Firecrawl MCP tools for web research (installed, available next session)