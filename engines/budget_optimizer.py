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


# ── Contexte Côte d'Ivoire (XOF / FCFA) ─────────────────────────────────────
CI_OPTIMIZATION_TIPS = {
    "Alimentation": {
        "icon": "🍽️",
        "benchmark_pct": 0.20,
        "color": "#4CAF50",
        "tips": [
            {
                "id": "marche_vivriers",
                "title": "Marchés vivriers : 2× moins cher que les supermarchés",
                "saving_pct": 0.35,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Les marchés vivriers (Adjamé, Gouro, Cocody, Yopougon) vendent les mêmes produits "
                    "2 à 3 fois moins cher que SPAR, Carrefour ou PlaYce. "
                    "Venez en semaine : prix plus bas, moins de monde."
                ),
                "examples": [
                    "Tomates marchés Gouro : 500 FCFA/kg vs SPAR : 1 400 FCFA/kg",
                    "Igname marché vivrier : 800 FCFA/kg vs supermarché : 2 200 FCFA/kg",
                    "Banane plantain : 150 FCFA/régime vs 600 FCFA en supermarché",
                    "Graine de palme fraîche : 500 FCFA/kg marché vs 1 800 FCFA en conserve",
                ],
                "actions": [
                    "Faites 1 grand marché hebdomadaire le mardi ou mercredi (prix les plus bas)",
                    "Apportez un grand sac, achetez en quantité pour 7 jours",
                    "Construisez une relation avec 1–2 vendeurs réguliers : prix fidèle + meilleure qualité",
                ],
                "monthly_saving_example": 18000,
            },
            {
                "id": "maquis_vs_restaurant",
                "title": "Maquis local vs restaurant climatisé",
                "saving_pct": 0.30,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Un repas au maquis (attiéké poisson, riz sauce, placali) coûte 1 500–3 000 FCFA. "
                    "Le même repas dans un restaurant climatisé ou une brasserie : 8 000–20 000 FCFA. "
                    "La nourriture est souvent meilleure au maquis."
                ),
                "examples": [
                    "Attiéké poisson grillé maquis : 1 500–2 500 FCFA vs brasserie : 9 000 FCFA",
                    "Riz sauce graine cuisine de rue : 500–800 FCFA vs restaurant : 5 000 FCFA",
                    "Aloco poulet maquis : 1 000 FCFA vs fast-food type KFC : 4 500 FCFA",
                ],
                "actions": [
                    "Identifiez 2–3 maquis propres et réguliers près de votre bureau / domicile",
                    "Déjeuner au maquis 4j/5 vs restaurant : économie ~25 000 FCFA/mois",
                    "Cuisinez soi-même le vendredi soir et le week-end pour équilibrer",
                ],
                "monthly_saving_example": 25000,
            },
            {
                "id": "cuisine_maison_ci",
                "title": "Cuisiner ses plats locaux soi-même",
                "saving_pct": 0.28,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Préparer soi-même le foutou, le riz sauce, le kedjenou ou l'attiéké "
                    "revient 4 à 6 fois moins cher qu'un repas acheté dehors. "
                    "1h de cuisine = 5 repas couverts."
                ),
                "examples": [
                    "Riz sauce tomate maison (4 portions) : 1 200 FCFA total = 300 FCFA/pers",
                    "Soupe de poisson maison (6 portions) : 3 500 FCFA = 580 FCFA/pers",
                    "Attiéké + thon en conserve maison : 800 FCFA vs acheté : 2 500 FCFA",
                ],
                "actions": [
                    "Batch cooking le dimanche : riz, sauce et protéine pour 3 jours",
                    "Achetez une glacière ou réfrigérateur d'occasion pour conserver les restes",
                    "Partagez les coûts : cuisinez à 2 ou 3 pour diviser le temps et les achats",
                ],
                "monthly_saving_example": 20000,
            },
            {
                "id": "achat_gros_adjame",
                "title": "Achats en gros au marché d'Adjamé",
                "saving_pct": 0.20,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Le grand marché d'Adjamé (et Abobo, Yopougon) permet d'acheter condiments, "
                    "huile, riz, sucre en grande quantité avec un prix grossiste. "
                    "1 achat mensuel remplace 4 petits achats."
                ),
                "examples": [
                    "Sac de riz 25 kg Adjamé : 16 000 FCFA vs petits sachets marché : 24 000 FCFA",
                    "Bidon huile 5L : 7 000 FCFA vs 1L × 5 = 10 500 FCFA",
                    "Condiments en gros (cube maggi, concentré tomate) : -40 % vs épicerie",
                ],
                "actions": [
                    "Faites un grand stock mensuel : riz, huile, sucre, savon, cube Maggi",
                    "Venez avec un ami pour partager les quantités et frais de transport",
                    "Évitez les épiceries de quartier pour les produits secs (marge × 2 à 3)",
                ],
                "monthly_saving_example": 12000,
            },
        ],
    },
    "Transport": {
        "icon": "🚗",
        "benchmark_pct": 0.12,
        "color": "#2196F3",
        "tips": [
            {
                "id": "gbaka_woro",
                "title": "Gbaka et woro-woro vs taxi personnel",
                "saving_pct": 0.55,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Un trajet en taxi individuel coûte 2 000–6 000 FCFA à Abidjan. "
                    "Le même trajet en gbaka + woro-woro : 300–700 FCFA. "
                    "5 trajets/jour × différence = 150 000 FCFA économisés par mois."
                ),
                "examples": [
                    "Cocody → Plateau taxi : 3 000 FCFA vs gbaka + woro : 500 FCFA",
                    "Yopougon → Adjamé taxi : 4 000 FCFA vs gbaka : 350 FCFA",
                    "Course Bolt/Yango centre-ville : 2 500–5 000 FCFA vs gbaka : 200–500 FCFA",
                ],
                "actions": [
                    "Identifiez les lignes gbaka de votre trajet domicile–travail",
                    "Réservez le taxi pour les urgences et rendez-vous importants seulement",
                    "Application Bolt en off-peak (6h–7h30) : jusqu'à 40 % moins cher",
                ],
                "monthly_saving_example": 45000,
            },
            {
                "id": "covoiturage_collegues",
                "title": "Covoiturage avec collègues ou voisins",
                "saving_pct": 0.40,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Partager la voiture avec 1 collègue de même quartier divise le carburant par 2. "
                    "À 700 FCFA/L d'essence et 30 km/jour, cela représente 30 000–40 000 FCFA/mois économisés."
                ),
                "examples": [
                    "Carburant solo Angré–Plateau : ~45 000 FCFA/mois vs partagé : 22 500 FCFA",
                    "Alternance conducteur : une semaine sur deux = 0 carburant payé les autres semaines",
                    "Groupe WhatsApp de covoiturage de quartier : gratuit, immédiat",
                ],
                "actions": [
                    "Annonce WhatsApp dans votre immeuble ou cité : 'cherche covoiturage vers Plateau'",
                    "Application Heetch / Bolt Pool pour le covoiturage organisé",
                    "Modèle simple : celui qui conduit ne paie pas l'essence cette semaine",
                ],
                "monthly_saving_example": 22000,
            },
            {
                "id": "entretien_voiture_ci",
                "title": "Entretien préventif : éviter les grosses pannes",
                "saving_pct": 0.20,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "En Côte d'Ivoire, une panne moteur sur route = remorquage + réparation = "
                    "200 000–600 000 FCFA. Une vidange à 15 000 FCFA toutes les 5 000 km évite cela."
                ),
                "examples": [
                    "Vidange + filtre à huile : 12 000–18 000 FCFA = évite casse moteur 250 000 FCFA",
                    "Pneus regonflés (pression correcte) : consommation -3 % = 1 500 FCFA/mois économisés",
                    "Remplacement courroie de distribution à temps : 35 000 FCFA vs moteur cassé : 400 000 FCFA",
                ],
                "actions": [
                    "Vidange tous les 5 000 km ou tous les 3 mois — notez la date dans votre téléphone",
                    "Garagiste de confiance dans le quartier : négociez un forfait entretien annuel",
                    "Vérification pression pneus : 1 fois par mois, 5 min, économie réelle",
                ],
                "monthly_saving_example": 8000,
            },
        ],
    },
    "Logement": {
        "icon": "🏠",
        "benchmark_pct": 0.30,
        "color": "#FF9800",
        "tips": [
            {
                "id": "cie_optimisation",
                "title": "Réduire sa facture CIE (électricité) de 30 %",
                "saving_pct": 0.30,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "La climatisation représente 60–70 % d'une facture CIE. "
                    "Un climatiseur laissé allumé toute la nuit à vide = 15 000–25 000 FCFA/mois gaspillés. "
                    "Les appareils en veille consomment en continu."
                ),
                "examples": [
                    "Clim à 26 °C (vs 18 °C) : consommation divisée par 2,5 = ~20 000 FCFA économisés",
                    "Clim avec minuterie (éteinte 4h avant réveil) : -30 % sur la facture clim",
                    "Ventilateur de plafond : 200 FCFA/mois vs clim : 8 000 FCFA/mois",
                ],
                "actions": [
                    "Programmez votre clim pour s'éteindre 2h après votre endormissement",
                    "Branchez les appareils sur multiprises à interrupteur : éteignez la nuit",
                    "Ampoules LED (500 FCFA pièce) vs incandescentes : -80 % sur éclairage",
                ],
                "monthly_saving_example": 15000,
            },
            {
                "id": "colocation_ci",
                "title": "Colocation : loyer divisé, qualité améliorée",
                "saving_pct": 0.40,
                "effort": "élevé",
                "effort_color": "#F44336",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "À Abidjan, un appartement 2 chambres en colocation revient moins cher "
                    "qu'un studio seul, pour plus d'espace. L'entraide sur les charges divise aussi l'eau et l'électricité."
                ),
                "examples": [
                    "Studio Cocody : 80 000 FCFA seul vs chambre en colocation T3 : 45 000 FCFA",
                    "Charges partagées (eau, électricité, gardien) : -50 % chacun",
                    "Yopougon T3 en colocation à 3 : 30 000 FCFA/pers vs studio 60 000 FCFA",
                ],
                "actions": [
                    "Groupe Facebook 'Colocation Abidjan' pour trouver des colocataires sérieux",
                    "Contrat de partage simple : chaque colocataire paie sa part directement au propriétaire",
                    "Vérifiez la compatibilité avant : horaires, habitudes, règles de vie commune",
                ],
                "monthly_saving_example": 35000,
            },
            {
                "id": "eau_sodeci",
                "title": "Optimiser sa consommation d'eau SODECI",
                "saving_pct": 0.25,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Les fuites non réparées (robinet qui goutte) peuvent tripler la facture SODECI. "
                    "Un robinet qui goutte perd 15 L/heure = 10 000 L/mois gaspillés."
                ),
                "examples": [
                    "Robinet qui goutte réparé : économie 3 000–8 000 FCFA/mois",
                    "Chasse d'eau qui coule : 20 000–40 000 FCFA/mois gaspillés",
                    "Récupération eau de pluie pour le jardin/lessive : -20 % facture eau",
                ],
                "actions": [
                    "Vérifiez tous les robinets : si ça goutte, réparez (moins de 2 000 FCFA de pièce)",
                    "Compteur principal coupé la nuit si pas d'utilisation : détecte les fuites cachées",
                    "Plombier de quartier pour inspection annuelle : 5 000 FCFA, peut éviter 50 000 FCFA de facture",
                ],
                "monthly_saving_example": 5000,
            },
        ],
    },
    "Mobile Money": {
        "icon": "📲",
        "benchmark_pct": 0.03,
        "color": "#FF5722",
        "tips": [
            {
                "id": "wave_vs_orange",
                "title": "Wave : transferts gratuits et retraits moins chers",
                "saving_pct": 0.60,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Wave (application bleue) propose les transferts entre comptes Wave gratuits "
                    "et des retraits à 1 % vs Orange Money à 1–3,5 %. "
                    "Sur 200 000 FCFA de transferts mensuels, l'économie est significative."
                ),
                "examples": [
                    "Transfert 50 000 FCFA Wave → Wave : 0 FCFA vs Orange Money → OM : 500–1 000 FCFA",
                    "Retrait 100 000 FCFA Wave : 1 000 FCFA vs Orange Money : 2 500 FCFA",
                    "Paiement marchand Wave : 0 % de frais vs espèces avec risque de fausse monnaie",
                ],
                "actions": [
                    "Téléchargez Wave et incitez vos proches à l'utiliser aussi (réseau = plus d'avantages)",
                    "Paiements marchands : privilégiez Wave pour les transactions du quotidien",
                    "Gardez Orange Money pour les destinataires qui n'ont pas Wave",
                ],
                "monthly_saving_example": 8000,
            },
            {
                "id": "eviter_frais_retrait",
                "title": "Planifier les retraits pour éviter les petits frais répétés",
                "saving_pct": 0.40,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "5 petits retraits de 10 000 FCFA coûtent 5 × 300 FCFA = 1 500 FCFA en frais. "
                    "1 seul retrait de 50 000 FCFA coûte 500 FCFA. "
                    "Planifier = économiser sur les frais répétitifs."
                ),
                "examples": [
                    "10 retraits de 5 000 FCFA/mois : 10 × 200 FCFA = 2 000 FCFA de frais",
                    "2 retraits de 25 000 FCFA/mois : 2 × 400 FCFA = 800 FCFA de frais",
                    "Économie annuelle : 14 400 FCFA simplement en groupant les retraits",
                ],
                "actions": [
                    "Retirez une fois par semaine en quantité suffisante plutôt que tous les jours",
                    "Utilisez le paiement mobile (Wave, Orange Money) pour éviter les retraits",
                    "Gardez un petit fond d'espèces à la maison pour les petites dépenses",
                ],
                "monthly_saving_example": 4000,
            },
            {
                "id": "epargne_mobile_money",
                "title": "Épargne automatique via mobile money",
                "saving_pct": 0.00,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Orange Money Épargne, Wave Épargne, ou MTN MoMo permettent de bloquer "
                    "automatiquement un montant à chaque réception de salaire. "
                    "'Payez-vous d'abord' : le meilleur réflexe financier."
                ),
                "examples": [
                    "Virement auto de 10 000 FCFA le jour du salaire : 120 000 FCFA/an sans effort",
                    "Orange Money Épargne : bloque l'argent et offre 3,5 % d'intérêt annuel",
                    "Règle des 24h : avant tout achat >10 000 FCFA, attendez 24h",
                ],
                "actions": [
                    "Configurez un virement automatique dès réception du salaire (10–20 % minimum)",
                    "Ouvrez un compte épargne distinct de votre compte courant Mobile Money",
                    "Ne liez PAS votre carte d'épargne au paiement marchand",
                ],
                "monthly_saving_example": 0,
            },
        ],
    },
    "Tontine & Épargne locale": {
        "icon": "🤝",
        "benchmark_pct": 0.10,
        "color": "#D4AF37",
        "tips": [
            {
                "id": "tontine_bien_choisie",
                "title": "Bien choisir et structurer sa tontine",
                "saving_pct": 0.00,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "La tontine (njangi, susu) est un outil puissant si bien structurée. "
                    "Membres fiables + montant adapté = discipline d'épargne forcée sans banque. "
                    "Mal structurée, elle peut devenir une source de conflits."
                ),
                "examples": [
                    "Tontine de 10 personnes à 25 000 FCFA/mois : chacun reçoit 250 000 FCFA à son tour",
                    "Tour mensuel = capital pour un projet (stock commerce, réparation maison)",
                    "Tontine avec intérêt (10 % ajouté au pot) : 275 000 FCFA reçus au lieu de 250 000",
                ],
                "actions": [
                    "Membres uniquement de confiance absolue — 1 défaillant = problème pour tous",
                    "Rédigez un document simple : ordre de passage, montant, pénalités de retard",
                    "Montant = ce que vous pouvez payer même un mauvais mois (ne vous surestimez pas)",
                ],
                "monthly_saving_example": 0,
            },
            {
                "id": "entraide_familiale_saine",
                "title": "Gérer sainement l'entraide familiale",
                "saving_pct": 0.15,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "L'entraide familiale est une valeur fondamentale, mais sans structure, "
                    "elle peut vider votre budget. Fixer un 'budget solidarité' mensuel fixe "
                    "protège votre épargne tout en restant généreux."
                ),
                "examples": [
                    "Budget solidarité fixe à 15 000 FCFA/mois : vous savez quoi donner et quand dire non",
                    "Aide en nature plutôt qu'en cash : moins de pression sur vos liquidités",
                    "Communiquez clairement : 'je peux aider de X mais pas plus ce mois'",
                ],
                "actions": [
                    "Définissez votre enveloppe solidarité avant de la distribuer, pas après",
                    "Priorité : vous-même → fonds urgence → épargne → solidarité",
                    "Non-remboursement : traiter comme un don, pas un prêt, pour éviter le ressentiment",
                ],
                "monthly_saving_example": 10000,
            },
            {
                "id": "microfinance_ci",
                "title": "Microfinance et COOPEC : alternatives à la banque classique",
                "saving_pct": 0.00,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Les COOPEC (coopératives d'épargne et crédit), Advans CI, FINCA, "
                    "et microfinances locales offrent des taux d'épargne 3–5 % et des "
                    "micro-crédits pour les projets, sans les frais bancaires classiques."
                ),
                "examples": [
                    "Compte COOPEC : 0 FCFA de frais de tenue vs banque classique : 3 000–6 000 FCFA/mois",
                    "Micro-crédit Advans CI à 18 % vs prêt personnel banque à 24–30 %",
                    "Épargne rémunérée COOPEC : 4,5 % vs compte bancaire ordinaire : 0 %",
                ],
                "actions": [
                    "Identifiez la COOPEC ou microfinance de votre quartier",
                    "Ouvrez un compte d'épargne là-bas pour votre fonds d'urgence",
                    "Comparez les taux avant tout crédit : banque vs microfinance vs mobile money",
                ],
                "monthly_saving_example": 5000,
            },
        ],
    },
    "Abonnements": {
        "icon": "📱",
        "benchmark_pct": 0.04,
        "color": "#9C27B0",
        "tips": [
            {
                "id": "canal_plus_ci",
                "title": "Optimiser son abonnement Canal+",
                "saving_pct": 0.40,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Canal+ est souvent l'abonnement le plus cher du foyer (5 000–15 000 FCFA/mois). "
                    "Le partager avec un voisin ou passer au forfait de base selon l'utilisation réelle."
                ),
                "examples": [
                    "Canal+ Access (basique) : 5 000 FCFA/mois vs Canal+ Tout en 1 : 14 000 FCFA",
                    "Partage antenne parabolique avec voisin : 2 500 FCFA chacun vs 5 000 FCFA seul",
                    "Showmax (inclus dans certains forfaits Canal+) : vérifiez si vous l'utilisez vraiment",
                ],
                "actions": [
                    "Vérifiez votre abonnement actuel : payez-vous pour des chaînes que vous ne regardez pas ?",
                    "Proposez à votre voisin de partager l'antenne et l'abonnement de base",
                    "Pendant la période sans matchs importants : passez temporairement au forfait inférieur",
                ],
                "monthly_saving_example": 6000,
            },
            {
                "id": "forfait_mobile_ci",
                "title": "Optimiser son forfait mobile Orange/MTN",
                "saving_pct": 0.35,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Beaucoup de gens recharge à la demande (plus cher à l'unité) "
                    "alors qu'un forfait mensuel adapté coûte 40–60 % moins cher par Mo et par minute."
                ),
                "examples": [
                    "Orange CI : forfait data 10 Go/mois = 5 000 FCFA vs recharges à la pièce = 9 000 FCFA",
                    "Forfait voix illimité nuit + weekend : 2 000 FCFA = 0 FCFA pour les appels familiaux",
                    "Comparateur de forfaits : site Orange CI vs MTN CI — chaque mois les offres changent",
                ],
                "actions": [
                    "Analysez vos 3 dernières recharges : data ou voix dominant ?",
                    "Passez au forfait mensuel adapté à votre usage réel",
                    "Activez le wifi domicile/bureau pour économiser votre data mobile",
                ],
                "monthly_saving_example": 4000,
            },
        ],
    },
    "Santé": {
        "icon": "💊",
        "benchmark_pct": 0.05,
        "color": "#E91E63",
        "tips": [
            {
                "id": "generiques_ci",
                "title": "Médicaments génériques en pharmacie",
                "saving_pct": 0.35,
                "effort": "très faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "En Côte d'Ivoire, les génériques coûtent 40–70 % moins cher que les marques importées "
                    "pour la même molécule. Demandez systématiquement le générique au pharmacien."
                ),
                "examples": [
                    "Paracétamol 500 mg générique : 200 FCFA vs Doliprane importé : 1 200 FCFA",
                    "Amoxicilline générique : 1 500 FCFA vs marque : 4 500 FCFA",
                    "Ibuprofène générique : 500 FCFA vs Nurofen importé : 2 800 FCFA",
                ],
                "actions": [
                    "Dites à votre médecin : 'je veux la version générique disponible localement'",
                    "Pharmacies LMCI ou Pharmacie Santé pour les génériques locaux",
                    "Ne jamais acheter de médicaments dans la rue — risque de faux médicaments",
                ],
                "monthly_saving_example": 5000,
            },
            {
                "id": "chu_vs_clinique",
                "title": "CHU / hôpital public pour les soins courants",
                "saving_pct": 0.50,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Une consultation dans une clinique privée coûte 15 000–40 000 FCFA. "
                    "La même consultation au CHU d'Abidjan ou à l'hôpital général : 2 000–5 000 FCFA. "
                    "Pour les urgences légères et consultations courantes, le public est suffisant."
                ),
                "examples": [
                    "Consultation généraliste CHU : 3 000 FCFA vs clinique privée : 20 000 FCFA",
                    "Prise de sang CHU : 5 000 FCFA vs clinique : 25 000 FCFA",
                    "Pharmacie Centrale CI : médicaments listés à prix encadrés par l'État",
                ],
                "actions": [
                    "Identifiez le centre de santé public le plus proche de chez vous",
                    "Clinique privée pour urgences vraies ou spécialistes — pas pour les rhumes",
                    "Mutuelle santé employeur : vérifiez ce qu'elle rembourse exactement",
                ],
                "monthly_saving_example": 8000,
            },
        ],
    },
    "Loisirs": {
        "icon": "🎉",
        "benchmark_pct": 0.06,
        "color": "#00BCD4",
        "tips": [
            {
                "id": "loisirs_gratuits_ci",
                "title": "Loisirs gratuits et peu chers à Abidjan",
                "saving_pct": 0.40,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "moyen",
                "impact_color": "#FF9800",
                "quick_win": True,
                "description": (
                    "Abidjan offre de nombreuses activités gratuites ou abordables : "
                    "plages accessibles, parcs, événements culturels, terrain de sport de quartier. "
                    "Les dépenses loisirs peuvent être divisées par 2 sans sacrifier la qualité de vie."
                ),
                "examples": [
                    "Plage Blockhaus (Bingerville) : gratuit vs Azuretti beach club : 5 000 FCFA/pers",
                    "Terrain de foot quartier : gratuit vs salle de sport huppée : 25 000 FCFA/mois",
                    "Festival musique et arts (MASA, FEMUA) : certains événements gratuits",
                ],
                "actions": [
                    "Identifiez 3 activités gratuites ou < 1 000 FCFA près de chez vous",
                    "Groupes Facebook 'Abidjan Sortie' pour trouver événements gratuits",
                    "Remplacez 1 sortie restaurant sur 2 par un pique-nique en famille",
                ],
                "monthly_saving_example": 12000,
            },
            {
                "id": "voyages_interieurs_ci",
                "title": "Voyages intérieurs : bus longue distance vs avion",
                "saving_pct": 0.50,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Un billet Abidjan–Bouaké en bus UTB : 6 000–8 000 FCFA vs Air Côte d'Ivoire : "
                    "50 000–80 000 FCFA. Pour les distances < 500 km, le bus confort est souvent suffisant."
                ),
                "examples": [
                    "Abidjan → Bouaké UTB : 7 000 FCFA (4h30) vs vol : 60 000 FCFA",
                    "Abidjan → Yamoussoukro VIP bus : 4 500 FCFA vs taxi de ville : 25 000 FCFA",
                    "Réservation à l'avance les bus longue distance (UTB, San Pedro Express) : places à tarif normal",
                ],
                "actions": [
                    "Bus UTB, TSR, Oumarou, Kéolis pour les grandes villes de l'intérieur",
                    "Réservez 48h à l'avance pour avoir les meilleures places",
                    "Avion uniquement pour les distances > 600 km ou urgences professionnelles",
                ],
                "monthly_saving_example": 15000,
            },
        ],
    },
    "Banque & Finances": {
        "icon": "🏦",
        "benchmark_pct": 0.02,
        "color": "#607D8B",
        "tips": [
            {
                "id": "frais_bancaires_ci",
                "title": "Réduire ou éliminer les frais bancaires",
                "saving_pct": 0.70,
                "effort": "faible",
                "effort_color": "#4CAF50",
                "impact": "élevé",
                "impact_color": "#4CAF50",
                "quick_win": True,
                "description": (
                    "Les banques classiques en CI (SGBCI, BICICI, SIB) facturent "
                    "3 000–8 000 FCFA/mois de frais de tenue de compte. "
                    "Les COOPEC et certains comptes Ecobank Basic sont à 0 FCFA."
                ),
                "examples": [
                    "SGBCI frais mensuels : 5 000 FCFA = 60 000 FCFA/an → COOPEC : 0 FCFA",
                    "Retrait DAB hors réseau : 500–1 000 FCFA à chaque fois",
                    "Ecobank Xpress Account : 0 frais de tenue, retrait via mobile money",
                ],
                "actions": [
                    "Demandez à votre banque la liste exacte de tous vos frais mensuels",
                    "Comparez avec Ecobank Xpress ou une COOPEC de quartier",
                    "Domiciliez votre salaire = souvent exonération des frais de tenue",
                ],
                "monthly_saving_example": 5000,
            },
            {
                "id": "credit_taux_ci",
                "title": "Éviter les crédits à la consommation à taux excessifs",
                "saving_pct": 0.30,
                "effort": "moyen",
                "effort_color": "#FF9800",
                "impact": "très élevé",
                "impact_color": "#4CAF50",
                "quick_win": False,
                "description": (
                    "Les crédits salaires et crédits consommation en CI affichent souvent "
                    "24–36 % d'intérêt annuel. Sur 500 000 FCFA empruntés, "
                    "vous pouvez rembourser 700 000–800 000 FCFA."
                ),
                "examples": [
                    "500 000 FCFA à 30 % sur 18 mois : remboursement total 673 000 FCFA",
                    "Même montant épargné en tontine sur 18 mois : 0 FCFA d'intérêts",
                    "Microfinance Advans CI : 18 % vs banque classique : 28 % — comparez avant",
                ],
                "actions": [
                    "Avant tout crédit : posez la question 'puis-je attendre 3 mois et payer cash ?'",
                    "Tontine ou épargne forcée Mobile Money = alternative au crédit pour les projets",
                    "Si crédit obligatoire : comparez TOUJOURS au moins 3 établissements",
                ],
                "monthly_saving_example": 10000,
            },
        ],
    },
}

