"""
Wealth Score Dashboard — Proprietary 0–1000 score + detailed breakdown.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.wealth_score import WealthScoreEngine
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(page_title="Wealth Score — Oswald Wealth", page_icon="⭐", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p   = st.session_state.profile
ws  = WealthScoreEngine(p)
result = ws.calculate()
bench  = ws.get_age_benchmark()

st.markdown(f'<div class="hero-banner"><div class="hero-title">⭐ Wealth Score</div><div class="hero-subtitle">Score patrimonial propriétaire — {p.name}</div></div>', unsafe_allow_html=True)

# ---- Score Hero ----
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    score = result["total_score"]
    color = result["color"]
    label = result["label"]
    pct   = result["percentile"]

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": f"{label}<br><span style='font-size:0.9rem;color:#8899BB'>{pct}</span>",
               "font": {"color": "#E8E8E8", "size": 16}},
        gauge={
            "axis": {"range": [0, 1000], "tickcolor": "#8899BB", "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.3},
            "steps": [
                {"range": [0,   250], "color": "rgba(244,67,54,0.12)"},
                {"range": [250, 500], "color": "rgba(255,152,0,0.12)"},
                {"range": [500, 750], "color": "rgba(76,175,80,0.12)"},
                {"range": [750,1000], "color": "rgba(212,175,55,0.12)"},
            ],
            "threshold": {"line": {"color": "#8899BB", "width": 2}, "thickness": 0.8,
                          "value": bench["benchmark"]},
        },
        number={"font": {"color": color, "size": 52}, "suffix": "/1000"},
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", height=300,
        margin=dict(l=30, r=30, t=40, b=0), font=dict(color="#C8D4E8"),
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a: st.metric("Votre score", f"{score}/1000")
    with col_b: st.metric("Benchmark âge", bench["benchmark"])
    with col_c:
        diff = score - bench["benchmark"]
        st.metric("Vs benchmark", f"{diff:+.0f}", f"{'✅ Au-dessus' if diff >= 0 else '⚠️ En dessous'}")

# ---- Score Breakdown ----
st.markdown("---")
st.markdown('<div class="section-header">Détail par Composante</div>', unsafe_allow_html=True)

fig_radar = go.Figure(go.Scatterpolar(
    r=[v["score"] / v["max"] * 100 for v in result["breakdown"].values()],
    theta=list(result["breakdown"].keys()),
    fill="toself",
    line=dict(color="#D4AF37"),
    fillcolor="rgba(212,175,55,0.15)",
    name="Votre score",
))
fig_radar.add_trace(go.Scatterpolar(
    r=[100] * len(result["breakdown"]),
    theta=list(result["breakdown"].keys()),
    line=dict(color="rgba(255,255,255,0.15)"),
    showlegend=False,
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)"),
               angularaxis=dict(gridcolor="rgba(255,255,255,0.1)")),
    paper_bgcolor="rgba(0,0,0,0)", height=380, font=dict(color="#C8D4E8"),
    showlegend=False, margin=dict(l=40,r=40,t=20,b=20),
)

c1, c2 = st.columns([1, 2])
with c1:
    st.plotly_chart(fig_radar, use_container_width=True)
with c2:
    for comp, data in result["breakdown"].items():
        pct   = data["score"] / data["max"] if data["max"] > 0 else 0
        color = data["color"]
        c_a, c_b, c_c = st.columns([2, 4, 1])
        with c_a:
            st.markdown(f"<div style='color:#C8D4E8; padding-top:6px; font-size:0.9rem;'>{comp}</div>", unsafe_allow_html=True)
        with c_b:
            st.progress(pct)
        with c_c:
            st.markdown(f"<div style='color:{color}; font-weight:700; font-size:0.9rem; text-align:center;'>{data['score']:.0f}/{data['max']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.78rem; color:#8899BB; margin:-10px 0 10px 8px;'>{data['note']}</div>", unsafe_allow_html=True)

# ---- Top 3 Improvements ----
st.markdown("---")
st.markdown('<div class="section-header">Top 3 Améliorations Prioritaires</div>', unsafe_allow_html=True)

cols_improve = st.columns(3)
for i, improvement in enumerate(result["top_3_improvements"]):
    with cols_improve[i]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">#{i+1} Priorité</div>
            <div style="font-size:1rem; font-weight:600; color:#D4AF37; margin-top:4px;">{improvement['area']}</div>
            <div style="font-size:0.85rem; color:#C8D4E8; margin-top:8px;">Gap : <strong style="color:#FF9800;">{improvement['gap']:.0f} pts</strong></div>
            <div style="font-size:0.8rem; color:#8899BB; margin-top:4px;">{improvement['note']}</div>
        </div>
        """, unsafe_allow_html=True)

# ---- Score Scale Reference ----
st.markdown("---")
st.markdown('<div class="section-header">Échelle de Référence</div>', unsafe_allow_html=True)
scale = [
    (0, 250, "Financial Reset Needed", "#F44336", "Situation critique — restructuration financière urgente"),
    (250, 500, "Getting Started", "#FF9800", "Base en construction — bons reflexes à ancrer"),
    (500, 700, "Wealth Builder", "#D4AF37", "Trajectoire positive — optimisations disponibles"),
    (700, 850, "Advanced Investor", "#4CAF50", "Excellent — patrimoine structuré et en croissance"),
    (850, 1000, "Elite Wealth Builder", "#9B59B6", "Top 5% — niveau family office"),
]
for lo, hi, label, color, desc in scale:
    current_range = lo <= score <= hi
    bg = "rgba(212,175,55,0.1)" if current_range else "transparent"
    border = f"border:1px solid {color}" if current_range else "border:1px solid rgba(255,255,255,0.05)"
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px; padding:10px 16px; border-radius:8px;
                background:{bg}; {border}; margin-bottom:6px;">
        <div style="min-width:80px; color:{color}; font-weight:700;">{lo}–{hi}</div>
        <div style="min-width:200px; font-weight:600; color:{'#E8E8E8' if current_range else '#8899BB'};">{label}
            {'  ◄ Vous êtes ici' if current_range else ''}
        </div>
        <div style="color:#8899BB; font-size:0.85rem;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
