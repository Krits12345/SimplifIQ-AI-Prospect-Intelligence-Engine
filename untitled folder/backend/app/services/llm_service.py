"""
Shared LLM client wrapper.

Routes calls to Gemini (preferred when GEMINI_API_KEY is set) or OpenAI.
Centralizing this here keeps the agents provider-agnostic and gives us one
place to handle "no key configured" and JSON-parsing concerns.

If no provider is configured, every call returns None — agents record the
gap on `state.errors` and leave their output fields empty rather than
fabricating placeholder content.
"""

import json
import logging
import re
from typing import Any, List, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Provider-agnostic chat-completions wrapper."""

    def __init__(self):
        self.provider: Optional[str] = None
        self._client = None
        self._init_failed = False
        self._model = ""

    def _get_client(self):
        if self._client is not None or self._init_failed:
            return self._client

        # Gemini first — typically free-tier friendly and the project default.
        if settings.gemini_api_key:
            try:
                from google import genai

                self._client = genai.Client(api_key=settings.gemini_api_key)
                self.provider = "gemini"
                self._model = settings.gemini_model
                logger.info(f"LLM provider: Gemini ({self._model})")
                return self._client
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")

        if settings.openai_api_key:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=settings.openai_api_key)
                self.provider = "openai"
                self._model = settings.openai_model
                logger.info(f"LLM provider: OpenAI ({self._model})")
                return self._client
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")

        logger.info("LLM disabled: neither GEMINI_API_KEY nor OPENAI_API_KEY set")
        self._init_failed = True
        return None

    @property
    def enabled(self) -> bool:
        return self._get_client() is not None

    def chat(
        self,
        messages: List[dict],
        *,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> Optional[str]:
        """Return the assistant's text content, or None if the call fails."""
        if not self._get_client():
            return None
        try:
            if self.provider == "gemini":
                return self._chat_gemini(messages, temperature, max_tokens)
            return self._chat_openai(messages, temperature, max_tokens)
        except Exception as e:
            logger.error(f"{self.provider} chat call failed: {e}")
            return None

    def _chat_openai(self, messages, temperature, max_tokens) -> Optional[str]:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def _chat_gemini(self, messages, temperature, max_tokens) -> Optional[str]:
        # Gemini has no system role — fold system prompts into instructions.
        # Also disable "thinking" on 2.5-flash family: reasoning tokens otherwise
        # consume max_output_tokens before any visible response is emitted, and
        # we want structured JSON, not chain-of-thought.
        from google.genai import types

        system_parts = [m["content"] for m in messages if m.get("role") == "system"]
        user_parts = [m["content"] for m in messages if m.get("role") != "system"]
        prompt = "\n\n".join(user_parts)

        config_kwargs = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "system_instruction": ("\n\n".join(system_parts) or None),
        }
        if "2.5" in self._model:
            config_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        return getattr(response, "text", None)

    def chat_json(
        self,
        system: str,
        user: str,
        *,
        temperature: float = 0.2,
        max_tokens: int = 800,
    ) -> Optional[Any]:
        """Run a chat call and parse the first `{...}` JSON block. None on failure."""
        raw = self.chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if not raw:
            return None
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            logger.warning("LLM response did not contain a JSON object")
            return None
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM JSON: {e}")
            return None
