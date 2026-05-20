"""
Budget Optimizer — Conseils hyper-concrets poste par poste.
Chaque tip inclut: economie estimee, effort, exemples chiffres, actions immediates.
"""

OPTIMIZATION_TIPS = {
    "Alimentation": {
        "icon": "🍽️",
        "benchmark_pct": 0.15,
        "color": "#4CAF50",
        "tips": [
            {
                "id": "meal_prep",
                "title": "Batch cooking le dimanche",
                "saving_pct": 0.28,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "elevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Un repas préparé maison coûte 2–4 € vs 12–20 € au restaurant ou 7–10 € en livraison. "
                    "3h de cuisine le dimanche couvrent 5 déjeuners de la semaine."
                ),
                "examples": [
                    "Riz + légumes rôtis + poulet pour 5 jours : ~15 € total = 3 €/repas",
                    "Pasta bolognaise (8 portions) : ~10 € = 1,25 €/repas",
                    "Soupe de légumes de saison (6 portions) : ~6 € = 1 €/repas",
                ],
                "actions": [
                    "Cuisinez 1 grosse protéine (poulet rôti, lentilles, œufs durs) + 2 féculents + 2 légumes",
                    "Investissez dans des boîtes hermétiques empilables (~20 € une fois)",
                    "Application gratuite : Jow ou Marmiton pour planifier la semaine",
                ],
                "monthly_saving_example": 180,
            },
            {
                "id": "bulk_buying",
                "title": "Achats en gros pour les produits secs",
                "saving_pct": 0.15,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Riz, pâtes, légumineuses, huile, farine en grand format coûtent 25–40 % moins cher "
                    "que les petits conditionnements. Durée de vie longue = zéro gaspillage."
                ),
                "examples": [
                    "Riz 5 kg : 4 € vs riz 500 g × 10 = 9 €  → économie 5 €",
                    "Lentilles 2 kg vrac : 3,50 € vs sachets 500 g × 4 = 7,20 €",
                    "Huile d'olive 3 L : 10 € vs 1 L × 3 = 15 €",
                ],
                "actions": [
                    "Faites un tour trimestriel en magasin discount (Lidl, Aldi) pour les stocks",
                    "Rejoignez un AMAP ou groupement d'achat local pour légumes 30–40 % moins chers",
                    "Vrac en ligne : Greenweez, Naturalia pour céréales et légumineuses",
                ],
                "monthly_saving_example": 40,
            },
            {
                "id": "marques_distributeur",
                "title": "Marques distributeur vs grandes marques",
                "saving_pct": 0.20,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Les marques distributeur (Casino, Carrefour, Leclerc) coûtent 30–50 % moins cher "
                    "pour une qualité quasi identique. Fabriqués souvent par les mêmes usines."
                ),
                "examples": [
                    "Yaourt nature × 8 : marque 1,80 € vs distributeur 0,95 €",
                    "Corn flakes 500 g : marque 3,20 € vs distributeur 1,10 €",
                    "Café moulu 250 g : marque 4,50 € vs distributeur 2,20 €",
                ],
                "actions": [
                    "Commencez par 5 produits ultra-consommés (café, yaourt, pâtes, beurre, lait)",
                    "Comparez uniquement les produits avec composition similaire",
                    "Appli Yuka pour vérifier que la qualité est équivalente",
                ],
                "monthly_saving_example": 35,
            },
            {
                "id": "anti_gaspi",
                "title": "Applications anti-gaspillage alimentaire",
                "saving_pct": 0.10,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Too Good To Go, Phenix, Optimiam permettent d'acheter des paniers invendus "
                    "de restaurants et boulangeries à -60/80 %. Parfait pour le dîner improvisé."
                ),
                "examples": [
                    "Panier boulangerie 3–5 pièces : 2 € (valeur 8 €)",
                    "Panier traiteur asiatique : 5 € (valeur 18 €)",
                    "Légumes du marché fin de journée : -50 % sur tout",
                ],
                "actions": [
                    "Téléchargez Too Good To Go — gratuit, disponible partout",
                    "Configurez des alertes pour les restaurants/boulangeries proches de chez vous",
                    "Marché couvert : arrivez 30 min avant la fermeture pour les prix soldés",
                ],
                "monthly_saving_example": 25,
            },
            {
                "id": "legumes_saison",
                "title": "Légumes de saison et surgelés stratégiques",
                "saving_pct": 0.12,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": False,
                "description": (
                    "Les légumes hors saison coûtent 2–4× plus cher et ont moins de valeur nutritive. "
                    "Les surgelés nature (sans sauce) sont identiques en nutrition, 40–60 % moins chers."
                ),
                "examples": [
                    "Haricots verts frais en janvier : 4 €/kg vs surgelés : 1,50 €/kg",
                    "Epinards frais hors saison : 5 €/kg vs surgelés : 2 €/kg",
                    "Tomates été vs tomates décembre : ×3 de prix",
                ],
                "actions": [
                    "Calendrier des saisons : cherchez 'légumes de saison [votre mois]'",
                    "Remplacez 40 % de vos légumes frais hors saison par des surgelés nature",
                    "Achetez et congelez vous-même en été quand les prix sont au plus bas",
                ],
                "monthly_saving_example": 20,
            },
        ],
    },
    "Transport": {
        "icon": "🚗",
        "benchmark_pct": 0.12,
        "color": "#2196F3",
        "tips": [
            {
                "id": "covoiturage",
                "title": "Covoiturage domicile-travail",
                "saving_pct": 0.40,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Partager le trajet avec un collègue divise les coûts carburant par 2 ou plus. "
                    "Même 2–3 jours/semaine représente une économie significative annuelle."
                ),
                "examples": [
                    "20 km domicile-travail × 2 trajets × 22 jours = 880 km/mois à 0,12 €/km = 105 €",
                    "Avec covoiturage 3j/5j : économie de ~63 €/mois",
                    "BlaBlaCar Daily gratuit pour trouver vos voisins de trajet",
                ],
                "actions": [
                    "Inscrivez-vous sur BlaBlaCar Daily ou Klaxit",
                    "Annonce dans le groupe WhatsApp de votre entreprise",
                    "Plan : alterner conducteur une semaine sur deux",
                ],
                "monthly_saving_example": 65,
            },
            {
                "id": "entretien_preventif",
                "title": "Entretien préventif = éviter les grosses pannes",
                "saving_pct": 0.25,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Une vidange à 80 € évite un moteur grippé à 3 000 €. "
                    "La pression des pneus à +0,5 bar sous-gonflé augmente la consommation de 2 %."
                ),
                "examples": [
                    "Vidange + filtre : 60–90 € = évite casse moteur 2 000–5 000 €",
                    "Pression pneus correcte : économie 0,2 L/100 km soit ~18 €/mois",
                    "Plaquettes de frein changées à temps : 200 € vs disques + plaquettes 600 €",
                ],
                "actions": [
                    "Notez dans votre agenda les échéances carnet d'entretien",
                    "Application Cardio Car : alertes entretien gratuites",
                    "Fiche de révision : pression pneus chaque 1er du mois (2 min)",
                ],
                "monthly_saving_example": 30,
            },
            {
                "id": "assurance_optimisation",
                "title": "Renégocier son assurance auto chaque année",
                "saving_pct": 0.20,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Les assureurs comptent sur votre inertie. Comparer et renégocier chaque année "
                    "peut économiser 150–400 € annuels à couverture identique."
                ),
                "examples": [
                    "Comparateur LeLynx / Assurland : 15 min pour 3 devis",
                    "Menace de résiliation = souvent une offre de rétention -15 %",
                    "Bonus 50 % acquis : passer en tiers + vol si voiture > 10 ans",
                ],
                "actions": [
                    "Date d'anniversaire du contrat = moment de comparer",
                    "Appelez votre assureur actuel avec la meilleure offre concurrente",
                    "Vérifiez si votre CB premium couvre déjà certains risques",
                ],
                "monthly_saving_example": 25,
            },
            {
                "id": "velo_transport_commun",
                "title": "Vélo / Transport en commun pour courts trajets",
                "saving_pct": 0.35,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Pour les trajets < 5 km, le vélo est plus rapide que la voiture en ville "
                    "et coûte 0 carburant. Un vélo à 300 € s'amortit en 3 mois vs voiture."
                ),
                "examples": [
                    "Abonnement vélo libre-service (Vélib) : 40 €/an vs voiture 150 €/mois",
                    "Trajet 3 km en voiture : 0,50 € + parking + stress vs vélo 0 €",
                    "Pass Navigo en IDF : 86 €/mois vs voiture 250–400 €/mois",
                ],
                "actions": [
                    "Identifiez 2–3 trajets hebdomadaires que vous pourriez faire en vélo",
                    "Employeur : demandez la prime vélo (jusqu'à 500 €/an défiscalisés)",
                    "Leasing vélo électrique via employeur : 20–40 €/mois",
                ],
                "monthly_saving_example": 80,
            },
        ],
    },
    "Logement": {
        "icon": "🏠",
        "benchmark_pct": 0.30,
        "color": "#FF9800",
        "tips": [
            {
                "id": "energie_optimisation",
                "title": "Réduire sa facture énergie de 30 %",
                "saving_pct": 0.25,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Chauffage = 60–70 % de la facture énergétique. "
                    "Baisser de 1 °C = -7 % de consommation. Un thermostat programmable = -15 %."
                ),
                "examples": [
                    "Thermostat à 19 °C (vs 21 °C) en journée : -14 % = ~15 €/mois",
                    "Mode nuit 16 °C : -20 % supplémentaires",
                    "Prises multiprises à interrupteur : éliminer les veilles = -5 €/mois",
                ],
                "actions": [
                    "Posez des joints de fenêtre (5 € aux bricoleurs) : -10 % de fuite thermique",
                    "Thermostat connecté Tado / Netatmo : 80 € amorti en 6 mois",
                    "Chauffe-eau : programmez sur heure creuse (22h–6h)",
                ],
                "monthly_saving_example": 35,
            },
            {
                "id": "assurance_habitation",
                "title": "Optimiser son assurance habitation",
                "saving_pct": 0.20,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "L'assurance habitation est souvent sur-calibrée. "
                    "Comparer prend 10 min et économise en moyenne 100–200 €/an."
                ),
                "examples": [
                    "Locataire : assurance entre 8 et 30 €/mois selon assureur",
                    "Direct assurance (Luko, Lovys) : 30–40 % moins cher que traditionnels",
                    "Regroupement auto + habitation : -15 % en général",
                ],
                "actions": [
                    "Comparez sur LeLynx ou Meilleurtaux",
                    "Vérifiez si votre mutuelle couvre déjà certains risques",
                    "Déclarez fidèlement la surface pour ne pas surpayer",
                ],
                "monthly_saving_example": 15,
            },
            {
                "id": "colocation",
                "title": "Colocation ou sous-location stratégique",
                "saving_pct": 0.40,
                "effort": "élevé",
                "effort_color": "#F44336",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Partager un T3 divise le loyer par 2 tout en bénéficiant d'un "
                    "logement plus grand. La sous-location d'une chambre vide est légale avec accord bailleur."
                ),
                "examples": [
                    "Paris : T3 1 500 € partagé = 750 €/pers vs T1 900 € seul",
                    "Sous-louer chambre vide 500 €/mois = 6 000 €/an de revenus",
                    "Louer sur Airbnb 2 week-ends/mois = 300–600 € extra",
                ],
                "actions": [
                    "Leboncoin, La Carte des Colocs pour trouver colocataires sérieux",
                    "Lettre de sous-location à demander à votre propriétaire (modèle Service Public)",
                    "Plateforme Flatlooker pour colocation clé en main",
                ],
                "monthly_saving_example": 200,
            },
        ],
    },
    "Abonnements": {
        "icon": "📱",
        "benchmark_pct": 0.05,
        "color": "#9C27B0",
        "tips": [
            {
                "id": "audit_abonnements",
                "title": "Audit complet de vos abonnements",
                "saving_pct": 0.40,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "En moyenne, les Français ont 12 abonnements actifs dont 3–4 oubliés. "
                    "Un relevé bancaire de 3 mois révèle tous les prélèvements automatiques."
                ),
                "examples": [
                    "Netflix (18 €) + Disney+ (9 €) + Amazon (7 €) + Spotify (10 €) = 44 €/mois",
                    "Salle de sport non utilisée : 30–50 €/mois = 400 € gaspillés/an",
                    "Logiciel abonné mais version gratuite suffisante : 5–15 €/mois",
                ],
                "actions": [
                    "Épluchure de 3 relevés bancaires : surlignez chaque prélèvement récurrent",
                    "Application Tricount ou Linxo pour automatiser la détection",
                    "Règle : si non utilisé 3 semaines de suite → annulez immédiatement",
                ],
                "monthly_saving_example": 45,
            },
            {
                "id": "mutualisation_streaming",
                "title": "Mutualiser les abonnements streaming",
                "saving_pct": 0.50,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Les formules famille permettent 4–6 profils. "
                    "Partager avec famille ou amis de confiance divise la facture par 2–4."
                ),
                "examples": [
                    "Netflix Premium (22 €) partagé à 4 = 5,50 €/pers",
                    "Spotify Duo (13 €) pour 2 personnes au même domicile",
                    "Apple One famille (22 €) pour 6 : Apple Music + TV + Arcade + 200 GB",
                ],
                "actions": [
                    "Identifiez 2–3 proches pour partager Netflix / Disney+",
                    "Spotify Family si même domicile (jusqu'à 6 comptes)",
                    "Rotation : un mois Netflix, un mois Disney+, annulez l'autre",
                ],
                "monthly_saving_example": 20,
            },
            {
                "id": "telephone_operateur",
                "title": "Changer d'opérateur mobile / box",
                "saving_pct": 0.35,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Les opérateurs low-cost (Free, SFR RED, B&You, Prixtel) offrent "
                    "les mêmes réseaux 50–60 % moins cher. Le changement prend 48h."
                ),
                "examples": [
                    "Orange 100 Go : 35 €/mois vs Free 210 Go : 10 €/mois (même réseau Orange)",
                    "SFR 200 € → RED 15 €/mois : économie 180 €/an",
                    "Box fibre Orange 45 € → Free 30 € = 180 €/an",
                ],
                "actions": [
                    "Conservez votre numéro (portabilité gratuite et automatique)",
                    "Comparez sur meilleurmobile.com — mise à jour en temps réel",
                    "Attendez les promotions Free (souvent < 12 €/mois les Black Friday)",
                ],
                "monthly_saving_example": 30,
            },
        ],
    },
    "Santé": {
        "icon": "💊",
        "benchmark_pct": 0.05,
        "color": "#E91E63",
        "tips": [
            {
                "id": "medicaments_generiques",
                "title": "Médicaments génériques systématiquement",
                "saving_pct": 0.30,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Les génériques ont la même molécule active, même dosage, même efficacité. "
                    "Ils coûtent 20–70 % moins cher. Le pharmacien peut les substituer automatiquement."
                ),
                "examples": [
                    "Doliprane vs paracétamol générique : 3,20 € vs 1,60 €",
                    "Ibuprofène 400 mg : marque 4 € vs générique 1,80 €",
                    "Oméprazole : marque 15 € vs générique 4,50 €",
                ],
                "actions": [
                    "Dites à votre médecin : 'Je souhaite la version générique'",
                    "Pharmacie en ligne agréée (Doctipharma) : -30 % sur parapharmacie",
                    "Appli Mediprix pour comparer prix dans les pharmacies proches",
                ],
                "monthly_saving_example": 15,
            },
            {
                "id": "mutuelle_optimisation",
                "title": "Optimiser sa mutuelle santé",
                "saving_pct": 0.25,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "80 % des Français surpayent leur mutuelle car ils n'ont pas revu leur "
                    "contrat depuis +2 ans. Vos besoins réels (dentaire, optique, hospit) doivent guider le choix."
                ),
                "examples": [
                    "Mutuelle étudiante : Age2r ou LMDE à 20–35 €/mois selon besoins",
                    "Mutuelle 'entrée de gamme' jeune sans enfant : 35–50 €/mois suffisent",
                    "Mutuelles en ligne (Acheel, Wazari) : 20–35 % moins cher",
                ],
                "actions": [
                    "Faites le bilan de vos dépenses santé des 2 dernières années",
                    "Comparez sur Santécompare ou LesFurets",
                    "Résiliation à tout moment après 1 an (loi Châtel/Hamon)",
                ],
                "monthly_saving_example": 20,
            },
            {
                "id": "prevention_sport",
                "title": "Prévention : sport régulier pour réduire les frais de santé",
                "saving_pct": 0.20,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "30 min de marche rapide/jour réduit les consultations médicales "
                    "et arrêts maladie. Coût : 0 €. Résultat : économie sur médicaments et médecins."
                ),
                "examples": [
                    "1 consultation médecin évitée = 25–60 € économisés",
                    "Arrêt maladie évité = pas de jour de carence ni perte de salaire",
                    "Sport sans salle : Fiit (gratuit 1 mois), YouTube, parcs",
                ],
                "actions": [
                    "30 min de marche rapide au déjeuner = 0 € et bienfaits prouvés",
                    "Application Nike Run Club ou Strava : gratuit, motivant",
                    "PASS Sport gouvernemental : jusqu'à 50 € d'aide pour une inscription sportive",
                ],
                "monthly_saving_example": 10,
            },
        ],
    },
    "Loisirs": {
        "icon": "🎉",
        "benchmark_pct": 0.08,
        "color": "#00BCD4",
        "tips": [
            {
                "id": "bibliotheque_culture",
                "title": "Médiathèque et culture gratuite",
                "saving_pct": 0.35,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "La médiathèque municipale donne accès gratuitement à milliers de livres, "
                    "films, musique, jeux vidéo, presse numérique. Carte gratuite ou -10 €/an."
                ),
                "examples": [
                    "Bibliothèque : 0 € vs 1 livre/semaine = 15 €/semaine = 60 €/mois",
                    "MédiaBib : journaux en ligne (Le Monde, L'Équipe) inclus = 30 €/mois économisés",
                    "Jeux vidéo : médiathèque prête Switch et PS5 dans certaines villes",
                ],
                "actions": [
                    "Inscrivez-vous en mairie : souvent gratuit jusqu'à 18 ans, 10–15 €/an pour adultes",
                    "Application PressReader via médiathèque : 7 000 journaux du monde",
                    "Cinémathèque / musées nationaux : gratuit 1er dimanche du mois",
                ],
                "monthly_saving_example": 40,
            },
            {
                "id": "sorties_smart",
                "title": "Sorties intelligentes : happy hours et réductions",
                "saving_pct": 0.30,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Cinéma UGC illimité à 22 €/mois si vous y allez 2× = rentable. "
                    "Happy hour 18h–20h : même qualité, moitié prix. Les sorties ne se suppriment pas, elles s'optimisent."
                ),
                "examples": [
                    "UGC Illimité : 22 €/mois vs 12 € × 3 séances = 36 € → économie 14 €",
                    "Restaurant midi vs soir : même plat -40 % avec le menu déjeuner",
                    "Apps Groupon / Dealabs pour les activités à -50 %",
                ],
                "actions": [
                    "Comparez les abonnements cinéma : UGC, Pathé Gaumont selon votre fréquence",
                    "Dealabs.com : alertes sur les offres loisirs de votre ville",
                    "Sorties culturelles en semaine : -30 à -50 % sur les musées et spectacles",
                ],
                "monthly_saving_example": 25,
            },
            {
                "id": "voyages_smart",
                "title": "Voyager moins cher avec la flexibilité",
                "saving_pct": 0.35,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Partir mardi–mercredi au lieu du week-end : billets -40 %. "
                    "Réserver 8 semaines à l'avance ou au contraire en last-minute : -30–50 %."
                ),
                "examples": [
                    "Paris–Marseille TGV : 140 € vendredi soir vs 39 € mardi matin",
                    "Hôtel 3★ Barcelone : 180 €/nuit week-end vs 90 € lundi–jeudi",
                    "Google Flights 'Calendrier des prix' : trouve le jour le moins cher",
                ],
                "actions": [
                    "Activez alertes Google Flights pour vos destinations préférées",
                    "Flexibilité de ±3 jours = économie de 35 % en moyenne",
                    "Airbnb avec cuisine vs hôtel : économisez 30–40 % sur la restauration",
                ],
                "monthly_saving_example": 30,
            },
        ],
    },
    "Vêtements": {
        "icon": "👗",
        "benchmark_pct": 0.04,
        "color": "#FF5722",
        "tips": [
            {
                "id": "seconde_main",
                "title": "Seconde main : même qualité, prix divisé par 3",
                "saving_pct": 0.55,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Vinted, Vestiaire Collective, dépôts-vente permettent d'acheter "
                    "marques et vêtements qualitatifs à -60 % du prix neuf."
                ),
                "examples": [
                    "Jean Levi's 501 neuf : 90 € vs Vinted occasion : 25 €",
                    "Manteau en laine neuf 200 € vs seconde main 55 €",
                    "Chaussures de sport neuves 120 € vs occasion 35–45 €",
                ],
                "actions": [
                    "Pour chaque achat neuf envisagé, vérifiez d'abord Vinted",
                    "Vendez vos vêtements inutilisés : 50 articles = souvent 200–400 €",
                    "Braderies saisonnières : réductions 60–80 % sur les fins de collection",
                ],
                "monthly_saving_example": 35,
            },
            {
                "id": "capsule_wardrobe",
                "title": "Garde-robe capsule : achetez moins, achetez mieux",
                "saving_pct": 0.40,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "30 pièces polyvalentes de qualité durent 5× plus longtemps que "
                    "50 pièces fast fashion. Coût par utilisation 3× moins élevé."
                ),
                "examples": [
                    "T-shirt H&M 15 € × 3 remplacements/an = 45 € vs t-shirt Uniqlo 30 € × 5 ans = 6 €/an",
                    "Réduction d'achats impulsifs de 40–60 % avec la règle '1 acheté = 1 sorti'",
                    "Programme de fidélité Uniqlo / Arket pour les basiques qualitatifs",
                ],
                "actions": [
                    "Faites un inventaire : quels vêtements portez-vous vraiment ?",
                    "Règle 30 jours : notez l'envie d'achat, si toujours là après 30 j → achetez",
                    "Capsule wardrobe : 5 hauts, 3 bas, 2 vestes, 2 paires de chaussures suffisent",
                ],
                "monthly_saving_example": 20,
            },
        ],
    },
    "Banque & Finances": {
        "icon": "🏦",
        "benchmark_pct": 0.02,
        "color": "#607D8B",
        "tips": [
            {
                "id": "frais_bancaires",
                "title": "Passer à une banque sans frais",
                "saving_pct": 0.80,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Les banques traditionnelles facturent 10–25 €/mois de frais de tenue de compte. "
                    "Boursobank, Hello bank, Fortuneo sont totalement gratuits."
                ),
                "examples": [
                    "BNP frais mensuels : 14,90 € = 178 €/an → Boursobank : 0 €",
                    "Commission de change sur paiement étranger : 2–3 % → Revolut : 0 %",
                    "Retrait DAB : 1–3 € par retrait → néobanques : gratuit",
                ],
                "actions": [
                    "Ouvrez un compte Boursobank (0 €) ou Revolut (0 €) en 10 min",
                    "Domiciliez votre salaire pour obtenir la carte gratuite",
                    "Gardez l'ancienne banque 3 mois puis clôturez (service de mobilité bancaire)",
                ],
                "monthly_saving_example": 18,
            },
            {
                "id": "taux_credit_reneg",
                "title": "Renégocier ou racheter son crédit consommation",
                "saving_pct": 0.30,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Un crédit à la consommation à 15 % peut être racheté à 7–8 %. "
                    "Sur 5 000 € sur 24 mois, c'est 300–400 € d'intérêts économisés."
                ),
                "examples": [
                    "5 000 € à 18 % sur 24 mois vs 8 % : économie 480 € d'intérêts",
                    "Regroupement de crédits : une mensualité unique, taux souvent réduit",
                    "Remboursement anticipé possible sans frais si < 10 000 € et taux fixe",
                ],
                "actions": [
                    "Comparez Younited Credit, Cofidis, votre banque en ligne",
                    "Simulateur meilleurtaux.com en 2 min",
                    "Stratégie : remboursez d'abord le crédit au taux le plus élevé",
                ],
                "monthly_saving_example": 25,
            },
        ],
    },
}


