"""
Life Trajectory Engine
Builds a year-by-year financial life model from current age to 85.
Models: income growth, expense inflation, wealth accumulation, key life events.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.financial_math import future_value, real_return, wealth_accumulation_projection
from utils.constants import COUNTRIES

class LifeTrajectoryEngine:

    def __init__(self, profile: UserProfile):
        self.p = profile
        self.country_data = COUNTRIES.get(profile.country, COUNTRIES["France"])

    def _income_at_age(self, age: int) -> float:
        """Annual income projection: career growth curve — steeper early, flattening after 50."""
        years = age - self.p.age
        base  = self.p.total_income * 12  # annualised
        if years < 0:
            return base
        peak_age = 48
        if age <= peak_age:
            growth_rate = self.p.salary_growth_pct + max(0, (peak_age - age) * 0.001)
        else:
            growth_rate = max(0, self.p.salary_growth_pct - 0.005)
        return base * (1 + growth_rate) ** years

    def _expenses_at_age(self, age: int) -> float:
        """Expenses grow with inflation plus life-stage modifiers."""
        inflation = self.country_data["inflation"]
        years     = age - self.p.age
        base_exp  = self.p.monthly_expenses * 12
        base      = base_exp * (1 + inflation) ** max(years, 0)

        # Marriage: +15% household expenses
        if age >= self.p.desired_marriage_age and self.p.marital_status in ("Célibataire", "En couple"):
            base *= 1.15

        # Children: add per-child annual cost
        num_children_active = 0
        for i in range(self.p.num_children):
            child_birth_age = self.p.desired_first_child_age + i * 2
            if child_birth_age <= age <= child_birth_age + 22:
                num_children_active += 1
        child_cost = self.country_data.get("child_monthly_cost", 850) * 12
        base += num_children_active * child_cost * (1 + inflation) ** max(years, 0)

        # House purchase: remove rent, add mortgage
        if self.p.wants_property and age >= self.p.target_purchase_age:
            from utils.financial_math import mortgage_payment
            mortgage_val = self.p.target_property_value * 0.80
            pmt = mortgage_payment(mortgage_val, self.country_data["mortgage_rate"], 25)
            base = base - self.p.current_rent * 12 + pmt * 12

        # Retirement: expenses drop ~20%
        if age >= self.p.target_retirement_age:
            base *= 0.80

        return base

    def _savings_at_age(self, age: int) -> float:
        income   = self._income_at_age(age)   # annual
        expenses = self._expenses_at_age(age) # annual
        if age >= self.p.target_retirement_age:
            pension = income * self.country_data.get("pension_replacement_rate", 0.50)
            return max(pension - expenses, 0)
        return max(income - expenses, 0)

    def build_trajectory(self) -> pd.DataFrame:
        rows    = []
        wealth  = self.p.current_net_worth
        r_nominal = 0.065  # conservative long-term portfolio return
        inflation = self.country_data["inflation"]
        r_real    = real_return(r_nominal, inflation)

        for age in range(self.p.age, 86):
            year      = age - self.p.age
            income    = self._income_at_age(age)
            expenses  = self._expenses_at_age(age)
            savings   = self._savings_at_age(age)

            wealth = wealth * (1 + r_nominal) + savings
            wealth_real = wealth / (1 + inflation) ** year

            rows.append({
                "age": age,
                "year": year,
                "income_annual": income,
                "expenses_annual": expenses,
                "savings_annual": savings,
                "savings_rate": savings / income if income > 0 else 0,
                "wealth_nominal": max(wealth, 0),
                "wealth_real": max(wealth_real, 0),
                "is_retired": age >= self.p.target_retirement_age,
            })

        return pd.DataFrame(rows)

    def get_milestones(self) -> list[dict]:
        milestones = []
        p = self.p

        milestones.append({"age": p.age, "event": "Aujourd'hui", "type": "current", "icon": "📍"})

        if p.marital_status == "Célibataire" and p.desired_marriage_age > p.age:
            milestones.append({"age": p.desired_marriage_age, "event": "Mariage prévu", "type": "family", "icon": "💍"})

        for i in range(p.num_children):
            ca = p.desired_first_child_age + i * 2
            if ca >= p.age:
                label = "1er enfant" if i == 0 else f"Enfant n°{i+1}"
                milestones.append({"age": ca, "event": label, "type": "family", "icon": "👶"})

        if p.wants_property and p.target_purchase_age >= p.age:
            milestones.append({"age": p.target_purchase_age, "event": f"Achat immobilier ({p.target_property_value:,.0f} {p.currency})", "type": "real_estate", "icon": "🏡"})

        milestones.append({"age": p.target_retirement_age, "event": "Retraite", "type": "retirement", "icon": "🏖️"})

        # Investment milestones
        traj = self.build_trajectory()
        for target in [100_000, 250_000, 500_000, 1_000_000]:
            row = traj[traj["wealth_real"] >= target]
            if not row.empty:
                a = int(row.iloc[0]["age"])
                milestones.append({"age": a, "event": f"Patrimoine : {target/1000:.0f}k {p.currency}", "type": "wealth", "icon": "💰"})

        return sorted(milestones, key=lambda x: x["age"])

    def retirement_readiness(self) -> dict:
        traj     = self.build_trajectory()
        ret_row  = traj[traj["age"] == self.p.target_retirement_age]
        if ret_row.empty:
            return {}
        wealth_at_ret  = float(ret_row.iloc[0]["wealth_real"])
        target_corpus  = self.p.desired_monthly_pension * 12 / 0.04  # 4% rule
        gap            = target_corpus - wealth_at_ret
        readiness_pct  = min(wealth_at_ret / target_corpus, 1.0) if target_corpus > 0 else 1.0

        # Sustainable withdrawal
        max_withdrawal = wealth_at_ret * 0.04 / 12

        return {
            "wealth_at_retirement": wealth_at_ret,
            "required_corpus": target_corpus,
            "gap": gap,
            "readiness_pct": readiness_pct,
            "max_monthly_withdrawal": max_withdrawal,
            "target_monthly_pension": self.p.desired_monthly_pension,
            "years_to_retirement": self.p.years_to_retirement,
        }

    def calculate_financial_independence_age(self) -> int:
        """Age when 4%-rule passive income >= current expenses."""
        traj      = self.build_trajectory()
        annual_exp = self.p.monthly_expenses * 12
        fi_rows   = traj[traj["wealth_real"] * 0.04 >= annual_exp]
        if fi_rows.empty:
            return 99
        return int(fi_rows.iloc[0]["age"])
