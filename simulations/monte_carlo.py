"""
Monte Carlo Simulation Engine
Geometric Brownian Motion for portfolio value + wealth projection.
1000 paths by default, monthly time steps.
"""
import numpy as np
import pandas as pd

class MonteCarloEngine:

    def __init__(self, n_simulations: int = 1000, seed: int = 42):
        self.n    = n_simulations
        self.rng  = np.random.default_rng(seed)

    def run_portfolio_simulation(
        self,
        initial_value:      float,
        monthly_contribution: float,
        annual_return:      float,
        annual_volatility:  float,
        years:              int,
        contribution_growth: float = 0.02,
    ) -> np.ndarray:
        """
        GBM simulation. Returns array of shape (n_simulations, years*12+1).
        Each row is one simulated portfolio path.
        """
        dt       = 1 / 12
        months   = years * 12
        paths    = np.zeros((self.n, months + 1))
        paths[:, 0] = initial_value

        mu  = annual_return
        sig = annual_volatility

        for t in range(1, months + 1):
            z = self.rng.standard_normal(self.n)
            # GBM: dS = S * (mu*dt + sigma*sqrt(dt)*Z)
            paths[:, t] = (
                paths[:, t - 1]
                * np.exp((mu - 0.5 * sig ** 2) * dt + sig * np.sqrt(dt) * z)
                + monthly_contribution * (1 + contribution_growth) ** (t / 12)
            )

        return paths

    def get_statistics(self, paths: np.ndarray) -> dict:
        """Compute percentile statistics across all simulations at each time step."""
        p5   = np.percentile(paths, 5, axis=0)
        p25  = np.percentile(paths, 25, axis=0)
        p50  = np.percentile(paths, 50, axis=0)
        p75  = np.percentile(paths, 75, axis=0)
        p95  = np.percentile(paths, 95, axis=0)
        mean = np.mean(paths, axis=0)
        return {
            "p5": p5, "p25": p25, "p50": p50,
            "p75": p75, "p95": p95, "mean": mean,
            "final_p5": float(p5[-1]),
            "final_p50": float(p50[-1]),
            "final_p95": float(p95[-1]),
            "final_mean": float(mean[-1]),
        }

    def calculate_ruin_probability(
        self,
        paths:           np.ndarray,
        monthly_withdrawal: float,
        years_in_retirement: int,
    ) -> float:
        """
        Probability that the portfolio runs out during retirement.
        Simulates withdrawal phase from final portfolio values.
        """
        final_values = paths[:, -1]
        ruined = 0

        for port in final_values:
            val = port
            for _ in range(years_in_retirement * 12):
                if val <= 0:
                    ruined += 1
                    break
                ret = self.rng.normal(0.005, 0.04)  # monthly return during retirement
                val = val * (1 + ret) - monthly_withdrawal

        return ruined / len(final_values)

    def wealth_distribution_at_retirement(self, paths: np.ndarray) -> pd.DataFrame:
        """Distribution of final portfolio values."""
        finals = paths[:, -1]
        return pd.DataFrame({
            "Patrimoine final": finals,
            "Catégorie": pd.cut(
                finals,
                bins=[0, 100_000, 250_000, 500_000, 1_000_000, float("inf")],
                labels=["<100k", "100-250k", "250-500k", "500k-1M", ">1M"],
            ),
        })

    def portfolio_var(self, paths: np.ndarray, confidence: float = 0.95) -> dict:
        """Value at Risk at 1-year horizon (first 12 steps)."""
        one_year_returns = (paths[:, 12] - paths[:, 0]) / paths[:, 0]
        var = np.percentile(one_year_returns, (1 - confidence) * 100)
        cvar = one_year_returns[one_year_returns <= var].mean()
        return {
            "var_pct": var,
            "cvar_pct": cvar,
            "var_amount": abs(var) * paths[0, 0],
            "cvar_amount": abs(cvar) * paths[0, 0],
            "confidence": confidence,
        }

    def to_dataframe(self, paths: np.ndarray, years: int, age_start: int = 30) -> pd.DataFrame:
        """Convert simulation paths to DataFrame for Plotly."""
        stats = self.get_statistics(paths)
        months = years * 12
        df = pd.DataFrame({
            "month": range(months + 1),
            "age": [age_start + m / 12 for m in range(months + 1)],
            "p5":   stats["p5"],
            "p25":  stats["p25"],
            "p50":  stats["p50"],
            "p75":  stats["p75"],
            "p95":  stats["p95"],
            "mean": stats["mean"],
        })
        return df
