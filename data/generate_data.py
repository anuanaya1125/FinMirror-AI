"""
FinMirror AI - Synthetic Data Generator

Generates realistic synthetic financial profiles for demo purposes.
Run:
    python data/generate_data.py

Produces:
    data/sample_data/financial_data.json
"""

import json
import random
from pathlib import Path

from faker import Faker

fake = Faker()

OUTPUT_PATH = Path(__file__).parent / "sample_data" / "financial_data.json"


def generate_history(
    monthly_income: float,
    fixed_expenses: dict,
    variable_expenses: dict,
    months: int = 6,
) -> list:
    """Generate trailing monthly cashflow history."""
    fixed_total = sum(fixed_expenses.values())
    variable_total = sum(variable_expenses.values())

    history = []

    for i in range(months, 0, -1):
        noise_income = monthly_income * random.uniform(-0.08, 0.08)
        noise_expense = variable_total * random.uniform(-0.15, 0.15)

        month_income = round(monthly_income + noise_income, 2)
        month_expenses = round(fixed_total + variable_total + noise_expense, 2)

        history.append(
            {
                "month_offset": -i,
                "income": month_income,
                "expenses": month_expenses,
                "net_cashflow": round(month_income - month_expenses, 2),
            }
        )

    return history


def generate_profile(seed: int | None = None) -> dict:
    """Generate one synthetic financial profile."""

    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    monthly_income = round(random.uniform(40000, 250000), 2)

    fixed_expenses = {
        "rent": round(monthly_income * random.uniform(0.15, 0.30), 2),
        "utilities": round(random.uniform(3000, 15000), 2),
        "loan_payments": round(random.uniform(0, monthly_income * 0.15), 2),
        "insurance": round(random.uniform(0, 5000), 2),
    }

    variable_expenses = {
        "groceries": round(random.uniform(10000, 40000), 2),
        "transport": round(random.uniform(3000, 20000), 2),
        "entertainment": round(random.uniform(2000, 15000), 2),
        "misc": round(random.uniform(2000, 10000), 2),
    }

    current_savings = round(random.uniform(5000, 500000), 2)
    savings_goal = round(
        current_savings + random.uniform(50000, 500000),
        2,
    )

    goal_deadline_months = random.choice([6, 12, 18, 24, 36])

    return {
        "user_id": fake.uuid4(),
        "name": fake.name(),
        "profile_type": random.choice(
            [
                "salaried",
                "freelancer",
                "small_business_owner",
                "gig_worker",
            ]
        ),
        "currency": "PKR",
        "income": {
            "monthly_income": monthly_income,
            "income_stability": random.choice(
                ["stable", "variable", "seasonal"]
            ),
        },
        "fixed_expenses": fixed_expenses,
        "variable_expenses": variable_expenses,
        "current_savings": current_savings,
        "savings_goal": {
            "target_amount": savings_goal,
            "deadline_months": goal_deadline_months,
        },
        "history_months": generate_history(
            monthly_income,
            fixed_expenses,
            variable_expenses,
        ),
    }


def generate_dataset(n_profiles: int = 5, seed: int = 42) -> list:
    """Generate multiple synthetic profiles."""
    random.seed(seed)

    return [
        generate_profile(seed=seed + i)
        for i in range(n_profiles)
    ]


def main() -> None:
    dataset = generate_dataset(n_profiles=5)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            dataset,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Generated {len(dataset)} synthetic profiles -> "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
