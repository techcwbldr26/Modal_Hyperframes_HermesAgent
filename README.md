# Modal + HyperFrames + Hermes Agent

Serverless **Qwen3.8-27B** (BF16, thinking mode) on **Modal H200** via vLLM, driven by **Hermes Agent** through the **Modal MCP server**, rendering **HyperFrames** videos.

## Status

- [x] Task 1: Project scaffold
- [x] Task 2: Modal MCP registered in Hermes
- [x] Task 3: Modal account state verified
- [x] Task 4: `qwen38_serve.py` written
- [x] Task 5: Deployed + endpoint smoke-tested
- [x] Task 6: Qwen client + CLI
- [x] Task 7: HyperFrames scaffold + hot-tips contract
- [x] Task 8: Harness-engineering 5–7 min course video (full test)
- [ ] Task 9: README + verification pass

## Architecture

```
Hermes Agent ──MCP (stdio)──> modal-mcp-server ──> Modal platform (apps, volumes, secrets)
     │
     └──OpenAI-compatible HTTP──> qwen38-serve (vLLM on H200) ──> Qwen/Qwen3.8-27B
                                                                        │
HyperFrames (local render) <── scene_descriptions.json <── vision analysis
```

## Quickstart

See `.hermes/plans/2026-08-17_084841-modal-hyperframes-hermes.md` for the full implementation plan.

## Verified environment (2026-08-17)

| Item | Value |
|---|---|
| Modal CLI | 1.5.2 |
| Modal profile | tamazightdev |
| Modal secrets | huggingface-token ✓ |
| Modal MCP | ✓ enabled — 57 tools (uv --directory ~/Desktop/modal-mcp-server) |
| Model | Qwen/Qwen3.8-27B (27B, BF16 ~52 GB, 262K ctx) |
| GPU | H200 SXM (141 GB, $4.54/hr) |
| Storage | Modal Volumes (1 TiB free, then $0.09/GiB/mo) |
| HF transfer | Xet (hf_xet, HF_XET_HIGH_PERFORMANCE=1) |
| Modal balance | $30.00 (user-confirmed, 2026-08-17) |

## Endpoint (live)

- **URL:** `https://tamazightdev--qwen38-serve-qwen38server.us-east.modal.direct`
- **Model:** `Qwen/Qwen3.8-27B` (BF16, 262,144 context, vision-enabled)
- **Image:** `vllm/vllm-openai:qwen38` (pre-built, all deps matched)
- **GPU:** H200 SXM (141 GB)
- **Cold start:** ~5 min (model download via Xet into volume) + ~3 min (torch.compile + CUDA graphs) = ~8 min total
- **Warm requests:** <3s for text, <3s for vision

## Troubleshooting

| Symptom | Fix |
|---|---|
| `TypeError: The @app.server() decorator must be used on a class.` | Modal 1.5.2 requires class-based `@app.server()` — see `qwen38_serve.py` |
| `Error: No such command 'validate'` | Validate locally: `uv run --with "modal>=1.5.2,<1.6" python -c "import qwen38_serve"` |
| `Error: No such command 'quota'` | Use `modal billing report --for "this month" --show-resources` |
| `hermes mcp add` cancels in scripts | Pipe `Y`: `echo "Y" \| hermes mcp add ...` |
| `--env` values land in `args` after `hermes mcp add` | Move them into an `env:` block in `~/.hermes/config.yaml` via a Python yaml script |
| `vllm: error: unrecognized arguments: --temperature` | Sampling params are request-time, not server flags — remove from `vllm serve` command |
| `torchvision/transforms/v2` import crash | Use `vllm/vllm-openai:qwen38` pre-built image instead of pip-installing vLLM on a bare CUDA image |
| `TimeoutError: vLLM did not become healthy in time` | Increase `_wait_ready` timeout to 900s + `startup_timeout=20*MINUTES` for 52 GB model cold start |
| `503 "no upstreams available"` after redeploy | `modal app stop <name> -y` before redeploying to force a fresh container |
| `proc.wait()` blocks container readiness | Don't call `proc.wait()` in `@modal.enter()` — vLLM runs in background; add `@modal.exit()` cleanup instead |
