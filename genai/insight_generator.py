"""
High-level entry points for Workstream B: turn a SimulationResult
into plain-language insight, and answer free-text questions grounded
in the simulation data.
"""

from __future__ import annotations

from engine.models import SimulationResult
from genai.client import GenAIResponse, get_client
from genai.prompts import build_insight_prompt, build_qa_prompt


def generate_insight(simulation: SimulationResult, language: str = "en") -> GenAIResponse:
    """Convert simulation JSON into a plain-language explanation + recommendation."""
    client = get_client()
    system_prompt, user_prompt = build_insight_prompt(simulation, language=language)
    return client.generate(system_prompt, user_prompt)


def answer_question(simulation: SimulationResult, question: str, language: str = "en") -> GenAIResponse:
    """Stretch goal: free-text Q&A grounded in the simulation data."""
    client = get_client()
    system_prompt, user_prompt = build_qa_prompt(simulation, question, language=language)
    return client.generate(system_prompt, user_prompt)
