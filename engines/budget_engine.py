"""
Budget Engine — Monthly budget tracker with goal impact.
Règle 50/30/20 adaptée. Langage simple, accessible à tous.
"""
import pandas as pd
from models.user_profile import UserProfile
from utils.constants import COUNTRIES

# Catégories de budget avec % recommandés (règle 50/30/20 adaptée)
BUDGET_CATEGORIES = {
    "🏠 Besoins Essentiels (50%)": {
        "Loyer / Crédit immobilier": {"pct": 0.28, "group": "essential"},
        "Alimentation (courses)":    {"pct": 0.12, "group": "essential"},
        "Transport":                 {"pct": 0.08, "group": "essential"},
        "Santé / Mutuelle":          {"pct": 0.05, "group": "essential"},
        "Factures (élec, eau, net)": {"pct": 0.04, "group": "essential"},
        "Assurances":                {"pct": 0.03, "group": "essential"},
    },
    "🎯 Envies & Style de Vie (30%)": {
        "Restaurants / Sorties":     {"pct": 0.06, "group": "lifestyle"},
        "Shopping / Vêtements":      {"pct": 0.05, "group": "lifestyle"},
        "Loisirs / Sport":           {"pct": 0.05, "group": "lifestyle"},
        "Abonnements (Netflix…)":    {"pct": 0.02, "group": "lifestyle"},
        "Voyages / Vacances":        {"pct": 0.04, "group": "lifestyle"},
        "Divers / Imprévus":         {"pct": 0.04, "group": "lifestyle"},
    },
    "💰 Épargne & Investissement (20%)": {
        "Épargne de précaution":     {"pct": 0.05, "group": "savings"},
        "Investissement (ETF/PEA)":  {"pct": 0.10, "group": "savings"},
        "Retraite / Long terme":     {"pct": 0.05, "group": "savings"},
    },
}

