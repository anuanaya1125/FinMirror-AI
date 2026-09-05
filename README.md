# FinMirror AI 💰🤖

### Simulating Financial Futures Through AI-Powered Scenario Analysis

FinMirror AI is an AI-powered Financial Digital Twin designed to help users understand, simulate, and improve their financial future.

Instead of only showing users what they have spent or saved, FinMirror AI lets them explore **"what-if" financial scenarios** and see how those decisions could affect their future.

---

## 🎯 Problem

Most personal finance tools focus on historical spending and current balances.

But users often need answers to questions like:

- What happens if my income decreases?
- Can I reach my savings goal?
- When could I run out of money?
- How will changing my expenses affect my future?
- What financial risks should I be aware of?

FinMirror AI addresses this gap by combining **financial simulation with Generative AI**.

---

## 💡 Solution

FinMirror AI creates a simplified digital twin of a user's financial state and simulates possible financial futures.

### Core Flow

**Financial Data → Simulation → Future Projection → Risk & Goal Analysis → AI Insights**

The simulation engine calculates the financial outcomes first.
The AI layer then interprets those results and explains them in clear, understandable language.

---

## ✨ Key Features

- 🔮 **What-If Scenario Simulation**
  - Modify income, expenses, and time horizons.
  - Explore the impact of financial changes.

- 📊 **Deterministic Financial Projection**
  - Projects future balances and cash flow month by month.

- 🎲 **Monte Carlo Forecasting**
  - Generates a range of possible financial outcomes under uncertainty.

- 🎯 **Savings Goal Analysis**
  - Tracks whether financial goals are achievable within the selected timeframe.

- ⚠️ **Risk Detection**
  - Identifies negative cash flow, potential negative balances, and missed financial goals.

- 🤖 **AI Financial Insights**
  - Uses Google Gemini to interpret simulation results and provide personalized explanations.

- 💬 **Ask Your Twin**
  - Allows users to ask questions about their simulated financial future.

---

## 🏗️ System Architecture

```text
Financial Profile
       ↓
Simulation Engine
       ↓
Structured Simulation Results
       ↓
Risk & Goal Analysis
       ↓
Generative AI Layer
       ↓
FastAPI Backend
       ↓
Interactive Streamlit Dashboard
```

### Important Design Principle

> **The numbers are calculated by the simulation engine. AI explains what they mean.**

This keeps financial projections grounded in deterministic calculations rather than letting the AI invent numerical results.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Data Processing | Pandas, NumPy |
| Generative AI | Google Gemini API |
| Frontend | Streamlit |
| Visualization | Plotly |
| Validation | Pydantic |
| Server | Uvicorn |
| Monitoring | Prometheus, Grafana |
| Containerization | Docker |
| Version Control | Git, GitHub |
| CI | GitHub Actions |

---

## 📁 Project Structure

```text
FinMirror-AI/
│
├── api/                # FastAPI backend
├── data/               # Financial/synthetic data
├── engine/             # Financial simulation engine
├── frontend/           # Streamlit dashboard
├── genai/              # Generative AI integration
├── infra/              # Docker, Prometheus & Grafana
├── tests/              # Automated tests
├── .github/workflows/  # CI workflows
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🚀 Running the Project

### Using Docker

```bash
git clone https://github.com/anuanaya1125/FinMirror-AI.git
cd FinMirror-AI
cp .env.example .env   # then fill in your GenAI provider config
docker compose -f infra/docker-compose.yml up --build
```

The dashboard will be available at `http://localhost:8501`.

---

## 🧪 Example Scenario

A user simulates a scenario such as **"income decreases by 20%."** FinMirror AI recalculates cash flow, projects future balances, checks the savings goal, flags any risks, and returns a plain-language explanation of what it means — moving from simply **tracking finances** to **understanding possible futures**.

---

## 🌍 Financial Inclusion

FinMirror AI is designed with accessibility in mind.

The concept is particularly useful for:

- Students
- Young professionals
- Early-career individuals
- Users with limited access to personalized financial guidance

The goal is to make financial planning more **accessible, understandable, and forward-looking**.

---

## 🔐 Security & Data

The current prototype uses synthetic financial data.

API keys and other sensitive credentials must be stored in environment variables and excluded from version control via `.gitignore`.

---

## 🔮 Future Scope

Future versions of FinMirror AI could include:

- Integration with real financial data sources
- Personalized financial alerts
- Regional language and voice support
- Advanced goal planning
- More sophisticated financial forecasting
- Expanded financial risk analysis
- Personalized long-term financial planning

---

## 🏆 AI Hackathon Pakistan 2026

**Project:** FinMirror AI
**Project ID:** P00058
**Track:** Financial Inclusion
**Region:** Islamabad
**Institution:** University of Engineering and Technology, Taxila

### Team

- **Anaya** — Team Lead
- **Abdur Rehman** — Analyst
- **Zeeshan Khan** — DevOps Engineer
- **Ammar Nisar Bodla** — Support Member

---

## 📌 Project Vision

> **Don't just track your finances. Simulate your future.**
