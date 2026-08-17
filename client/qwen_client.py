"""OpenAI-compatible Qwen3.8-27B client with official sampling defaults.

Usage:
    from client.qwen_client import QwenClient
    client = QwenClient()  # reads QWEN_BASE_URL from env
    response = client.ask_text("Explain agent harnesses")
"""
import base64
import json
import os
from pathlib import Path
from typing import Optional, Union

from openai import OpenAI

# Official Qwen3.8-27B model card defaults (verified 2026-08-17)
QWEN_MODEL = "Qwen/Qwen3.8-27B"
QWEN_SAMPLING_DEFAULTS = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 20,
    "min_p": 0.0,
    "presence_penalty": 0.0,
    "repetition_penalty": 1.0,
}
QWEN_REASONING_EFFORT = "xhigh"  # official default; "medium" | "low" allowed
QWEN_BASE_URL = os.environ.get(
    "QWEN_BASE_URL",
    "https://tamazightdev--qwen38-serve-qwen38server.us-east.modal.direct/v1",
)


class QwenClient:
    """Thin wrapper around the OpenAI client with Qwen3.8-27B defaults baked in."""

    def __init__(
        self,
        base_url: str = QWEN_BASE_URL,
        api_key: str = "modal",  # unauthenticated endpoint
        model: str = QWEN_MODEL,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    def chat(
        self,
        messages: list[dict],
        reasoning_effort: str = QWEN_REASONING_EFFORT,
        enable_thinking: bool = True,
        preserve_thinking: bool = True,
        max_tokens: int = 8192,
        **overrides,
    ) -> dict:
        """Send a chat completion with official Qwen3.8 defaults.

        Returns dict with 'content', 'reasoning_content', and 'usage'.
        """
        params = {
            "model": self.model,
            "messages": messages,
            "reasoning_effort": reasoning_effort,
            "max_tokens": max_tokens,
            **QWEN_SAMPLING_DEFAULTS,
            **overrides,
        }
        # Qwen3.8 thinking-mode params via extra_body (vLLM passthrough)
        extra_body = overrides.pop("extra_body", {})
        params["extra_body"] = {
            "chat_template_kwargs": {
                "enable_thinking": enable_thinking,
                "preserve_thinking": preserve_thinking,
            },
            **extra_body,  # merge caller's extra_body (e.g. mm_processor_kwargs)
        }
        resp = self.client.chat.completions.create(**params)
        msg = resp.choices[0].message
        return {
            "content": msg.content or "",
            "reasoning_content": getattr(msg, "reasoning_content", None) or "",
            "usage": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
                "total_tokens": resp.usage.total_tokens,
            }
            if resp.usage
            else {},
        }

    def ask_text(
        self,
        prompt: str,
        reasoning_effort: str = QWEN_REASONING_EFFORT,
        **kwargs,
    ) -> str:
        """Simple text prompt → response string."""
        result = self.chat(
            messages=[{"role": "user", "content": prompt}],
            reasoning_effort=reasoning_effort,
            **kwargs,
        )
        return result["content"]

    def ask_image(
        self,
        image: Union[str, Path],
        prompt: str,
        reasoning_effort: str = QWEN_REASONING_EFFORT,
        **kwargs,
    ) -> str:
        """Image input (file path or URL) + text prompt → response string."""
        image_url = self._to_image_url(image)
        result = self.chat(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            reasoning_effort=reasoning_effort,
            **kwargs,
        )
        return result["content"]

    def ask_video(
        self,
        video: Union[str, Path],
        prompt: str,
        reasoning_effort: str = QWEN_REASONING_EFFORT,
        fps: int = 2,
        **kwargs,
    ) -> str:
        """Video input (file path or URL) + text prompt → response string.

        fps=2 and do_sample_frames=True are the model card defaults.
        """
        video_url = self._to_url(video)
        extra_body = kwargs.pop("extra_body", {})
        extra_body["mm_processor_kwargs"] = {
            "fps": fps,
            "do_sample_frames": True,
        }
        result = self.chat(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "video_url", "video_url": {"url": video_url}},
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
            reasoning_effort=reasoning_effort,
            extra_body=extra_body,
            **kwargs,
        )
        return result["content"]

    @staticmethod
    def _to_image_url(image: Union[str, Path]) -> str:
        """Convert a file path to a base64 data URI, or pass URLs through."""
        p = Path(image) if not str(image).startswith(("http://", "https://")) else None
        if p and p.exists():
            mime = "image/png" if p.suffix == ".png" else "image/jpeg"
            data = base64.b64encode(p.read_bytes()).decode()
            return f"data:{mime};base64,{data}"
        return str(image)

    @staticmethod
    def _to_url(resource: Union[str, Path]) -> str:
        """Pass URLs through; for local files, return as-is (vLLM handles file paths)."""
        return str(resource)