class BudgetEngine:

    def __init__(self, profile: UserProfile):
        self.p      = profile
        self.cd     = COUNTRIES.get(profile.country, COUNTRIES["France"])
        self.income = profile.total_income

    def recommended_budget(self) -> dict:
        """Returns recommended monthly amounts per category based on income."""
        result = {}
        for group, cats in BUDGET_CATEGORIES.items():
            result[group] = {}
            for cat, data in cats.items():
                result[group][cat] = {
                    "recommended": round(self.income * data["pct"]),
                    "pct": data["pct"],
                    "group": data["group"],
                }
        return result

    def analyze_budget(self, actual_spending: dict) -> dict:
        """
        Compare actual spending vs recommended.
        actual_spending: {category_name: amount}
        Returns compliance score and insights.
        """
        recommended = self.recommended_budget()
        all_cats    = {}
        for group_data in recommended.values():
            all_cats.update(group_data)

        total_essential  = 0
        total_lifestyle  = 0
        total_savings    = 0
        total_actual     = 0
        over_budget_cats = []
        under_save_cats  = []
        breakdown        = {}

        for cat, data in all_cats.items():
            actual    = actual_spending.get(cat, data["recommended"])
            rec       = data["recommended"]
            diff      = actual - rec
            pct_used  = actual / rec if rec > 0 else 1
            status    = "✅" if pct_used <= 1.05 else ("⚠️" if pct_used <= 1.25 else "❌")

            breakdown[cat] = {
                "actual": actual,
                "recommended": rec,
                "diff": diff,
                "pct_used": pct_used,
                "status": status,
                "group": data["group"],
            }

            total_actual += actual
            if data["group"] == "essential":
                total_essential += actual
            elif data["group"] == "lifestyle":
                total_lifestyle += actual
            else:
                total_savings += actual

            if diff > 50 and data["group"] != "savings":
                over_budget_cats.append({"cat": cat, "excess": diff})
            if diff < -50 and data["group"] == "savings":
                under_save_cats.append({"cat": cat, "shortfall": -diff})

        # 50/30/20 actual ratios
        ratio_essential = total_essential / self.income if self.income > 0 else 0
        ratio_lifestyle = total_lifestyle / self.income if self.income > 0 else 0
        ratio_savings   = total_savings / self.income if self.income > 0 else 0

        # Budget compliance score (0-100)
        savings_score  = min(ratio_savings / 0.20, 1.0) * 40
        essential_score = max(1 - max(ratio_essential - 0.50, 0) * 5, 0) * 30
        lifestyle_score = max(1 - max(ratio_lifestyle - 0.30, 0) * 5, 0) * 20
        balance_score   = (1 if total_actual <= self.income else 0) * 10
        compliance_score = savings_score + essential_score + lifestyle_score + balance_score

        surplus = self.income - total_actual

        return {
            "breakdown": breakdown,
            "total_actual": total_actual,
            "total_essential": total_essential,
            "total_lifestyle": total_lifestyle,
            "total_savings": total_savings,
            "ratio_essential": ratio_essential,
            "ratio_lifestyle": ratio_lifestyle,
            "ratio_savings":   ratio_savings,
            "compliance_score": compliance_score,
            "surplus": surplus,
            "is_balanced": total_actual <= self.income,
            "over_budget_cats": sorted(over_budget_cats, key=lambda x: -x["excess"])[:3],
            "under_save_cats":  under_save_cats,
        }

    def budget_goal_impact(self, monthly_excess: float, target_wealth: float,
                            target_age: int, annual_return: float) -> dict:
        """
        How does respecting the budget (saving the excess) impact the final goal?
        """
        years = max(target_age - self.p.age, 1)
        n     = years * 12
        r_m   = (1 + annual_return) ** (1 / 12) - 1

        extra_fv = monthly_excess * ((1 + r_m) ** n - 1) / r_m if r_m > 0 else monthly_excess * n

        months_saved = extra_fv / (target_wealth / n) if target_wealth > 0 else 0

        return {
            "monthly_excess":    monthly_excess,
            "future_value":      extra_fv,
            "months_closer":     months_saved,
            "years_earlier":     months_saved / 12,
        }

    def top_savings_opportunities(self, actual_spending: dict) -> list[dict]:
        """Top 3 categories to cut to improve savings."""
        recommended = self.recommended_budget()
        all_cats    = {}
        for group_data in recommended.values():
            all_cats.update(group_data)

        opportunities = []
        for cat, data in all_cats.items():
            if data["group"] == "savings":
                continue
            actual = actual_spending.get(cat, data["recommended"])
            rec    = data["recommended"]
            excess = actual - rec
            if excess > 20:
                opportunities.append({
                    "category": cat,
                    "actual": actual,
                    "recommended": rec,
                    "monthly_saving": excess,
                    "annual_saving": excess * 12,
                })

        return sorted(opportunities, key=lambda x: -x["monthly_saving"])[:3]

    def simple_budget_message(self, analysis: dict, currency: str = "EUR") -> str:
        """Generate a single plain-language budget summary sentence."""
        from utils.formatters import format_currency
        score = analysis["compliance_score"]
        surplus = analysis["surplus"]
        savings_pct = analysis["ratio_savings"]

        if score >= 80:
            return f"✅ Excellent ! Vous maîtrisez bien votre budget. Vous épargnez {savings_pct*100:.0f}% de vos revenus."
        elif score >= 60:
            return f"👍 Bon budget globalement. Petit écart sur quelques postes — {format_currency(abs(min(surplus,0)), currency)} à corriger."
        elif score >= 40:
            return f"⚠️ Votre budget est déséquilibré. Vous épargnez seulement {savings_pct*100:.0f}% au lieu de 20% recommandés."
        else:
            if surplus < 0:
                return f"❌ Attention : vous dépensez {format_currency(abs(surplus), currency)} de PLUS que vos revenus ce mois-ci. C'est urgent à corriger."
            return f"❌ Votre budget nécessite une révision profonde. Seulement {savings_pct*100:.0f}% d'épargne — votre objectif est en danger."
