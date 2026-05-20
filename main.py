"""
OSWALD WEALTH MANAGEMENT — Accueil
Page d'accueil simple et orientée objectif.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from models.user_profile import UserProfile
from engines.goal_engine import GoalEngine
from engines.wealth_score import WealthScoreEngine
from utils.constants import RISK_PROFILES
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(
    page_title="Oswald Wealth Management",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open(os.path.join(os.path.dirname(__file__), "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

db = DatabaseManager()
db.initialize()

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px;'>
        <div style='font-size:2rem;'>💎</div>
        <div style='font-size:1.1rem; font-weight:700; color:#D4AF37;'>OSWALD WEALTH</div>
        <div style='font-size:0.7rem; color:#8899BB; margin-top:2px;'>Votre banquier privé IA</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    users = db.list_users()
    if users:
        user_names = ["-- Sélectionner --"] + [f"{u['name']}" for u in users]
        selected = st.selectbox("Mon profil", user_names, label_visibility="visible")
        if selected != "-- Sélectionner --":
            idx = user_names.index(selected) - 1
            uid = users[idx]["id"]
            if st.session_state.user_id != uid:
                st.session_state.user_id = uid
                raw = db.load_full_profile(uid)
                st.session_state.profile = UserProfile.from_db(raw)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem; color:#8899BB;'>
        <div style='margin-bottom:6px;'>📌 Pages disponibles :</div>
        <div>🎯 Mon Objectif</div>
        <div>👤 Profil</div>
        <div>📈 Trajectoire</div>
        <div>💼 Investissements</div>
        <div>🏡 Immobilier</div>
        <div>👶 Enfants</div>
        <div>⚡ Simulation de Crise</div>
        <div>🔮 Scénarios</div>
        <div>🤖 Coaching IA</div>
        <div>⭐ Wealth Score</div>
        <div>💳 Mon Budget</div>
    </div>
    """, unsafe_allow_html=True)

# ── Contenu principal ─────────────────────────

