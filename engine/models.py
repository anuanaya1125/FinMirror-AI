"""
Pydantic models defining the data contract used across the system:
data -> engine -> genai -> api -> frontend.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class IncomeStability(str, Enum):
    stable = "stable"
    variable = "variable"
    seasonal = "seasonal"


class ProfileType(str, Enum):
    salaried = "salaried"
    freelancer = "freelancer"
    small_business_owner = "small_business_owner"
    gig_worker = "gig_worker"


class Income(BaseModel):
    monthly_income: float = Field(..., gt=0)
    income_stability: IncomeStability = IncomeStability.stable


class FixedExpenses(BaseModel):
    rent: float = 0
    utilities: float = 0
    loan_payments: float = 0
    insurance: float = 0

    def total(self) -> float:
        return (
            self.rent
            + self.utilities
            + self.loan_payments
            + self.insurance
        )


class VariableExpenses(BaseModel):
    groceries: float = 0
    transport: float = 0
    entertainment: float = 0
    misc: float = 0

    def total(self) -> float:
        return (
            self.groceries
            + self.transport
            + self.entertainment
            + self.misc
        )


class SavingsGoal(BaseModel):
    target_amount: float = Field(..., ge=0)
    deadline_months: int = Field(..., gt=0)


class HistoryMonth(BaseModel):
    month_offset: int
    income: float
    expenses: float
    net_cashflow: float


class FinancialProfile(BaseModel):
    """Full input profile for a user."""

    user_id: str
    name: str
    profile_type: ProfileType = ProfileType.salaried
    currency: str = "PKR"
    income: Income
    fixed_expenses: FixedExpenses
    variable_expenses: VariableExpenses
    current_savings: float = Field(..., ge=0)
    savings_goal: SavingsGoal
    history_months: list[HistoryMonth] = Field(default_factory=list)


class ScenarioParams(BaseModel):
    """Parameters controlling one what-if simulation."""

    income_change_pct: float = 0.0
    expense_change_pct: float = 0.0
    horizon_months: int = Field(12, gt=0, le=120)

    monte_carlo: bool = False
    monte_carlo_runs: int = Field(200, gt=0, le=5000)

    income_volatility_pct: float = Field(5.0, ge=0)
    expense_volatility_pct: float = Field(8.0, ge=0)


class RiskFlag(BaseModel):
    code: str
    severity: str
    message: str


class MonthlyProjection(BaseModel):
    month: int
    balance: float
    balance_p10: Optional[float] = None
    balance_p50: Optional[float] = None
    balance_p90: Optional[float] = None


class SimulationResult(BaseModel):
    """Structured contract passed from engine to GenAI."""

    user_id: str
    currency: str
    current_balance: float
    monthly_net_cashflow: float
    scenario: ScenarioParams
    scenario_description: str
    projected_balances: list[MonthlyProjection]
    goal_target_amount: float
    goal_deadline_months: int
    goal_projected_status: str
    risk_flags: list[RiskFlag] = Field(default_factory=list)
