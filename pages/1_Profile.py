"""
User Profile & Financial Onboarding — ultra-detailed intake form.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.db_manager import DatabaseManager
from models.user_profile import UserProfile
from utils.constants import COUNTRIES, RISK_PROFILES, CURRENCY_SYMBOLS

st.set_page_config(page_title="Profil — Oswald Wealth", page_icon="👤", layout="wide")

with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

db = DatabaseManager()
db.initialize()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.markdown('<div class="hero-banner"><div class="hero-title">👤 Profil Financier</div><div class="hero-subtitle">Votre dossier de banquier privé personnel</div></div>', unsafe_allow_html=True)

# Load existing if any
existing = {}
if st.session_state.user_id:
    existing = db.load_full_profile(st.session_state.user_id)

country_list = list(COUNTRIES.keys())

with st.form("profile_form", clear_on_submit=False):
    # ==== SECTION 1: PERSONAL ====
    st.markdown('<div class="section-header">1. Informations Personnelles</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        name = st.text_input("Votre prénom *", value=existing.get("name", ""), placeholder="Ex: Oswald")
        age  = st.number_input("Âge *", 16, 85, int(existing.get("age", 28)))
    with c2:
        country = st.selectbox("Pays de résidence *", country_list,
                               index=country_list.index(existing.get("country", "France")))
        city    = st.text_input("Ville", value=existing.get("city", ""))
    with c3:
        marital = st.selectbox("Situation matrimoniale", ["Célibataire","En couple","Marié(e)","Divorcé(e)","Veuf/ve"],
                               index=["Célibataire","En couple","Marié(e)","Divorcé(e)","Veuf/ve"].index(existing.get("marital_status","Célibataire")))
        education = st.selectbox("Niveau d'études", ["Lycée","Bac","Bac+2","Bac+3","Bac+5","Doctorat","Autre"],
                                 index=["Lycée","Bac","Bac+2","Bac+3","Bac+5","Doctorat","Autre"].index(existing.get("education_level","Bac+5")))

    currency = COUNTRIES[country]["currency"]
    sym      = CURRENCY_SYMBOLS.get(currency, currency)

    career  = st.text_input("Domaine professionnel", value=existing.get("career_field",""), placeholder="Ex: Finance, IT, Santé, Entrepreneuriat...")
    health  = st.text_area("Notes santé (impact financier potentiel)", value=existing.get("health_notes",""), placeholder="Ex: maladie chronique, besoin mutuelle renforcée...", height=60)

    # ==== SECTION 2: FINANCIAL ====
    st.markdown('<div class="section-header">2. Situation Financière</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        income       = st.number_input(f"Revenu net mensuel ({sym}) *", 0.0, 1_000_000.0, float(existing.get("monthly_income", 3000)), step=100.0)
        side_income  = st.number_input(f"Revenus complémentaires ({sym}/mois)", 0.0, 100_000.0, float(existing.get("side_income", 0)), step=50.0)
        salary_growth = st.slider("Croissance salariale annuelle (%)", 0.0, 15.0, float(existing.get("salary_growth_pct", 2.0) * 100), 0.5) / 100
    with c2:
        expenses     = st.number_input(f"Dépenses mensuelles totales ({sym}) *", 0.0, 500_000.0, float(existing.get("monthly_expenses", 1800)), step=100.0)
        savings      = st.number_input(f"Épargne mensuelle ({sym})", 0.0, 100_000.0, float(existing.get("monthly_savings", 400)), step=50.0)
        debt_pmt     = st.number_input(f"Remboursements dettes/mois ({sym})", 0.0, 50_000.0, float(existing.get("monthly_debt_payment", 0)), step=50.0)
    with c3:
        cur_savings  = st.number_input(f"Épargne liquide actuelle ({sym})", 0.0, 10_000_000.0, float(existing.get("current_savings", 5000)), step=500.0)
        cur_invest   = st.number_input(f"Investissements actuels ({sym})", 0.0, 10_000_000.0, float(existing.get("current_investments", 0)), step=500.0)
        cur_debt     = st.number_input(f"Dette totale encours ({sym})", 0.0, 5_000_000.0, float(existing.get("current_debt", 0)), step=1000.0)
        emergency    = st.number_input(f"Fonds d'urgence ({sym})", 0.0, 1_000_000.0, float(existing.get("emergency_fund", 0)), step=500.0)

    # ==== SECTION 3: LIFESTYLE ====
    st.markdown('<div class="section-header">3. Mode de Vie & Dépenses</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        transport = st.number_input(f"Transport mensuel ({sym})", 0.0, 10_000.0, float(existing.get("transport_monthly", 200)), step=50.0)
        subscriptions = st.number_input(f"Abonnements ({sym}/mois)", 0.0, 2_000.0, float(existing.get("subscriptions_monthly", 50)), step=10.0)
    with c2:
        leisure      = st.number_input(f"Loisirs ({sym}/mois)", 0.0, 10_000.0, float(existing.get("leisure_monthly", 150)), step=50.0)
        travel       = st.number_input(f"Voyages ({sym}/an)", 0.0, 100_000.0, float(existing.get("travel_annual", 1000)), step=100.0)
    with c3:
        luxury       = st.number_input(f"Dépenses luxe ({sym}/mois)", 0.0, 50_000.0, float(existing.get("luxury_monthly", 0)), step=50.0)

    st.markdown("**Auto-évaluation comportementale** *(1 = très faible, 10 = excellent)*")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        discipline   = st.slider("Discipline financière", 1, 10, int(existing.get("discipline_score", 6)))
    with c2:
        emotional    = st.slider("Achats impulsifs (10=jamais)", 1, 10, int(existing.get("emotional_spending", 5)))
    with c3:
        anxiety      = st.slider("Anxiété financière (10=zen)", 1, 10, int(existing.get("financial_anxiety", 5)))
    with c4:
        consistency  = st.slider("Constance sur le long terme", 1, 10, int(existing.get("consistency_score", 6)))

    # ==== SECTION 4: FAMILY ====
    st.markdown('<div class="section-header">4. Projet Familial</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        marriage_age  = st.number_input("Âge souhaité mariage", 18, 70, int(existing.get("desired_marriage_age", 30)))
        first_child   = st.number_input("Âge 1er enfant souhaité", 18, 55, int(existing.get("desired_first_child_age", 32)))
    with c2:
        num_children  = st.slider("Nombre d'enfants souhaité", 0, 6, int(existing.get("num_children", 1)))
        family_support = st.number_input(f"Soutien famille ({sym}/mois)", 0.0, 10_000.0, float(existing.get("family_support_monthly", 0)), step=50.0)
    with c3:
        parents_dep   = st.checkbox("Parents financièrement dépendants", bool(existing.get("parents_dependency", 0)))
        inheritance   = st.number_input(f"Héritage attendu ({sym})", 0.0, 10_000_000.0, float(existing.get("inheritance_expected", 0)), step=1000.0)

    # ==== SECTION 5: REAL ESTATE ====
    st.markdown('<div class="section-header">5. Projet Immobilier</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        wants_prop    = st.checkbox("Souhait d'acheter un bien", bool(existing.get("wants_property", True)))
        target_age    = st.number_input("Âge d'achat cible", 20, 70, int(existing.get("target_purchase_age", 35)))
    with c2:
        prop_value    = st.number_input(f"Valeur du bien cible ({sym})", 0.0, 10_000_000.0, float(existing.get("target_property_value", 250000)), step=5000.0)
        current_rent  = st.number_input(f"Loyer actuel ({sym}/mois)", 0.0, 20_000.0, float(existing.get("current_rent", 800)), step=50.0)
    with c3:
        rent_pref     = st.radio("Préférence", ["Acheter","Louer"], index=["Acheter","Louer"].index(existing.get("rent_vs_buy_pref","Acheter")))
        inv_prop      = st.checkbox("Intérêt pour l'investissement locatif", bool(existing.get("investment_property", 0)))

    # ==== SECTION 6: INVESTING ====
    st.markdown('<div class="section-header">6. Profil Investisseur</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        risk         = st.selectbox("Profil de risque", list(RISK_PROFILES.keys()),
                                    index=list(RISK_PROFILES.keys()).index(existing.get("risk_tolerance","Modéré")))
        knowledge    = st.selectbox("Niveau de connaissance", ["Débutant","Intermédiaire","Avancé","Expert"],
                                   index=["Débutant","Intermédiaire","Avancé","Expert"].index(existing.get("investing_knowledge","Débutant")))
    with c2:
        stocks_pct   = st.slider("Part actions (%)", 0, 100, int(float(existing.get("stocks_pct", 0)) * 100)) / 100
        etf_pct      = st.slider("Part ETF (%)", 0, 100, int(float(existing.get("etf_pct", 0)) * 100)) / 100
    with c3:
        crypto_pct   = st.slider("Part crypto (%)", 0, 100, int(float(existing.get("crypto_pct", 0)) * 100)) / 100

    # ==== SECTION 7: RETIREMENT ====
    st.markdown('<div class="section-header">7. Objectifs Retraite</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        ret_age      = st.number_input("Âge de retraite souhaité", 45, 75, int(existing.get("target_retirement_age", 62)))
    with c2:
        ret_pension  = st.number_input(f"Retraite mensuelle souhaitée ({sym})", 0.0, 50_000.0, float(existing.get("desired_monthly_pension", 2500)), step=100.0)
    with c3:
        ret_lifestyle = st.selectbox("Style de vie retraite", ["Modeste","Confortable","Aisé","Luxueux"],
                                    index=["Modeste","Confortable","Aisé","Luxueux"].index(existing.get("retirement_lifestyle","Confortable")))

    # Submit
    submitted = st.form_submit_button("💾 Sauvegarder le profil", use_container_width=True)

if submitted:
    if not name:
        st.error("Veuillez saisir votre prénom.")
    else:
        user_data = {"name": name, "age": age, "country": country, "city": city,
                     "currency": currency, "marital_status": marital,
                     "education_level": education, "career_field": career, "health_notes": health}
        uid = db.save_profile(user_data)

        db.save_financial(uid, {
            "monthly_income": income, "side_income": side_income,
            "monthly_expenses": expenses, "monthly_savings": savings,
            "salary_growth_pct": salary_growth, "current_savings": cur_savings,
            "current_investments": cur_invest, "current_debt": cur_debt,
            "monthly_debt_payment": debt_pmt, "emergency_fund": emergency,
            "risk_tolerance": risk, "investing_knowledge": knowledge,
            "crypto_pct": crypto_pct, "stocks_pct": stocks_pct, "etf_pct": etf_pct,
        })
        db.save_lifestyle(uid, {
            "transport_monthly": transport, "subscriptions_monthly": subscriptions,
            "leisure_monthly": leisure, "travel_annual": travel, "luxury_monthly": luxury,
            "discipline_score": discipline, "emotional_spending": emotional,
            "financial_anxiety": anxiety, "consistency_score": consistency,
        })
        db.save_family(uid, {
            "desired_marriage_age": marriage_age, "desired_first_child_age": first_child,
            "num_children": num_children, "family_support_monthly": family_support,
            "parents_dependency": int(parents_dep), "inheritance_expected": inheritance,
        })
        db.save_real_estate(uid, {
            "wants_property": int(wants_prop), "target_purchase_age": target_age,
            "target_property_value": prop_value, "rent_vs_buy_pref": rent_pref,
            "investment_property": int(inv_prop), "current_rent": current_rent,
        })
        db.save_retirement(uid, {
            "target_retirement_age": ret_age, "desired_monthly_pension": ret_pension,
            "retirement_lifestyle": ret_lifestyle,
        })

        st.session_state.user_id = uid
        raw = db.load_full_profile(uid)
        st.session_state.profile = UserProfile.from_db(raw)
        st.success(f"✅ Profil de **{name}** sauvegardé. Naviguez vers les analyses dans le menu gauche.")
        st.balloons()
