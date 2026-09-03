"""
Gemini client for FinMirror AI.

Keeps the same interface used by the existing insight layer:
    client.generate(system_prompt, user_prompt)
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger("finmirror.genai")


@dataclass
class GenAIResponse:
    text: str
    used_fallback: bool = False


class GeminiClient:
    """Small wrapper around the Google Gemini API."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> GenAIResponse:
        """Generate a response using Gemini."""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config={
                    "system_instruction": system_prompt,
                },
            )

            text = response.text

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return GenAIResponse(text=text, used_fallback=False)

        except Exception as exc:
            logger.exception("Gemini request failed: %s", exc)

            return GenAIResponse(
                text=(
                    "I could not generate the AI insight right now. "
                    "Please review the simulation results shown on the dashboard."
                ),
                used_fallback=True,
            )


def get_client() -> GeminiClient:
    """Return the configured Gemini client."""
    return GeminiClient()
