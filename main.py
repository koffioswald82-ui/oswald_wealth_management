"""
OSWALD WEALTH MANAGEMENT
Your AI Private Banker — Institutional Wealth Intelligence
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from models.user_profile import UserProfile
from engines.wealth_score import WealthScoreEngine
from engines.life_trajectory import LifeTrajectoryEngine
from utils.formatters import format_currency, format_percentage, score_label, color_for_score
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Oswald Wealth Management",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS ---
with open(os.path.join(os.path.dirname(__file__), "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- DB ---
db = DatabaseManager()
db.initialize()

# --- Session State ---
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "profile" not in st.session_state:
    st.session_state.profile = None

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-size:2rem;'>💎</div>
        <div style='font-size:1.1rem; font-weight:700; color:#D4AF37;'>OSWALD WEALTH</div>
        <div style='font-size:0.7rem; color:#8899BB; margin-top:4px;'>Private Banking Intelligence</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    users = db.list_users()
    if users:
        user_names = ["-- Sélectionner --"] + [f"{u['name']} ({u['age']} ans, {u['country']})" for u in users]
        selected = st.selectbox("Profil", user_names, label_visibility="collapsed")
        if selected != "-- Sélectionner --":
            idx = user_names.index(selected) - 1
            uid = users[idx]["id"]
            if st.session_state.user_id != uid:
                st.session_state.user_id = uid
                raw = db.load_full_profile(uid)
                st.session_state.profile = UserProfile.from_db(raw)
    else:
        st.info("Créez votre profil pour commencer.")

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; color:#8899BB; text-align:center;'>v1.0 · Local · Privé</div>", unsafe_allow_html=True)

# ================== MAIN CONTENT ==================

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">💎 Oswald Wealth Management</div>
    <div class="hero-subtitle">Your AI Private Banker — Institutional Wealth Intelligence for Everyone</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.profile is None:
    # Welcome screen for new users
    col1, col2, col3 = st.columns(3)
    features = [
        ("🏦", "Trajectoire Patrimoniale", "Modélisation complète de votre vie financière jusqu'à la retraite"),
        ("📊", "Monte Carlo & MPT", "1000 simulations de marché, optimisation de portefeuille"),
        ("🤖", "IA Coaching", "Conseils personnalisés avec impact chiffré sur votre patrimoine"),
        ("🏡", "Immobilier", "Calcul d'accessibilité, louer vs acheter, investissement locatif"),
        ("👶", "Planning Enfants", "Coût réel, score de préparation, épargne études"),
        ("⚡", "Simulation de Crise", "Test de résilience : chômage, krach, inflation, urgence médicale"),
    ]
    for i, (icon, title, desc) in enumerate(features):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left; margin-bottom:16px;">
                <div style="font-size:1.8rem; margin-bottom:8px;">{icon}</div>
                <div style="font-weight:600; color:#D4AF37; margin-bottom:4px;">{title}</div>
                <div style="font-size:0.85rem; color:#8899BB;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; padding:20px;'>
        <div style='font-size:1.2rem; color:#E8E8E8; margin-bottom:8px;'>
            Commencez par créer votre profil financier
        </div>
        <div style='font-size:0.9rem; color:#8899BB;'>
            👈 Allez dans <strong style='color:#D4AF37;'>Profil</strong> dans le menu de gauche
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    p = st.session_state.profile
    ws = WealthScoreEngine(p).calculate()
    traj_engine = LifeTrajectoryEngine(p)
    traj = traj_engine.build_trajectory()
    ret_ready = traj_engine.retirement_readiness()
    fi_age = traj_engine.calculate_financial_independence_age()

    # KPI Row
    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        ("Patrimoine Net", format_currency(p.current_net_worth, p.currency, compact=True), ""),
        ("Wealth Score", f"{ws['total_score']}/1000", ws["label"]),
        ("Taux d'Épargne", format_percentage(p.net_savings_rate), "cible 20%"),
        ("Retraite", f"{p.target_retirement_age} ans", f"dans {p.years_to_retirement} ans"),
        ("Liberté Financière", f"{fi_age} ans" if fi_age < 99 else "Non calculé", "FIRE age"),
    ]
    for col, (label, value, note) in zip([c1, c2, c3, c4, c5], kpis):
        with col:
            st.metric(label, value, note)

    st.markdown("---")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="section-header">Trajectoire Patrimoniale</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=traj["age"], y=traj["wealth_real"],
            fill="tozeroy", name="Patrimoine réel",
            line=dict(color="#D4AF37", width=2.5),
            fillcolor="rgba(212,175,55,0.12)",
        ))
        # Milestone vertical lines
        for m in traj_engine.get_milestones():
            fig.add_vline(x=m["age"], line_dash="dash", line_color="rgba(212,175,55,0.35)",
                         annotation_text=f"{m['icon']} {m['age']}", annotation_position="top")

        fig.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=320, margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(title="Âge", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title=f"Patrimoine ({p.currency})", gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            font=dict(color="#C8D4E8"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">Wealth Score</div>', unsafe_allow_html=True)
        score = ws["total_score"]
        color = ws["color"]

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": ws["label"], "font": {"color": "#E8E8E8", "size": 13}},
            gauge={
                "axis": {"range": [0, 1000], "tickcolor": "#8899BB"},
                "bar": {"color": color},
                "steps": [
                    {"range": [0,   250], "color": "rgba(244,67,54,0.15)"},
                    {"range": [250, 500], "color": "rgba(255,152,0,0.15)"},
                    {"range": [500, 750], "color": "rgba(76,175,80,0.15)"},
                    {"range": [750,1000], "color": "rgba(212,175,55,0.15)"},
                ],
            },
            number={"font": {"color": color, "size": 36}},
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=220,
            margin=dict(l=20, r=20, t=30, b=0),
            font=dict(color="#C8D4E8"),
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"<div style='text-align:center; color:{color}; font-size:0.9rem;'>{ws['percentile']}</div>", unsafe_allow_html=True)

    # Retirement Readiness
    if ret_ready:
        st.markdown('<div class="section-header">Préparation Retraite</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Corpus projeté", format_currency(ret_ready["wealth_at_retirement"], p.currency, compact=True))
        with c2:
            st.metric("Corpus requis", format_currency(ret_ready["required_corpus"], p.currency, compact=True))
        with c3:
            gap = ret_ready["gap"]
            st.metric("Gap", format_currency(abs(gap), p.currency, compact=True),
                     "✅ Surplus" if gap <= 0 else "⚠️ Déficit")
        with c4:
            st.metric("Retrait max/mois", format_currency(ret_ready["max_monthly_withdrawal"], p.currency))

        progress_val = min(ret_ready["readiness_pct"], 1.0)
        pct_color = "#4CAF50" if progress_val >= 0.80 else ("#D4AF37" if progress_val >= 0.50 else "#F44336")
        st.markdown(f"**Préparation retraite : {progress_val*100:.0f}%**")
        st.progress(progress_val)

    # Milestones
    st.markdown('<div class="section-header">Jalons Financiers Clés</div>', unsafe_allow_html=True)
    milestones = traj_engine.get_milestones()
    cols = st.columns(min(len(milestones), 5))
    for i, m in enumerate(milestones[:5]):
        with cols[i]:
            type_colors = {"current":"#D4AF37","family":"#E8C547","real_estate":"#5CB85C",
                           "wealth":"#4A90D9","retirement":"#9B59B6"}
            c = type_colors.get(m["type"], "#8899BB")
            st.markdown(f"""
            <div style='background:rgba(19,27,46,0.8); border-left:3px solid {c}; border-radius:0 8px 8px 0; padding:12px; margin-bottom:8px;'>
                <div style='font-size:1.4rem;'>{m['icon']}</div>
                <div style='font-size:1.1rem; font-weight:700; color:{c};'>{m['age']} ans</div>
                <div style='font-size:0.8rem; color:#C8D4E8;'>{m['event']}</div>
            </div>
            """, unsafe_allow_html=True)
