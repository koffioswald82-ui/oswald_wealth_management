# 💎 Oswald Wealth Management

> **Your AI Private Banker — Institutional Wealth Intelligence for Everyone**

A full-featured, locally-runnable wealth management platform built with Python and Streamlit. Designed as a life financial operating system for students, immigrants, families, entrepreneurs, and middle-class individuals who deserve institutional-grade financial planning.

---

## Features

| Module | Description |
|---|---|
| 📈 Life Trajectory | Year-by-year wealth projection to age 85 + Prophet ML forecasts |
| 💼 Investments | Monte Carlo (1000 paths), MPT Efficient Frontier, Portfolio Optimizer |
| 🏡 Real Estate | Mortgage affordability, Rent vs Buy NPV, Investment property analysis |
| 👶 Children Planning | True cost of raising a child, financial readiness score, education savings |
| ⚡ Crisis Simulation | Unemployment, medical emergency, market crash, inflation shock, divorce |
| 🔮 Scenarios | Compare up to 4 life paths (Base, Disciplined Investor, Premium Lifestyle, FIRE) |
| 🤖 AI Coaching | Rule-based + optional Claude API personalized insights with dollar impact |
| ⭐ Wealth Score | Proprietary 0–1000 multi-factor score with age benchmark |

---

## Tech Stack

- **Frontend:** Streamlit
- **Database:** SQLite (local, no cloud required)
- **Math:** NumPy, SciPy, Pandas
- **Charts:** Plotly
- **ML:** Prophet (time-series forecasting), scikit-learn
- **Finance:** Modern Portfolio Theory, GBM Monte Carlo, Amortization
- **AI (optional):** Anthropic Claude API

---

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/oswald-wealth-management.git
cd oswald-wealth-management
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note Prophet:** If you have issues installing Prophet, you can skip it — the platform falls back to linear projection automatically.
> ```bash
> pip install prophet  # May require pystan: pip install pystan==2.19.1.1 first on some systems
> ```

### 4. Run
```bash
streamlit run main.py
```

Open `http://localhost:8501` in your browser.

---

## Streamlit Cloud Deployment

1. Push to GitHub (repo must be public or you must be on Streamlit Cloud paid plan for private repos)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo, `main` branch, `main.py` as entrypoint
5. Add secrets (optional): `ANTHROPIC_API_KEY = "sk-ant-..."`

---

## Environment Variables (Optional)

Create a `.env` file or set in Streamlit Cloud secrets:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

This enables the Claude AI deep analysis feature in the Coaching module.

---

## Project Structure

```
oswald_wealth_management/
├── main.py                      # Home dashboard
├── requirements.txt
├── .streamlit/config.toml       # Dark gold theme
├── assets/style.css             # Premium UI styling
├── app/config.py                # App configuration
├── database/db_manager.py       # SQLite operations
├── models/user_profile.py       # User data model
├── utils/
│   ├── constants.py             # Country data, asset classes
│   ├── financial_math.py        # Core financial formulas
│   └── formatters.py            # Display formatting
├── engines/
│   ├── life_trajectory.py       # Life modeling engine
│   ├── child_planning.py        # Child cost engine
│   ├── real_estate.py           # Property engine
│   ├── investment.py            # Investment engine
│   ├── crisis_simulation.py     # Crisis scenarios
│   ├── wealth_score.py          # Wealth scoring
│   ├── ai_coaching.py           # AI coaching logic
│   └── scenario_simulation.py  # Life scenarios
├── simulations/
│   ├── monte_carlo.py           # GBM Monte Carlo
│   ├── portfolio_optimizer.py   # MPT optimization
│   └── prophet_forecasting.py  # Prophet forecasts
└── pages/
    ├── 1_Profile.py
    ├── 2_Trajectory.py
    ├── 3_Investments.py
    ├── 4_Real_Estate.py
    ├── 5_Children.py
    ├── 6_Crisis.py
    ├── 7_Scenarios.py
    ├── 8_Coaching.py
    └── 9_Wealth_Score.py
```

---

## Countries Supported

France · Belgium · Germany · United Kingdom · United States · Canada · Switzerland · Ivory Coast · Senegal

Each country has calibrated data: income benchmarks, mortgage rates, inflation, child costs, tax brackets, pension replacement rates.

---

## Financial Models Used

- **GBM (Geometric Brownian Motion)** — Monte Carlo portfolio simulation
- **Modern Portfolio Theory (MPT)** — Efficient frontier, max Sharpe portfolio
- **Fisher Equation** — Real vs nominal returns
- **4% Safe Withdrawal Rule (Bengen)** — Retirement planning
- **Prophet (Meta)** — ML time-series forecasting for income and property
- **28/36 Rule** — Mortgage affordability
- **DSCR** — Investment property viability

---

## Roadmap

- [ ] Tax optimization module (PEA, assurance-vie, deficit foncier)
- [ ] Insurance planning (life, disability, health gap analysis)
- [ ] Multi-currency portfolio for immigrants
- [ ] PDF report export
- [ ] Mobile-responsive PWA wrapper
- [ ] Plaid/Bankin integration for automatic account sync
- [ ] Social comparison (anonymized peer benchmarks)

---

## License

MIT License — Free for personal and commercial use.

---

*Built with institutional-grade financial logic. Not investment advice.*