# ── Sélecteur de contexte ─────────────────────────────────────────────────────

def get_tips(currency: str = "EUR") -> dict:
    """Returns the appropriate tips dict based on currency context."""
    return CI_OPTIMIZATION_TIPS if currency == "XOF" else OPTIMIZATION_TIPS


def get_context_label(currency: str) -> dict:
    """Returns UI labels for the current market context."""
    if currency == "XOF":
        return {
            "country": "Côte d'Ivoire",
            "flag": "🇨🇮",
            "meal_restaurant_cost": 3000,
            "meal_home_cost": 600,
            "restaurant_label": "maquis / restaurant",
            "home_label": "repas maison (plats locaux)",
        }
    return {
        "country": "France / Europe",
        "flag": "🇫🇷",
        "meal_restaurant_cost": 16,
        "meal_home_cost": 3.5,
        "restaurant_label": "restaurant / livraison",
        "home_label": "repas préparé maison",
    }


class BudgetOptimizer:

    def __init__(self, profile):
        self.profile = profile
        self._tips = get_tips(getattr(profile, "currency", "EUR"))
        self._ctx = get_context_label(getattr(profile, "currency", "EUR"))

    @property
    def tips(self):
        return self._tips

    @property
    def context(self):
        return self._ctx

    def analyze_category(self, category: str, monthly_amount: float) -> dict:
        """Returns tips with estimated savings for a given category and spend."""
        cat = self._tips.get(category)
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
            "benchmark_pct": cat["benchmark_pct"],
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

    def meal_cost_comparison(self, budget_restaurant: float, budget_groceries: float) -> dict:
        """Detailed food breakdown analysis — adapted to local context."""
        resto_cost = self._ctx["meal_restaurant_cost"]
        home_cost = self._ctx["meal_home_cost"]
        if budget_restaurant > 0:
            meals_count = budget_restaurant / resto_cost
            home_equivalent_cost = meals_count * home_cost
            saving = budget_restaurant - home_equivalent_cost
        else:
            saving = 0
            home_equivalent_cost = 0
            meals_count = 0
        return {
            "restaurant_budget": budget_restaurant,
            "restaurant_meals_count": round(meals_count),
            "home_equivalent_cost": round(home_equivalent_cost),
            "potential_saving": round(max(saving, 0)),
            "groceries_budget": budget_groceries,
            "cost_per_home_meal": home_cost,
            "cost_per_restaurant_meal": resto_cost,
            "restaurant_label": self._ctx["restaurant_label"],
            "home_label": self._ctx["home_label"],
        }
