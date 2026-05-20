"""
Crisis Simulation — Stress test financial resilience under major shocks.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.crisis_simulation import CrisisSimulationEngine
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(page_title="Simulation de Crise — Oswald Wealth", page_icon="⚡", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p   = st.session_state.profile
crisis = CrisisSimulationEngine(p)

st.markdown(f'<div class="hero-banner"><div class="hero-title">⚡ Simulation de Crise</div><div class="hero-subtitle">Test de résilience financière — Chômage · Crise médicale · Krach · Inflation — {p.name}</div></div>', unsafe_allow_html=True)

# Overall resilience score
resilience = crisis.overall_resilience_score()
res_score  = resilience["total_score"]
res_color  = resilience["color"]

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    fig_res = go.Figure(go.Indicator(
        mode="gauge+number",
        value=res_score,
        title={"text": f"Score de Résilience : {resilience['level']}", "font": {"color": "#E8E8E8", "size": 14}},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": res_color},
            "steps": [
                {"range": [0, 20],  "color": "rgba(244,67,54,0.2)"},
                {"range": [20, 40], "color": "rgba(255,87,34,0.2)"},
                {"range": [40, 60], "color": "rgba(255,152,0,0.2)"},
                {"range": [60, 80], "color": "rgba(76,175,80,0.2)"},
                {"range": [80,100], "color": "rgba(212,175,55,0.2)"},
            ],
        },
        number={"font": {"color": res_color, "size": 42}, "suffix": "/100"},
    ))
    fig_res.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(l=20,r=20,t=30,b=0), font=dict(color="#C8D4E8"))
    st.plotly_chart(fig_res, use_container_width=True)

st.markdown(f"""
<div style="text-align:center; margin-bottom:16px;">
    <span style="color:#FF9800;">Vulnérabilité principale : <strong style="color:{res_color};">{resilience['top_vulnerability']}</strong></span>
</div>
""", unsafe_allow_html=True)

# Breakdown
cols = st.columns(4)
for i, (name, data) in enumerate(resilience["breakdown"].items()):
    with cols[i]:
        pct = data["score"] / data["max"]
        c = "#4CAF50" if pct >= 0.70 else ("#D4AF37" if pct >= 0.40 else "#F44336")
        st.metric(name, f"{data['score']:.0f}/{data['max']}")
        st.progress(pct)

st.markdown("---")

# Individual scenarios
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💼 Chômage", "🏥 Urgence Médicale", "📉 Krach Boursier", "📈 Inflation", "💔 Divorce"])

with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        duration = st.slider("Durée de chômage (mois)", 1, 24, 6)
        replacement = st.slider("Taux d'allocation chômage (%)", 0, 90, 65) / 100

    sim = crisis.simulate_unemployment(duration, replacement)
    with c2:
        color_surv = "#4CAF50" if sim["can_survive"] else "#F44336"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Durée de survie</div>
            <div class="kpi-value" style="color:{color_surv};">{sim['months_survivable']:.1f} mois</div>
            <div class="kpi-delta {'negative' if not sim['can_survive'] else ''}"">
                {'✅ Vous pouvez tenir ' + str(duration) + ' mois' if sim['can_survive'] else '❌ Fonds épuisés avant la fin'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    kpis = [
        ("Revenu de remplacement", format_currency(sim["replacement_income"], p.currency) + "/mois"),
        ("Déficit mensuel", format_currency(sim["monthly_shortfall"], p.currency) + "/mois"),
        ("Cash disponible", format_currency(sim["available_cash"], p.currency)),
        ("Déficit total à fin", format_currency(sim["deficit_at_end"], p.currency)),
        ("Mois de récupération", f"{sim['recovery_months']:.0f} mois"),
        ("Impact patrimoine", format_currency(sim["wealth_impact"], p.currency)),
    ]
    cols = st.columns(3)
    for i, (label, val) in enumerate(kpis):
        with cols[i % 3]:
            st.metric(label, val)

    # Timeline chart
    months_sim = list(range(duration + 1))
    available  = [max(sim["available_cash"] - sim["monthly_shortfall"] * m, 0) for m in months_sim]
    fig_unemp = go.Figure()
    fig_unemp.add_trace(go.Scatter(x=months_sim, y=available, name="Fonds disponibles",
                                    fill="tozeroy", line=dict(color="#D4AF37"), fillcolor="rgba(212,175,55,0.15)"))
    fig_unemp.add_hline(y=0, line_color="#F44336", annotation_text="Zéro — insolvabilité")
    fig_unemp.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             height=280, font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=10,b=0),
                             xaxis=dict(title="Mois"), yaxis=dict(title=p.currency))
    st.plotly_chart(fig_unemp, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        med_cost = st.number_input(f"Coût de l'urgence médicale ({p.currency})", 1000.0, 500_000.0, 20000.0, step=1000.0)
    sim_med = crisis.simulate_medical_emergency(med_cost)
    with c2:
        absorb_color = "#4CAF50" if sim_med["can_absorb"] else "#F44336"
        st.markdown(f"**Verdict : <span style='color:{absorb_color};'>{'✅ Absorbable' if sim_med['can_absorb'] else '❌ Non absorbable'}</span>**", unsafe_allow_html=True)

    kpis_med = [
        ("Coût total", format_currency(sim_med["cost"], p.currency)),
        ("Couverture assurance (estimée 70%)", format_currency(sim_med["insurance_covered"], p.currency)),
        ("À votre charge", format_currency(sim_med["out_of_pocket"], p.currency)),
        ("Fonds disponibles", format_currency(sim_med["available_funds"], p.currency)),
        ("Gap non couvert", format_currency(sim_med["gap"], p.currency)),
        ("Mois de récupération", f"{sim_med['months_to_recover']:.0f} mois"),
    ]
    cols = st.columns(3)
    for i, (label, val) in enumerate(kpis_med):
        with cols[i % 3]:
            st.metric(label, val)

    st.markdown(f"""
    <div class="insight-card {'danger' if not sim_med['can_absorb'] else 'success'}">
        <div class="insight-text">{sim_med['recommendation']}</div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    drawdown = st.slider("Amplitude du krach (%)", 10, 70, 35) / 100
    sim_mkt  = crisis.simulate_market_crash(drawdown)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Portefeuille avant", format_currency(sim_mkt["portfolio_before"], p.currency, compact=True))
        st.metric("Perte estimée", format_currency(sim_mkt["loss"], p.currency, compact=True))
    with c2:
        st.metric("Portefeuille après", format_currency(sim_mkt["portfolio_after"], p.currency, compact=True))
        st.metric("Temps de récupération", f"{sim_mkt['recovery_years']:.1f} ans")
    with c3:
        st.metric("Bonus DCA estimé", format_currency(sim_mkt["dca_benefit"], p.currency, compact=True))
        st.metric("Fonds d'urgence OK", "✅ Oui" if sim_mkt["cash_buffer_ok"] else "❌ Non")

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-icon">📊</div>
        <div class="insight-text">{sim_mkt['advice']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Drawdown simulation chart
    time_pts = list(range(0, int(sim_mkt["recovery_years"] * 12) + 1))
    portfolio_before = sim_mkt["portfolio_before"]
    drawdown_val = sim_mkt["portfolio_after"]
    monthly_ret  = 0.065 / 12
    path = [portfolio_before]
    path.append(drawdown_val)
    for t in range(1, len(time_pts) - 1):
        path.append(path[-1] * (1 + monthly_ret))

    fig_crash = go.Figure()
    fig_crash.add_trace(go.Scatter(x=time_pts[:len(path)], y=path, line=dict(color="#D4AF37", width=2.5), fill="tozeroy", fillcolor="rgba(212,175,55,0.10)"))
    fig_crash.add_hline(y=portfolio_before, line_dash="dash", line_color="#4CAF50", annotation_text="Valeur initiale")
    fig_crash.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             height=280, font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=10,b=0),
                             xaxis=dict(title="Mois"), yaxis=dict(title=p.currency))
    st.plotly_chart(fig_crash, use_container_width=True)

