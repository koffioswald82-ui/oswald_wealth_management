"""
Life Stage Engine — 7 stages from student to retirement.
Each stage has savings tolerance bands, priorities, and risks.
No hard targets — flexible ranges adapted to each life situation.
"""
from models.user_profile import UserProfile

LIFE_STAGES = {
    "Etudiant": {
        "icon": "🎓",
        "color": "#4A90D9",
        "label": "Etudiant(e)",
        "age_start": 18, "age_end": 26,
        "description": "Construire les bases sans se ruiner",
        "priority": "Creer l'habitude d'epargne, eviter les dettes",
        "savings_min_pct":   0.00,
        "savings_ok_pct":    0.05,
        "savings_ideal_pct": 0.10,
        "emergency_months_min":   1,
        "emergency_months_ideal": 2,
        "income_factor": 0.25,
        "key_actions": [
            "Evitez les credits a la consommation et les decouvertes",
            "Epargner 20€/mois est deja une victoire — l'habitude est tout",
            "Profitez des aides disponibles (CAF, bourses, tarifs reduits)",
            "Suivez votre budget chaque mois, meme approximativement",
        ],
        "key_risks": [
            "Decouvert bancaire → frais qui s'accumulent vite",
            "Credit conso pour smartphones ou voyages",
            "Pas de filet de securite pour les imprevu",
        ],
        "message": "Meme 20€/mois maintenant vaut mieux que 200€ plus tard. L'habitude compte plus que le montant.",
        "tolerance_note": "Vous n'avez pas encore les revenus pour epargner beaucoup — c'est normal. Zero dette et une petite epargne = deja une reussite.",
    },
    "Debut de carriere": {
        "icon": "🚀",
        "color": "#D4AF37",
        "label": "Debut de carriere",
        "age_start": 22, "age_end": 30,
        "description": "Premiers revenus, contrats parfois precaires",
        "priority": "Construire le fonds d'urgence, rembourser les dettes etudiantes",
        "savings_min_pct":   0.05,
        "savings_ok_pct":    0.10,
        "savings_ideal_pct": 0.15,
        "emergency_months_min":   2,
        "emergency_months_ideal": 4,
        "income_factor": 0.65,
        "key_actions": [
            "Constituez 3 mois de depenses en fonds d'urgence AVANT d'investir",
            "Remboursez les dettes etudiantes en priorite",
            "Commencez avec un Livret A — simple, liquide, sans risque",
            "Negociez votre salaire a chaque opportunite — c'est maintenant que ca se joue",
        ],
        "key_risks": [
            "CDD non renouvele → perte totale de revenu",
            "Lifestyle inflation avec le premier salaire",
            "Fonds d'urgence insuffisant en cas de coup dur",
        ],
        "message": "Le fonds d'urgence passe avant tout investissement. 3 mois de depenses en securite, ensuite on optimise.",
        "tolerance_note": "5% d'epargne est suffisant si vous avez encore des dettes ou etes en CDD. L'essentiel est de ne pas depenser tout votre salaire.",
    },
    "Stabilisation": {
        "icon": "⚡",
        "color": "#4CAF50",
        "label": "Phase de stabilisation",
        "age_start": 28, "age_end": 38,
        "description": "Revenus stables, grands projets a l'horizon",
        "priority": "Investir, preparer l'immobilier, optimiser",
        "savings_min_pct":   0.10,
        "savings_ok_pct":    0.15,
        "savings_ideal_pct": 0.20,
        "emergency_months_min":   3,
        "emergency_months_ideal": 6,
        "income_factor": 0.90,
        "key_actions": [
            "Ouvrez un PEA et commencez avec des ETF World (MSCI World)",
            "Preparez votre apport immobilier (10-20% de la valeur du bien)",
            "Automatisez votre epargne par virement automatique le jour de la paie",
            "Verifiez et renegociez vos assurances et abonnements",
        ],
        "key_risks": [
            "Acheter trop grand/cher par rapport a votre budget reel",
            "Negliger la retraite — chaque annee compte double maintenant",
            "Depenses de couple / vie commune mal planifiees",
        ],
        "message": "Chaque euro investi maintenant a 25-35 ans pour travailler. C'est votre meilleure periode d'accumulation.",
        "tolerance_note": "Visez 15-20%. Si vous avez un credit immobilier, 10% est tres bien. L'essentiel est de rester constant.",
    },
    "Famille": {
        "icon": "👨‍👩‍👧",
        "color": "#FF9800",
        "label": "Phase famille",
        "age_start": 30, "age_end": 48,
        "description": "Enfants, credit immobilier, charges elevees",
        "priority": "Equilibrer budget-famille et epargne, preparer l'education",
        "savings_min_pct":   0.08,
        "savings_ok_pct":    0.12,
        "savings_ideal_pct": 0.18,
        "emergency_months_min":   4,
        "emergency_months_ideal": 6,
        "income_factor": 1.00,
        "key_actions": [
            "Ouvrez un livret pour les etudes des enfants des la naissance",
            "Verifiez votre prevoyance (deces, invalidite) — vous etes responsable de votre famille",
            "Gardez 6 mois de charges en fonds d'urgence (charges plus elevees)",
            "Planifiez les grandes depenses longtemps a l'avance",
        ],
        "key_risks": [
            "Separation / divorce — impact financier majeur",
            "Perte d'emploi d'un des parents",
            "Couts d'education largement sous-estimes",
            "Credit immobilier + credit conso simultanement",
        ],
        "message": "Les charges sont elevees pendant cette phase — c'est normal. Meme 10% d'epargne est une victoire.",
        "tolerance_note": "8% minimum, 12% bien, 18% excellent. Avec des enfants et un credit, ne vous frustrez pas si vous n'atteignez pas 20%.",
    },
    "Pic de carriere": {
        "icon": "💼",
        "color": "#9C27B0",
        "label": "Pic de carriere",
        "age_start": 42, "age_end": 55,
        "description": "Revenus au maximum, charges qui diminuent",
        "priority": "Accelerer l'epargne retraite, se desendetter",
        "savings_min_pct":   0.15,
        "savings_ok_pct":    0.22,
        "savings_ideal_pct": 0.30,
        "emergency_months_min":   4,
        "emergency_months_ideal": 6,
        "income_factor": 1.20,
        "key_actions": [
            "Maximisez les versements sur PER (Plan Epargne Retraite) — deduction fiscale",
            "Soldez les credits restants en priorite",
            "Diversifiez (immobilier locatif si cela fait sens, obligations pour equilibrer)",
            "Aidez les enfants intelligemment sans sacrifier votre retraite",
        ],
        "key_risks": [
            "Burn-out / arret de travail long",
            "Soutenir financierement les enfants adultes au detriment de sa retraite",
            "Placements trop risques a 10-15 ans de la retraite",
        ],
        "message": "C'est votre meilleure fenetre d'epargne. Chaque euro supplementaire maintenant = liberte a la retraite.",
        "tolerance_note": "Visez 22-30%. Vous en avez les moyens et c'est la derniere grande fenetre avant la retraite.",
    },
    "Pre-retraite": {
        "icon": "🏁",
        "color": "#E91E63",
        "label": "Pre-retraite",
        "age_start": 54, "age_end": 65,
        "description": "Derniere ligne droite avant la liberte financiere",
        "priority": "Maximiser, securiser, planifier la succession",
        "savings_min_pct":   0.20,
        "savings_ok_pct":    0.28,
        "savings_ideal_pct": 0.35,
        "emergency_months_min":   6,
        "emergency_months_ideal": 12,
        "income_factor": 1.15,
        "key_actions": [
            "Soldez TOUS les credits avant l'arret du travail",
            "Reduisez l'exposition aux actions (glide path vers securite)",
            "Planifiez la succession (testament, donations)",
            "Calculez precisement votre pension vs vos besoins mensuels",
        ],
        "key_risks": [
            "Licenciement economique sans retrouver d'emploi a cet age",
            "Problemes de sante reduisant la capacite de travail",
            "Soutien financier aux parents ages ou aux enfants",
        ],
        "message": "Securisez plutot qu'optimisez. L'objectif est d'arriver sans dette et avec un coussin solide.",
        "tolerance_note": "Visez 25-35% si possible. Mais soldez les dettes AVANT d'epargner plus — la liberte sans dette vaut plus que l'epargne avec credit.",
    },
    "Retraite": {
        "icon": "🌅",
        "color": "#4CAF50",
        "label": "Retraite",
        "age_start": 62, "age_end": 100,
        "description": "Profitez — votre argent travaille pour vous",
        "priority": "Maintenir le niveau de vie, ne pas epuiser le capital",
        "savings_min_pct":   0.00,
        "savings_ok_pct":    0.00,
        "savings_ideal_pct": 0.05,
        "emergency_months_min":   6,
        "emergency_months_ideal": 12,
        "income_factor": 0.60,
        "key_actions": [
            "Respectez la regle des 4% pour les retraits annuels",
            "Gardez 2 ans de depenses en liquidites (livret, fonds euros)",
            "Minimisez les impots sur les revenus du capital (optimisation fiscale)",
            "Protegez-vous des arnaques — la vigilance augmente avec l'age",
        ],
        "key_risks": [
            "Longevite — risque de survivre a son capital",
            "Dependance — couts de sante et aide a domicile",
            "Inflation qui erode le pouvoir d'achat sur 20-30 ans",
        ],
        "message": "Vous avez construit ce patrimoine. Profitez-en intelligemment et durablement.",
        "tolerance_note": "L'objectif n'est plus d'epargner mais de depenser intelligemment sans epuiser le capital.",
    },
}

