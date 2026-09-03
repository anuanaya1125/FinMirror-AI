"""
Simulation logic for the Financial Digital Twin.

Implements:
- Baseline: deterministic month-by-month projection under a
  percentage change to income/expenses.
- Enhanced: Monte Carlo simulation with randomized monthly variation,
  producing a distribution of possible futures (p10/p50/p90 bands).

This is step 4-5 of Workstream A in the TRD, and produces the
structured JSON result (SimulationResult) handed to Workstream B.
"""

from __future__ import annotations

import numpy as np

from engine.calculations import compute_monthly_net_cashflow, compute_net_worth
from engine.models import (
    FinancialProfile,
    MonthlyProjection,
    RiskFlag,
    ScenarioParams,
    SimulationResult,
)


def _scenario_description(params: ScenarioParams) -> str:
    parts = []
    if params.income_change_pct:
        direction = "increase" if params.income_change_pct > 0 else "decrease"
        parts.append(f"income {direction}s {abs(params.income_change_pct):.0f}%")
    if params.expense_change_pct:
        direction = "increase" if params.expense_change_pct > 0 else "decrease"
        parts.append(f"expenses {direction}s {abs(params.expense_change_pct):.0f}%")
    if not parts:
        parts.append("no change to income or expenses (baseline continuation)")
    mode = "Monte Carlo" if params.monte_carlo else "deterministic"
    return f"{', '.join(parts)} over {params.horizon_months} months ({mode} projection)"


def _deterministic_projection(
    start_balance: float,
    monthly_income: float,
    monthly_expenses: float,
    params: ScenarioParams,
) -> list[MonthlyProjection]:
    adj_income = monthly_income * (1 + params.income_change_pct / 100)
    adj_expenses = monthly_expenses * (1 + params.expense_change_pct / 100)
    net = adj_income - adj_expenses

    projections = []
    balance = start_balance
    for month in range(1, params.horizon_months + 1):
        balance = round(balance + net, 2)
        projections.append(MonthlyProjection(month=month, balance=balance))
    return projections


def _monte_carlo_projection(
    start_balance: float,
    monthly_income: float,
    monthly_expenses: float,
    params: ScenarioParams,
) -> list[MonthlyProjection]:
    rng = np.random.default_rng()

    adj_income = monthly_income * (1 + params.income_change_pct / 100)
    adj_expenses = monthly_expenses * (1 + params.expense_change_pct / 100)

    income_sigma = adj_income * (params.income_volatility_pct / 100)
    expense_sigma = adj_expenses * (params.expense_volatility_pct / 100)

    n_runs = params.monte_carlo_runs
    horizon = params.horizon_months

    # shape: (n_runs, horizon)
    income_samples = rng.normal(adj_income, income_sigma, size=(n_runs, horizon))
    expense_samples = rng.normal(adj_expenses, expense_sigma, size=(n_runs, horizon))

    net_samples = income_samples - expense_samples
    balances = start_balance + np.cumsum(net_samples, axis=1)

    p10 = np.percentile(balances, 10, axis=0)
    p50 = np.percentile(balances, 50, axis=0)
    p90 = np.percentile(balances, 90, axis=0)

    projections = []
    for i in range(horizon):
        projections.append(
            MonthlyProjection(
                month=i + 1,
                balance=round(float(p50[i]), 2),
                balance_p10=round(float(p10[i]), 2),
                balance_p50=round(float(p50[i]), 2),
                balance_p90=round(float(p90[i]), 2),
            )
        )
    return projections


def _evaluate_goal(
    projections: list[MonthlyProjection],
    goal_target: float,
    goal_deadline_months: int,
) -> str:
    if not projections:
        return "at_risk"

    horizon = len(projections)
    deadline_idx = min(goal_deadline_months, horizon) - 1
    balance_at_deadline = projections[deadline_idx].balance

    if balance_at_deadline >= goal_target:
        # check if achieved earlier than deadline
        for p in projections:
            if p.balance >= goal_target:
                if p.month < goal_deadline_months:
                    return "achieved_early"
                return "on_track"
        return "on_track"

    # Not met by deadline - is it close (within 10%) or a clear miss?
    shortfall_pct = (goal_target - balance_at_deadline) / max(goal_target, 1) * 100
    return "at_risk" if shortfall_pct <= 15 else "missed"


def _generate_risk_flags(
    projections: list[MonthlyProjection],
    monthly_net_cashflow: float,
    goal_status: str,
) -> list[RiskFlag]:
    flags: list[RiskFlag] = []

    negative_months = [p for p in projections if p.balance < 0]
    if negative_months:
        first_negative = negative_months[0]
        flags.append(
            RiskFlag(
                code="NEGATIVE_BALANCE",
                severity="critical",
                message=(
                    f"Projected balance goes negative in month {first_negative.month} "
                    f"under this scenario."
                ),
            )
        )

    if monthly_net_cashflow < 0:
        flags.append(
            RiskFlag(
                code="NEGATIVE_CASHFLOW",
                severity="warning",
                message="Current monthly net cashflow is already negative before applying the scenario.",
            )
        )

    if goal_status == "missed":
        flags.append(
            RiskFlag(
                code="GOAL_MISSED",
                severity="critical",
                message="Savings goal is projected to be missed by the deadline under this scenario.",
            )
        )
    elif goal_status == "at_risk":
        flags.append(
            RiskFlag(
                code="GOAL_AT_RISK",
                severity="warning",
                message="Savings goal is close but at risk of being missed under this scenario.",
            )
        )

    return flags


def run_simulation(profile: FinancialProfile, params: ScenarioParams) -> SimulationResult:
    """Main entry point for Workstream A: run a scenario simulation
    for a given profile and return the structured JSON contract."""

    start_balance = compute_net_worth(profile)
    monthly_income = profile.income.monthly_income
    monthly_expenses = profile.fixed_expenses.total() + profile.variable_expenses.total()
    monthly_net_cashflow = compute_monthly_net_cashflow(profile)

    if params.monte_carlo:
        projections = _monte_carlo_projection(start_balance, monthly_income, monthly_expenses, params)
    else:
        projections = _deterministic_projection(start_balance, monthly_income, monthly_expenses, params)

    goal_status = _evaluate_goal(
        projections, profile.savings_goal.target_amount, profile.savings_goal.deadline_months
    )
    risk_flags = _generate_risk_flags(projections, monthly_net_cashflow, goal_status)

    return SimulationResult(
        user_id=profile.user_id,
        currency=profile.currency,
        current_balance=start_balance,
        monthly_net_cashflow=monthly_net_cashflow,
        scenario=params,
        scenario_description=_scenario_description(params),
        projected_balances=projections,
        goal_target_amount=profile.savings_goal.target_amount,
        goal_deadline_months=profile.savings_goal.deadline_months,
        goal_projected_status=goal_status,
        risk_flags=risk_flags,
    )

