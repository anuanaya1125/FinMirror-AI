"""Service layer between the API and simulation engine."""

from __future__ import annotations

import logging

from api.routes.metrics import SIMULATIONS_RUN_COUNTER
from engine.models import FinancialProfile, ScenarioParams, SimulationResult
from engine.simulation import run_simulation

logger = logging.getLogger("finmirror.simulation_service")


def simulate(
    profile: FinancialProfile,
    scenario: ScenarioParams,
) -> SimulationResult:
    logger.info(
        "Running simulation",
        extra={
            "user_id": profile.user_id,
            "monte_carlo": scenario.monte_carlo,
        },
    )

    result = run_simulation(profile, scenario)

    SIMULATIONS_RUN_COUNTER.labels(
        monte_carlo=str(scenario.monte_carlo)
    ).inc()

    logger.info(
        "Simulation complete",
        extra={
            "user_id": profile.user_id,
            "goal_status": result.goal_projected_status,
        },
    )

    return result
