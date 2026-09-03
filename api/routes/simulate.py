"""POST /simulate - run a financial scenario simulation."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import SimulateRequest, SimulateResponse
from api.services.simulation_service import simulate

router = APIRouter(tags=["simulate"])


@router.post("/simulate", response_model=SimulateResponse)
def simulate_endpoint(request: SimulateRequest) -> SimulateResponse:
    try:
        result = simulate(request.profile, request.scenario)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {exc}",
        ) from exc

    return SimulateResponse(result=result)

