"""
Goal Engine — Reverse financial calculator.
"Je veux X€ à Y ans → voici exactement quoi faire chaque mois."
Langage simple, accessible à tous.
"""
import numpy as np
import pandas as pd
from models.user_profile import UserProfile
from utils.constants import COUNTRIES, RISK_PROFILES
from utils.financial_math import future_value

class GoalEngine:

    def __init__(self, profile: UserProfile):
        self.p  = profile
        self.cd = COUNTRIES.get(profile.country, COUNTRIES["France"])

    def required_monthly_savings(
        self,
        target_wealth: float,
        target_age: int,
        annual_return: float,
        current_wealth: float = None,
    ) -> float:
        """
        Reverse compound interest: how much must I save each month
        to reach target_wealth at target_age?
        """
        pv    = current_wealth if current_wealth is not None else self.p.current_net_worth
        years = max(target_age - self.p.age, 1)
        n     = years * 12
        r_m   = (1 + annual_return) ** (1 / 12) - 1

        fv_current = pv * (1 + r_m) ** n
        if fv_current >= target_wealth:
            return 0.0

        gap = target_wealth - fv_current
        if r_m == 0:
            return gap / n
        return gap * r_m / ((1 + r_m) ** n - 1)

    def build_plan(
        self,
        target_wealth: float,
        target_age: int,
        annual_return: float,
        required_monthly: float,
    ) -> dict:
        """
        Build a plain-language step-by-step plan.
        Returns milestones, split recommendation, interest earned per year.
        """
        p       = self.p
        years   = max(target_age - p.age, 1)
        r_m     = (1 + annual_return) ** (1 / 12) - 1
        wealth  = p.current_net_worth
        milestones = []
        yearly_interest = []

        for y in range(years + 1):
            age_y      = p.age + y
            interest_y = wealth * annual_return
            yearly_interest.append({"year": y, "age": age_y, "interest": interest_y, "wealth": wealth})
            wealth = wealth * (1 + annual_return) + required_monthly * 12

        # Key milestone ages
        milestone_ages = [a for a in [p.age + 5, p.age + 10, p.age + 15, target_age]
                          if p.age < a <= target_age]
        for row in yearly_interest:
            if row["age"] in milestone_ages:
                milestones.append(row)

        # Recommended split of monthly savings
        alloc = self._savings_split(required_monthly, p.risk_tolerance)

        # Progress percentage now
        progress_pct = min(p.current_net_worth / target_wealth, 1.0) if target_wealth > 0 else 0

        # "Daily cost" framing
        daily_cost = required_monthly / 30

        # Interests this year
        interest_this_year = p.current_net_worth * annual_return

        return {
            "target_wealth":      target_wealth,
            "target_age":         target_age,
            "years_left":         years,
            "required_monthly":   required_monthly,
            "daily_equivalent":   daily_cost,
            "annual_return":      annual_return,
            "progress_pct":       progress_pct,
            "current_wealth":     p.current_net_worth,
            "milestones":         milestones,
            "yearly_data":        yearly_interest,
            "savings_split":      alloc,
            "interest_this_year": interest_this_year,
            "on_track":           p.monthly_savings >= required_monthly,
            "monthly_gap":        max(required_monthly - p.monthly_savings, 0),
        }

    def _savings_split(self, monthly: float, risk_profile: str) -> dict:
        """How to split the monthly savings between vehicles."""
        profiles = {
            "Très conservateur":  {"💰 Livret A / Épargne liquide": 0.60, "📊 ETF Obligataires": 0.40},
            "Conservateur":       {"💰 Livret A": 0.45, "📊 ETF Mixtes": 0.40, "🛡️ Fonds euros": 0.15},
            "Modéré":             {"💰 Épargne liquide": 0.25, "📈 ETF World (MSCI)": 0.55, "📊 Obligations": 0.20},
            "Dynamique":          {"💰 Épargne liquide": 0.15, "📈 ETF World": 0.65, "📊 ETF Sectoriels": 0.20},
            "Agressif":           {"💰 Épargne urgence min.": 0.10, "📈 ETF World": 0.70, "📊 Actions": 0.20},
            "Très agressif":      {"💰 Épargne min.": 0.08, "📈 ETF World": 0.72, "📊 Actions/Thématiques": 0.20},
        }
        alloc = profiles.get(risk_profile, profiles["Modéré"])
        return {label: round(pct * monthly) for label, pct in alloc.items()}

    def trajectory_dataframe(self, target_wealth: float, target_age: int,
                              annual_return: float, required_monthly: float) -> pd.DataFrame:
        """Year-by-year table for visualization."""
        years  = max(target_age - self.p.age, 1)
        rows   = []
        wealth = self.p.current_net_worth

        for y in range(years + 1):
            age_y      = self.p.age + y
            contrib_y  = required_monthly * 12
            interest_y = wealth * annual_return
            rows.append({
                "Âge": age_y,
                "Patrimoine": wealth,
                "Intérêts annuels": interest_y,
                "Cotisation annuelle": contrib_y,
                "% de l'objectif": min(wealth / target_wealth * 100, 100) if target_wealth > 0 else 0,
            })
            wealth = wealth * (1 + annual_return) + contrib_y

        return pd.DataFrame(rows)

    def explain_in_plain_language(self, plan: dict, currency: str = "EUR") -> list[str]:
        """Generate plain-language explanations (no jargon)."""
        from utils.formatters import format_currency
        sym   = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(currency, currency)
        msgs  = []
        p     = plan
        r_m   = p["required_monthly"]
        t_w   = p["target_wealth"]
        t_a   = p["target_age"]
        yrs   = p["years_left"]

        if r_m == 0:
            msgs.append(f"🎉 Bonne nouvelle ! Votre patrimoine actuel suffit déjà pour atteindre votre objectif sans effort supplémentaire.")
            return msgs

        msgs.append(
            f"Pour atteindre {format_currency(t_w, currency)} à {t_a} ans, "
            f"vous devez mettre de côté {sym}{r_m:.0f} par mois pendant {yrs} ans."
        )

        msgs.append(
            f"C'est {sym}{p['daily_equivalent']:.0f} par jour — "
            f"l'équivalent d'{'un café et une baguette' if p['daily_equivalent'] < 5 else 'un repas' if p['daily_equivalent'] < 20 else 'quelques sorties'} en moins."
        )

        if p["interest_this_year"] > 100:
            msgs.append(
                f"Cette année, votre argent déjà placé vous rapporte {format_currency(p['interest_this_year'], currency)} "
                f"en intérêts — sans rien faire de plus."
            )

        for m in p["milestones"]:
            msgs.append(
                f"À {m['age']} ans → vous aurez environ {format_currency(m['wealth'], currency, compact=True)} "
                f"({m['wealth']/t_w*100:.0f}% de votre objectif)."
            )

        if p["on_track"]:
            msgs.append(f"✅ Vous épargnez déjà suffisamment pour atteindre votre objectif. Continuez comme ça !")
        else:
            msgs.append(
                f"⚠️ Il vous manque {sym}{p['monthly_gap']:.0f}/mois par rapport à votre épargne actuelle. "
                f"Réduire une dépense non essentielle peut suffire."
            )

        return msgs
