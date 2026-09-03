"""Service layer between the API and the GenAI insight layer."""

from __future__ import annotations

import logging

from api.routes.metrics import GENAI_FALLBACK_COUNTER
from engine.models import SimulationResult
from genai.insight_generator import answer_question, generate_insight

logger = logging.getLogger("finmirror.insight_service")


def get_insight(
    simulation: SimulationResult,
    language: str = "en",
):
    response = generate_insight(simulation, language=language)

    if response.used_fallback:
        logger.warning(
            "Insight generation used fallback response",
            extra={"user_id": simulation.user_id},
        )
        GENAI_FALLBACK_COUNTER.inc()

    return response


def get_answer(
    simulation: SimulationResult,
    question: str,
    language: str = "en",
):
    response = answer_question(
        simulation,
        question,
        language=language,
    )

    if response.used_fallback:
        logger.warning(
            "Q&A used fallback response",
            extra={"user_id": simulation.user_id},
        )
        GENAI_FALLBACK_COUNTER.inc()

    return response