# Micro-crises that affect everyday people
MICRO_CRISES = {
    "fin_cdd": {
        "name": "Fin de CDD non renouvele",
        "icon": "📋",
        "color": "#F44336",
        "severity": "Majeur",
        "severity_color": "#F44336",
        "description": "Votre contrat a duree determinee n'est pas renouvele. Zero revenu jusqu'au prochain emploi.",
        "income_loss_monthly_pct": 0.43,
        "income_loss_pct": 1.00,
        "allocation_pct": 0.57,
        "duration_months_low": 2,
        "duration_months_high": 6,
        "has_allocation": True,
        "allocation_label": "Allocation Pole Emploi (~57% du salaire brut apres 4 mois de cotisation)",
        "actions": [
            "Inscrivez-vous a Pole Emploi dans les 12 jours (delai de carence sinon)",
            "Activez le mode economie : coupez abonnements non-essentiels",
            "Cherchez des missions courtes (Malt, Upwork, interim) pour combler",
            "Contactez votre banque pour suspendre ou reporter certains prelevements",
        ],
    },
    "arret_maladie": {
        "name": "Arret maladie prolonge",
        "icon": "🏥",
        "color": "#FF9800",
        "severity": "Modere",
        "severity_color": "#FF9800",
        "description": "Vous etes en arret de travail plusieurs semaines. Revenu reduit a 80%.",
        "income_loss_pct": 0.20,
        "allocation_pct": 0.80,
        "duration_months_low": 1,
        "duration_months_high": 3,
        "has_allocation": True,
        "allocation_label": "Indemnites journalieres Secu (env. 50% du salaire brut + complement employeur)",
        "actions": [
            "Verifiez si votre contrat inclut un maintien de salaire (souvent 90 jours)",
            "Controlez votre mutuelle — elle peut compenser le reste",
            "Anticipez les 3 jours de carence sans indemnisation",
            "Evitez de toucher a l'epargne long terme si les 3-4 premiers mois sont couverts",
        ],
    },
    "panne_voiture": {
        "name": "Panne grave ou accident de voiture",
        "icon": "🚗",
        "color": "#FF9800",
        "severity": "Modere",
        "severity_color": "#FF9800",
        "description": "Votre voiture tombe en panne ou est accidentee. Reparation ou remplacement urgent.",
        "one_time_cost": 1800,
        "income_loss_pct": 0.0,
        "has_allocation": False,
        "duration_months_low": 0,
        "duration_months_high": 0,
        "actions": [
            "Contactez votre assurance auto immediatement — verifiez la couverture",
            "Comparez au moins 3 devis avant de commander les pieces",
            "Considerez les transports en commun / covoiturage temporairement",
            "Evitez le credit conso pour cette depense si votre fonds d'urgence peut absorber",
        ],
    },
    "hausse_loyer": {
        "name": "Augmentation de loyer soudaine",
        "icon": "🏠",
        "color": "#D4AF37",
        "severity": "Modere",
        "severity_color": "#D4AF37",
        "description": "Votre proprietaire augmente votre loyer. Impact permanent sur votre budget mensuel.",
        "monthly_increase": 120,
        "income_loss_pct": 0.0,
        "has_allocation": False,
        "duration_months_low": 999,
        "duration_months_high": 999,
        "actions": [
            "Verifiez que l'augmentation respecte l'IRL (indice de reference des loyers)",
            "Renegociez le loyer — les proprietaires acceptent souvent de maintenir si locataire fiable",
            "Comparez le cout d'un demenagement vs la hausse sur 2-3 ans",
            "Compensez en reduisant une autre categorie de depenses du meme montant",
        ],
    },
    "impot_surprise": {
        "name": "Regularisation fiscale imprevisible",
        "icon": "📊",
        "color": "#D4AF37",
        "severity": "Faible",
        "severity_color": "#D4AF37",
        "description": "Rappel d'impots ou cotisation imprevisible a regler rapidement.",
        "one_time_cost": 2200,
        "income_loss_pct": 0.0,
        "has_allocation": False,
        "duration_months_low": 0,
        "duration_months_high": 0,
        "actions": [
            "Demandez un echelonnement de paiement aux impots (mensualisation acceptee souvent)",
            "Verifiez si vous avez bien declare tous vos revenus cette annee",
            "Constituez une reserve fiscale (1-2% du revenu annuel de cote)",
            "Consultez un comptable si le montant est important",
        ],
    },
    "separation": {
        "name": "Separation ou divorce",
        "icon": "💔",
        "color": "#F44336",
        "severity": "Majeur",
        "severity_color": "#F44336",
        "description": "Vous vous separez. Les charges passent d'un budget partage a un budget seul.",
        "expense_increase_pct": 0.40,
        "income_loss_pct": 0.0,
        "has_allocation": False,
        "duration_months_low": 6,
        "duration_months_high": 18,
        "actions": [
            "Securisez un nouveau logement en priorite (budget revu a la baisse)",
            "Listez et separez tous les comptes et contrats partages immediatement",
            "Consultez un avocat pour proteger vos droits patrimoniaux",
            "Recentrez-vous sur votre fonds d'urgence personnel — repartir de zero prend 6-12 mois",
        ],
    },
    "chomage_partiel": {
        "name": "Chomage partiel ou activite reduite",
        "icon": "📉",
        "color": "#FF9800",
        "severity": "Modere",
        "severity_color": "#FF9800",
        "description": "Votre entreprise vous met en activite partielle. Salaire reduit a 84%.",
        "income_loss_pct": 0.16,
        "allocation_pct": 0.84,
        "duration_months_low": 2,
        "duration_months_high": 6,
        "has_allocation": True,
        "allocation_label": "Indemnite activite partielle (84% du net habituel)",
        "actions": [
            "Identifiez les depenses pouvant etre reportees sans penalite",
            "Cherchez un complement de revenu (freelance, formations remunere",
            "Evitez de puiser dans l'epargne long terme si possible",
            "Profitez du temps partiel pour monter en competences",
        ],
    },
    "sante_non_rembourse": {
        "name": "Depenses de sante non couvertes",
        "icon": "💊",
        "color": "#D4AF37",
        "severity": "Faible",
        "severity_color": "#D4AF37",
        "description": "Soins dentaires, optique, specialiste — depassement non rembourse.",
        "one_time_cost": 800,
        "income_loss_pct": 0.0,
        "has_allocation": False,
        "duration_months_low": 0,
        "duration_months_high": 0,
        "actions": [
            "Comparez les mutuelles — une bonne mutuelle peut economiser 400-600€/an",
            "Consultez les centres de sante mutualistes (tarifs sans depassement)",
            "Echelonnez les soins non-urgents sur plusieurs mois",
            "Demandez une entente prealable a votre mutuelle avant les soins importants",
        ],
    },
}


