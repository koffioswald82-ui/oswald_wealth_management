"""
Timeline de Vie — Votre parcours financier de 18 ans a la retraite.
Etapes de vie adaptatives + tolerance d'epargne flexible.
"""
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.life_stage_engine import LifeStageEngine, LIFE_STAGES
from engines.goal_engine import GoalEngine
from utils.constants import RISK_PROFILES
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(page_title="Timeline de Vie — Oswald Wealth", page_icon="🗺️", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("Creez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
lse = LifeStageEngine(p)
eng = GoalEngine(p)
annual_return = RISK_PROFILES.get(p.risk_tolerance, RISK_PROFILES["Modéré"])["expected_return"]
target_wealth = p.desired_monthly_pension * 12 / 0.04
required_monthly = eng.required_monthly_savings(target_wealth, p.target_retirement_age, annual_return)

current_stage_name = lse.detect_stage()
current_stage_cfg = lse.get_stage(current_stage_name)
tolerance = lse.savings_tolerance(current_stage_name)

st.markdown(
    '<div class="hero-banner">'
    '<div class="hero-title">🗺️ Ma Timeline de Vie</div>'
    '<div class="hero-subtitle">'
    'Votre parcours financier complet — de l\'etudiant a la retraite. '
    'Chaque etape a ses propres regles.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Etape actuelle ─────────────────────────────────────────
st.markdown("### Vous etes ici")

ic = current_stage_cfg["icon"]
cc = current_stage_cfg["color"]
stage_label = current_stage_cfg.get("label", current_stage_name)
stage_desc = current_stage_cfg["description"]
stage_priority = current_stage_cfg["priority"]
stage_message = current_stage_cfg["message"]
tolerance_note = current_stage_cfg["tolerance_note"]

st.markdown(
    f'<div style="background:rgba(19,27,46,0.9); border:2px solid {cc}; '
    f'border-radius:16px; padding:24px 28px; margin-bottom:24px;">'
    f'<div style="display:flex; align-items:center; gap:14px; margin-bottom:14px;">'
    f'<span style="font-size:2.5rem;">{ic}</span>'
    f'<div>'
    f'<div style="font-size:1.3rem; font-weight:800; color:{cc};">{stage_label}</div>'
    f'<div style="color:#C8D4E8; font-size:0.95rem;">{stage_desc}</div>'
    f'</div>'
    f'</div>'
    f'<div style="color:#8899BB; font-size:0.92rem; font-style:italic; '
    f'border-left:3px solid {cc}; padding-left:12px; margin-bottom:12px;">'
    f'{stage_message}'
    f'</div>'
    f'<div style="color:#C8D4E8; font-size:0.88rem;">'
    f'<strong style="color:{cc};">Priorite :</strong> {stage_priority}'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Fourchette d'epargne adaptee ──────────────────────────
st.markdown("### Votre fourchette d'epargne pour cette etape")
st.markdown(
    f'<div style="background:rgba(19,27,46,0.7); border-radius:10px; '
    f'padding:12px 16px; color:#8899BB; font-size:0.88rem; margin-bottom:16px;">'
    f'{tolerance_note}'
    f'</div>',
    unsafe_allow_html=True,
)

bands = [
    ("🎯 Ideal",   tolerance["ideal_amount"], tolerance["ideal_pct"], "#4CAF50"),
    ("✅ Bien",    tolerance["ok_amount"],    tolerance["ok_pct"],    "#D4AF37"),
    ("⚠️ Minimum", tolerance["min_amount"],   tolerance["min_pct"],   "#FF9800"),
]

band_cols = st.columns(3)
for i, (band_label, band_amt, band_pct, band_color) in enumerate(bands):
    with band_cols[i]:
        is_current = False
        current_savings = tolerance["current"]
        ok_amt = tolerance["ok_amount"]
        min_amt = tolerance["min_amount"]
        ideal_amt = tolerance["ideal_amount"]
        if i == 0 and current_savings >= ideal_amt:
            is_current = True
        elif i == 1 and ok_amt <= current_savings < ideal_amt:
            is_current = True
        elif i == 2 and min_amt <= current_savings < ok_amt:
            is_current = True

        border_style = f"border:2px solid {band_color}" if is_current else "border:1px solid rgba(255,255,255,0.08)"
        you_badge = (
            f'<div style="color:{band_color}; font-size:0.75rem; '
            f'font-weight:700; margin-top:4px;">← Vous etes ici</div>'
            if is_current else ""
        )
        pct_display = str(round(band_pct * 100)) + "%"
        if band_pct == 0:
            amt_display = "Tout montant positif"
        else:
            amt_display = sym + str(band_amt) + "/mois"
        st.markdown(
            f'<div style="background:rgba(19,27,46,0.8); {border_style}; '
            f'border-radius:12px; padding:16px; text-align:center; margin-bottom:8px;">'
            f'<div style="color:{band_color}; font-weight:700; font-size:0.95rem;">'
            f'{band_label}</div>'
            f'<div style="color:#E8E8E8; font-size:1.2rem; font-weight:800; margin:6px 0;">'
            f'{amt_display}</div>'
            f'<div style="color:#8899BB; font-size:0.78rem;">{pct_display} du revenu</div>'
            f'{you_badge}'
            f'</div>',
            unsafe_allow_html=True,
        )

tol_label = tolerance["label"]
tol_color = tolerance["color"]
st.markdown(
    f'<div style="background:rgba(19,27,46,0.8); border-left:4px solid {tol_color}; '
    f'border-radius:0 10px 10px 0; padding:12px 16px; margin:8px 0;">'
    f'<span style="color:{tol_color}; font-weight:600;">'
    f'Votre situation : {tol_label}'
    f'</span>'
    f'<span style="color:#C8D4E8; font-size:0.88rem;"> — vous epargnez {sym}{tolerance["current"]:,.0f}/mois</span>'
    f'</div>',
    unsafe_allow_html=True,
)

# ── Timeline visuelle ─────────────────────────────────────
st.markdown("---")
st.markdown("### Votre parcours de vie — toutes les etapes")

stages = lse.life_timeline_stages()
age_min = 18
age_max = p.target_retirement_age + 25

fig_timeline = go.Figure()

for row_idx, stage in enumerate(stages):
    s_start = max(stage["start"], age_min)
    s_end   = min(stage["end"],   age_max)
    if s_start >= s_end:
        continue
    is_current = (s_start <= p.age <= s_end)
    opacity = 0.9 if is_current else 0.45
    border_color = stage["color"] if is_current else "rgba(255,255,255,0.1)"

    fig_timeline.add_trace(go.Bar(
        x=[s_end - s_start],
        y=[stage["icon"] + " " + stage["name"]],
        base=s_start,
        orientation="h",
        marker=dict(
            color=stage["color"],
            opacity=opacity,
            line=dict(color=border_color, width=2 if is_current else 0),
        ),
        text=stage["name"] if (s_end - s_start) > 4 else "",
        textposition="inside",
        textfont=dict(color="white", size=11),
        hovertemplate=(
            "<b>" + stage["icon"] + " " + stage["name"] + "</b><br>"
            + str(stage["start"]) + " → " + str(stage["end"]) + " ans<br>"
            + "<extra></extra>"
        ),
        showlegend=False,
    ))

fig_timeline.add_vline(
    x=p.age, line_dash="dash", line_color="#D4AF37", line_width=2.5,
    annotation_text="Aujourd'hui (" + str(p.age) + " ans)",
    annotation_font_color="#D4AF37",
    annotation_position="top right",
)
fig_timeline.add_vline(
    x=p.target_retirement_age, line_dash="dot", line_color="#4CAF50", line_width=2,
    annotation_text="Retraite (" + str(p.target_retirement_age) + " ans)",
    annotation_font_color="#4CAF50",
    annotation_position="top left",
)

fig_timeline.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=320, margin=dict(l=160, r=20, t=20, b=30),
    xaxis=dict(title="Age", range=[age_min, age_max], gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(0,0,0,0)"),
    font=dict(color="#C8D4E8"),
    barmode="overlay",
)
st.plotly_chart(fig_timeline, use_container_width=True)

# ── Trajectoire financiere par etape ──────────────────────
st.markdown("---")
st.markdown("### Votre trajectoire financiere")

df = eng.trajectory_dataframe(target_wealth, p.target_retirement_age, annual_return, required_monthly)

fig_wealth = go.Figure()
fig_wealth.add_trace(go.Scatter(
    x=df["Age"], y=df["Patrimoine"],
    fill="tozeroy", name="Votre patrimoine",
    line=dict(color="#D4AF37", width=2.5),
    fillcolor="rgba(212,175,55,0.10)",
))
fig_wealth.add_hline(
    y=target_wealth, line_dash="dash", line_color="#4CAF50", line_width=2,
    annotation_text="Objectif : " + format_currency(target_wealth, cur, compact=True),
    annotation_font_color="#4CAF50", annotation_position="top right",
)
fig_wealth.add_vline(
    x=p.age, line_dash="dot", line_color="#D4AF37", opacity=0.6,
    annotation_text="Maintenant",
    annotation_font_color="#D4AF37",
)

# Color bands for life stages on wealth chart
stage_colors_map = {
    "Etudiant": "rgba(74,144,217,0.04)",
    "Debut de carriere": "rgba(212,175,55,0.04)",
    "Stabilisation": "rgba(76,175,80,0.04)",
    "Famille": "rgba(255,152,0,0.04)",
    "Pic de carriere": "rgba(156,39,176,0.04)",
    "Pre-retraite": "rgba(233,30,99,0.04)",
    "Retraite": "rgba(76,175,80,0.04)",
}
for stage in stages:
    s_start = max(stage["start"], p.age)
    s_end   = min(stage["end"], p.target_retirement_age + 5)
    if s_start >= s_end:
        continue
    bg = stage_colors_map.get(stage["name"], "rgba(255,255,255,0.02)")
    fig_wealth.add_vrect(
        x0=s_start, x1=s_end,
        fillcolor=bg, layer="below",
        line_width=0,
    )

fig_wealth.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=360, margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(title="Age", gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(title=cur, gridcolor="rgba(255,255,255,0.05)"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    font=dict(color="#C8D4E8"),
)
st.plotly_chart(fig_wealth, use_container_width=True)

# ── Ce qu'il faut faire a chaque etape ───────────────────
st.markdown("---")
st.markdown("### Ce qu'il faut faire a chaque etape")

stage_cols = st.columns(2)
for idx, (stage_key, stage_data) in enumerate(LIFE_STAGES.items()):
    is_current = (stage_key == current_stage_name)
    border = f"border:2px solid {stage_data['color']}" if is_current else "border:1px solid rgba(255,255,255,0.07)"
    badge = (
        f'<div style="display:inline-block; background:{stage_data["color"]}; '
        f'color:#0A0E1A; font-size:0.7rem; font-weight:700; '
        f'padding:2px 8px; border-radius:99px; margin-bottom:8px;">Votre etape actuelle</div>'
        if is_current else ""
    )

    age_range_text = str(stage_data["age_start"]) + "-" + str(stage_data["age_end"]) + " ans"
    ok_pct_text = str(round(stage_data["savings_ok_pct"] * 100)) + "% d'epargne"
    key_action_1 = stage_data["key_actions"][0] if stage_data["key_actions"] else ""

    actions_html = ""
    for action in stage_data["key_actions"][:3]:
        actions_html += (
            f'<div style="color:#8899BB; font-size:0.8rem; padding:3px 0;">'
            f'• {action}</div>'
        )

    with stage_cols[idx % 2]:
        st.markdown(
            f'<div style="background:rgba(19,27,46,0.8); {border}; '
            f'border-radius:12px; padding:16px; margin-bottom:12px;">'
            f'{badge}'
            f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">'
            f'<span style="font-size:1.4rem;">{stage_data["icon"]}</span>'
            f'<div>'
            f'<div style="font-weight:700; color:{stage_data["color"]}; font-size:0.95rem;">'
            f'{stage_data.get("label", stage_key)}</div>'
            f'<div style="color:#8899BB; font-size:0.75rem;">{age_range_text} · {ok_pct_text}</div>'
            f'</div>'
            f'</div>'
            f'{actions_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Risques par etape actuelle ────────────────────────────
st.markdown("---")
col_risk, col_act = st.columns(2)

with col_risk:
    st.markdown("#### Risques a surveiller a votre etape")
    for risk in current_stage_cfg["key_risks"]:
        st.markdown(
            f'<div style="display:flex; gap:10px; padding:10px 12px; '
            f'background:rgba(244,67,54,0.06); border-left:3px solid #F44336; '
            f'border-radius:0 8px 8px 0; margin-bottom:8px;">'
            f'<span style="color:#F44336;">⚠</span>'
            f'<span style="color:#C8D4E8; font-size:0.88rem;">{risk}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_act:
    st.markdown("#### Actions prioritaires maintenant")
    for i, action in enumerate(current_stage_cfg["key_actions"], 1):
        st.markdown(
            f'<div style="display:flex; gap:10px; padding:10px 12px; '
            f'background:rgba(76,175,80,0.06); border-left:3px solid #4CAF50; '
            f'border-radius:0 8px 8px 0; margin-bottom:8px;">'
            f'<span style="color:#4CAF50; font-weight:800;">{i}.</span>'
            f'<span style="color:#C8D4E8; font-size:0.88rem;">{action}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
