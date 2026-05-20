"""
Progressive Savings Plan Engine.
Start small, grow gradually. Catch-up logic for missed months.
"Chaque mois compte — meme un petit pas."
"""
import math
from models.user_profile import UserProfile

MONTH_FR = {
    1: "Janvier", 2: "Fevrier", 3: "Mars", 4: "Avril",
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Aout",
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Decembre",
}


class ProgressivePlanEngine:

    def __init__(self, profile: UserProfile):
        self.p = profile

    def full_required_monthly(self, target_wealth: float, target_age: int,
                               annual_return: float) -> float:
        years = max(target_age - self.p.age, 1)
        n = years * 12
        r_m = (1 + annual_return) ** (1 / 12) - 1
        fv_current = self.p.current_net_worth * (1 + r_m) ** n
        if fv_current >= target_wealth:
            return 0.0
        gap = target_wealth - fv_current
        if r_m == 0:
            return gap / n
        return gap * r_m / ((1 + r_m) ** n - 1)

    def build_progressive_plans(self, target_wealth: float, target_age: int,
                                 annual_return: float) -> list:
        required = self.full_required_monthly(target_wealth, target_age, annual_return)
        years_left = max(target_age - self.p.age, 1)

        plans = []

        # Plan 1: Regulier — montant fixe
        year_targets_1 = {y + 1: round(required) for y in range(years_left)}
        plans.append({
            "name": "Epargne reguliere",
            "icon": "🚀",
            "description": "Meme montant chaque mois — objectif atteint pile a temps",
            "color": "#4CAF50",
            "difficulty": "Ambitieux",
            "start_pct": 100,
            "year_targets": year_targets_1,
            "months_delayed": 0,
        })

        # Plan 2: Montee en puissance — debut a 55%, +20%/an
        year_targets_2 = {}
        amt = required * 0.55
        for y in range(1, years_left + 1):
            year_targets_2[y] = round(min(amt, required * 1.05))
            amt = amt * 1.20
        delay_2 = self._estimate_delay_months(target_wealth, annual_return,
                                               year_targets_2, years_left)
        plans.append({
            "name": "Montee en puissance",
            "icon": "📈",
            "description": "Commencez petit, augmentez chaque annee — ideal si les finances sont serrees",
            "color": "#D4AF37",
            "difficulty": "Equilibre",
            "start_pct": 55,
            "year_targets": year_targets_2,
            "months_delayed": delay_2,
        })

        # Plan 3: A votre rythme — debut a 30%, +25%/an
        year_targets_3 = {}
        amt = required * 0.30
        for y in range(1, years_left + 1):
            year_targets_3[y] = round(min(amt, required * 1.08))
            amt = amt * 1.25
        delay_3 = self._estimate_delay_months(target_wealth, annual_return,
                                               year_targets_3, years_left)
        plans.append({
            "name": "A votre rythme",
            "icon": "🛡️",
            "description": "Demarrage tres doux — pour construire l'habitude sans pression",
            "color": "#4A90D9",
            "difficulty": "Accessible",
            "start_pct": 30,
            "year_targets": year_targets_3,
            "months_delayed": delay_3,
        })

        return plans

    def _estimate_delay_months(self, target_wealth: float, annual_return: float,
                                year_targets: dict, years_left: int) -> int:
        wealth = self.p.current_net_worth
        for y in range(1, years_left + 1):
            monthly = year_targets.get(y, 0)
            wealth = wealth * (1 + annual_return) + monthly * 12
        if wealth >= target_wealth:
            return 0
        r_m = (1 + annual_return) ** (1 / 12) - 1
        if r_m > 0 and wealth > 0 and target_wealth > wealth:
            extra = math.log(target_wealth / wealth) / math.log(1 + r_m)
            return max(0, round(extra))
        return 0

    def catch_up_analysis(self, savings_history: list, annual_return: float) -> dict:
        if not savings_history:
            return {
                "shortfall": 0, "catch_up_monthly": 0, "n_missed": 0,
                "status": "on_track",
                "message": "Aucun historique — commencez ce mois-ci !",
            }

        total_shortfall = sum(max(h["target"] - h["actual"], 0) for h in savings_history)
        n_missed = sum(1 for h in savings_history if h["actual"] < h["target"] * 0.75)
        months_remaining = max(
            (self.p.target_retirement_age - self.p.age) * 12 - len(savings_history), 1
        )
        r_m = (1 + annual_return) ** (1 / 12) - 1

        if total_shortfall > 0 and months_remaining > 0:
            fv_shortfall = (total_shortfall * (1 + r_m) ** months_remaining
                            if r_m > 0 else total_shortfall)
            if r_m > 0:
                catch_up = fv_shortfall * r_m / ((1 + r_m) ** months_remaining - 1)
            else:
                catch_up = fv_shortfall / months_remaining
        else:
            catch_up = 0.0

        first_target = savings_history[0]["target"] if savings_history else 1

        if total_shortfall == 0:
            status = "excellent"
            message = "Parfait — vous suivez votre plan a la lettre. Continuez !"
        elif n_missed >= 4:
            status = "discipline_year"
            message = "Plusieurs mois difficiles. Ce mois-ci est votre mois de la discipline — priorite epargne !"
        elif total_shortfall < first_target * 3:
            status = "good"
            message = "Petit retard, tres rattrapable. Un effort supplementaire ce mois suffira."
        else:
            status = "warning"
            message = "Retard accumule — pensez a renegocier votre plan ou intensifier l'effort."

        return {
            "shortfall": total_shortfall,
            "catch_up_monthly": round(catch_up),
            "n_missed": n_missed,
            "n_months": len(savings_history),
            "status": status,
            "message": message,
        }

    def yearly_recap(self, savings_history: list) -> list:
        if not savings_history:
            return []
        by_year = {}
        for h in savings_history:
            y = h["year"]
            if y not in by_year:
                by_year[y] = {"year": y, "months": 0, "target_total": 0.0, "actual_total": 0.0}
            by_year[y]["months"] += 1
            by_year[y]["target_total"] += h["target"]
            by_year[y]["actual_total"] += h["actual"]

        result = []
        for y, data in sorted(by_year.items(), reverse=True):
            pct = (data["actual_total"] / data["target_total"] * 100
                   if data["target_total"] > 0 else 0)
            data["achievement_pct"] = pct
            if pct >= 95:
                data["label"] = "Excellent"
                data["label_icon"] = "🎉"
                data["label_color"] = "#4CAF50"
            elif pct >= 75:
                data["label"] = "Bien"
                data["label_icon"] = "✅"
                data["label_color"] = "#D4AF37"
            elif pct >= 50:
                data["label"] = "Partiel"
                data["label_icon"] = "⚠️"
                data["label_color"] = "#FF9800"
            else:
                data["label"] = "Difficile"
                data["label_icon"] = "❌"
                data["label_color"] = "#F44336"
            result.append(data)
        return result