class LifeStageEngine:

    def __init__(self, profile: UserProfile):
        self.p = profile

    def detect_stage(self) -> str:
        age = self.p.age
        income = self.p.total_income
        country_avg = self.p.country_avg_income
        income_ratio = income / country_avg if country_avg > 0 else 1.0

        if age >= self.p.target_retirement_age:
            return "Retraite"
        if age >= max(self.p.target_retirement_age - 11, 54):
            return "Pre-retraite"
        if age >= 42 and income_ratio >= 0.95:
            return "Pic de carriere"
        if age < 25 or (age < 28 and income_ratio < 0.45):
            return "Etudiant"
        if age < 30 or (age < 33 and income_ratio < 0.65):
            return "Debut de carriere"
        if self.p.num_children > 0 and age <= 48:
            return "Famille"
        return "Stabilisation"

    def get_stage(self, stage_name: str = None) -> dict:
        if stage_name is None:
            stage_name = self.detect_stage()
        return LIFE_STAGES.get(stage_name, LIFE_STAGES["Stabilisation"])

    def savings_tolerance(self, stage_name: str = None) -> dict:
        cfg = self.get_stage(stage_name)
        income = self.p.total_income
        current = self.p.monthly_savings

        min_amt   = round(income * cfg["savings_min_pct"])
        ok_amt    = round(income * cfg["savings_ok_pct"])
        ideal_amt = round(income * cfg["savings_ideal_pct"])

        if current >= ideal_amt:
            status, color = "excellent", "#4CAF50"
            label = "Excellent pour votre etape de vie !"
        elif current >= ok_amt:
            status, color = "good", "#D4AF37"
            label = "Bien — vous etes dans la bonne fourchette"
        elif current >= min_amt and min_amt > 0:
            status, color = "minimum", "#FF9800"
            label = "Minimum acceptable — progressez quand vous pouvez"
        elif cfg["savings_min_pct"] == 0 and current > 0:
            status, color = "good", "#D4AF37"
            label = "Vous epargnez deja — c'est l'essentiel a cette etape !"
        else:
            status, color = "below", "#F44336"
            label = "En-dessous du minimum — priorite urgente"

        return {
            "min_pct":    cfg["savings_min_pct"],
            "ok_pct":     cfg["savings_ok_pct"],
            "ideal_pct":  cfg["savings_ideal_pct"],
            "min_amount": min_amt,
            "ok_amount":  ok_amt,
            "ideal_amount": ideal_amt,
            "current":    current,
            "status":     status,
            "label":      label,
            "color":      color,
            "tolerance_note": cfg["tolerance_note"],
        }

    def simulate_micro_crisis(self, crisis_key: str, duration_months: int = None) -> dict:
        crisis = MICRO_CRISES[crisis_key]
        p = self.p
        income = p.total_income
        expenses = p.monthly_expenses
        emergency = p.emergency_fund

        if duration_months is None:
            duration_months = crisis["duration_months_high"]

        # Monthly income during crisis
        if crisis.get("income_loss_pct", 0) > 0:
            reduced_income = income * (1 - crisis["income_loss_pct"])
            if crisis.get("has_allocation"):
                net_income_during = income * crisis.get("allocation_pct", 0.80)
            else:
                net_income_during = reduced_income
        else:
            net_income_during = income

        # Monthly expenses during crisis
        monthly_expense_increase = 0
        if "expense_increase_pct" in crisis:
            monthly_expense_increase = expenses * crisis["expense_increase_pct"]
        if "monthly_increase" in crisis:
            monthly_expense_increase = crisis["monthly_increase"]

        new_expenses = expenses + monthly_expense_increase

        # One-time cost
        one_time = crisis.get("one_time_cost", 0)

        # Monthly deficit during crisis
        monthly_deficit = max(new_expenses - net_income_during, 0)
        total_shortfall = monthly_deficit * duration_months + one_time

        # Emergency fund runway (months before empty)
        if monthly_deficit > 0:
            runway_months = emergency / monthly_deficit if emergency > 0 else 0
        elif one_time > 0:
            runway_months = 999 if emergency >= one_time else 0
        else:
            runway_months = 999

        # Can emergency fund cover the crisis?
        ef_covers = emergency >= total_shortfall
        ef_covers_partial = emergency >= total_shortfall * 0.5

        # Recovery time after crisis ends (months to rebuild emergency fund)
        normal_surplus = income - expenses
        rebuild_months = round(total_shortfall / normal_surplus) if normal_surplus > 50 else 999

        return {
            "crisis": crisis,
            "duration_months": duration_months,
            "income_normal": income,
            "income_during": net_income_during,
            "expenses_during": new_expenses,
            "one_time_cost": one_time,
            "monthly_deficit": monthly_deficit,
            "total_shortfall": total_shortfall,
            "emergency_fund": emergency,
            "runway_months": runway_months,
            "ef_covers": ef_covers,
            "ef_covers_partial": ef_covers_partial,
            "rebuild_months": rebuild_months,
            "missing_amount": max(total_shortfall - emergency, 0),
        }

    def life_timeline_stages(self) -> list:
        p = self.p
        ret_age = p.target_retirement_age

        return [
            {"name": "Etudiant",          "icon": "🎓", "color": "#4A90D9",  "start": 18, "end": min(25, ret_age)},
            {"name": "Debut de carriere", "icon": "🚀", "color": "#D4AF37",  "start": 22, "end": min(30, ret_age)},
            {"name": "Stabilisation",     "icon": "⚡", "color": "#4CAF50",  "start": 28, "end": min(38, ret_age)},
            {"name": "Famille",           "icon": "👨‍👩‍👧","color": "#FF9800", "start": 30, "end": min(48, ret_age)},
            {"name": "Pic de carriere",   "icon": "💼", "color": "#9C27B0",  "start": 42, "end": min(55, ret_age)},
            {"name": "Pre-retraite",      "icon": "🏁", "color": "#E91E63",  "start": max(ret_age - 10, 55), "end": ret_age},
            {"name": "Retraite",          "icon": "🌅", "color": "#4CAF50",  "start": ret_age, "end": ret_age + 25},
        ]
