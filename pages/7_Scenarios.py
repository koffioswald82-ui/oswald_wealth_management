"""
Life Scenario Comparison — Compare multiple financial life paths.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.scenario_simulation import ScenarioSimulationEngine
from utils.formatters import format_currency
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Scénarios — Oswald Wealth", page_icon="🔮", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p   = st.session_state.profile
sim = ScenarioSimulationEngine(p)

st.markdown(f'<div class="hero-banner"><div class="hero-title">🔮 Simulation de Scénarios</div><div class="hero-subtitle">Comparez vos futurs financiers possibles — {p.name}</div></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Comparaison Standard", "⚙️ Scénarios Personnalisés"])

with tab1:
    scenarios = sim.default_scenario_set()
    results   = sim.compare_scenarios(scenarios)
    comp_df   = sim.build_comparison_dataframe(results)

    # Trajectory chart
    fig = go.Figure()
    scenario_colors = {
        "Scénario A — Base":                  "#D4AF37",
        "Scénario B — Investisseur Discipliné":"#4CAF50",
        "Scénario C — Style de Vie Premium":  "#FF9800",
        "Scénario D — FIRE (Liberté Financière)":"#9B59B6",
    }
    for name, data in results.items():
        traj = data["result"]["trajectory"]
        color = scenario_colors.get(name, "#8899BB")
        fig.add_trace(go.Scatter(
            x=traj["age"], y=traj["wealth_real"],
            name=name, line=dict(color=color, width=2.5),
        ))

    fig.add_vline(x=p.target_retirement_age, line_dash="dash", line_color="#8899BB",
                 annotation_text=f"Retraite {p.target_retirement_age} ans")
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=450, font=dict(color="#C8D4E8"),
        xaxis=dict(title="Âge", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title=f"Patrimoine réel ({p.currency})", gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.12),
        title="Trajectoires Patrimoniales — 4 Futurs Possibles",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Comparison table
    st.markdown('<div class="section-header">Comparatif des Scénarios</div>', unsafe_allow_html=True)
    display = comp_df.copy()
    display["Patrimoine final (réel)"]    = display["Patrimoine final (réel)"].map(lambda x: format_currency(x, p.currency, compact=True))
    display["Retrait mensuel retraite"]   = display["Retrait mensuel retraite"].map(lambda x: format_currency(x, p.currency))
    display["Épargne mensuelle effective"]= display["Épargne mensuelle effective"].map(lambda x: format_currency(x, p.currency))
    display["Score de stress financier"]  = display["Score de stress financier"].map(lambda x: f"{x:.0f}/100")
    st.dataframe(display, use_container_width=True, hide_index=True)

    # Bar chart — final wealth comparison
    fig_bar = go.Figure(go.Bar(
        x=comp_df["Scénario"],
        y=comp_df["Patrimoine final (réel)"],
        marker_color=[scenario_colors.get(s, "#8899BB") for s in comp_df["Scénario"]],
        text=[format_currency(v, p.currency, compact=True) for v in comp_df["Patrimoine final (réel)"]],
        textposition="outside",
    ))
    fig_bar.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=360, font=dict(color="#C8D4E8"),
        xaxis=dict(tickangle=-15), yaxis=dict(title=p.currency),
        title="Patrimoine final à la retraite par scénario",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Stress score chart
    fig_stress = go.Figure(go.Bar(
        x=comp_df["Scénario"],
        y=comp_df["Score de stress financier"].str.replace("/100","").astype(float),
        marker_color=["#4CAF50" if int(str(s).replace("/100","")) < 30 else ("#FF9800" if int(str(s).replace("/100","")) < 60 else "#F44336") for s in comp_df["Score de stress financier"]],
        text=comp_df["Score de stress financier"],
        textposition="outside",
    ))
    fig_stress.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=300, font=dict(color="#C8D4E8"),
        title="Score de Stress Financier (0=serein, 100=critique)",
    )
    st.plotly_chart(fig_stress, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header">Créez Vos Propres Scénarios</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Scénario 1**")
        s1_name    = st.text_input("Nom", "Mon scénario optimiste")
        s1_savings = st.slider("Épargne mensuelle (€)", 0, 10000, int(p.monthly_savings), 100, key="s1s")
        s1_luxury  = st.slider("Luxe mensuel (€)", 0, 5000, int(p.luxury_monthly), 50, key="s1l")
        s1_children = st.slider("Enfants", 0, 5, p.num_children, key="s1c")
        s1_return   = st.slider("Rendement annuel (%)", 1.0, 12.0, 6.5, 0.5, key="s1r") / 100

    with c2:
        st.markdown("**Scénario 2**")
        s2_name    = st.text_input("Nom", "Mon scénario conservateur")
        s2_savings = st.slider("Épargne mensuelle (€)", 0, 10000, max(int(p.monthly_savings) - 200, 0), 100, key="s2s")
        s2_luxury  = st.slider("Luxe mensuel (€)", 0, 5000, min(int(p.luxury_monthly) + 200, 5000), 50, key="s2l")
        s2_children = st.slider("Enfants", 0, 5, min(p.num_children + 1, 5), key="s2c")
        s2_return   = st.slider("Rendement annuel (%)", 1.0, 12.0, 5.0, 0.5, key="s2r") / 100

    if st.button("Comparer ces 2 scénarios", type="primary"):
        custom_scenarios = [
            {"name": s1_name, "description": s1_name, "overrides": {
                "monthly_savings": s1_savings, "luxury_monthly": s1_luxury,
                "num_children": s1_children, "annual_return": s1_return,
            }},
            {"name": s2_name, "description": s2_name, "overrides": {
                "monthly_savings": s2_savings, "luxury_monthly": s2_luxury,
                "num_children": s2_children, "annual_return": s2_return,
            }},
        ]
        custom_results = sim.compare_scenarios(custom_scenarios)

        fig_custom = go.Figure()
        for i, (name, data) in enumerate(custom_results.items()):
            traj  = data["result"]["trajectory"]
            color = ["#D4AF37","#4A90D9"][i]
            fig_custom.add_trace(go.Scatter(
                x=traj["age"], y=traj["wealth_real"], name=name,
                line=dict(color=color, width=3),
                fill="tozeroy" if i == 0 else None,
                fillcolor="rgba(212,175,55,0.08)" if i == 0 else None,
            ))
        fig_custom.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=380, font=dict(color="#C8D4E8"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_custom, use_container_width=True)

        for name, data in custom_results.items():
            r = data["result"]
            st.metric(f"Patrimoine final — {name}",
                     format_currency(r["final_wealth_real"], p.currency, compact=True),
                     f"Stress: {r['financial_stress_score']:.0f}/100")
