# Modal + HyperFrames + Hermes Agent

Serverless **Qwen3.8-27B** (BF16, thinking mode) on **Modal H200** via vLLM, driven by **Hermes Agent** through the **Modal MCP server**, rendering **HyperFrames** videos.

## Status

- [x] Task 1: Project scaffold
- [x] Task 2: Modal MCP registered in Hermes
- [x] Task 3: Modal account state verified
- [x] Task 4: `qwen38_serve.py` written
- [ ] Task 5: Deployed + endpoint smoke-tested
- [ ] Task 6: Qwen client + CLI
- [ ] Task 7: HyperFrames scaffold + hot-tips contract
- [ ] Task 8: Harness-engineering 5–7 min course video (full test)
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

## Troubleshooting

| Symptom | Fix |
|---|---|
| `TypeError: The @app.server() decorator must be used on a class.` | Modal 1.5.2 requires class-based `@app.server()` — see `qwen38_serve.py` |
| `Error: No such command 'validate'` | Validate locally: `uv run --with "modal>=1.5.2,<1.6" python -c "import qwen38_serve"` |
| `Error: No such command 'quota'` | Use `modal billing report --for "this month" --show-resources` |
| `hermes mcp add` cancels in scripts | Pipe `Y`: `echo "Y" \| hermes mcp add ...` |
| `--env` values land in `args` after `hermes mcp add` | Move them into an `env:` block in `~/.hermes/config.yaml` via a Python yaml script |
