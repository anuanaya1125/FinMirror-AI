"""
FinMirror AI - FastAPI backend entry point.

Run locally:

    uvicorn api.main:app --reload --host 0.0.0.0 --port 9000

Then visit:
    http://localhost:9000/docs
    http://localhost:9000/health
    http://localhost:9000/metrics
"""

from __future__ import annotations

import logging
import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pythonjsonlogger import jsonlogger

from api.routes import health, insight, simulate
from api.routes.metrics import setup_metrics

load_dotenv()


def configure_logging() -> None:
    """Configure structured JSON logging."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = [handler]


configure_logging()

logger = logging.getLogger("finmirror.api")


app = FastAPI(
    title="FinMirror AI API",
    description="Financial Digital Twin - simulation + GenAI insight backend.",
    version="2.2.0",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Prometheus metrics
setup_metrics(app)


# API routes
app.include_router(health.router)
app.include_router(simulate.router)
app.include_router(insight.router)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("FinMirror AI API starting up")


@app.get("/", tags=["root"])
def root() -> dict:
    return {
        "service": "finmirror-ai-api",
        "status": "running",
        "docs": "/docs",
        "endpoints": [
            "/simulate",
            "/insight",
            "/insight/ask",
            "/health",
            "/metrics",
        ],
    }
