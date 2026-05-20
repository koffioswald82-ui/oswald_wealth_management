"""
AI Coaching Engine
Rule-based intelligent financial coaching with optional Claude API enhancement.
Generates personalized, impact-quantified insights — not generic advice.
"""
from models.user_profile import UserProfile
from utils.constants import COUNTRIES, CAR_COSTS
from utils.financial_math import future_value
from utils.formatters import format_currency

class AICoachingEngine:

    def __init__(self, profile: UserProfile):
        self.p  = profile
        self.cd = COUNTRIES.get(profile.country, COUNTRIES["France"])
        self.cur = profile.currency

    def _fmt(self, amount: float) -> str:
        return format_currency(amount, self.cur)

    def generate_all_insights(self) -> list[dict]:
        insights = []
        insights.extend(self._income_insights())
        insights.extend(self._savings_insights())
        insights.extend(self._debt_insights())
        insights.extend(self._investment_insights())
        insights.extend(self._lifestyle_insights())
        insights.extend(self._emergency_fund_insights())
        insights.extend(self._family_insights())
        insights.extend(self._real_estate_insights())
        insights.extend(self._retirement_insights())
        # Sort by priority
        priority_order = {"critical": 0, "warning": 1, "success": 2, "info": 3}
        insights.sort(key=lambda x: priority_order.get(x.get("type","info"), 3))
        return insights

    def _income_insights(self) -> list[dict]:
        p = self.p
        insights = []
        avg    = self.cd["avg_income"]
        ratio  = p.monthly_income / avg if avg > 0 else 1

        if ratio < 0.80:
            insights.append({
                "type": "warning", "category": "Revenus",
                "title": "Revenu sous la médiane nationale",
                "text": f"Votre revenu ({self._fmt(p.monthly_income)}/mois) est {(1-ratio)*100:.0f}% en dessous de la médiane {p.country}. Prioriser les leviers de revenu est votre meilleur levier patrimonial.",
                "actions": ["Négocier une augmentation (objectif +10%)", "Développer une source de revenus complémentaire", "Formation/reconversion pour changer de tranche salariale"],
                "impact": f"Une augmentation de 200 {self.cur}/mois investis sur 20 ans = {self._fmt(future_value(0, 0.06/12, 240, 200))}",
            })
        if p.side_income == 0:
            insights.append({
                "type": "info", "category": "Revenus",
                "title": "Aucun revenu complémentaire détecté",
                "text": "Un second flux de revenus (freelance, location, dividendes) réduit considérablement votre risque financier.",
                "actions": ["Explorer les activités de consulting/freelance dans votre domaine", "Location courte durée si vous êtes propriétaire", "Investissement en ETF dividendes"],
                "impact": f"200 {self.cur}/mois de side income investis sur 15 ans = {self._fmt(future_value(0, 0.06/12, 180, 200))}",
            })
        return insights

    def _savings_insights(self) -> list[dict]:
        p = self.p
        sr = p.monthly_savings / p.total_income if p.total_income > 0 else 0
        insights = []

        if sr < 0.05:
            insights.append({
                "type": "critical", "category": "Épargne",
                "title": "Taux d'épargne critique (< 5%)",
                "text": f"Vous épargnez {sr*100:.1f}% de vos revenus. En dessous de 5%, il est mathématiquement impossible de construire du patrimoine significatif.",
                "actions": ["Payer-vous en premier : virement automatique le jour de paie", "Identifier les 3 plus grosses fuites budgétaires", "Objectif 10% minimum d'ici 6 mois"],
                "impact": f"Passer de {sr*100:.0f}% à 15% d'épargne représente {self._fmt((0.15 - sr) * p.total_income)}/mois de plus investis.",
            })
        elif sr < 0.10:
            insights.append({
                "type": "warning", "category": "Épargne",
                "title": "Taux d'épargne insuffisant (< 10%)",
                "text": f"Votre taux d'épargne ({sr*100:.1f}%) est en dessous du minimum recommandé de 10%. La règle des banquiers privés : épargner 20% pour construire une vraie liberté financière.",
                "actions": ["Augmenter progressivement de 1% par mois", "Automatiser l'épargne pour éliminer la tentation"],
                "impact": f"+5% d'épargne = {self._fmt(p.total_income * 0.05)}/mois supplémentaires capitalisés.",
            })
        elif sr >= 0.20:
            insights.append({
                "type": "success", "category": "Épargne",
                "title": "Excellent taux d'épargne !",
                "text": f"Vous épargnez {sr*100:.1f}% de vos revenus — vous faites partie du top 10% des épargnants. Assurez-vous que cet argent est bien investi, pas seulement sur un compte courant.",
                "actions": ["Optimiser l'allocation de l'épargne (ETF, PEA, assurance-vie)"],
                "impact": "",
            })
        return insights

    def _debt_insights(self) -> list[dict]:
        p = self.p
        insights = []
        dti = p.monthly_debt_payment / p.total_income if p.total_income > 0 else 0

        if dti > 0.40:
            insights.append({
                "type": "critical", "category": "Dette",
                "title": f"Ratio d'endettement dangereux ({dti*100:.0f}%)",
                "text": f"Vous consacrez {dti*100:.0f}% de vos revenus au remboursement de dettes. Au-delà de 40%, vous êtes en zone de surendettement — votre capacité à épargner est nulle.",
                "actions": ["Renégocier les taux d'intérêt de vos crédits", "Méthode boule de neige : rembourser le plus petit crédit en premier", "Consolidation de dettes si possible"],
                "impact": f"Réduire le DTI à 30% libère {self._fmt((dti - 0.30) * p.total_income)}/mois pour investir.",
            })
        elif dti > 0.30:
            insights.append({
                "type": "warning", "category": "Dette",
                "title": f"Endettement élevé ({dti*100:.0f}%)",
                "text": f"Votre ratio dette/revenu de {dti*100:.0f}% laisse peu de marge. Priorité absolue : ne pas contracter de nouvelles dettes.",
                "actions": ["Stopper tout nouveau crédit à la consommation", "Rembourser par anticipation les crédits à taux >5%"],
                "impact": "",
            })
        return insights

    def _investment_insights(self) -> list[dict]:
        p = self.p
        insights = []

        if p.current_investments < p.total_income * 6 and p.age > 30:
            target = p.total_income * 12
            insights.append({
                "type": "warning", "category": "Investissements",
                "title": "Capital investi insuffisant pour votre âge",
                "text": f"À {p.age} ans, votre capital investi ({self._fmt(p.current_investments)}) est inférieur à 12 mois de revenus — le benchmark minimum à cet âge.",
                "actions": ["Ouvrir un PEA ou compte-titres si absent", "Investir en ETF World (MSCI World) pour commencer simplement", f"Objectif court terme : {self._fmt(target)} investis"],
                "impact": f"{self._fmt(target)} investis à 7%/an = {self._fmt(future_value(target, 0.07, p.years_to_retirement))} à la retraite.",
            })

        if p.crypto_pct > 0.20:
            loss_scenario = p.current_investments * p.crypto_pct * 0.60
            insights.append({
                "type": "critical", "category": "Investissements",
                "title": f"Surexposition crypto ({p.crypto_pct*100:.0f}% du portfolio)",
                "text": f"Plus de 20% en crypto représente un risque de perte majeure. La crypto est volatile à >60%. Un krach crypto détruirait {self._fmt(loss_scenario)} de votre patrimoine.",
                "actions": ["Réduire la part crypto à 5-15% maximum", "Ne jamais investir en crypto ce que vous ne pouvez pas vous permettre de perdre à 100%"],
                "impact": f"Scénario -60% crypto : perte potentielle de {self._fmt(loss_scenario)}",
            })

        if p.stocks_pct + p.etf_pct < 0.30 and p.years_to_retirement > 15:
            insights.append({
                "type": "info", "category": "Investissements",
                "title": "Sous-exposition aux actions pour un horizon long terme",
                "text": f"Avec {p.years_to_retirement} ans avant la retraite, une allocation actions/ETF de {(p.stocks_pct+p.etf_pct)*100:.0f}% est trop conservatrice. Les marchés actions surperforment historiquement sur >15 ans.",
                "actions": ["Augmenter progressivement la part ETF World", "Mettre en place un versement mensuel automatique sur ETF"],
                "impact": f"Différence 4% vs 7%/an sur 20 ans sur {self._fmt(50000)} = {self._fmt(future_value(50000,0.07,20) - future_value(50000,0.04,20))} de patrimoine en plus.",
            })

        return insights

    def _lifestyle_insights(self) -> list[dict]:
        p = self.p
        insights = []

        transport_pct = p.transport_monthly / p.total_income if p.total_income > 0 else 0
        if transport_pct > 0.15:
            opp_cost = future_value(0, 0.06/12, min(p.years_to_retirement, 25) * 12, p.transport_monthly * 0.5)
            insights.append({
                "type": "warning", "category": "Mode de vie",
                "title": f"Transport = {transport_pct*100:.0f}% du revenu",
                "text": f"Vous consacrez {self._fmt(p.transport_monthly)}/mois au transport. Au-delà de 15% du revenu, c'est un frein majeur à l'accumulation de patrimoine.",
                "actions": ["Analyser la nécessité d'un véhicule premium vs utilitaire", "Calculer le coût réel (assurance, carburant, entretien, dépréciation)"],
                "impact": f"Réduire le budget transport de 50% et investir la différence = {self._fmt(opp_cost)} dans {min(p.years_to_retirement, 25)} ans.",
            })

        if p.luxury_monthly > p.total_income * 0.10:
            opp_cost_luxury = future_value(0, 0.065/12, 240, p.luxury_monthly)
            insights.append({
                "type": "warning", "category": "Mode de vie",
                "title": "Dépenses luxe élevées",
                "text": f"Vous dépensez {self._fmt(p.luxury_monthly)}/mois en luxe ({p.luxury_monthly/p.total_income*100:.0f}% du revenu). Pas de jugement — mais mesurer le coût d'opportunité est essentiel.",
                "actions": ["Fixer un 'budget luxe' conscient et non expansible", "Appliquer la règle 72h avant tout achat luxe"],
                "impact": f"Ces {self._fmt(p.luxury_monthly)}/mois investis sur 20 ans = {self._fmt(opp_cost_luxury)}.",
            })

        return insights

    def _emergency_fund_insights(self) -> list[dict]:
        p = self.p
        insights = []
        ef_months = p.emergency_fund / p.monthly_expenses if p.monthly_expenses > 0 else 0

        if ef_months < 1:
            insights.append({
                "type": "critical", "category": "Sécurité",
                "title": "Aucun fonds d'urgence — Risque maximal",
                "text": "Sans fonds d'urgence, le moindre imprévu (perte d'emploi, panne, maladie) vous force à vous endetter ou vendre vos investissements au pire moment.",
                "actions": [f"Objectif immédiat : {self._fmt(p.monthly_expenses * 2)} (2 mois)", "Ce capital doit être liquide, pas investi", "Compte épargne séparé — intouchable"],
                "impact": f"Cible finale : {self._fmt(p.monthly_expenses * 6)} (6 mois de dépenses).",
            })
        elif ef_months < 3:
            insights.append({
                "type": "warning", "category": "Sécurité",
                "title": f"Fonds d'urgence insuffisant ({ef_months:.1f} mois)",
                "text": f"Vous avez {ef_months:.1f} mois de dépenses couvertes. L'objectif standard est 6 mois, idéalement 9 pour les indépendants/entrepreneurs.",
                "actions": [f"Compléter jusqu'à {self._fmt(p.monthly_expenses * 6)}"],
                "impact": "",
            })
        else:
            insights.append({
                "type": "success", "category": "Sécurité",
                "title": f"Fonds d'urgence solide ({ef_months:.1f} mois)",
                "text": f"Votre fonds d'urgence de {ef_months:.1f} mois est au-dessus du standard. Vous pouvez désormais prendre plus de risque d'investissement en toute sérénité.",
                "actions": ["Ne pas gonfler davantage ce fonds — l'excès doit être investi"],
                "impact": "",
            })

        return insights

    def _family_insights(self) -> list[dict]:
        p = self.p
        insights = []

        if p.num_children > 0:
            child_cost = self.cd.get("child_monthly_cost", 850)
            total_child = child_cost * p.num_children
            pct = total_child / p.total_income if p.total_income > 0 else 0
            if pct > 0.30:
                insights.append({
                    "type": "warning", "category": "Famille",
                    "title": "Charge familiale élevée",
                    "text": f"{p.num_children} enfant(s) représente(nt) ~{self._fmt(total_child)}/mois, soit {pct*100:.0f}% de vos revenus. Planification rigoureuse indispensable.",
                    "actions": ["Maximiser les allocations familiales", "Planifier l'épargne études dès maintenant", "Revoir le budget en priorité"],
                    "impact": "",
                })

        return insights

    def _real_estate_insights(self) -> list[dict]:
        p = self.p
        insights = []

        if p.wants_property and p.target_purchase_age <= p.age + 3:
            from utils.financial_math import mortgage_payment
            loan = p.target_property_value * 0.80
            pmt  = mortgage_payment(loan, self.cd["mortgage_rate"], 25)
            dti_post = (pmt + p.monthly_debt_payment) / p.total_income if p.total_income > 0 else 1

            if dti_post > 0.40:
                insights.append({
                    "type": "critical", "category": "Immobilier",
                    "title": "Achat immobilier prévu trop tôt / bien trop cher",
                    "text": f"Un bien à {self._fmt(p.target_property_value)} entraînerait un DTI de {dti_post*100:.0f}% — au-dessus du seuil de 35% des banques. Risque de refus bancaire.",
                    "actions": ["Réduire la valeur du bien cible", "Repousser l'achat de 3-5 ans pour consolider l'apport", "Augmenter l'apport personnel à 25-30%"],
                    "impact": "",
                })

        return insights

    def _retirement_insights(self) -> list[dict]:
        p = self.p
        insights = []
        ytr = p.years_to_retirement

        if ytr <= 0:
            return insights

        target_corpus   = p.desired_monthly_pension * 12 / 0.04
        current_corpus  = p.current_investments + p.current_savings * 0.5
        projected_corpus = future_value(current_corpus, 0.065, ytr, p.monthly_savings * 0.5 * 12)  # annual pmt

        if projected_corpus < target_corpus * 0.70:
            gap = target_corpus - projected_corpus
            insights.append({
                "type": "warning", "category": "Retraite",
                "title": f"Déficit retraite projeté de {self._fmt(gap)}",
                "text": f"À votre rythme actuel, vous n'atteindrez que {projected_corpus/target_corpus*100:.0f}% du corpus nécessaire pour votre retraite souhaitée.",
                "actions": [
                    f"Augmenter l'épargne retraite de {self._fmt(gap/(ytr*12))} /mois supplémentaires",
                    "Envisager de travailler 2-3 ans de plus",
                    "Réduire les dépenses retraite cibles",
                ],
                "impact": f"Corpus cible : {self._fmt(target_corpus)} pour {self._fmt(p.desired_monthly_pension)}/mois à la retraite.",
            })
        else:
            insights.append({
                "type": "success", "category": "Retraite",
                "title": "Trajectoire retraite en bonne voie",
                "text": f"Votre projection de {self._fmt(projected_corpus)} couvre {projected_corpus/target_corpus*100:.0f}% de votre objectif retraite.",
                "actions": ["Continuer le cap — envisager d'optimiser fiscalement"],
                "impact": "",
            })

        return insights

    def claude_ai_analysis(self, api_key: str) -> str:
        """Enhanced analysis using Claude API (optional)."""
        if not api_key:
            return ""
        try:
            import anthropic
            p = self.p
            prompt = f"""
Tu es un conseiller en gestion de patrimoine privé de niveau family office.
Analyse ce profil financier et donne 3 recommandations ultra-précises et personnalisées.
Sois direct, chiffré et ne donne AUCUN conseil générique.

Profil :
- Age : {p.age} ans, pays : {p.country}
- Revenu total : {p.total_income:,.0f} {p.currency}/mois
- Épargne mensuelle : {p.monthly_savings:,.0f} {p.currency}/mois (taux: {p.net_savings_rate*100:.1f}%)
- Patrimoine net : {p.current_net_worth:,.0f} {p.currency}
- Dette mensuelle : {p.monthly_debt_payment:,.0f} {p.currency}/mois
- Fonds d'urgence : {p.emergency_fund:,.0f} {p.currency} ({p.emergency_fund/max(p.monthly_expenses,1):.1f} mois)
- Profil risque : {p.risk_tolerance}
- Horizon retraite : {p.years_to_retirement} ans
- Objectif retraite : {p.desired_monthly_pension:,.0f} {p.currency}/mois

Format : 3 recommandations numérotées, chacune avec un impact chiffré précis.
"""
            client   = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-opus-4-7",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"API non disponible : {str(e)}"
