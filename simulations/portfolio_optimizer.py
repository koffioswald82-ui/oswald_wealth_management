"""
Modern Portfolio Theory — Efficient Frontier + Maximum Sharpe Ratio Portfolio.
Uses scipy optimization with realistic asset class return/volatility/correlation estimates.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Asset class expected returns, volatilities, and correlation matrix
ASSET_RETURNS = np.array([0.075, 0.065, 0.085, 0.030, 0.040, 0.060, 0.040, 0.025])
ASSET_VOLS    = np.array([0.160, 0.150, 0.220, 0.050, 0.070, 0.120, 0.180, 0.005])
ASSET_NAMES   = [
    "Global Equities", "European Equities", "Emerging Markets",
    "Gov Bonds", "Corp Bonds", "Real Estate (REIT)",
    "Commodities", "Cash"
]

# Correlation matrix (8x8)
CORR = np.array([
    [1.00, 0.85, 0.72, -0.20, -0.10, 0.45,  0.15, -0.05],
    [0.85, 1.00, 0.65, -0.15, -0.05, 0.40,  0.10, -0.02],
    [0.72, 0.65, 1.00, -0.25, -0.15, 0.38,  0.20, -0.03],
    [-0.20,-0.15,-0.25, 1.00,  0.75, 0.10, -0.10,  0.05],
    [-0.10,-0.05,-0.15, 0.75,  1.00, 0.15, -0.05,  0.04],
    [0.45, 0.40, 0.38,  0.10,  0.15, 1.00,  0.25,  0.00],
    [0.15, 0.10, 0.20, -0.10, -0.05, 0.25,  1.00,  0.00],
    [-0.05,-0.02,-0.03, 0.05,  0.04, 0.00,  0.00,  1.00],
])

COV = np.outer(ASSET_VOLS, ASSET_VOLS) * CORR

class PortfolioOptimizer:

    def __init__(self, risk_free_rate: float = 0.025):
        self.rf       = risk_free_rate
        self.returns  = ASSET_RETURNS
        self.cov      = COV
        self.names    = ASSET_NAMES
        self.n        = len(self.names)

    def portfolio_stats(self, weights: np.ndarray) -> tuple[float, float, float]:
        ret  = np.dot(weights, self.returns)
        vol  = np.sqrt(np.dot(weights, np.dot(self.cov, weights)))
        sharpe = (ret - self.rf) / vol if vol > 0 else 0
        return ret, vol, sharpe

    def max_sharpe_portfolio(self, constraints: dict = None) -> dict:
        """Find the portfolio with maximum Sharpe ratio."""
        def neg_sharpe(w):
            r, v, s = self.portfolio_stats(w)
            return -s

        w0 = np.ones(self.n) / self.n
        bounds  = tuple((0.0, 1.0) for _ in range(self.n))
        con_list = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]

        if constraints:
            if "max_equity" in constraints:
                equity_idx = [0, 1, 2]
                con_list.append({
                    "type": "ineq",
                    "fun": lambda w, idx=equity_idx, mx=constraints["max_equity"]: mx - sum(w[i] for i in idx)
                })
            if "min_bonds" in constraints:
                bond_idx = [3, 4]
                con_list.append({
                    "type": "ineq",
                    "fun": lambda w, idx=bond_idx, mn=constraints["min_bonds"]: sum(w[i] for i in idx) - mn
                })
            if "max_cash" in constraints:
                con_list.append({
                    "type": "ineq",
                    "fun": lambda w, mx=constraints["max_cash"]: mx - w[7]
                })

        result = minimize(neg_sharpe, w0, method="SLSQP", bounds=bounds, constraints=con_list,
                          options={"maxiter": 1000, "ftol": 1e-9})
        w = result.x
        r, v, s = self.portfolio_stats(w)
        return {"weights": w, "return": r, "volatility": v, "sharpe": s,
                "allocation": dict(zip(self.names, w))}

    def min_variance_portfolio(self) -> dict:
        """Find minimum variance portfolio."""
        def portfolio_vol(w):
            return np.sqrt(np.dot(w, np.dot(self.cov, w)))

        w0     = np.ones(self.n) / self.n
        bounds = tuple((0.0, 1.0) for _ in range(self.n))
        cons   = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        result = minimize(portfolio_vol, w0, method="SLSQP", bounds=bounds, constraints=cons)
        w = result.x
        r, v, s = self.portfolio_stats(w)
        return {"weights": w, "return": r, "volatility": v, "sharpe": s,
                "allocation": dict(zip(self.names, w))}

    def efficient_frontier(self, n_points: int = 50) -> pd.DataFrame:
        """Generate the efficient frontier."""
        min_ret  = self.returns.min()
        max_ret  = self.returns.max()
        targets  = np.linspace(min_ret + 0.005, max_ret - 0.005, n_points)
        frontier = []

        for target in targets:
            def portfolio_vol(w):
                return np.sqrt(np.dot(w, np.dot(self.cov, w)))

            cons = [
                {"type": "eq", "fun": lambda w: np.sum(w) - 1},
                {"type": "eq", "fun": lambda w, t=target: np.dot(w, self.returns) - t},
            ]
            bounds = tuple((0.0, 1.0) for _ in range(self.n))
            result = minimize(portfolio_vol, np.ones(self.n) / self.n,
                              method="SLSQP", bounds=bounds, constraints=cons,
                              options={"maxiter": 1000, "ftol": 1e-9})
            if result.success:
                r, v, s = self.portfolio_stats(result.x)
                frontier.append({"return": r, "volatility": v, "sharpe": s})

        return pd.DataFrame(frontier)

    def risk_profiled_portfolio(self, risk_profile: str) -> dict:
        """
        Return a pre-set allocation based on risk profile.
        Then optimize within those bounds using MPT.
        """
        from utils.constants import RISK_PROFILES
        base = RISK_PROFILES.get(risk_profile, RISK_PROFILES["Modéré"])
        equity_max = base["equities"] + 0.10
        bond_min   = max(base["bonds"] - 0.05, 0)
        constraints = {
            "max_equity": equity_max,
            "min_bonds":  bond_min,
            "max_cash":   base.get("cash", 0.10) + 0.05,
        }
        return self.max_sharpe_portfolio(constraints=constraints)

    def random_portfolios(self, n: int = 3000) -> pd.DataFrame:
        """Generate random portfolios for visualization."""
        rets, vols, sharpes, weights_list = [], [], [], []
        rng = np.random.default_rng(42)
        for _ in range(n):
            w = rng.dirichlet(np.ones(self.n))
            r, v, s = self.portfolio_stats(w)
            rets.append(r); vols.append(v); sharpes.append(s)
            weights_list.append(w)
        return pd.DataFrame({
            "return": rets, "volatility": vols, "sharpe": sharpes,
            **{f"w_{name}": [wl[i] for wl in weights_list] for i, name in enumerate(self.names)}
        })
