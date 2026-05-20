"""
Investment Engine — MPT, Monte Carlo, Portfolio Optimizer, Compound Scenarios.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.investment import InvestmentEngine
from simulations.monte_carlo import MonteCarloEngine
from simulations.portfolio_optimizer import PortfolioOptimizer
from utils.formatters import format_currency, format_percentage
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Investissements — Oswald Wealth", page_icon="💼", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p   = st.session_state.profile
inv = InvestmentEngine(p)
mc  = MonteCarloEngine(n_simulations=1000)
opt = PortfolioOptimizer()

st.markdown(f'<div class="hero-banner"><div class="hero-title">💼 Moteur d\'Investissement</div><div class="hero-subtitle">MPT · Monte Carlo · Frontière Efficiente — {p.name}</div></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🎰 Monte Carlo", "📐 Optimisation MPT", "📈 Projections", "🔍 Analyse Portefeuille"])

with tab1:
    st.markdown('<div class="section-header">Simulation Monte Carlo — 1000 Trajectoires</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        mc_initial = st.number_input(f"Capital initial ({p.currency})", 0.0, value=float(p.current_investments + p.current_savings * 0.5), step=1000.0)
    with c2:
        mc_monthly = st.number_input(f"Versement mensuel ({p.currency})", 0.0, value=float(p.monthly_savings), step=50.0)
    with c3:
        mc_years   = st.slider("Horizon (années)", 5, 40, p.years_to_retirement or 25)

    alloc = inv.recommended_allocation()
    mc_return = alloc.get("expected_return", 0.065)
    mc_vol    = alloc.get("volatility", 0.12)

    st.markdown(f"**Hypothèses :** Rendement = {mc_return*100:.1f}%/an · Volatilité = {mc_vol*100:.1f}%/an · Profil {p.risk_tolerance}")

    if st.button("▶ Lancer la simulation", type="primary"):
        with st.spinner("Simulation en cours..."):
            paths = mc.run_portfolio_simulation(mc_initial, mc_monthly, mc_return, mc_vol, mc_years)
            df    = mc.to_dataframe(paths, mc_years, p.age)
            stats = mc.get_statistics(paths)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["age"], y=df["p95"], name="95e percentile",
                                     line=dict(color="#4CAF50", width=1.5, dash="dash")))
            fig.add_trace(go.Scatter(x=df["age"], y=df["p75"], fill="tonexty",
                                     fillcolor="rgba(212,175,55,0.10)", name="75e percentile", line=dict(color="#D4AF37", width=1)))
            fig.add_trace(go.Scatter(x=df["age"], y=df["p50"], name="Médiane",
                                     line=dict(color="#D4AF37", width=3)))
            fig.add_trace(go.Scatter(x=df["age"], y=df["p25"], fill="tonexty",
                                     fillcolor="rgba(212,175,55,0.08)", name="25e percentile", line=dict(color="#FF9800", width=1)))
            fig.add_trace(go.Scatter(x=df["age"], y=df["p5"], name="5e percentile",
                                     line=dict(color="#F44336", width=1.5, dash="dash")))
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              height=420, font=dict(color="#C8D4E8"),
                              xaxis=dict(title="Âge"), yaxis=dict(title=p.currency),
                              legend=dict(bgcolor="rgba(0,0,0,0)"),
                              title=f"1000 simulations — {mc_years} ans")
            st.plotly_chart(fig, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric("Scénario pessimiste (P5)", format_currency(stats["final_p5"], p.currency, compact=True))
            with c2: st.metric("Scénario médian (P50)", format_currency(stats["final_p50"], p.currency, compact=True))
            with c3: st.metric("Scénario optimiste (P95)", format_currency(stats["final_p95"], p.currency, compact=True))
            with c4: st.metric("Espérance", format_currency(stats["final_mean"], p.currency, compact=True))

            # VaR
            var = mc.portfolio_var(paths, 0.95)
            st.markdown(f"""
            <div class="insight-card warning">
                <div class="insight-text">
                    <strong>Value at Risk (95%, 1 an) :</strong> -{format_currency(var['var_amount'], p.currency)} |
                    <strong>CVaR :</strong> -{format_currency(var['cvar_amount'], p.currency)}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Ruin probability
            ret_monthly = p.desired_monthly_pension
            ruin_prob = mc.calculate_ruin_probability(paths, ret_monthly, 25)
            ruin_color = "#4CAF50" if ruin_prob < 0.05 else ("#FF9800" if ruin_prob < 0.20 else "#F44336")
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-text">
                    <strong>Probabilité de ruin en retraite (25 ans, retrait {format_currency(ret_monthly, p.currency)}/mois) :</strong>
                    <span style="color:{ruin_color}; font-size:1.3rem; font-weight:700;"> {ruin_prob*100:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Frontière Efficiente & Portefeuille Optimal</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        with st.spinner("Calcul frontière efficiente..."):
            frontier = opt.efficient_frontier(40)
            random_p = opt.random_portfolios(2000)
            max_sharpe = opt.risk_profiled_portfolio(p.risk_tolerance)
            min_var    = opt.min_variance_portfolio()

        fig_frontier = go.Figure()
        fig_frontier.add_trace(go.Scatter(
            x=random_p["volatility"] * 100, y=random_p["return"] * 100,
            mode="markers", name="Portefeuilles aléatoires",
            marker=dict(color=random_p["sharpe"], colorscale="Viridis", size=4, opacity=0.5,
                       colorbar=dict(title="Sharpe")),
        ))
        if not frontier.empty:
            fig_frontier.add_trace(go.Scatter(
                x=frontier["volatility"] * 100, y=frontier["return"] * 100,
                name="Frontière Efficiente", line=dict(color="#D4AF37", width=3),
            ))
        fig_frontier.add_trace(go.Scatter(
            x=[max_sharpe["volatility"] * 100], y=[max_sharpe["return"] * 100],
            name=f"Optimal ({p.risk_tolerance})",
            mode="markers", marker=dict(color="#D4AF37", size=15, symbol="star"),
        ))
        fig_frontier.add_trace(go.Scatter(
            x=[min_var["volatility"] * 100], y=[min_var["return"] * 100],
            name="Variance Minimale",
            mode="markers", marker=dict(color="#4CAF50", size=12, symbol="diamond"),
        ))
        fig_frontier.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=420, font=dict(color="#C8D4E8"),
            xaxis=dict(title="Volatilité (%)"), yaxis=dict(title="Rendement Attendu (%)"),
            title="Frontière Efficiente de Markowitz",
        )
        st.plotly_chart(fig_frontier, use_container_width=True)

    with col_b:
        st.markdown(f"**Portefeuille Optimal — {p.risk_tolerance}**")
        allocation = max_sharpe["allocation"]
        filtered   = {k: v for k, v in allocation.items() if v > 0.01}

        fig_pie = go.Figure(go.Pie(
            labels=list(filtered.keys()),
            values=[v * 100 for v in filtered.values()],
            hole=0.5,
            marker=dict(colors=["#D4AF37","#B8963E","#E8C547","#4A90D9","#357ABD","#5CB85C","#F0AD4E","#9B9B9B"]),
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=300, margin=dict(l=0,r=0,t=20,b=0),
            showlegend=True, legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
            font=dict(color="#C8D4E8"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Rendement", f"{max_sharpe['return']*100:.1f}%")
        with c2: st.metric("Volatilité", f"{max_sharpe['volatility']*100:.1f}%")
        with c3: st.metric("Sharpe", f"{max_sharpe['sharpe']:.2f}")

with tab3:
    st.markdown('<div class="section-header">Scénarios de Croissance du Capital</div>', unsafe_allow_html=True)
    scenarios_df = inv.compound_scenarios()

    fig_comp = go.Figure()
    colors   = ["#F44336","#D4AF37","#4CAF50","#9B59B6"]
    for i, row in scenarios_df.iterrows():
        rate  = row["Rendement annuel"]
        years = p.years_to_retirement or 25
        fvs   = []
        initial = p.current_investments + p.current_savings * 0.5
        w = initial
        for y in range(years + 1):
            fvs.append(w)
            w = w * (1 + rate) + p.monthly_savings * 12
        fig_comp.add_trace(go.Scatter(
            x=list(range(p.age, p.age + years + 1)),
            y=fvs, name=row["Scénario"], line=dict(color=colors[i], width=2),
        ))
    fig_comp.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=380, font=dict(color="#C8D4E8"),
        xaxis=dict(title="Âge"), yaxis=dict(title=p.currency),
        title="Impact du rendement sur le patrimoine final",
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    display = scenarios_df.copy()
    for col in ["Patrimoine initial","Contribution mensuelle",f"Patrimoine dans {p.years_to_retirement or 25} ans"]:
        display[col] = display[col].map(lambda x: format_currency(x, p.currency, compact=True))
    display["Rendement annuel"] = display["Rendement annuel"].map(lambda x: f"{x*100:.1f}%")
    display["Multiplicateur"]   = display["Multiplicateur"].map(lambda x: f"{x:.1f}x")
    st.dataframe(display, use_container_width=True, hide_index=True)

    # Opportunity cost
    if p.luxury_monthly > 0:
        oc = inv.opportunity_cost_analysis(p.luxury_monthly)
        st.markdown(f"""
        <div class="insight-card warning">
            <div class="insight-icon">💡</div>
            <div class="insight-text">{oc['message']}</div>
            <div class="insight-impact">Coût d'opportunité : {format_currency(oc['opportunity_cost'], p.currency, compact=True)} sur {oc['years']} ans</div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">Analyse du Portefeuille Actuel</div>', unsafe_allow_html=True)
    analysis = inv.analyze_current_portfolio()
    recommendations = inv.rebalancing_recommendation()

    if analysis["total"] <= 0:
        st.info("Aucun investissement enregistré. Ajoutez vos investissements dans votre profil.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Capital Total", format_currency(analysis["total"], p.currency, compact=True))
        with c2: st.metric("Score Portefeuille", f"{analysis['portfolio_score']:.0f}/100")
        with c3: st.metric("Diversification", f"{analysis['diversification_score']*100:.0f}%")

        alloc_fig = go.Figure(go.Pie(
            labels=list(analysis["allocation"].keys()),
            values=[v * 100 for v in analysis["allocation"].values()],
            hole=0.5,
            marker=dict(colors=["#D4AF37","#4A90D9","#5CB85C","#FF6B35","#9B9B9B"]),
        ))
        alloc_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=280,
                                font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(alloc_fig, use_container_width=True)

    if recommendations:
        st.markdown("**Recommandations de Rééquilibrage**")
        for rec in recommendations:
            type_map = {"warning":"warning","danger":"danger","info":""}
            st.markdown(f"""
            <div class="insight-card {type_map.get(rec['type'],'')}">
                <div class="insight-text"><strong>{rec['action']}</strong></div>
                <div class="insight-impact">{rec.get('impact','')}</div>
            </div>
            """, unsafe_allow_html=True)
