"""
Priorisation des Objectifs — Gerez plusieurs projets de vie en parallele.
Allocation dynamique, conflits detectes, ordre optimal, impact sur chaque objectif.
"""
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.goal_engine import GoalEngine
from utils.formatters import format_currency
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Objectifs Multiples — Oswald Wealth",
    page_icon="🎯",
    layout="wide",
)
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("Créez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
eng = GoalEngine(p)

st.markdown(
    '<div class="hero-banner">'
    '<div class="hero-title">🎯 Mes Objectifs de Vie</div>'
    '<div class="hero-subtitle">'
    "Gérez plusieurs projets en même temps — maison, études, retraite, voyage... "
    "et voyez l'impact de chaque euro alloué."
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Session state init ────────────────────────────────────────
if "goals_list" not in st.session_state:
    st.session_state.goals_list = [
        {
            "name": "Retraite",
            "icon": "🏖️",
            "target": round(p.desired_monthly_pension * 12 / 0.04),
            "years": max(1, p.target_retirement_age - p.age),
            "priority": 1,
            "color": "#D4AF37",
        },
    ]

goals = st.session_state.goals_list

# ── Sidebar: budget disponible ────────────────────────────────
monthly_income = p.monthly_income or 3000
monthly_savings_available = p.monthly_savings or 0

st.sidebar.markdown("### Budget épargne disponible")
budget = st.sidebar.number_input(
    "Épargne mensuelle totale disponible",
    min_value=0,
    max_value=int(monthly_income),
    value=int(monthly_savings_available),
    step=50,
    help="Combien pouvez-vous épargner en tout chaque mois ?",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Ajouter un objectif")

GOAL_PRESETS = {
    "Personnalisé": ("✏️", "#8899BB"),
    "Achat immobilier": ("🏠", "#4CAF50"),
    "Fond d'urgence": ("🛡️", "#2196F3"),
    "Études / Formation": ("🎓", "#9C27B0"),
    "Voyage / Sabbatique": ("✈️", "#00BCD4"),
    "Voiture": ("🚗", "#FF9800"),
    "Mariage": ("💍", "#E91E63"),
    "Enfants": ("👶", "#FF5722"),
    "Création d'entreprise": ("🚀", "#607D8B"),
    "Retraite": ("🏖️", "#D4AF37"),
    "Autre": ("⭐", "#78909C"),
}

with st.sidebar.form("add_goal_form", clear_on_submit=True):
    preset = st.selectbox("Type d'objectif", list(GOAL_PRESETS.keys()))
    goal_name = st.text_input("Nom", placeholder="Ex: Achat appartement")
    goal_target = st.number_input("Montant cible", min_value=100, max_value=5_000_000, value=20_000, step=500)
    goal_years = st.number_input("Dans combien d'années ?", min_value=1, max_value=40, value=5)
    goal_priority = st.selectbox("Priorité", [1, 2, 3, 4, 5], index=1,
                                  help="1 = plus prioritaire, 5 = moins urgent")
    add_btn = st.form_submit_button("➕ Ajouter", use_container_width=True)

    if add_btn and goal_name.strip():
        icon, color = GOAL_PRESETS[preset]
        st.session_state.goals_list.append({
            "name": goal_name.strip(),
            "icon": icon,
            "target": goal_target,
            "years": goal_years,
            "priority": goal_priority,
            "color": color,
        })
        st.rerun()

if not goals:
    st.info("Ajoutez au moins un objectif dans la barre latérale.")
    st.stop()

# ── Calculs par objectif ──────────────────────────────────────
annual_return = 0.05  # conservative default

def required_monthly(target, years, rate=annual_return):
    r_m = (1 + rate) ** (1 / 12) - 1
    n = years * 12
    if r_m > 0 and n > 0:
        return target * r_m / ((1 + r_m) ** n - 1)
    return target / max(n, 1)

def future_value(monthly, years, rate=annual_return):
    r_m = (1 + rate) ** (1 / 12) - 1
    n = years * 12
    if r_m > 0:
        return monthly * ((1 + r_m) ** n - 1) / r_m
    return monthly * n

# Enrich goals with computed fields
enriched = []
for g in sorted(goals, key=lambda x: x["priority"]):
    req = required_monthly(g["target"], g["years"])
    enriched.append({**g, "required_monthly": req})

total_required = sum(g["required_monthly"] for g in enriched)
budget_remaining = budget

# Allocate budget in priority order (waterfall)
alloc_results = []
for g in enriched:
    alloc = min(g["required_monthly"], budget_remaining)
    budget_remaining = max(budget_remaining - alloc, 0)
    funded_pct = alloc / g["required_monthly"] * 100 if g["required_monthly"] > 0 else 100
    fv_alloc = future_value(alloc, g["years"])
    shortfall_monthly = max(g["required_monthly"] - alloc, 0)
    shortfall_total = g["target"] - fv_alloc
    extra_years = 0
    if shortfall_monthly > 0 and alloc > 0:
        # how many extra years to reach goal at current alloc
        r_m = (1 + annual_return) ** (1 / 12) - 1
        if r_m > 0:
            import math
            ratio = g["target"] * r_m / alloc + 1
            if ratio > 0:
                extra_years = max(0, math.log(ratio) / math.log(1 + r_m) / 12 - g["years"])

    alloc_results.append({
        **g,
        "alloc": alloc,
        "funded_pct": funded_pct,
        "fv_alloc": fv_alloc,
        "shortfall_monthly": shortfall_monthly,
        "shortfall_total": max(shortfall_total, 0),
        "extra_years": round(extra_years, 1),
    })

conflict = total_required > budget

# ── KPI row ───────────────────────────────────────────────────
st.markdown("### Vue d'ensemble")
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Objectifs actifs</div>'
        f'<div class="metric-value">{len(goals)}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Besoin mensuel total</div>'
        f'<div class="metric-value">{sym}{total_required:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with k3:
    budget_color = "#4CAF50" if not conflict else "#F44336"
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Budget disponible</div>'
        f'<div class="metric-value" style="color:{budget_color};">{sym}{budget:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with k4:
    surplus = budget - total_required
    surplus_color = "#4CAF50" if surplus >= 0 else "#F44336"
    surplus_label = "Surplus mensuel" if surplus >= 0 else "Déficit mensuel"
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">{surplus_label}</div>'
        f'<div class="metric-value" style="color:{surplus_color};">{sym}{abs(surplus):,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Conflit alert ─────────────────────────────────────────────
if conflict:
    st.markdown(
        f'<div style="background:rgba(244,67,54,0.08); border:1px solid #F44336; '
        f'border-radius:12px; padding:16px 20px; margin:16px 0;">'
        f'<div style="color:#F44336; font-weight:700; font-size:1rem; margin-bottom:6px;">'
        f'⚠️ Conflit budgétaire détecté</div>'
        f'<div style="color:#C8D4E8; font-size:0.88rem;">'
        f'Vos objectifs nécessitent <strong>{sym}{total_required:,.0f}/mois</strong> '
        f'mais vous n\'avez que <strong>{sym}{budget:,.0f}/mois</strong>. '
        f'Il manque <strong>{sym}{total_required - budget:,.0f}/mois</strong>. '
        f'Les objectifs moins prioritaires seront partiellement financés.'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<div style="background:rgba(76,175,80,0.08); border:1px solid #4CAF50; '
        f'border-radius:12px; padding:14px 20px; margin:16px 0;">'
        f'<div style="color:#4CAF50; font-weight:700;">✅ Budget suffisant</div>'
        f'<div style="color:#C8D4E8; font-size:0.88rem;">'
        f'Votre budget couvre tous vos objectifs. '
        f'Surplus de {sym}{surplus:,.0f}/mois disponible.'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Objectifs cards ───────────────────────────────────────────
st.markdown("---")
st.markdown("### Mes objectifs — allocation et progression")

for i, g in enumerate(alloc_results):
    funded_pct = g["funded_pct"]
    bar_color = g["color"] if funded_pct >= 100 else ("#FF9800" if funded_pct >= 50 else "#F44336")
    status_icon = "✅" if funded_pct >= 100 else ("⚠️" if funded_pct >= 50 else "❌")
    status_text = "Entièrement financé" if funded_pct >= 100 else (
        f"Partiellement financé ({funded_pct:.0f}%)" if funded_pct > 0 else "Non financé"
    )

    pct_bar_width = min(funded_pct, 100)
    extra_note = ""
    if g["extra_years"] > 0.5:
        extra_note = f" (+{g['extra_years']:.1f} ans supplémentaires au rythme actuel)"

    col_card, col_del = st.columns([11, 1])
    with col_card:
        st.markdown(
            f'<div style="background:rgba(19,27,46,0.85); border:1px solid rgba(255,255,255,0.08); '
            f'border-left:4px solid {g["color"]}; border-radius:12px; padding:18px 20px; margin-bottom:12px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">'
            f'<div style="display:flex; align-items:center; gap:10px;">'
            f'<span style="font-size:1.8rem;">{g["icon"]}</span>'
            f'<div>'
            f'<div style="font-size:1rem; font-weight:700; color:#E8E8E8;">{g["name"]}</div>'
            f'<div style="color:#8899BB; font-size:0.78rem;">Priorité {g["priority"]} · Dans {g["years"]} an{"s" if g["years"] > 1 else ""}</div>'
            f'</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div style="font-size:1.1rem; font-weight:800; color:{g["color"]};">{sym}{g["target"]:,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.75rem;">objectif cible</div>'
            f'</div>'
            f'</div>'
            # Progress bar
            f'<div style="background:rgba(255,255,255,0.06); border-radius:99px; height:8px; margin-bottom:10px;">'
            f'<div style="background:{bar_color}; width:{pct_bar_width:.0f}%; height:8px; border-radius:99px; '
            f'transition:width 0.4s;"></div>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">'
            f'<div style="color:#C8D4E8; font-size:0.82rem;">'
            f'{status_icon} {status_text}{extra_note}'
            f'</div>'
            f'<div style="display:flex; gap:16px;">'
            f'<div style="font-size:0.8rem; color:#8899BB;">'
            f'Besoin: <span style="color:#C8D4E8;">{sym}{g["required_monthly"]:,.0f}/mois</span>'
            f'</div>'
            f'<div style="font-size:0.8rem; color:#8899BB;">'
            f'Alloué: <span style="color:{bar_color}; font-weight:600;">{sym}{g["alloc"]:,.0f}/mois</span>'
            f'</div>'
            f'<div style="font-size:0.8rem; color:#8899BB;">'
            f'Valeur finale: <span style="color:{g["color"]};">{sym}{g["fv_alloc"]:,.0f}</span>'
            f'</div>'
            f'</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col_del:
        if st.button("✕", key=f"del_goal_{i}", help="Supprimer cet objectif"):
            st.session_state.goals_list = [
                x for j, x in enumerate(st.session_state.goals_list) if j != i
            ]
            st.rerun()

# ── Visualisation allocation ──────────────────────────────────
st.markdown("---")
st.markdown("### Répartition de votre épargne")

col_pie, col_bar = st.columns(2)

with col_pie:
    labels = [g["name"] for g in alloc_results] + (["Non alloué"] if surplus > 0 else [])
    values = [g["alloc"] for g in alloc_results] + ([surplus] if surplus > 0 else [])
    colors = [g["color"] for g in alloc_results] + (["#2a3a5a"] if surplus > 0 else [])

    fig_pie = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color="#0A0E1A", width=2)),
        textfont=dict(color="white", size=12),
        hovertemplate="%{label}<br>%{value:.0f} " + cur + "/mois<br>%{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#C8D4E8", size=11)),
        font=dict(color="#C8D4E8"),
        title=dict(text="Allocation mensuelle", font=dict(color="#C8D4E8", size=13)),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    fig_bar = go.Figure()
    for g in alloc_results:
        fig_bar.add_trace(go.Bar(
            name=g["name"],
            x=[g["name"]],
            y=[g["required_monthly"]],
            marker_color="rgba(255,255,255,0.10)",
            showlegend=False,
            hovertemplate=f"Besoin: {sym}{g['required_monthly']:,.0f}/mois<extra></extra>",
        ))
        fig_bar.add_trace(go.Bar(
            name=g["name"],
            x=[g["name"]],
            y=[g["alloc"]],
            marker_color=g["color"],
            text=f"{sym}{g['alloc']:,.0f}",
            textposition="outside",
            textfont=dict(color=g["color"], size=10),
            showlegend=False,
            hovertemplate=f"Alloué: {sym}{g['alloc']:,.0f}/mois<extra></extra>",
        ))

    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        barmode="overlay",
        margin=dict(l=0, r=0, t=30, b=0),
        height=280,
        yaxis=dict(title=f"{cur}/mois", gridcolor="rgba(255,255,255,0.05)"),
        font=dict(color="#C8D4E8"),
        title=dict(text="Besoin vs Alloué (barres grises = besoin total)", font=dict(color="#C8D4E8", size=13)),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Scénarios trade-off ───────────────────────────────────────
st.markdown("---")
st.markdown("### Et si je changeais mes priorités ?")
st.markdown(
    '<div style="color:#8899BB; font-size:0.88rem; margin-bottom:16px;">'
    "Voyez l'impact concret de chaque arbitrage — quel objectif sacrifier pour booster un autre ?"
    "</div>",
    unsafe_allow_html=True,
)

if len(goals) < 2:
    st.info("Ajoutez au moins 2 objectifs pour voir les scénarios de trade-off.")
else:
    focus_names = [g["name"] for g in alloc_results]
    focus_goal = st.selectbox(
        "Je veux maximiser cet objectif :",
        focus_names,
        key="tradeoff_focus",
    )
    sacrifice_options = [n for n in focus_names if n != focus_goal]
    sacrifice_goal = st.selectbox(
        "En réduisant cet objectif :",
        sacrifice_options,
        key="tradeoff_sacrifice",
    )

    focus_data = next(g for g in alloc_results if g["name"] == focus_goal)
    sacrifice_data = next(g for g in alloc_results if g["name"] == sacrifice_goal)

    transfer_max = int(sacrifice_data["alloc"])
    if transfer_max > 0:
        transfer = st.slider(
            f"Montant mensuel à transférer de « {sacrifice_goal} » vers « {focus_goal} »",
            min_value=0,
            max_value=transfer_max,
            value=min(int(sacrifice_data["shortfall_monthly"]) if sacrifice_data["shortfall_monthly"] == 0 else transfer_max // 2, transfer_max),
            step=10,
        )

        new_focus_alloc = focus_data["alloc"] + transfer
        new_sacrifice_alloc = sacrifice_data["alloc"] - transfer

        new_focus_fv = future_value(new_focus_alloc, focus_data["years"])
        new_focus_pct = new_focus_fv / focus_data["target"] * 100 if focus_data["target"] > 0 else 0
        new_sacrifice_fv = future_value(new_sacrifice_alloc, sacrifice_data["years"])
        new_sacrifice_pct = new_sacrifice_fv / sacrifice_data["target"] * 100 if sacrifice_data["target"] > 0 else 0

        tc1, tc2 = st.columns(2)
        with tc1:
            delta_fv = new_focus_fv - focus_data["fv_alloc"]
            delta_sign = "+" if delta_fv >= 0 else ""
            st.markdown(
                f'<div style="background:rgba(76,175,80,0.08); border:1px solid #4CAF50; '
                f'border-radius:12px; padding:16px; text-align:center;">'
                f'<div style="color:#4CAF50; font-weight:700; font-size:0.9rem; margin-bottom:6px;">'
                f'{focus_data["icon"]} {focus_goal} — BOOSTÉ</div>'
                f'<div style="color:#E8E8E8; font-size:1.2rem; font-weight:800;">'
                f'{sym}{new_focus_alloc:,.0f}/mois</div>'
                f'<div style="color:#8899BB; font-size:0.78rem; margin:4px 0;">'
                f'Valeur finale : {sym}{new_focus_fv:,.0f} ({new_focus_pct:.0f}% de l\'objectif)</div>'
                f'<div style="color:#4CAF50; font-size:0.8rem;">'
                f'{delta_sign}{sym}{delta_fv:,.0f} de plus</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with tc2:
            delta_fv2 = new_sacrifice_fv - sacrifice_data["fv_alloc"]
            delta_sign2 = "+" if delta_fv2 >= 0 else ""
            st.markdown(
                f'<div style="background:rgba(244,67,54,0.08); border:1px solid #F44336; '
                f'border-radius:12px; padding:16px; text-align:center;">'
                f'<div style="color:#F44336; font-weight:700; font-size:0.9rem; margin-bottom:6px;">'
                f'{sacrifice_data["icon"]} {sacrifice_goal} — RÉDUIT</div>'
                f'<div style="color:#E8E8E8; font-size:1.2rem; font-weight:800;">'
                f'{sym}{new_sacrifice_alloc:,.0f}/mois</div>'
                f'<div style="color:#8899BB; font-size:0.78rem; margin:4px 0;">'
                f'Valeur finale : {sym}{new_sacrifice_fv:,.0f} ({new_sacrifice_pct:.0f}% de l\'objectif)</div>'
                f'<div style="color:#F44336; font-size:0.8rem;">'
                f'{delta_sign2}{sym}{delta_fv2:,.0f}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info(f"« {sacrifice_goal} » n'a pas de budget alloué à transférer.")

# ── Recommandations intelligentes ────────────────────────────
st.markdown("---")
st.markdown("### Recommandations")

reco_items = []

if conflict:
    gap = total_required - budget
    reco_items.append((
        "💡",
        f"Pour financer tous vos objectifs, il vous faudrait {sym}{gap:,.0f}/mois supplémentaires.",
        "#FF9800",
    ))
    non_funded = [g for g in alloc_results if g["funded_pct"] < 50]
    if non_funded:
        names = ", ".join(g["name"] for g in non_funded)
        reco_items.append((
            "⚠️",
            f"Les objectifs suivants sont insuffisamment financés : {names}. "
            f"Envisagez d'allonger leur horizon ou de réduire leur cible.",
            "#F44336",
        ))

if surplus > 0:
    reco_items.append((
        "✅",
        f"Vous avez {sym}{surplus:,.0f}/mois non alloués. Redirigez-les vers votre objectif le plus prioritaire ou votre fond d'urgence.",
        "#4CAF50",
    ))

long_goals = [g for g in alloc_results if g["years"] >= 15 and g["funded_pct"] < 80]
if long_goals:
    reco_items.append((
        "📈",
        "Pour les objectifs à long terme (15+ ans), même une légère augmentation mensuelle aujourd'hui crée un effet de capitalisation massif.",
        "#D4AF37",
    ))

short_goals = [g for g in alloc_results if g["years"] <= 2 and g["funded_pct"] < 100]
if short_goals:
    names = ", ".join(g["name"] for g in short_goals)
    reco_items.append((
        "⏰",
        f"Objectifs urgents non entièrement financés : {names}. Priorisez ces objectifs avant les autres.",
        "#2196F3",
    ))

if not reco_items:
    reco_items.append((
        "🎉",
        "Bravo ! Votre plan d'épargne couvre tous vos objectifs à temps. Continuez ainsi.",
        "#4CAF50",
    ))

for icon, text, color in reco_items:
    st.markdown(
        f'<div style="display:flex; gap:12px; padding:12px 16px; '
        f'background:rgba(19,27,46,0.7); border-left:3px solid {color}; '
        f'border-radius:0 10px 10px 0; margin-bottom:8px;">'
        f'<span style="font-size:1.1rem;">{icon}</span>'
        f'<span style="color:#C8D4E8; font-size:0.88rem;">{text}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
