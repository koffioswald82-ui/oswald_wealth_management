"""
Child Financial Planning Engine
Calculates the TRUE cost of raising children + financial readiness score.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.constants import CHILD_COST_CATEGORIES, HIGHER_EDUCATION_COSTS, COUNTRIES
from utils.financial_math import future_value

class ChildPlanningEngine:

    def __init__(self, profile: UserProfile):
        self.p  = profile
        self.cd = COUNTRIES.get(profile.country, COUNTRIES["France"])
        self.inflation = self.cd["inflation"]

    def monthly_child_cost_at_age(self, child_age: int) -> float:
        """Returns monthly cost for one child at a given child-age (0-22)."""
        base = 0.0
        for cat, data in CHILD_COST_CATEGORIES.items():
            base += data["monthly_base"]
        # Crèche/Garde only 0-3
        if child_age > 3:
            base -= CHILD_COST_CATEGORIES["Garde/Crèche"]["monthly_base"]
        # Higher costs for teenagers (12-18)
        if 12 <= child_age <= 18:
            base *= 1.25
        # Student costs (18-22) — assume dorm/university
        if 18 <= child_age <= 22:
            base = base * 0.8 + 600  # living costs + reduced parental support
        return base * (1 + self.inflation) ** child_age

    def total_cost_per_child(self, education_type: str = "Université publique (FR)") -> dict:
        """Total cost to raise one child from birth to 22."""
        monthly_costs = {}
        total = 0.0

        for child_age in range(23):
            mc = self.monthly_child_cost_at_age(child_age)
            monthly_costs[child_age] = mc
            total += mc * 12

        # Higher education lump
        edu = HIGHER_EDUCATION_COSTS.get(education_type, HIGHER_EDUCATION_COSTS["Université publique (FR)"])
        edu_total = edu["annual_base"] * edu["duration"] * (1 + self.inflation) ** 18
        total += edu_total

        return {
            "total_cost": total,
            "education_cost": edu_total,
            "living_cost": total - edu_total,
            "monthly_breakdown": monthly_costs,
            "avg_monthly_first_3_years": sum(monthly_costs[i] for i in range(4)) / 4,
            "avg_monthly_school_years": sum(monthly_costs[i] for i in range(4, 18)) / 14,
            "avg_monthly_university": sum(monthly_costs[i] for i in range(18, 23)) / 5,
        }

    def total_cost_all_children(self, education_type: str = "Université publique (FR)") -> float:
        """Total cost for planned family."""
        n = self.p.num_children
        if n == 0:
            return 0.0
        cost_per = self.total_cost_per_child(education_type)["total_cost"]
        # Siblings share some fixed costs (~15% reduction per additional child)
        total = cost_per
        for i in range(1, n):
            total += cost_per * (1 - 0.15 * i)
        return total

    def readiness_score(self) -> dict:
        """
        Financial readiness score for having a child (0–100).
        Weights: emergency_fund(30) + income_surplus(25) + savings_rate(20) + debt_ratio(15) + stability(10)
        """
        p = self.p
        score = 0.0
        breakdown = {}

        # 1. Emergency fund: need 6 months expenses
        ef_months = p.emergency_fund / (p.monthly_expenses + 700) if (p.monthly_expenses + 700) > 0 else 0
        ef_score  = min(ef_months / 6, 1.0) * 30
        score += ef_score
        breakdown["Fonds d'urgence"] = {"score": ef_score, "max": 30, "note": f"{ef_months:.1f} mois / 6 requis"}

        # 2. Monthly income surplus after child cost
        child_cost_monthly = self.cd.get("child_monthly_cost", 850)
        surplus = p.total_income - p.monthly_expenses - child_cost_monthly
        surplus_score = min(max(surplus / p.total_income, 0), 0.25) / 0.25 * 25
        score += surplus_score
        breakdown["Surplus mensuel"] = {"score": surplus_score, "max": 25, "note": f"{surplus:+.0f} {p.currency}/mois après enfant"}

        # 3. Savings rate ≥ 10% after child
        adjusted_savings = p.monthly_savings - child_cost_monthly
        adj_rate = adjusted_savings / p.total_income if p.total_income > 0 else 0
        sr_score = min(max(adj_rate / 0.10, 0), 1.0) * 20
        score += sr_score
        breakdown["Taux d'épargne"] = {"score": sr_score, "max": 20, "note": f"{adj_rate*100:.1f}% après enfant / 10% min"}

        # 4. Debt ratio < 33%
        dti = p.monthly_debt_payment / p.total_income if p.total_income > 0 else 0
        dti_score = max(1 - dti / 0.33, 0) * 15
        score += dti_score
        breakdown["Ratio dette/revenu"] = {"score": dti_score, "max": 15, "note": f"DTI = {dti*100:.1f}% / max 33%"}

        # 5. Behavioral stability
        stab = (p.discipline_score + p.consistency_score) / 20
        stab_score = stab * 10
        score += stab_score
        breakdown["Stabilité financière"] = {"score": stab_score, "max": 10, "note": f"Score comportemental {stab*100:.0f}%"}

        return {
            "total_score": score,
            "percentage": score,
            "breakdown": breakdown,
            "recommendation": self._readiness_recommendation(score),
            "required_emergency_fund": (p.monthly_expenses + child_cost_monthly) * 6,
            "monthly_child_cost": child_cost_monthly,
            "ready": score >= 60,
        }

    def _readiness_recommendation(self, score: float) -> str:
        if score >= 80:
            return "Vous êtes financièrement prêt(e) pour un enfant. Votre base est solide."
        if score >= 60:
            return "Vous pouvez envisager un enfant avec quelques ajustements préalables."
        if score >= 40:
            return "Il est recommandé de consolider votre situation financière 12-18 mois avant."
        return "Des fondations financières plus solides sont nécessaires avant d'envisager un enfant."

    def savings_plan_before_child(self) -> dict:
        """How much to save and for how long before the child arrives."""
        child_cost_monthly = self.cd.get("child_monthly_cost", 850)
        target_ef = (self.p.monthly_expenses + child_cost_monthly) * 6
        gap_ef    = max(target_ef - self.p.emergency_fund, 0)
        # First year costs (higher due to equipment, setup)
        first_year_extra = 3000 * (1 + self.inflation) ** max(self.p.desired_first_child_age - self.p.age, 0)
        total_target = gap_ef + first_year_extra
        months_to_save = total_target / max(self.p.monthly_savings, 1)

        return {
            "target_emergency_fund": target_ef,
            "current_emergency_fund": self.p.emergency_fund,
            "gap": gap_ef,
            "first_year_extra_costs": first_year_extra,
            "total_savings_target": total_target,
            "months_to_save": months_to_save,
            "monthly_savings_needed": total_target / max(months_to_save, 1),
            "recommended_monthly_increase": max(total_target / 24 - self.p.monthly_savings, 0),
        }

    def education_cost_comparison(self) -> pd.DataFrame:
        rows = []
        years_until_18 = max(18 - (self.p.desired_first_child_age - self.p.age), 1)
        for edu_type, data in HIGHER_EDUCATION_COSTS.items():
            raw_cost  = data["annual_base"] * data["duration"]
            fut_cost  = raw_cost * (1 + self.inflation) ** years_until_18
            monthly_save = fut_cost / (years_until_18 * 12) if years_until_18 > 0 else fut_cost / 12
            rows.append({
                "Type": edu_type,
                "Durée": f"{data['duration']} ans",
                "Coût actuel": raw_cost,
                "Coût futur (inflationné)": fut_cost,
                "Épargne mensuelle requise": monthly_save,
            })
        return pd.DataFrame(rows)