if st.session_state.profile is None:
    # ── Écran d'accueil pour nouveaux utilisateurs ──
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">💎 Oswald Wealth Management</div>
        <div class="hero-subtitle">
            Votre conseiller financier personnel — Gratuit · Local · Privé
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding:20px 0; font-size:1.1rem; color:#C8D4E8;'>
        Cette application vous aide à <strong style='color:#D4AF37;'>construire de la richesse durablement</strong>,
        même en partant de zéro — comme un banquier privé dans votre poche.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    steps = [
        ("1️⃣", "Créez votre profil", "Renseignez vos revenus, dépenses et objectifs de vie.", "Profil →", "#D4AF37"),
        ("2️⃣", "Fixez votre objectif", "Dites combien vous voulez avoir et à quel âge.", "Mon Objectif →", "#4CAF50"),
        ("3️⃣", "Suivez votre budget", "Gérez vos dépenses et voyez l'impact sur votre objectif.", "Budget →", "#4A90D9"),
    ]
    for col, (num, title, desc, action, color) in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
            <div style="background:rgba(19,27,46,0.8); border:1px solid rgba(212,175,55,0.15);
                        border-radius:12px; padding:24px; text-align:center; height:200px;">
                <div style="font-size:2rem;">{num}</div>
                <div style="font-weight:700; color:{color}; margin:8px 0;">{title}</div>
                <div style="font-size:0.88rem; color:#8899BB; line-height:1.5;">{desc}</div>
                <div style="margin-top:12px; color:{color}; font-size:0.85rem; font-weight:600;">{action}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Ce que la plateforme fait
    st.markdown("<div style='text-align:center; font-size:1.1rem; font-weight:600; color:#E8E8E8; margin:8px 0 20px;'>Ce que vous pouvez faire ici</div>", unsafe_allow_html=True)

    features = [
        ("🎯", "Calculer combien épargner chaque mois pour atteindre votre objectif"),
        ("📈", "Voir votre patrimoine croître année par année jusqu'à la retraite"),
        ("💳", "Gérer votre budget mensuel par catégorie (loyer, bouffe, transport…)"),
        ("🏡", "Calculer si vous pouvez acheter un bien immobilier"),
        ("👶", "Savoir si vous êtes prêt(e) financièrement pour un enfant"),
        ("⚡", "Tester la résistance de vos finances en cas de coup dur"),
        ("🤖", "Recevoir des conseils personnalisés avec impact chiffré"),
        ("⭐", "Obtenir votre score patrimonial sur 1000"),
    ]
    cols = st.columns(2)
    for i, (icon, text) in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px; padding:10px 12px;
                        background:rgba(19,27,46,0.5); border-radius:8px; margin-bottom:8px;">
                <span style="font-size:1.2rem;">{icon}</span>
                <span style="color:#C8D4E8; font-size:0.9rem;">{text}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:24px; padding:16px;
                background:rgba(212,175,55,0.08); border-radius:12px;'>
        <div style='color:#D4AF37; font-size:1.1rem; font-weight:600;'>
            👈 Commencez par <strong>Profil</strong> dans le menu à gauche
        </div>
        <div style='color:#8899BB; font-size:0.85rem; margin-top:4px;'>
            2 minutes suffisent pour créer votre profil et voir votre plan personnalisé
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Tableau de bord pour utilisateur existant ──
    p   = st.session_state.profile
    cur = p.currency
    sym = {"EUR":"€","USD":"$","GBP":"£","CHF":"CHF","CAD":"CA$","XOF":"FCFA"}.get(cur, cur)

    st.markdown(f"""
    <div class="hero-banner">
        <div style="font-size:1rem; color:#8899BB; margin-bottom:6px;">Bonjour {p.name} 👋</div>
        <div class="hero-title">💎 Tableau de Bord</div>
        <div class="hero-subtitle">Voici l'état de votre patrimoine aujourd'hui</div>
    </div>
    """, unsafe_allow_html=True)

    # Calculer l'objectif et la progression
    annual_return = RISK_PROFILES.get(p.risk_tolerance, RISK_PROFILES["Modéré"])["expected_return"]
    goal_eng      = GoalEngine(p)
    target_wealth = p.desired_monthly_pension * 12 / 0.04
    required_monthly = goal_eng.required_monthly_savings(target_wealth, p.target_retirement_age, annual_return)
    plan = goal_eng.build_plan(target_wealth, p.target_retirement_age, annual_return, required_monthly)
    ws   = WealthScoreEngine(p).calculate()

    # ── KPIs principaux ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("💰 Patrimoine net", format_currency(p.current_net_worth, cur, compact=True))
    with c2:
        st.metric("🎯 Objectif retraite", format_currency(target_wealth, cur, compact=True))
    with c3:
        on_track = p.monthly_savings >= required_monthly
        st.metric(
            "📅 Épargne mensuelle",
            f"{sym}{p.monthly_savings:,.0f}",
            f"{'✅ En bonne voie' if on_track else f'⚠️ Besoin de {sym}{required_monthly:,.0f}'}",
        )
    with c4:
        st.metric("⭐ Wealth Score", f"{ws['total_score']}/1000", ws["label"])

    # ── Message d'état ──
    progress = plan["progress_pct"]
    if progress >= 0.80:
        msg_color, msg_icon = "#4CAF50", "🎉"
        msg_txt = f"Excellent ! Vous êtes à {progress*100:.0f}% de votre objectif. Continuez comme ça."
    elif progress >= 0.40:
        msg_color, msg_icon = "#D4AF37", "👍"
        msg_txt = f"Bonne progression ! Vous êtes à {progress*100:.0f}% de votre objectif."
    else:
        msg_color, msg_icon = "#FF9800", "💡"
        msg_txt = f"Vous avez démarré votre parcours ({progress*100:.0f}% atteint). Chaque mois compte !"

    st.markdown(f"""
    <div style="background:rgba(19,27,46,0.8); border-left:4px solid {msg_color};
                border-radius:0 12px 12px 0; padding:16px 20px; margin:16px 0; color:#E8E8E8;">
        <span style="font-size:1.3rem;">{msg_icon}</span>
        <span style="margin-left:8px;">{msg_txt}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Barre de progression vers l'objectif ──
    st.markdown(f"""
    <div style="margin:8px 0 4px; display:flex; justify-content:space-between;">
        <span style="color:#8899BB; font-size:0.9rem;">Progression vers {format_currency(target_wealth, cur, compact=True)}</span>
        <span style="color:{msg_color}; font-weight:700;">{progress*100:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(min(progress, 1.0))

    st.markdown("---")

    # ── Deux colonnes : Objectif + Prochaines actions ──
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("#### 📈 Trajectoire vers votre objectif")
        df = goal_eng.trajectory_dataframe(target_wealth, p.target_retirement_age, annual_return, required_monthly)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["Âge"], y=df["Patrimoine"],
            fill="tozeroy", name="Votre patrimoine",
            line=dict(color="#D4AF37", width=2.5),
            fillcolor="rgba(212,175,55,0.10)",
        ))
        fig.add_hline(y=target_wealth, line_dash="dash", line_color="#4CAF50",
                      annotation_text=f"🎯 {format_currency(target_wealth, cur, compact=True)}",
                      annotation_font_color="#4CAF50")
        fig.add_vline(x=p.age, line_dash="dot", line_color="#D4AF37", opacity=0.5)
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=300, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#C8D4E8"),
            xaxis=dict(title="Âge", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title=cur, gridcolor="rgba(255,255,255,0.05)"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("#### ✅ Vos prochaines actions")
        actions = []

        if p.emergency_fund < p.monthly_expenses * 3:
            actions.append(("🛡️", "Constituez un fonds d'urgence", f"Objectif : {sym}{p.monthly_expenses*6:,.0f} (6 mois de dépenses)", "#F44336"))

        if p.net_savings_rate < 0.10:
            actions.append(("💰", "Augmentez votre épargne", f"Passez à au moins {sym}{p.total_income*0.10:,.0f}/mois (10% du revenu)", "#FF9800"))

        if p.current_investments < p.total_income * 3:
            actions.append(("📈", "Commencez à investir", "Ouvrez un PEA ou compte-titres et achetez un ETF World", "#D4AF37"))

        if not actions:
            actions.append(("⭐", "Continuez sur cette lancée !", "Votre situation financière est sur la bonne voie.", "#4CAF50"))

        if p.monthly_savings < required_monthly:
            actions.insert(0, ("🎯", "Renforcez votre épargne mensuelle",
                               f"Il vous faut {sym}{required_monthly:,.0f}/mois pour atteindre votre objectif",
                               "#FF9800"))

        for icon, title, desc, color in actions[:4]:
            st.markdown(f"""
            <div style="background:rgba(19,27,46,0.7); border-left:3px solid {color};
                        border-radius:0 8px 8px 0; padding:12px 14px; margin-bottom:10px;">
                <div style="color:{color}; font-weight:600; font-size:0.9rem;">{icon} {title}</div>
                <div style="color:#8899BB; font-size:0.82rem; margin-top:4px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(76,175,80,0.08); border:1px solid rgba(76,175,80,0.2);
                    border-radius:8px; padding:12px; text-align:center; margin-top:8px;">
            <div style="color:#8899BB; font-size:0.8rem;">Vos intérêts cette année</div>
            <div style="color:#4CAF50; font-size:1.5rem; font-weight:700;">
                +{format_currency(plan['interest_this_year'], cur, compact=True)}
            </div>
            <div style="color:#8899BB; font-size:0.75rem;">votre argent travaille pour vous</div>
        </div>
        """, unsafe_allow_html=True)
