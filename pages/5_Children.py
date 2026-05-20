"""
Child Financial Planning — True cost, readiness score, education savings.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.child_planning import ChildPlanningEngine
from utils.formatters import format_currency
from utils.constants import HIGHER_EDUCATION_COSTS
import plotly.graph_objects as go

st.set_page_config(page_title="Enfants — Oswald Wealth", page_icon="👶", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p  = st.session_state.profile
cp = ChildPlanningEngine(p)

st.markdown(f'<div class="hero-banner"><div class="hero-title">👶 Planning Familial</div><div class="hero-subtitle">Coût réel · Score de préparation · Épargne études — {p.name}</div></div>', unsafe_allow_html=True)

if p.num_children == 0:
    st.info("Vous avez indiqué ne pas souhaiter d'enfants. Vous pouvez modifier cela dans votre Profil ou simuler ci-dessous.")

tab1, tab2, tab3 = st.tabs(["💰 Coût Réel", "✅ Score de Préparation", "🎓 Épargne Études"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        num_ch = st.slider("Nombre d'enfants à simuler", 0, 5, max(p.num_children, 1))
        edu_type = st.selectbox("Type d'études envisagé", list(HIGHER_EDUCATION_COSTS.keys()))

    cost_per = cp.total_cost_per_child(edu_type)
    total_all = cp.total_cost_all_children(edu_type)

    with c2:
        kpis = [
            ("Coût 1 enfant (0-22 ans)", format_currency(cost_per["total_cost"], p.currency)),
            ("dont Éducation supérieure", format_currency(cost_per["education_cost"], p.currency)),
            ("dont Vie courante", format_currency(cost_per["living_cost"], p.currency)),
            (f"Coût total {num_ch} enfant(s)", format_currency(total_all, p.currency)),
        ]
        cols = st.columns(2)
        for i, (label, val) in enumerate(kpis):
            with cols[i % 2]:
                st.metric(label, val)

    # Monthly cost by child age chart
    monthly_costs = cost_per["monthly_breakdown"]
    fig_monthly = go.Figure()
    ages   = list(monthly_costs.keys())
    costs  = list(monthly_costs.values())
    colors = ["#F44336" if a < 4 else ("#D4AF37" if a < 12 else ("#4CAF50" if a < 18 else "#4A90D9")) for a in ages]

    fig_monthly.add_trace(go.Bar(
        x=ages, y=costs, marker_color=colors,
        text=[format_currency(c, p.currency) for c in costs],
        textposition="outside",
    ))
    fig_monthly.add_annotation(x=1.5, y=max(costs) * 0.9, text="Crèche/Garde", font=dict(color="#F44336"))
    fig_monthly.add_annotation(x=14, y=max(costs) * 0.9, text="Ado", font=dict(color="#D4AF37"))
    fig_monthly.add_annotation(x=20, y=max(costs) * 0.9, text="Études", font=dict(color="#4A90D9"))

    fig_monthly.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=350, font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=20,b=0),
        xaxis=dict(title="Âge de l'enfant"), yaxis=dict(title=f"Coût mensuel ({p.currency})"),
        title="Coût mensuel d'un enfant par âge",
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Cost breakdown donut
    fig_pie = go.Figure(go.Pie(
        labels=["Vie courante (0-18)", "Études supérieures (18-22)"],
        values=[cost_per["living_cost"], cost_per["education_cost"]],
        hole=0.55,
        marker=dict(colors=["#D4AF37","#4A90D9"]),
    ))
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=260, font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=10,b=0))

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**Répartition des coûts**")
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.markdown("**Averages par phase**")
        phases = [
            ("0-3 ans (crèche)", cost_per["avg_monthly_first_3_years"]),
            ("4-17 ans (scolarité)", cost_per["avg_monthly_school_years"]),
            ("18-22 ans (études)", cost_per["avg_monthly_university"]),
        ]
        for label, val in phases:
            st.metric(label, format_currency(val, p.currency) + "/mois")

with tab2:
    readiness = cp.readiness_score()
    score     = readiness["total_score"]
    color     = "#4CAF50" if score >= 70 else ("#D4AF37" if score >= 50 else "#F44336")

    st.markdown(f"""
    <div style="text-align:center; padding:20px;">
        <div style="font-size:3.5rem; font-weight:700; color:{color};">{score:.0f}/100</div>
        <div style="font-size:1.2rem; color:#E8E8E8; margin-top:8px;">
            {'✅ Financièrement prêt(e)' if readiness['ready'] else '⚠️ Préparation recommandée'}
        </div>
        <div style="font-size:0.95rem; color:#C8D4E8; max-width:600px; margin:12px auto;">
            {readiness['recommendation']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Détail par critère**")
    for criterion, data in readiness["breakdown"].items():
        pct = data["score"] / data["max"] if data["max"] > 0 else 0
        bar_color = "#4CAF50" if pct >= 0.70 else ("#D4AF37" if pct >= 0.40 else "#F44336")
        c1, c2, c3 = st.columns([2, 4, 1])
        with c1:
            st.markdown(f"<div style='color:#C8D4E8; padding-top:4px;'>{criterion}</div>", unsafe_allow_html=True)
        with c2:
            st.progress(pct)
        with c3:
            st.markdown(f"<div style='color:{bar_color}; font-weight:700;'>{data['score']:.0f}/{data['max']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.8rem; color:#8899BB; margin:-12px 0 8px 8px;'>{data['note']}</div>", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    savings_plan = cp.savings_plan_before_child()
    with c1:
        st.metric("Fonds d'urgence cible avant enfant", format_currency(savings_plan["target_emergency_fund"], p.currency))
        st.metric("Gap à combler", format_currency(savings_plan["gap"], p.currency))
    with c2:
        st.metric("Coûts 1ère année supplémentaires", format_currency(savings_plan["first_year_extra_costs"], p.currency))
        st.metric("Mois d'épargne nécessaires", f"{savings_plan['months_to_save']:.0f} mois")

with tab3:
    st.markdown('<div class="section-header">Comparatif Épargne Études</div>', unsafe_allow_html=True)
    edu_df = cp.education_cost_comparison()

    fig_edu = go.Figure()
    fig_edu.add_trace(go.Bar(x=edu_df["Type"], y=edu_df["Coût futur (inflationné)"],
                             name="Coût futur", marker_color="#D4AF37",
                             text=[format_currency(v, p.currency, compact=True) for v in edu_df["Coût futur (inflationné)"]],
                             textposition="outside"))
    fig_edu.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           height=360, font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=20,b=0),
                           xaxis=dict(tickangle=-25), yaxis=dict(title=p.currency),
                           title="Coût des études supérieures (inflationné au départ à 18 ans)")
    st.plotly_chart(fig_edu, use_container_width=True)

    display_edu = edu_df.copy()
    for col in ["Coût actuel","Coût futur (inflationné)","Épargne mensuelle requise"]:
        display_edu[col] = display_edu[col].map(lambda x: format_currency(x, p.currency))
    st.dataframe(display_edu, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">💡</div>
        <div class="insight-text">
            Commencer l'épargne études <strong>dès la naissance</strong> divise la mensualité par {18:.0f}
            (vs 5 ans avant le départ). Les intérêts composés sur 18 ans sont votre meilleur allié.
        </div>
    </div>
    """, unsafe_allow_html=True)
