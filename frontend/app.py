"""
FinMirror AI - Streamlit Dashboard (Workstream D).

Run locally:
    streamlit run frontend/app.py

Requires the FastAPI backend to be running (default http://localhost:9000).
Set API_BASE_URL in .env to point elsewhere (e.g. the Docker Compose
service name http://api:9000 when running inside Compose).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# Allow running `streamlit run frontend/app.py` from repo root without install
sys.path.insert(0, str(Path(__file__).parent.parent))

from frontend.components.charts import render_projection_chart
from frontend.components.dashboard import render_current_state
from frontend.components.insight_panel import render_insight_panel, render_qa_panel
from frontend.components.scenario_controls import render_scenario_controls

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:9000")

DATA_PATH = Path(__file__).parent.parent / "data" / "sample_data" / "financial_data.json"

LANGUAGE_OPTIONS = {"English": "en", "Urdu": "ur", "Roman Urdu": "roman_ur"}

st.set_page_config(page_title="FinMirror AI", page_icon="💠", layout="wide")


@st.cache_data(ttl=5)
def load_profiles() -> list[dict]:
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def call_simulate(profile: dict, scenario: dict) -> dict:
    resp = requests.post(f"{API_BASE_URL}/simulate", json={"profile": profile, "scenario": scenario}, timeout=30)
    resp.raise_for_status()
    return resp.json()["result"]


def call_insight(simulation_result: dict, language: str) -> tuple[str, bool]:
    resp = requests.post(
        f"{API_BASE_URL}/insight",
        json={"simulation": simulation_result, "language": language},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["insight_text"], data["used_fallback"]


def call_ask(simulation_result: dict, question: str, language: str) -> tuple[str, bool]:
    resp = requests.post(
        f"{API_BASE_URL}/insight/ask",
        json={"simulation": simulation_result, "question": question, "language": language},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["answer_text"], data["used_fallback"]


def main() -> None:
    st.title("💠 FinMirror AI — Financial Digital Twin")
    st.caption("Alibaba Cloud AI Hackathon 2026 — Bano Qabil / Alkhidmat Foundation Pakistan × Alibaba Cloud")

    profiles = load_profiles()
    if not profiles:
        st.error(
            "No sample data found. Run `python data/generate_data.py` first, "
            "then refresh this page."
        )
        st.stop()

    with st.sidebar:
        st.header("Settings")
        names = [f"{p['name']} ({p['profile_type']})" for p in profiles]
        idx = st.selectbox("Demo profile", range(len(profiles)), format_func=lambda i: names[i])
        language_label = st.selectbox("AI response language", list(LANGUAGE_OPTIONS.keys()))
        language = LANGUAGE_OPTIONS[language_label]
        st.divider()
        st.caption(f"API: `{API_BASE_URL}`")
        try:
            health = requests.get(f"{API_BASE_URL}/health", timeout=3)
            st.success("API reachable ✅") if health.ok else st.error("API returned an error")
        except requests.exceptions.RequestException:
            st.error("API unreachable — is the backend running?")

    profile = profiles[idx]
    currency = profile.get("currency", "PKR")

    render_current_state(profile, currency=currency)
    st.divider()

    scenario = render_scenario_controls()

    if st.button("Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            try:
                result = call_simulate(profile, scenario)
                st.session_state["last_result"] = result
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not reach the API: {exc}")
                st.stop()

    result = st.session_state.get("last_result")
    if result:
        st.divider()
        render_projection_chart(result, currency=currency)

        st.divider()
        with st.spinner("Generating AI insight..."):
            try:
                insight_text, used_fallback = call_insight(result, language)
                render_insight_panel(insight_text, used_fallback, language_label)
            except requests.exceptions.RequestException as exc:
                st.error(f"Could not reach the API for insight: {exc}")

        st.divider()
        render_qa_panel(call_ask, result, language)
    else:
        st.info("Adjust the sliders above and click **Run Simulation** to see your twin's projection.")


if __name__ == "__main__":
    main()
