"""Simulation chart: baseline vs. scenario projection, with Monte Carlo bands."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st


def render_projection_chart(simulation_result: dict, currency: str = "PKR") -> None:
    st.subheader("Projected Balance")

    projections = simulation_result["projected_balances"]
    months = [p["month"] for p in projections]
    balances = [p["balance"] for p in projections]

    fig = go.Figure()

    is_monte_carlo = projections and projections[0].get("balance_p10") is not None

    if is_monte_carlo:
        p10 = [p["balance_p10"] for p in projections]
        p90 = [p["balance_p90"] for p in projections]

        fig.add_trace(
            go.Scatter(
                x=months + months[::-1],
                y=p90 + p10[::-1],
                fill="toself",
                fillcolor="rgba(99, 110, 250, 0.15)",
                line=dict(color="rgba(255,255,255,0)"),
                name="p10-p90 range",
                hoverinfo="skip",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=months,
                y=balances,
                mode="lines",
                name="Median (p50)",
                line=dict(width=3),
            )
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=months,
                y=balances,
                mode="lines+markers",
                name="Projected balance",
            )
        )

    fig.add_hline(
        y=0,
        line_dash="dot",
        line_color="red",
        annotation_text="Zero balance",
    )

    fig.add_hline(
        y=simulation_result["goal_target_amount"],
        line_dash="dash",
        line_color="green",
        annotation_text="Savings goal",
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=f"Balance ({currency})",
        height=420,
        margin=dict(l=10, r=10, t=30, b=10),
    )

    st.plotly_chart(fig, use_container_width=True)

    status_colors = {
        "on_track": "🟢",
        "achieved_early": "🟢",
        "at_risk": "🟡",
        "missed": "🔴",
    }

    status = simulation_result["goal_projected_status"]

    st.markdown(
        f"**Goal status:** {status_colors.get(status, '')} `{status}`"
    )

    for flag in simulation_result.get("risk_flags", []):
        icon = {
            "critical": "🔴",
            "warning": "🟡",
            "info": "🔵",
        }.get(flag["severity"], "🔵")

        st.markdown(
            f"{icon} **{flag['code']}** — {flag['message']}"
        )
