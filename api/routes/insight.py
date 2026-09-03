"""POST /insight and POST /insight/ask endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import InsightRequest, InsightResponse, QARequest, QAResponse
from api.services.insight_service import get_answer, get_insight

router = APIRouter(tags=["insight"])


@router.post("/insight", response_model=InsightResponse)
def insight_endpoint(request: InsightRequest) -> InsightResponse:
    try:
        response = get_insight(request.simulation, language=request.language)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Insight generation failed: {exc}",
        ) from exc

    return InsightResponse(
        insight_text=response.text,
        used_fallback=response.used_fallback,
        language=request.language,
    )


@router.post("/insight/ask", response_model=QAResponse)
def ask_endpoint(request: QARequest) -> QAResponse:
    try:
        response = get_answer(
            request.simulation,
            request.question,
            language=request.language,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Q&A failed: {exc}",
        ) from exc

    return QAResponse(
        answer_text=response.text,
        used_fallback=response.used_fallback,
    )

