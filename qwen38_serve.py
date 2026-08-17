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
    modal.Image.from_registry("vllm/vllm-openai:qwen38", add_python=None)
    .entrypoint([])
    .run_commands("ln -s $(which python3) /usr/bin/python")
    .pip_install("huggingface_hub>=0.32.0")  # ensure hf_xet (Xet) is available
    .env(
        {
            "HF_HUB_CACHE": "/root/.cache/huggingface",
            # Xet: saturate bandwidth (LFS is deprecated on the Hub)
            "HF_XET_HIGH_PERFORMANCE": "1",
            "VLLM_USE_V1": "1",
        }
    )
)


def _wait_ready(proc, port: int, timeout_s: int = 900) -> None:
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
    startup_timeout=20 * MINUTES,
    volumes={
        "/root/.cache/huggingface": hf_cache_vol,
        "/root/.cache/vllm": vllm_cache_vol,
    },
    secrets=[hf_secret],
    port=VLLM_PORT,
    target_concurrency=100,
    unauthenticated=True,               # public OpenAI-compatible endpoint
)
class Qwen38Server:
    @modal.enter()
    def start(self):
        # NOTE: sampling params (temperature, top_p, top_k, min_p, etc.) and
        # reasoning_effort are NOT vLLM CLI flags — they're request-time params
        # set by the client. The model's generation_config.json already carries
        # the official Qwen3.8 defaults; the client (Task 6) enforces them too.
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
        ]
        self.proc = subprocess.Popen(cmd)
        _wait_ready(self.proc, VLLM_PORT)
        # Return — do NOT call proc.wait() here; that blocks the container
        # from ever becoming "ready". The vLLM process runs in the background
        # and Modal keeps the container alive until scaledown.

    @modal.exit()
    def stop(self):
        if hasattr(self, "proc"):
            self.proc.terminate()