with tab4:
    infl_rate = st.slider("Taux d'inflation choc (%)", 4.0, 15.0, 7.0, 0.5) / 100
    sim_infl  = crisis.simulate_inflation_shock(infl_rate)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Perte pouvoir d'achat", f"{sim_infl['purchasing_power_loss']*100:.1f}%")
        st.metric("Surcoût mensuel", format_currency(sim_infl["monthly_cost_increase"], p.currency))
    with c2:
        st.metric("Perte réelle épargne", format_currency(sim_infl["savings_real_loss"], p.currency))
        st.metric("Coût extra total 3 ans", format_currency(sim_infl["total_extra_cost"], p.currency))
    with c3:
        st.metric("Bénéfice propriétaire", format_currency(sim_infl["mortgage_benefit"], p.currency))
        net_impact_color = "normal" if sim_infl["net_impact"] > 0 else "inverse"
        st.metric("Impact net", format_currency(abs(sim_infl["net_impact"]), p.currency),
                 "✅ Bénéfice" if sim_infl["net_impact"] > 0 else "⚠️ Perte")

    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-text">{sim_infl['advice']}</div>
    </div>
    """, unsafe_allow_html=True)

with tab5:
    sim_div = crisis.simulate_divorce()
    if not sim_div.get("applicable", True):
        st.info(sim_div.get("message", "Non applicable"))
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Partage d'actifs (50/50)", format_currency(sim_div["asset_split_loss"], p.currency, compact=True))
            st.metric("Frais juridiques", format_currency(sim_div["legal_costs"], p.currency))
        with c2:
            st.metric("Impact revenu", format_currency(sim_div["income_impact"], p.currency))
            st.metric("Coûts logement", format_currency(sim_div["housing_costs"], p.currency))
        with c3:
            st.metric("Impact total", format_currency(abs(sim_div["total_impact"]), p.currency, compact=True))
            st.metric("Mois de récupération", f"{sim_div['months_to_recover']:.0f}")
        st.info(f"Un contrat de mariage (régime séparation) pourrait vous épargner ~{format_currency(sim_div['prenuptial_benefit'], p.currency)} en cas de séparation.")
