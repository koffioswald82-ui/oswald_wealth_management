"""
Flat dataclass that merges all DB tables into one Python object.
Passed between engines and pages to avoid repeated DB calls.
"""
from dataclasses import dataclass, field
from typing import Optional
from utils.constants import COUNTRIES

@dataclass
class UserProfile:
    # ---- Personal ----
    user_id:            int    = 0
    name:               str    = "Utilisateur"
    age:                int    = 30
    country:            str    = "France"
    city:               str    = ""
    currency:           str    = "EUR"
    marital_status:     str    = "Célibataire"
    education_level:    str    = "Bac+5"
    career_field:       str    = "Privé"
    health_notes:       str    = ""

    # ---- Financial ----
    monthly_income:         float = 3000.0
    side_income:            float = 0.0
    monthly_expenses:       float = 2000.0
    monthly_savings:        float = 500.0
    salary_growth_pct:      float = 0.02
    current_savings:        float = 5000.0
    current_investments:    float = 0.0
    current_debt:           float = 0.0
    monthly_debt_payment:   float = 0.0
    emergency_fund:         float = 0.0
    risk_tolerance:         str   = "Modéré"
    investing_knowledge:    str   = "Débutant"
    crypto_pct:             float = 0.0
    stocks_pct:             float = 0.0
    etf_pct:                float = 0.0

    # ---- Lifestyle ----
    transport_monthly:      float = 200.0
    subscriptions_monthly:  float = 50.0
    leisure_monthly:        float = 150.0
    travel_annual:          float = 1000.0
    luxury_monthly:         float = 0.0
    discipline_score:       int   = 6
    emotional_spending:     int   = 5
    financial_anxiety:      int   = 5
    consistency_score:      int   = 6

    # ---- Family ----
    desired_marriage_age:       int   = 30
    desired_first_child_age:    int   = 32
    num_children:               int   = 1
    family_support_monthly:     float = 0.0
    parents_dependency:         int   = 0
    inheritance_expected:       float = 0.0

    # ---- Real Estate ----
    wants_property:         int   = 1
    target_purchase_age:    int   = 35
    target_property_value:  float = 250000.0
    rent_vs_buy_pref:       str   = "Acheter"
    investment_property:    int   = 0
    current_rent:           float = 800.0

    # ---- Retirement ----
    target_retirement_age:      int   = 62
    desired_monthly_pension:    float = 2500.0
    retirement_lifestyle:       str   = "Confortable"

    # ---- Computed helpers ----
    @property
    def total_income(self) -> float:
        return self.monthly_income + self.side_income

    @property
    def net_savings_rate(self) -> float:
        if self.total_income <= 0:
            return 0
        return self.monthly_savings / self.total_income

    @property
    def current_net_worth(self) -> float:
        return self.current_savings + self.current_investments - self.current_debt

    @property
    def years_to_retirement(self) -> int:
        return max(self.target_retirement_age - self.age, 0)

    @property
    def inflation(self) -> float:
        return COUNTRIES.get(self.country, {}).get("inflation", 0.025)

    @property
    def country_mortgage_rate(self) -> float:
        return COUNTRIES.get(self.country, {}).get("mortgage_rate", 0.038)

    @property
    def country_avg_income(self) -> float:
        return COUNTRIES.get(self.country, {}).get("avg_income", 2800)

    @classmethod
    def from_db(cls, db_dict: dict) -> "UserProfile":
        """Hydrate from a merged DB row dict."""
        p = cls()
        for field_name in cls.__dataclass_fields__:
            if field_name in db_dict and db_dict[field_name] is not None:
                try:
                    expected_type = cls.__dataclass_fields__[field_name].type
                    val = db_dict[field_name]
                    if expected_type in (int, "int"):
                        setattr(p, field_name, int(val))
                    elif expected_type in (float, "float"):
                        setattr(p, field_name, float(val))
                    else:
                        setattr(p, field_name, val)
                except Exception:
                    setattr(p, field_name, db_dict[field_name])
        return p
