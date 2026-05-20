"""
Crisis Simulation Engine
Stress-tests the user's financial resilience under major adverse events.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.constants import COUNTRIES
from utils.financial_math import future_value

class CrisisSimulationEngine:

    def __init__(self, profile: UserProfile):
        self.p  = profile
        self.cd = COUNTRIES.get(profile.country, COUNTRIES["France"])

    def simulate_unemployment(self, duration_months: int = 6, replacement_rate: float = 0.65) -> dict:
        """Job loss scenario."""
        monthly_income   = self.p.total_income
        unemployment_bft = monthly_income * replacement_rate
        monthly_shortfall = max(self.p.monthly_expenses + self.p.monthly_debt_payment - unemployment_bft, 0)
        burn_rate        = monthly_shortfall
        available_cash   = self.p.emergency_fund + self.p.current_savings * 0.5
        months_survivable = available_cash / burn_rate if burn_rate > 0 else 999

        deficit_at_end  = max(burn_rate * duration_months - available_cash, 0)
        recovery_months = deficit_at_end / (monthly_income - self.p.monthly_expenses) if monthly_income > self.p.monthly_expenses else 24

        wealth_impact   = -(burn_rate * min(duration_months, months_survivable))

        return {
            "scenario": "Perte d'emploi",
            "duration_months": duration_months,
            "replacement_income": unemployment_bft,
            "monthly_shortfall": monthly_shortfall,
            "available_cash": available_cash,
            "months_survivable": months_survivable,
            "can_survive": months_survivable >= duration_months,
            "deficit_at_end": deficit_at_end,
            "recovery_months": recovery_months,
            "wealth_impact": wealth_impact,
            "resilience_level": "Solide" if months_survivable >= 12 else ("Modéré" if months_survivable >= 6 else "Fragile"),
        }

    def simulate_medical_emergency(self, cost: float = 20000) -> dict:
        """Major medical expense."""
        available  = self.p.emergency_fund + self.p.current_savings * 0.3
        gap        = max(cost - available, 0)
        months_to_recover = gap / max(self.p.monthly_savings, 1)

        insurance_gap = max(cost * 0.30, 0)  # assume 70% covered
        wealth_impact = -min(cost, available) - gap * 0.5

        return {
            "scenario": "Urgence Médicale",
            "cost": cost,
            "insurance_covered": cost * 0.70,
            "out_of_pocket": insurance_gap,
            "available_funds": available,
            "gap": gap,
            "months_to_recover": months_to_recover,
            "can_absorb": available >= insurance_gap,
            "wealth_impact": wealth_impact,
            "recommendation": "Souscrire une mutuelle complémentaire et renforcer le fonds d'urgence" if gap > 0 else "Couverture suffisante",
        }

    def simulate_market_crash(self, drawdown_pct: float = 0.35) -> dict:
        """Stock market crash: portfolio loses X%."""
        portfolio = self.p.current_investments
        loss      = portfolio * drawdown_pct
        recovery_years_historical = {0.20: 1.5, 0.35: 2.8, 0.50: 4.5, 0.60: 6.0}
        recovery_yrs = 3.0  # default
        for k, v in sorted(recovery_years_historical.items()):
            if drawdown_pct <= k:
                recovery_yrs = v
                break

        # Monthly contribution continues during crash — dollar cost averaging benefit
        recovery_contribution_boost = self.p.monthly_savings * recovery_yrs * 12 * 0.20

        return {
            "scenario": f"Krach Boursier (-{drawdown_pct*100:.0f}%)",
            "portfolio_before": portfolio,
            "loss": loss,
            "portfolio_after": portfolio - loss,
            "recovery_years": recovery_yrs,
            "dca_benefit": recovery_contribution_boost,
            "net_impact": -loss + recovery_contribution_boost,
            "advice": (
                "Continuez d'investir régulièrement — le DCA transforme les krachs en opportunités."
                if self.p.monthly_savings > 0 else
                "Aucune contribution mensuelle détectée — vous ratez l'opportunité DCA."
            ),
            "cash_buffer_ok": self.p.emergency_fund >= self.p.monthly_expenses * 6,
        }

    def simulate_inflation_shock(self, inflation_rate: float = 0.08) -> dict:
        """Sustained high inflation scenario."""
        normal_inflation = self.cd["inflation"]
        extra_inflation  = inflation_rate - normal_inflation
        years            = 3

        purchasing_power_loss = 1 - (1 / (1 + inflation_rate) ** years)
        monthly_cost_increase = self.p.monthly_expenses * extra_inflation
        annual_cost_increase  = monthly_cost_increase * 12 * years

        savings_real_loss = self.p.current_savings * purchasing_power_loss
        portfolio_real_loss = self.p.current_investments * purchasing_power_loss * 0.5  # equities partly hedge

        # Mortgage holders benefit: fixed payments, rising asset values
        mortgage_benefit = 0
        if self.p.wants_property:
            mortgage_benefit = self.p.target_property_value * inflation_rate * years * 0.5

        return {
            "scenario": f"Choc d'Inflation ({inflation_rate*100:.0f}%/an)",
            "normal_inflation": normal_inflation,
            "shock_inflation": inflation_rate,
            "duration_years": years,
            "purchasing_power_loss": purchasing_power_loss,
            "monthly_cost_increase": monthly_cost_increase,
            "total_extra_cost": annual_cost_increase,
            "savings_real_loss": savings_real_loss,
            "portfolio_real_loss": portfolio_real_loss,
            "mortgage_benefit": mortgage_benefit,
            "net_impact": -savings_real_loss - portfolio_real_loss + mortgage_benefit,
            "advice": "Actions et immobilier offrent une couverture naturelle contre l'inflation.",
        }

    def simulate_divorce(self) -> dict:
        """Financial impact of divorce."""
        if self.p.marital_status == "Célibataire":
            return {"applicable": False, "message": "Non applicable (célibataire)"}

        shared_assets = self.p.current_net_worth * 0.50  # simplified 50/50 split
        legal_costs   = 3000 + self.p.current_net_worth * 0.02
        income_impact = self.p.total_income * 0.10 * 12  # lawyer / court time lost
        housing_shock = self.p.current_rent * 6  # need new housing

        total_financial_impact = -(shared_assets + legal_costs + income_impact + housing_shock)

        return {
            "scenario": "Divorce",
            "applicable": True,
            "asset_split_loss": shared_assets,
            "legal_costs": legal_costs,
            "income_impact": income_impact,
            "housing_costs": housing_shock,
            "total_impact": total_financial_impact,
            "months_to_recover": abs(total_financial_impact) / max(self.p.monthly_savings, 1),
            "prenuptial_benefit": shared_assets * 0.5,
        }

    def overall_resilience_score(self) -> dict:
        """Composite resilience score (0–100) across all risk categories."""
        unemployment = self.simulate_unemployment(6)
        medical      = self.simulate_medical_emergency(20000)
        market       = self.simulate_market_crash(0.35)
        inflation    = self.simulate_inflation_shock(0.07)

        # Component scores
        unemp_score = min(unemployment["months_survivable"] / 12, 1.0) * 30
        med_score   = (1 if medical["can_absorb"] else 0.3) * 20
        mkt_score   = (1 if market["cash_buffer_ok"] else 0.5) * 25
        infl_score  = min(self.p.stocks_pct + self.p.etf_pct + 0.3, 1.0) * 25

        total = unemp_score + med_score + mkt_score + infl_score

        if total >= 80:
            level, color = "Très Résilient", "#4CAF50"
        elif total >= 60:
            level, color = "Résilient", "#8BC34A"
        elif total >= 40:
            level, color = "Modérément Fragile", "#FF9800"
        elif total >= 20:
            level, color = "Fragile", "#FF5722"
        else:
            level, color = "Très Fragile", "#F44336"

        return {
            "total_score": total,
            "level": level,
            "color": color,
            "breakdown": {
                "Résistance chômage": {"score": unemp_score, "max": 30},
                "Urgence médicale":   {"score": med_score,   "max": 20},
                "Krach boursier":     {"score": mkt_score,   "max": 25},
                "Choc inflationniste":{"score": infl_score,  "max": 25},
            },
            "top_vulnerability": min(
                [("Chômage", unemp_score/30), ("Médical", med_score/20),
                 ("Marché", mkt_score/25), ("Inflation", infl_score/25)],
                key=lambda x: x[1]
            )[0],
        }
