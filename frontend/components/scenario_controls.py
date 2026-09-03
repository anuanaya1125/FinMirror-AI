"""Scenario controls: sliders for income change %, expense change %, time horizon."""

from __future__ import annotations

import streamlit as st


def render_scenario_controls() -> dict:
    st.subheader("Scenario Simulator")

    col1, col2 = st.columns(2)

    with col1:
        income_change_pct = st.slider(
            "Income change (%)",
            min_value=-100,
            max_value=100,
            value=0,
            step=5,
            help="Simulate a raise, a pay cut, or a full income loss.",
        )

        horizon_months = st.slider(
            "Time horizon (months)",
            min_value=3,
            max_value=60,
            value=12,
            step=1,
        )

    with col2:
        expense_change_pct = st.slider(
            "Expense change (%)",
            min_value=-50,
            max_value=100,
            value=0,
            step=5,
            help="Simulate rising costs (e.g. inflation) or successful budget cuts.",
        )

        monte_carlo = st.checkbox(
            "Enable Monte Carlo mode",
            value=False,
            help="Show a range of possible futures instead of a single line, using randomized monthly variation.",
        )

    return {
        "income_change_pct": float(income_change_pct),
        "expense_change_pct": float(expense_change_pct),
        "horizon_months": int(horizon_months),
        "monte_carlo": monte_carlo,
        "monte_carlo_runs": 300,
        "income_volatility_pct": 5.0,
        "expense_volatility_pct": 8.0,
    }