class BudgetOptimizer:

    def __init__(self, profile):
        self.profile = profile

    def analyze_category(self, category: str, monthly_amount: float) -> dict:
        """Returns tips with estimated savings for a given category and spend."""
        cat = OPTIMIZATION_TIPS.get(category)
        if not cat:
            return {}
        tips_out = []
        for tip in cat["tips"]:
            saving_est = monthly_amount * tip["saving_pct"]
            tips_out.append({**tip, "estimated_saving": round(saving_est)})
        return {
            "category": category,
            "icon": cat["icon"],
            "color": cat["color"],
            "monthly_amount": monthly_amount,
            "benchmark": monthly_amount * 0.8,  # simplified benchmark
            "tips": tips_out,
            "total_potential_saving": round(sum(t["estimated_saving"] for t in tips_out)),
        }

    def top_opportunities(self, spending: dict, n: int = 8) -> list:
        """spending: {category: monthly_amount}. Returns top n tips by saving amount."""
        all_tips = []
        for cat, amount in spending.items():
            result = self.analyze_category(cat, amount)
            if result:
                for tip in result["tips"]:
                    all_tips.append({
                        **tip,
                        "category": cat,
                        "category_icon": result["icon"],
                        "category_color": result["color"],
                    })
        return sorted(all_tips, key=lambda t: t["estimated_saving"], reverse=True)[:n]

    def quick_wins(self, spending: dict) -> list:
        """Low-effort, high-impact tips only."""
        all_tips = self.top_opportunities(spending, n=50)
        return [t for t in all_tips if t["effort"] in ("très faible", "faible")][:5]

    def total_potential_monthly_saving(self, spending: dict) -> float:
        tips = self.top_opportunities(spending, n=20)
        return sum(t["estimated_saving"] for t in tips)

    @staticmethod
    def wealth_impact(monthly_saving: float, years: int, rate: float = 0.07) -> float:
        """Compound wealth if monthly saving is invested."""
        r_m = (1 + rate) ** (1 / 12) - 1
        n = years * 12
        if r_m > 0:
            return monthly_saving * ((1 + r_m) ** n - 1) / r_m
        return monthly_saving * n

    @staticmethod
    def meal_cost_comparison(budget_restaurant: float, budget_groceries: float) -> dict:
        """Detailed food breakdown analysis."""
        if budget_restaurant > 0 and budget_groceries > 0:
            restaurant_meals_per_month = budget_restaurant / 16
            home_equivalent_cost = restaurant_meals_per_month * 3.5
            saving = budget_restaurant - home_equivalent_cost
        else:
            saving = 0
            home_equivalent_cost = 0
            restaurant_meals_per_month = 0
        return {
            "restaurant_budget": budget_restaurant,
            "restaurant_meals_count": round(restaurant_meals_per_month),
            "home_equivalent_cost": round(home_equivalent_cost),
            "potential_saving": round(max(saving, 0)),
            "groceries_budget": budget_groceries,
            "cost_per_home_meal": 3.5,
            "cost_per_restaurant_meal": 16,
        }
