"""
Current financial state calculations.
"""

from __future__ import annotations

from engine.models import FinancialProfile


def compute_monthly_net_cashflow(profile: FinancialProfile) -> float:
    """Monthly income minus fixed and variable expenses."""
    total_expenses = (
        profile.fixed_expenses.total()
        + profile.variable_expenses.total()
    )

    return round(
        profile.income.monthly_income - total_expenses,
        2,
    )


def compute_net_worth(profile: FinancialProfile) -> float:
    """Simplified MVP net worth: current liquid savings."""
    return round(profile.current_savings, 2)


def compute_savings_trajectory(profile: FinancialProfile) -> dict:
    """Estimate time required to reach the savings goal."""
    net_cashflow = compute_monthly_net_cashflow(profile)

    remaining = (
        profile.savings_goal.target_amount
        - profile.current_savings
    )

    if remaining <= 0:
        return {
            "months_to_goal": 0,
            "on_track": True,
            "note": "Savings goal already met.",
        }

    if net_cashflow <= 0:
        return {
            "months_to_goal": None,
            "on_track": False,
            "note": (
                "Current net cashflow is zero or negative; "
                "goal is not reachable without a change."
            ),
        }

    months_needed = remaining / net_cashflow
    on_track = (
        months_needed
        <= profile.savings_goal.deadline_months
    )

    return {
        "months_to_goal": round(months_needed, 1),
        "on_track": on_track,
        "note": (
            "On track to meet the goal within the deadline."
            if on_track
            else "At current pace, the goal will be missed before the deadline."
        ),
    }


def compute_current_state(profile: FinancialProfile) -> dict:
    """Bundle current-state figures for the dashboard."""
    return {
        "net_worth": compute_net_worth(profile),
        "monthly_net_cashflow": compute_monthly_net_cashflow(profile),
        "savings_trajectory": compute_savings_trajectory(profile),
    }
