"""
Investment Engine — Modern Portfolio Theory + asset allocation logic.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.constants import ASSET_CLASSES, RISK_PROFILES
from utils.financial_math import future_value, real_return, compound_annual_growth_rate

class InvestmentEngine:

    def __init__(self, profile: UserProfile):
        self.p = profile

    def recommended_allocation(self) -> dict:
        """
        Return optimal allocation based on risk profile + age + time horizon.
        Applies the 'age in bonds' heuristic adjusted for modern longevity.
        """
        base = RISK_PROFILES.get(self.p.risk_tolerance, RISK_PROFILES["Modéré"]).copy()

        # Age glide path: reduce equities as retirement approaches
        years_to_ret = self.p.years_to_retirement
        if years_to_ret < 5:
            shift = 0.20
            base["equities"]   = max(base["equities"] - shift, 0.15)
            base["bonds"]      = min(base["bonds"] + shift, 0.70)
        elif years_to_ret < 10:
            shift = 0.10
            base["equities"]   = max(base["equities"] - shift, 0.25)
            base["bonds"]      = min(base["bonds"] + shift, 0.60)

        return base

    def portfolio_growth_projection(self, years: int = None) -> pd.DataFrame:
        years = years or self.p.years_to_retirement or 30
        alloc = self.recommended_allocation()
        ret   = alloc.get("expected_return", 0.06)
        vol   = alloc.get("volatility", 0.10)
        initial  = self.p.current_investments + self.p.current_savings * 0.5
        monthly  = self.p.monthly_savings
        inflation = self.p.inflation

        rows = []
        wealth = initial
        for y in range(years + 1):
            real_w = wealth / (1 + inflation) ** y
            rows.append({
                "year": y,
                "age": self.p.age + y,
                "wealth_nominal": wealth,
                "wealth_real": real_w,
                "monthly_contribution": monthly,
            })
            wealth  = wealth * (1 + ret) + monthly * 12
            monthly = monthly * (1 + self.p.salary_growth_pct * 0.5)

        return pd.DataFrame(rows)

    def analyze_current_portfolio(self) -> dict:
        total = self.p.current_investments + self.p.current_savings
        if total <= 0:
            return {"total": 0, "allocation": {}, "score": 0}

        alloc_actual = {
            "Cash / Épargne":    self.p.current_savings / total,
            "Actions":          self.p.stocks_pct,
            "ETF":              self.p.etf_pct,
            "Crypto":           self.p.crypto_pct,
        }
        other = max(1 - self.p.stocks_pct - self.p.etf_pct - self.p.crypto_pct - self.p.current_savings / total, 0)
        alloc_actual["Obligations / Autre"] = other

        # Diversification score
        non_zero = sum(1 for v in alloc_actual.values() if v > 0.05)
        diversification = min(non_zero / 4, 1.0)

        # Concentration risk
        max_alloc = max(alloc_actual.values())
        concentration_penalty = max(max_alloc - 0.60, 0) * 2

        # Crypto risk flag
        crypto_flag = self.p.crypto_pct > 0.15

        portfolio_score = diversification * 70 - concentration_penalty * 30
        portfolio_score = max(0, min(100, portfolio_score))

        return {
            "total": total,
            "allocation": alloc_actual,
            "diversification_score": diversification,
            "max_concentration": max_alloc,
            "crypto_flag": crypto_flag,
            "portfolio_score": portfolio_score,
            "is_diversified": diversification >= 0.6,
        }

    def rebalancing_recommendation(self) -> list[dict]:
        current  = self.analyze_current_portfolio()
        target   = self.recommended_allocation()
        insights = []
        total    = current["total"]
        alloc    = current["allocation"]

        # Map target to simpler keys
        target_map = {
            "Actions / ETF": target.get("equities", 0.50),
            "Obligations":   target.get("bonds", 0.30),
        }

        # Check savings rate relative to income
        if self.p.net_savings_rate < 0.10:
            insights.append({
                "type": "warning",
                "action": f"Augmenter le taux d'épargne à ≥ 10% (actuel : {self.p.net_savings_rate*100:.1f}%)",
                "impact": "Critique pour la construction patrimoniale",
            })

        if self.p.crypto_pct > 0.15:
            insights.append({
                "type": "danger",
                "action": f"Réduire l'exposition crypto à <15% (actuel: {self.p.crypto_pct*100:.0f}%)",
                "impact": "Risque de perte >50% sur le capital crypto investi",
            })

        if self.p.stocks_pct + self.p.etf_pct < 0.30 and self.p.years_to_retirement > 10:
            insights.append({
                "type": "info",
                "action": "Augmenter l'exposition actions/ETF pour les horizons >10 ans",
                "impact": "Historiquement +2-4% de rendement annuel vs obligations",
            })

        if self.p.current_savings / max(total, 1) > 0.70:
            insights.append({
                "type": "warning",
                "action": "Trop de cash — l'inflation érode votre pouvoir d'achat",
                "impact": f"Perte réelle estimée : {self.p.inflation*100:.1f}%/an sur la part liquide",
            })

        return insights

    def compound_scenarios(self) -> pd.DataFrame:
        initial  = max(self.p.current_investments + self.p.current_savings * 0.5, 1000)
        monthly  = self.p.monthly_savings
        years    = self.p.years_to_retirement or 30

        scenarios = {
            "Conservative (3.5%)": 0.035,
            "Base Case (6%)":      0.060,
            "Optimiste (8%)":      0.080,
            "Agressif (10%)":      0.100,
        }
        rows = []
        for label, r in scenarios.items():
            final = future_value(initial, r, years, monthly * 12)  # annual rate, annual periods, annual pmt
            rows.append({
                "Scénario": label,
                "Rendement annuel": r,
                "Patrimoine initial": initial,
                "Contribution mensuelle": monthly,
                f"Patrimoine dans {years} ans": final,
                "Multiplicateur": final / initial if initial > 0 else 0,
            })
        return pd.DataFrame(rows)

    def opportunity_cost_analysis(self, monthly_luxury: float, years: int = 20) -> dict:
        """Calculate what investing luxury spending would produce instead."""
        if monthly_luxury <= 0:
            return {}
        r     = self.recommended_allocation().get("expected_return", 0.065)
        fv    = future_value(0, r / 12, years * 12, monthly_luxury)
        return {
            "monthly_amount": monthly_luxury,
            "years": years,
            "opportunity_cost": fv,
            "total_contributed": monthly_luxury * years * 12,
            "gain": fv - monthly_luxury * years * 12,
            "message": (
                f"Investir {monthly_luxury:.0f} {self.p.currency}/mois au lieu de dépenser "
                f"vous donnerait {fv:,.0f} {self.p.currency} dans {years} ans."
            ),
        }
