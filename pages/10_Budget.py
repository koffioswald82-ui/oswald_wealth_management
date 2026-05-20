"""
MON BUDGET — Suivi mensuel simple.
Règle 50/30/20. Respect du budget = rapprochement de l'objectif.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.budget_engine import BudgetEngine, BUDGET_CATEGORIES
from engines.goal_engine import GoalEngine
from utils.constants import RISK_PROFILES
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(page_title="Mon Budget — Oswald Wealth", page_icon="💳", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("👈 Créez votre profil d'abord.")
    st.stop()

p   = st.session_state.profile
bud = BudgetEngine(p)
cur = p.currency
sym = {"EUR":"€","USD":"$","GBP":"£","CHF":"CHF","CAD":"CA$","XOF":"FCFA"}.get(cur, cur)

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">💳 Mon Budget Mensuel</div>
    <div class="hero-subtitle">
        Gérez votre argent simplement. Chaque euro économisé vous rapproche de votre objectif.
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# REVENU AFFICHÉ
# ──────────────────────────────────────────────
st.markdown(f"""
<div style="background:rgba(19,27,46,0.8); border:1px solid rgba(212,175,55,0.2);
            border-radius:12px; padding:16px 24px; margin-bottom:24px; display:inline-block;">
    <span style="color:#8899BB;">Revenu mensuel net : </span>
    <span style="color:#D4AF37; font-size:1.4rem; font-weight:700;">{sym}{p.total_income:,.0f}</span>
    <span style="color:#8899BB; font-size:0.85rem;"> — basé sur votre profil</span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# EXPLICATION 50/30/20
# ──────────────────────────────────────────────
with st.expander("ℹ️ La règle 50/30/20 — Comment ça marche ?"):
    st.markdown(f"""
    C'est la règle la plus simple pour gérer son argent :

    | Catégorie | Pourcentage | Montant pour vous |
    |---|---|---|
    | 🏠 **Besoins essentiels** (loyer, courses, transport…) | 50% | **{sym}{p.total_income*0.50:,.0f}** |
    | 🎯 **Envies & loisirs** (restaurants, shopping, voyages…) | 30% | **{sym}{p.total_income*0.30:,.0f}** |
    | 💰 **Épargne & investissement** | 20% | **{sym}{p.total_income*0.20:,.0f}** |

    Si vous respectez cette règle, vous construisez de la richesse automatiquement.
    """)

# ──────────────────────────────────────────────
# FORMULAIRE DE BUDGET
# ──────────────────────────────────────────────
recommended = bud.recommended_budget()
actual_spending: dict = {}

st.markdown("### Entrez vos dépenses de ce mois")
st.markdown("<div style='color:#8899BB; font-size:0.85rem; margin-bottom:16px;'>Les montants pré-remplis sont des suggestions basées sur votre revenu. Modifiez selon votre réalité.</div>", unsafe_allow_html=True)

for group_name, cats in BUDGET_CATEGORIES.items():
    group_color = "#D4AF37" if "Essentiels" in group_name else ("#4A90D9" if "Envies" in group_name else "#4CAF50")
    st.markdown(f"""
    <div style="border-left:4px solid {group_color}; padding-left:12px; margin:20px 0 12px;">
        <span style="font-size:1.05rem; font-weight:600; color:{group_color};">{group_name}</span>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    cat_list = list(cats.items())

    for i, (cat_name, cat_data) in enumerate(cat_list):
        rec_amount = round(p.total_income * cat_data["pct"])
        with cols[i % 3]:
            val = st.number_input(
                cat_name,
                min_value=0.0,
                max_value=float(p.total_income * 2),
                value=float(rec_amount),
                step=10.0,
                key=f"budget_{cat_name}",
                label_visibility="visible",
            )
            actual_spending[cat_name] = val

# ──────────────────────────────────────────────
# ANALYSE
# ──────────────────────────────────────────────
analysis = bud.analyze_budget(actual_spending)

st.markdown("---")
st.markdown("### 📊 Votre bilan du mois")

# Score global
score = analysis["compliance_score"]
score_color = "#4CAF50" if score >= 75 else ("#D4AF37" if score >= 50 else "#F44336")
score_label_str = "Excellent" if score >= 75 else ("Bon" if score >= 50 else ("À améliorer" if score >= 30 else "Critique"))

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Score budget</div>
        <div class="kpi-value" style="color:{score_color};">{score:.0f}/100</div>
        <div style="color:{score_color}; font-size:0.85rem;">{score_label_str}</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    surplus = analysis["surplus"]
    s_color = "#4CAF50" if surplus >= 0 else "#F44336"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{'Surplus' if surplus >= 0 else 'Déficit'}</div>
        <div class="kpi-value" style="color:{s_color};">{sym}{abs(surplus):,.0f}</div>
        <div style="color:#8899BB; font-size:0.8rem;">ce mois</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    sav_pct = analysis["ratio_savings"]
    sav_color = "#4CAF50" if sav_pct >= 0.18 else ("#D4AF37" if sav_pct >= 0.10 else "#F44336")
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Épargné ce mois</div>
        <div class="kpi-value" style="color:{sav_color};">{sav_pct*100:.0f}%</div>
        <div style="color:#8899BB; font-size:0.8rem;">{sym}{analysis['total_savings']:,.0f} · cible 20%</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    total = analysis["total_actual"]
    t_color = "#4CAF50" if total <= p.total_income else "#F44336"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total dépensé</div>
        <div class="kpi-value" style="color:{t_color};">{sym}{total:,.0f}</div>
        <div style="color:#8899BB; font-size:0.8rem;">sur {sym}{p.total_income:,.0f} de revenu</div>
    </div>
    """, unsafe_allow_html=True)

