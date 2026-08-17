"""Unit tests for the Qwen3.8-27B client.

Tests verify that the client correctly encodes the official sampling
parameters and message formats — no live endpoint needed (mocked).
"""
import json
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from client.qwen_client import (
    QwenClient,
    QWEN_MODEL,
    QWEN_SAMPLING_DEFAULTS,
    QWEN_REASONING_EFFORT,
)


class TestSamplingDefaults:
    """Verify the official Qwen3.8-27B model-card defaults are encoded."""

    def test_model_name(self):
        assert QWEN_MODEL == "Qwen/Qwen3.8-27B"

    def test_temperature(self):
        assert QWEN_SAMPLING_DEFAULTS["temperature"] == 1.0

    def test_top_p(self):
        assert QWEN_SAMPLING_DEFAULTS["top_p"] == 0.95

    def test_top_k(self):
        assert QWEN_SAMPLING_DEFAULTS["top_k"] == 20

    def test_min_p(self):
        assert QWEN_SAMPLING_DEFAULTS["min_p"] == 0.0

    def test_presence_penalty(self):
        assert QWEN_SAMPLING_DEFAULTS["presence_penalty"] == 0.0

    def test_repetition_penalty(self):
        assert QWEN_SAMPLING_DEFAULTS["repetition_penalty"] == 1.0

    def test_reasoning_effort_default(self):
        assert QWEN_REASONING_EFFORT == "xhigh"


def _mock_response(content="test", reasoning="thinking..."):
    """Build a mock OpenAI chat completion response."""
    msg = MagicMock()
    msg.content = content
    msg.reasoning_content = reasoning
    choice = MagicMock()
    choice.message = msg
    resp = MagicMock()
    resp.choices = [choice]
    resp.usage = MagicMock(
        prompt_tokens=10, completion_tokens=20, total_tokens=30
    )
    return resp


class TestChatPayload:
    """Verify the chat() method builds the correct request payload."""

    @patch("client.qwen_client.OpenAI")
    def test_chat_includes_sampling_defaults(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.chat([{"role": "user", "content": "hello"}])

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        # Standard OpenAI params
        assert call_kwargs["temperature"] == 1.0
        assert call_kwargs["top_p"] == 0.95
        assert call_kwargs["presence_penalty"] == 0.0
        # vLLM-only params in extra_body
        extra = call_kwargs["extra_body"]
        assert extra["top_k"] == 20
        assert extra["min_p"] == 0.0
        assert extra["repetition_penalty"] == 1.0

    @patch("client.qwen_client.OpenAI")
    def test_chat_includes_reasoning_effort(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.chat([{"role": "user", "content": "hello"}])

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["reasoning_effort"] == "xhigh"

    @patch("client.qwen_client.OpenAI")
    def test_chat_thinking_enabled_by_default(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.chat([{"role": "user", "content": "hello"}])

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        extra = call_kwargs["extra_body"]
        assert extra["chat_template_kwargs"]["enable_thinking"] is True
        assert extra["chat_template_kwargs"]["preserve_thinking"] is True

    @patch("client.qwen_client.OpenAI")
    def test_chat_thinking_disabled(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.chat(
            [{"role": "user", "content": "hello"}],
            enable_thinking=False,
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        extra = call_kwargs["extra_body"]
        assert extra["chat_template_kwargs"]["enable_thinking"] is False

    @patch("client.qwen_client.OpenAI")
    def test_chat_override_reasoning_effort(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.chat(
            [{"role": "user", "content": "hello"}],
            reasoning_effort="medium",
        )

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["reasoning_effort"] == "medium"


class TestImagePayload:
    """Verify image input serialization."""

    @patch("client.qwen_client.OpenAI")
    def test_image_url_content_parts(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.ask_image("https://example.com/img.jpg", "describe this")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        msg = call_kwargs["messages"][0]
        assert msg["role"] == "user"
        parts = msg["content"]
        assert len(parts) == 2
        assert parts[0]["type"] == "image_url"
        assert parts[0]["image_url"]["url"] == "https://example.com/img.jpg"
        assert parts[1]["type"] == "text"
        assert parts[1]["text"] == "describe this"

    @patch("client.qwen_client.OpenAI")
    def test_image_file_to_base64(self, mock_openai_cls, tmp_path):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        # Create a tiny fake PNG
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNG\r\n\x1a\n")  # PNG header

        client = QwenClient()
        client.ask_image(str(img), "describe this")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        url = call_kwargs["messages"][0]["content"][0]["image_url"]["url"]
        assert url.startswith("data:image/png;base64,")


class TestVideoPayload:
    """Verify video input serialization."""

    @patch("client.qwen_client.OpenAI")
    def test_video_url_content_parts(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.ask_video("https://example.com/clip.mp4", "analyze this")

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        msg = call_kwargs["messages"][0]
        parts = msg["content"]
        assert len(parts) == 2
        assert parts[0]["type"] == "video_url"
        assert parts[0]["video_url"]["url"] == "https://example.com/clip.mp4"
        assert parts[1]["type"] == "text"

    @patch("client.qwen_client.OpenAI")
    def test_video_fps_processor_kwargs(self, mock_openai_cls):
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.return_value = _mock_response()

        client = QwenClient()
        client.ask_video("https://example.com/clip.mp4", "analyze this", fps=4)

        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        extra = call_kwargs["extra_body"]
        assert extra["mm_processor_kwargs"]["fps"] == 4
        assert extra["mm_processor_kwargs"]["do_sample_frames"] is True