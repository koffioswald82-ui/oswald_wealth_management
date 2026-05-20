"""
Proprietary Wealth Score Engine (0–1000).
Multi-factor model: savings, debt, investments, emergency fund,
behavioral discipline, future preparedness, insurance.
"""
import numpy as np
from models.user_profile import UserProfile
from utils.financial_math import emergency_fund_months, savings_rate, debt_to_income_ratio

class WealthScoreEngine:

    MAX_SCORE = 1000

    COMPONENTS = {
        "Taux d'Épargne":           200,
        "Gestion de la Dette":      200,
        "Fonds d'Urgence":          150,
        "Investissements":          200,
        "Préparation Retraite":     150,
        "Discipline & Comportement":100,
    }

    def __init__(self, profile: UserProfile):
        self.p = profile

    def calculate(self) -> dict:
        p = self.p
        breakdown = {}
        total = 0.0

        # ---- 1. Savings Rate (200pts) ----
        sr = savings_rate(p.monthly_savings, p.total_income)
        # Benchmark: 20% excellent, 10% good, <5% poor
        sr_score = min(sr / 0.20, 1.0) * 200
        breakdown["Taux d'Épargne"] = {
            "score": sr_score, "max": 200,
            "value": sr, "benchmark": 0.20,
            "note": f"{sr*100:.1f}% de votre revenu épargné (cible : 20%+)",
            "color": "#4CAF50" if sr >= 0.20 else ("#D4AF37" if sr >= 0.10 else "#F44336"),
        }
        total += sr_score

        # ---- 2. Debt Management (200pts) ----
        dti = debt_to_income_ratio(p.monthly_debt_payment, p.total_income)
        # Below 20%: excellent; 20-36%: ok; >36%: poor
        if dti <= 0.20:
            dti_score = 200
        elif dti <= 0.36:
            dti_score = 200 * (1 - (dti - 0.20) / 0.16 * 0.5)
        else:
            dti_score = max(200 * (1 - (dti - 0.36) / 0.30), 0)
        breakdown["Gestion de la Dette"] = {
            "score": dti_score, "max": 200,
            "value": dti, "benchmark": 0.20,
            "note": f"DTI = {dti*100:.1f}% (max recommandé : 36%)",
            "color": "#4CAF50" if dti <= 0.20 else ("#D4AF37" if dti <= 0.36 else "#F44336"),
        }
        total += dti_score

        # ---- 3. Emergency Fund (150pts) ----
        ef_months = emergency_fund_months(p.emergency_fund, p.monthly_expenses)
        ef_score  = min(ef_months / 6.0, 1.0) * 150
        breakdown["Fonds d'Urgence"] = {
            "score": ef_score, "max": 150,
            "value": ef_months, "benchmark": 6.0,
            "note": f"{ef_months:.1f} mois de dépenses couverts (cible : 6 mois)",
            "color": "#4CAF50" if ef_months >= 6 else ("#D4AF37" if ef_months >= 3 else "#F44336"),
        }
        total += ef_score

        # ---- 4. Investment Quality (200pts) ----
        inv_total = p.current_investments + p.current_savings
        # Diversification bonus
        asset_types = sum([
            1 if p.stocks_pct > 0.05 else 0,
            1 if p.etf_pct > 0.05 else 0,
            1 if p.crypto_pct > 0 and p.crypto_pct < 0.15 else 0,
        ])
        has_investments = p.current_investments > p.total_income * 3
        diversification = asset_types / 3
        crypto_penalty  = max((p.crypto_pct - 0.15) * 200, 0)  # penalize >15% crypto
        inv_score = (
            (0.5 if has_investments else 0.2) +
            diversification * 0.5
        ) * 200 - crypto_penalty
        inv_score = max(0, min(200, inv_score))
        breakdown["Investissements"] = {
            "score": inv_score, "max": 200,
            "value": diversification, "benchmark": 1.0,
            "note": f"{asset_types} classes d'actifs investies (pénalité crypto: {crypto_penalty:.0f}pts)",
            "color": "#4CAF50" if inv_score >= 150 else ("#D4AF37" if inv_score >= 80 else "#F44336"),
        }
        total += inv_score

        # ---- 5. Retirement Preparedness (150pts) ----
        years_to_ret    = p.years_to_retirement
        target_corpus   = p.desired_monthly_pension * 12 / 0.04
        current_corpus  = p.current_investments + p.current_savings * 0.5
        # What corpus should they have by now? (linear glide to target)
        total_working   = max(p.target_retirement_age - 22, 1)
        years_worked    = p.age - 22
        ideal_now_pct   = years_worked / total_working
        ideal_now       = target_corpus * ideal_now_pct
        ret_score       = min(current_corpus / max(ideal_now, 1), 1.5) * 100  # up to 150
        ret_score       = min(ret_score, 150)
        breakdown["Préparation Retraite"] = {
            "score": ret_score, "max": 150,
            "value": current_corpus / max(target_corpus, 1),
            "benchmark": 1.0,
            "note": f"Corpus actuel : {current_corpus:,.0f} {p.currency} / Cible : {target_corpus:,.0f} {p.currency}",
            "color": "#4CAF50" if ret_score >= 120 else ("#D4AF37" if ret_score >= 60 else "#F44336"),
        }
        total += ret_score

        # ---- 6. Behavioral Discipline (100pts) ----
        behavioral = (
            p.discipline_score * 0.35 +
            (10 - p.emotional_spending) * 0.30 +
            p.consistency_score * 0.35
        ) / 10
        beh_score = behavioral * 100
        breakdown["Discipline & Comportement"] = {
            "score": beh_score, "max": 100,
            "value": behavioral, "benchmark": 1.0,
            "note": f"Score comportemental : {behavioral*100:.0f}/100",
            "color": "#4CAF50" if behavioral >= 0.70 else ("#D4AF37" if behavioral >= 0.50 else "#F44336"),
        }
        total += beh_score

        total = round(max(0, min(self.MAX_SCORE, total)))
        label = self._label(total)
        color = self._color(total)
        percentile = self._percentile(total)

        return {
            "total_score": total,
            "max_score": self.MAX_SCORE,
            "percentage": total / self.MAX_SCORE,
            "label": label,
            "color": color,
            "percentile": percentile,
            "breakdown": breakdown,
            "top_3_improvements": self._top_improvements(breakdown),
        }

    def _label(self, score: int) -> str:
        if score >= 850: return "Elite Wealth Builder"
        if score >= 700: return "Advanced Investor"
        if score >= 550: return "Wealth Builder"
        if score >= 400: return "On Track"
        if score >= 250: return "Getting Started"
        return "Financial Reset Needed"

    def _color(self, score: int) -> str:
        if score >= 700: return "#D4AF37"
        if score >= 500: return "#4CAF50"
        if score >= 300: return "#FF9800"
        return "#F44336"

    def _percentile(self, score: int) -> str:
        # Approximate percentile vs general population
        if score >= 850: return "Top 5%"
        if score >= 700: return "Top 15%"
        if score >= 550: return "Top 30%"
        if score >= 400: return "Top 50%"
        if score >= 250: return "Top 70%"
        return "Bottom 30%"

    def _top_improvements(self, breakdown: dict) -> list[dict]:
        gaps = [
            {"area": k, "gap": v["max"] - v["score"], "note": v["note"]}
            for k, v in breakdown.items()
        ]
        return sorted(gaps, key=lambda x: x["gap"], reverse=True)[:3]

    def get_age_benchmark(self) -> dict:
        """What score should someone your age have?"""
        age = self.p.age
        if age < 25:
            benchmark = 200
        elif age < 30:
            benchmark = 320
        elif age < 35:
            benchmark = 440
        elif age < 40:
            benchmark = 560
        elif age < 45:
            benchmark = 650
        elif age < 50:
            benchmark = 720
        elif age < 55:
            benchmark = 780
        else:
            benchmark = 820
        return {
            "benchmark": benchmark,
            "description": f"Benchmark pour {age} ans : {benchmark}/1000",
        }
