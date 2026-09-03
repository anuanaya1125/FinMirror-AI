"""Current state summary panel: net worth, cashflow."""

from __future__ import annotations

import streamlit as st


def render_current_state(profile: dict, currency: str = "PKR") -> None:
    st.subheader("Current Financial State")

    fixed_total = sum(profile["fixed_expenses"].values())
    variable_total = sum(profile["variable_expenses"].values())
    net_cashflow = profile["income"]["monthly_income"] - fixed_total - variable_total

    col1, col2, col3 = st.columns(3)
    col1.metric("Net Worth (savings)", f"{currency} {profile['current_savings']:,.0f}")
    col2.metric("Monthly Income", f"{currency} {profile['income']['monthly_income']:,.0f}")
    col3.metric(
        "Monthly Net Cashflow",
        f"{currency} {net_cashflow:,.0f}",
        delta=None,
        delta_color="normal" if net_cashflow >= 0 else "inverse",
    )

    goal = profile["savings_goal"]
    st.progress(
        min(profile["current_savings"] / goal["target_amount"], 1.0),
        text=(
            f"Savings goal: {currency} {profile['current_savings']:,.0f} / "
            f"{currency} {goal['target_amount']:,.0f} within {goal['deadline_months']} months"
        ),
    )