# Message principal
msg = bud.simple_budget_message(analysis, cur)
if "✅" in msg:
    st.success(msg)
elif "⚠️" in msg:
    st.warning(msg)
else:
    st.error(msg)

# ──────────────────────────────────────────────
# RÉPARTITION 50/30/20
# ──────────────────────────────────────────────
col_gauche, col_droite = st.columns(2)

with col_gauche:
    st.markdown("**Répartition réelle vs recommandée**")

    categories_bar = ["🏠 Besoins", "🎯 Envies", "💰 Épargne"]
    actual_vals = [
        analysis["ratio_essential"] * 100,
        analysis["ratio_lifestyle"] * 100,
        analysis["ratio_savings"]   * 100,
    ]
    target_vals = [50, 30, 20]
    bar_colors  = [
        "#4CAF50" if abs(a - t) <= 5 else ("#FF9800" if abs(a - t) <= 10 else "#F44336")
        for a, t in zip(actual_vals, target_vals)
    ]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Votre répartition",
        x=categories_bar, y=actual_vals,
        marker_color=bar_colors,
        text=[f"{v:.0f}%" for v in actual_vals],
        textposition="outside",
    ))
    fig_bar.add_trace(go.Scatter(
        name="Cible recommandée",
        x=categories_bar, y=target_vals,
        mode="markers+lines",
        line=dict(color="#D4AF37", dash="dash", width=2),
        marker=dict(size=10, color="#D4AF37"),
    ))
    fig_bar.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=300, margin=dict(l=0,r=0,t=20,b=0), font=dict(color="#C8D4E8"),
        yaxis=dict(title="% du revenu", range=[0,70]),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.2),
        showlegend=True,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_droite:
    st.markdown("**Détail par catégorie**")
    for cat, data in analysis["breakdown"].items():
        pct_used = data["pct_used"]
        bar_color = "#4CAF50" if pct_used <= 1.0 else ("#FF9800" if pct_used <= 1.20 else "#F44336")
        c_a, c_b, c_c = st.columns([3, 4, 1])
        with c_a:
            st.markdown(f"<div style='font-size:0.82rem; color:#C8D4E8; padding-top:4px;'>{cat}</div>", unsafe_allow_html=True)
        with c_b:
            st.progress(min(pct_used, 1.5) / 1.5)
        with c_c:
            st.markdown(f"<div style='color:{bar_color}; font-size:0.85rem; font-weight:700;'>{data['status']}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# IMPACT SUR L'OBJECTIF
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎯 Impact sur votre objectif de vie")

opportunities = bud.top_savings_opportunities(actual_spending)
target_wealth_goal = p.desired_monthly_pension * 12 / 0.04
annual_return = RISK_PROFILES.get(p.risk_tolerance, RISK_PROFILES["Modéré"])["expected_return"]

if opportunities:
    st.markdown("**En réduisant ces dépenses, voici ce que vous gagnez :**")
    for opp in opportunities:
        impact = bud.budget_goal_impact(opp["monthly_saving"], target_wealth_goal,
                                         p.target_retirement_age, annual_return)
        st.markdown(f"""
        <div class="insight-card warning" style="margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:600; color:#FF9800;">{opp['category']}</div>
                    <div style="color:#C8D4E8; font-size:0.9rem; margin-top:4px;">
                        Vous dépensez {sym}{opp['actual']:,.0f} · recommandé {sym}{opp['recommended']:,.0f}
                        · écart <strong style="color:#FF9800;">{sym}{opp['monthly_saving']:,.0f}/mois</strong>
                    </div>
                </div>
                <div style="text-align:right; min-width:180px;">
                    <div style="color:#4CAF50; font-weight:700; font-size:1rem;">
                        +{format_currency(impact['future_value'], cur, compact=True)}
                    </div>
                    <div style="color:#8899BB; font-size:0.8rem;">à votre objectif final</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    if analysis["compliance_score"] >= 70:
        st.success("✅ Votre budget est bien optimisé — continuez comme ça !")

# ──────────────────────────────────────────────
# SI SURPLUS — Conseil d'allocation
# ──────────────────────────────────────────────
if analysis["surplus"] > 50:
    goal_eng = GoalEngine(p)
    split = goal_eng._savings_split(analysis["surplus"], p.risk_tolerance)
    st.markdown(f"""
    <div style="background:rgba(76,175,80,0.08); border:1px solid rgba(76,175,80,0.3);
                border-radius:12px; padding:20px; margin-top:16px;">
        <div style="color:#4CAF50; font-weight:600; font-size:1.05rem; margin-bottom:12px;">
            💡 Vous avez {sym}{analysis['surplus']:,.0f} de surplus ce mois — voici comment les placer :
        </div>
    """, unsafe_allow_html=True)
    for vehicle, amount in split.items():
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
            <span style="color:#C8D4E8;">{vehicle}</span>
            <span style="color:#D4AF37; font-weight:700;">{sym}{amount:.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
