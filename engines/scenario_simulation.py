"""
Life Scenario Comparison Engine
Compare multiple financial life paths side by side.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.financial_math import future_value, real_return
from utils.constants import COUNTRIES

class ScenarioSimulationEngine:

    def __init__(self, profile: UserProfile):
        self.p  = profile
        self.cd = COUNTRIES.get(profile.country, COUNTRIES["France"])

    def run_scenario(self, overrides: dict, years: int = None) -> dict:
        """Run a single scenario with parameter overrides."""
        p = self.p
        years = years or p.years_to_retirement or 30

        income            = overrides.get("monthly_income", p.total_income)
        monthly_savings   = overrides.get("monthly_savings", p.monthly_savings)
        savings_growth    = overrides.get("savings_growth", 0.02)
        return_rate       = overrides.get("annual_return", 0.065)
        initial_wealth    = overrides.get("initial_wealth", p.current_net_worth)
        extra_expense     = overrides.get("extra_monthly_expense", 0)
        num_children      = overrides.get("num_children", p.num_children)
        has_property      = overrides.get("has_property", p.wants_property)
        property_value    = overrides.get("property_value", p.target_property_value)
        luxury_monthly    = overrides.get("luxury_monthly", p.luxury_monthly)
        inflation         = self.cd["inflation"]

        # Adjust monthly savings for scenario constraints
        child_cost    = self.cd.get("child_monthly_cost", 850) * num_children
        effective_sav = monthly_savings - extra_expense - luxury_monthly * 0.5

        rows = []
        wealth = initial_wealth
        eff_sav = max(effective_sav, 0)

        for y in range(years + 1):
            real_w = wealth / (1 + inflation) ** y
            rows.append({
                "year": y,
                "age": p.age + y,
                "wealth_nominal": max(wealth, 0),
                "wealth_real": max(real_w, 0),
                "annual_savings": eff_sav * 12,
            })
            wealth  = wealth * (1 + return_rate) + eff_sav * 12
            eff_sav = eff_sav * (1 + savings_growth)

        df = pd.DataFrame(rows)
        final_wealth = float(df.iloc[-1]["wealth_real"])

        # Financial stress score (higher = more stress)
        stress = 0
        if effective_sav < 0:           stress += 40
        if num_children > 2:            stress += 10
        if luxury_monthly > income * 0.15: stress += 20
        if extra_expense > income * 0.10:  stress += 15
        stress = min(stress, 100)

        return {
            "trajectory": df,
            "final_wealth_real": final_wealth,
            "retirement_age": p.target_retirement_age,
            "monthly_withdrawal": final_wealth * 0.04 / 12,
            "financial_stress_score": stress,
            "effective_monthly_savings": eff_sav,
            "params": overrides,
        }

    def compare_scenarios(self, scenarios: list[dict]) -> dict:
        """
        Run multiple scenarios and return comparison.
        Each scenario: {"name": str, "description": str, "overrides": dict}
        """
        results = {}
        for sc in scenarios:
            name     = sc["name"]
            overrides = sc.get("overrides", {})
            results[name] = {
                "name": name,
                "description": sc.get("description", ""),
                "result": self.run_scenario(overrides),
                "overrides": overrides,
            }

        return results

    def default_scenario_set(self) -> list[dict]:
        """Predefined scenarios for most users."""
        p = self.p

        return [
            {
                "name": "Scénario A — Base",
                "description": "Votre trajectoire actuelle sans changements majeurs",
                "overrides": {
                    "monthly_savings": p.monthly_savings,
                    "luxury_monthly": p.luxury_monthly,
                    "num_children": p.num_children,
                },
            },
            {
                "name": "Scénario B — Investisseur Discipliné",
                "description": "Augmenter l'épargne à 20% du revenu, réduire le luxe",
                "overrides": {
                    "monthly_savings": max(p.total_income * 0.20, p.monthly_savings),
                    "luxury_monthly": min(p.luxury_monthly, p.total_income * 0.05),
                    "num_children": p.num_children,
                    "annual_return": 0.07,
                },
            },
            {
                "name": "Scénario C — Style de Vie Premium",
                "description": "Lifestyle élevé, moindre épargne, enfants supplémentaires",
                "overrides": {
                    "monthly_savings": p.monthly_savings * 0.60,
                    "luxury_monthly": p.total_income * 0.15,
                    "num_children": min(p.num_children + 1, 4),
                    "extra_monthly_expense": p.total_income * 0.05,
                },
            },
            {
                "name": "Scénario D — FIRE (Liberté Financière)",
                "description": "Épargne maximale (35%), vie minimaliste, retraite précoce",
                "overrides": {
                    "monthly_savings": p.total_income * 0.35,
                    "luxury_monthly": 0,
                    "num_children": 0,
                    "annual_return": 0.075,
                    "savings_growth": 0.03,
                },
            },
        ]

    def build_comparison_dataframe(self, scenario_results: dict) -> pd.DataFrame:
        """Flatten scenario results for comparison table."""
        rows = []
        for name, data in scenario_results.items():
            r = data["result"]
            rows.append({
                "Scénario": name,
                "Description": data["description"],
                "Patrimoine final (réel)": r["final_wealth_real"],
                "Retrait mensuel retraite": r["monthly_withdrawal"],
                "Score de stress financier": r["financial_stress_score"],
                "Épargne mensuelle effective": r["effective_monthly_savings"],
            })
        return pd.DataFrame(rows)

    def sensitivity_analysis(self, variable: str, values: list, years: int = 20) -> pd.DataFrame:
        """Test sensitivity of final wealth to one variable."""
        rows = []
        for v in values:
            result = self.run_scenario({variable: v}, years=years)
            rows.append({
                variable: v,
                "Patrimoine Final": result["final_wealth_real"],
                "Retrait Mensuel": result["monthly_withdrawal"],
                "Score Stress": result["financial_stress_score"],
            })
        return pd.DataFrame(rows)
