"""
Real Estate Wealth Engine
Mortgage affordability, rent vs buy NPV, investment property viability.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.financial_math import (
    mortgage_payment, mortgage_amortization, net_present_value_rent_vs_buy, future_value
)
from utils.constants import COUNTRIES

class RealEstateEngine:

    def __init__(self, profile: UserProfile):
        self.p  = profile
        self.cd = COUNTRIES.get(profile.country, COUNTRIES["France"])

    def affordability_analysis(self, property_value: float = None, down_pmt_pct: float = 0.20) -> dict:
        pv   = property_value or self.p.target_property_value
        rate = self.cd["mortgage_rate"]
        years_until = max(self.p.target_purchase_age - self.p.age, 0)
        income_at_purchase = self.p.total_income * (1 + self.p.salary_growth_pct) ** years_until

        down_pmt  = pv * down_pmt_pct
        loan      = pv - down_pmt
        monthly_pmt = mortgage_payment(loan, rate, 25)

        dti_with_mortgage = (monthly_pmt + self.p.monthly_debt_payment) / income_at_purchase
        ltv = loan / pv

        # 28/36 rule
        piti_ratio = monthly_pmt / income_at_purchase  # housing expense ratio
        total_debt_ratio = (monthly_pmt + self.p.monthly_debt_payment) / income_at_purchase

        # Stress test: +2% rate increase
        stress_pmt = mortgage_payment(loan, rate + 0.02, 25)
        stress_dti = (stress_pmt + self.p.monthly_debt_payment) / income_at_purchase

        # Current savings trajectory toward down payment
        from utils.financial_math import time_to_target
        months_to_down = time_to_target(self.p.current_savings, down_pmt,
                                        self.p.monthly_savings, 0.025)

        return {
            "property_value": pv,
            "down_payment_required": down_pmt,
            "loan_amount": loan,
            "monthly_payment": monthly_pmt,
            "monthly_payment_stress": stress_pmt,
            "dti_with_mortgage": dti_with_mortgage,
            "dti_stressed": stress_dti,
            "piti_ratio": piti_ratio,
            "ltv": ltv,
            "income_at_purchase": income_at_purchase,
            "is_affordable": dti_with_mortgage <= 0.35,
            "is_stressed_affordable": stress_dti <= 0.40,
            "months_to_down_payment": months_to_down,
            "years_to_down_payment": months_to_down / 12,
            "current_savings_gap": max(down_pmt - self.p.current_savings, 0),
        }

    def amortization_summary(self, property_value: float = None, down_pmt_pct: float = 0.20,
                             years: int = 25) -> pd.DataFrame:
        pv   = property_value or self.p.target_property_value
        loan = pv * (1 - down_pmt_pct)
        rate = self.cd["mortgage_rate"]
        schedule = mortgage_amortization(loan, rate, years)
        df = pd.DataFrame(schedule)
        # Yearly summary
        yearly = df.groupby("year").agg(
            total_paid=("payment", "sum"),
            interest_paid=("interest", "sum"),
            principal_paid=("principal", "sum"),
            balance_end=("balance", "last"),
        ).reset_index()
        yearly["equity"] = loan - yearly["balance_end"] + pv * 0.20
        return yearly

    def rent_vs_buy(self, years: int = 20, appreciation: float = 0.03) -> dict:
        return net_present_value_rent_vs_buy(
            home_value=self.p.target_property_value,
            down_payment=self.p.target_property_value * 0.20,
            mortgage_rate=self.cd["mortgage_rate"],
            mortgage_years=25,
            monthly_rent=self.p.current_rent,
            property_appreciation=appreciation,
            inflation=self.cd["inflation"],
            years=years,
            discount_rate=0.04,
        )

    def property_appreciation_scenarios(self, years: int = 20) -> pd.DataFrame:
        scenarios = {"Pessimiste (-1%/an)": -0.01, "Base (+2%/an)": 0.02,
                     "Modéré (+3%/an)": 0.03, "Optimiste (+5%/an)": 0.05}
        rows = []
        pv = self.p.target_property_value
        for name, rate in scenarios.items():
            fv = pv * (1 + rate) ** years
            rows.append({
                "Scénario": name,
                "Valeur initiale": pv,
                f"Valeur dans {years} ans": fv,
                "Plus-value brute": fv - pv,
                "Plus-value %": (fv - pv) / pv,
            })
        return pd.DataFrame(rows)

    def investment_property_analysis(self, purchase_price: float, monthly_rent: float,
                                     vacancy_rate: float = 0.05,
                                     management_fees: float = 0.08) -> dict:
        effective_rent  = monthly_rent * (1 - vacancy_rate) * (1 - management_fees)
        annual_rent     = effective_rent * 12
        gross_yield     = (monthly_rent * 12) / purchase_price
        net_yield       = annual_rent / purchase_price
        maintenance     = purchase_price * 0.01
        net_rent_after_maint = annual_rent - maintenance

        loan   = purchase_price * 0.75
        pmt    = mortgage_payment(loan, self.cd["mortgage_rate"], 20)
        cash_flow_monthly = effective_rent - pmt - maintenance / 12

        dscr = effective_rent / pmt if pmt > 0 else 0  # Debt Service Coverage Ratio

        # 10-year projection
        rows = []
        for y in range(1, 11):
            rent_y   = effective_rent * (1 + 0.02) ** y
            val_y    = purchase_price * (1 + 0.03) ** y
            equity_y = val_y - loan * (1 - y / 20)
            rows.append({"Année": y, "Loyer mensuel net": rent_y, "Valeur bien": val_y, "Equity estimée": equity_y})

        return {
            "purchase_price": purchase_price,
            "monthly_rent_gross": monthly_rent,
            "monthly_rent_effective": effective_rent,
            "gross_yield": gross_yield,
            "net_yield": net_yield,
            "monthly_cash_flow": cash_flow_monthly,
            "annual_cash_flow": cash_flow_monthly * 12,
            "dscr": dscr,
            "is_cash_flow_positive": cash_flow_monthly > 0,
            "is_investment_viable": dscr >= 1.2 and net_yield >= 0.04,
            "projection": pd.DataFrame(rows),
        }

    def ideal_purchase_timing(self) -> dict:
        """Calculate optimal age to buy based on financial readiness."""
        best_age = self.p.age
        best_score = 0
        results = {}

        for test_age in range(self.p.age, min(self.p.age + 20, 60)):
            years_saving = test_age - self.p.age
            projected_savings = future_value(
                self.p.current_savings,
                0.025,
                years_saving,
                self.p.monthly_savings * 12  # annual rate, annual periods, annual pmt
            )
            income = self.p.total_income * (1 + self.p.salary_growth_pct) ** years_saving
            down_pmt = self.p.target_property_value * 0.20
            loan  = self.p.target_property_value * 0.80
            pmt   = mortgage_payment(loan, self.cd["mortgage_rate"], 25)
            dti   = (pmt + self.p.monthly_debt_payment) / income

            has_down = projected_savings >= down_pmt
            dti_ok   = dti <= 0.35
            score    = (1 if has_down else 0) + (1 if dti_ok else 0) + (1 - dti / 0.5)

            results[test_age] = {
                "savings": projected_savings, "income": income,
                "dti": dti, "has_down": has_down, "dti_ok": dti_ok, "score": score
            }
            if score > best_score:
                best_score = score
                best_age   = test_age

        return {"optimal_age": best_age, "details": results}
