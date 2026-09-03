"""
API-level request/response schemas. These wrap engine.models types
with validation tailored to the HTTP layer (TRD Workstream C, task
A.4: input validation with Pydantic, reject malformed requests early).
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from engine.models import FinancialProfile, ScenarioParams, SimulationResult


class SimulateRequest(BaseModel):
    profile: FinancialProfile
    scenario: ScenarioParams = ScenarioParams()


class SimulateResponse(BaseModel):
    result: SimulationResult


class InsightRequest(BaseModel):
    simulation: SimulationResult
    language: str = Field("en", description="'en', 'ur', or 'roman_ur'")


class InsightResponse(BaseModel):
    insight_text: str
    used_fallback: bool
    language: str


class QARequest(BaseModel):
    simulation: SimulationResult
    question: str = Field(..., min_length=1, max_length=500)
    language: str = "en"


class QAResponse(BaseModel):
    answer_text: str
    used_fallback: bool


class HealthResponse(BaseModel):
    status: str
    service: str = "finmirror-ai-api"
