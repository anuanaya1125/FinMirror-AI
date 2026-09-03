"""
Prompt templates that take the simulation JSON and produce a concise,
plain-language explanation plus a recommendation (TRD Workstream B,
task 2), including risk-flagging language (task 3).

Supports English, Urdu, and Roman Urdu output for financial
inclusion / low-literacy users.
"""

from __future__ import annotations

import json

from engine.models import SimulationResult

SYSTEM_PROMPT_TEMPLATE = """You are FinMirror AI's financial twin assistant. You explain the \
output of a financial simulation engine to everyday, potentially first-time-banked users \
in {language}. Your users may not have financial literacy or access to a financial advisor, \
so:
- Use short, plain sentences. Avoid jargon (no "amortization", "liquidity ratio", etc.).
- Be concrete: reference actual numbers from the simulation.
- If risk flags are present, clearly and calmly call them out - do not bury them.
- Always end with one clear, actionable recommendation.
- Keep the whole response under 150 words.
- Do not invent numbers that are not present in the provided JSON.
"""

INSIGHT_USER_PROMPT_TEMPLATE = """Here is the structured output of a financial scenario \
simulation for a user. Explain what it means and what they should consider doing.

Simulation JSON:
{simulation_json}
"""

QA_SYSTEM_PROMPT_TEMPLATE = """You are FinMirror AI's conversational financial twin assistant, \
speaking in {language}. Answer the user's question using ONLY the simulation data provided as \
grounding context below - do not make up numbers. If the answer isn't in the data, say so plainly \
and suggest what scenario they could run to find out. Keep answers short (under 120 words), \
plain-language, and free of jargon.

Simulation JSON (grounding context):
{simulation_json}
"""

LANGUAGE_LABELS = {
    "en": "English",
    "ur": "Urdu (written in Urdu script)",
    "roman_ur": "Roman Urdu (Urdu written in Latin/English letters, e.g. 'aap ka kharcha zyada hai')",
}


def build_insight_prompt(simulation: SimulationResult, language: str = "en") -> tuple[str, str]:
    """Returns (system_prompt, user_prompt) for the insight-generation call."""
    lang_label = LANGUAGE_LABELS.get(language, LANGUAGE_LABELS["en"])
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(language=lang_label)
    user_prompt = INSIGHT_USER_PROMPT_TEMPLATE.format(
        simulation_json=json.dumps(simulation.model_dump(), indent=2, default=str)
    )
    return system_prompt, user_prompt


def build_qa_prompt(simulation: SimulationResult, question: str, language: str = "en") -> tuple[str, str]:
    """Returns (system_prompt, user_prompt) for the free-text Q&A stretch goal
    (TRD Workstream B, task 4)."""
    lang_label = LANGUAGE_LABELS.get(language, LANGUAGE_LABELS["en"])
    system_prompt = QA_SYSTEM_PROMPT_TEMPLATE.format(
        language=lang_label,
        simulation_json=json.dumps(simulation.model_dump(), indent=2, default=str),
    )
    return system_prompt, question
