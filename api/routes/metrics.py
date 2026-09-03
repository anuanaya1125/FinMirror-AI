"""Prometheus metrics for the FinMirror AI API."""

from __future__ import annotations

from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator


GENAI_FALLBACK_COUNTER = Counter(
    "finmirror_genai_fallback_total",
    "Number of times the GenAI layer used a fallback response.",
)


SIMULATIONS_RUN_COUNTER = Counter(
    "finmirror_simulations_total",
    "Total number of scenario simulations run.",
    labelnames=("monte_carlo",),
)


def setup_metrics(app: FastAPI) -> None:
    """Attach Prometheus HTTP metrics to the FastAPI application."""
    Instrumentator().instrument(app).expose(
        app,
        endpoint="/metrics",
        include_in_schema=False,
    )
