"""
Life Trajectory — Full financial life timeline with milestones and Prophet forecasts.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.life_trajectory import LifeTrajectoryEngine
from simulations.prophet_forecasting import ProphetForecaster
from utils.formatters import format_currency
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Trajectoire — Oswald Wealth", page_icon="📈", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord (menu gauche → Profil).")
    st.stop()

p   = st.session_state.profile
eng = LifeTrajectoryEngine(p)

st.markdown(f'<div class="hero-banner"><div class="hero-title">📈 Trajectoire Financière</div><div class="hero-subtitle">Projection complète de {p.age} à 85 ans — {p.name}</div></div>', unsafe_allow_html=True)

traj      = eng.build_trajectory()
milestones = eng.get_milestones()
ret_ready  = eng.retirement_readiness()
fi_age     = eng.calculate_financial_independence_age()

# ---- Tabs ----
tab1, tab2, tab3, tab4 = st.tabs(["📊 Trajectoire", "🏁 Jalons", "🏖️ Retraite", "🔮 Forecast Prophet"])

with tab1:
    c1, c2 = st.columns([3, 1])
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=traj["age"], y=traj["wealth_real"],
            name="Patrimoine réel", fill="tozeroy",
            line=dict(color="#D4AF37", width=3),
            fillcolor="rgba(212,175,55,0.10)",
        ))
        fig.add_trace(go.Scatter(
            x=traj["age"], y=traj["wealth_nominal"],
            name="Patrimoine nominal", line=dict(color="#4A90D9", dash="dash", width=1.5),
        ))
        fig.add_trace(go.Bar(
            x=traj["age"], y=traj["savings_annual"],
            name="Épargne annuelle", yaxis="y2",
            marker_color="rgba(76,175,80,0.4)",
            opacity=0.6,
        ))
        for m in milestones:
            colors_m = {"current":"#D4AF37","family":"#E8C547","real_estate":"#5CB85C","wealth":"#4A90D9","retirement":"#9B59B6"}
            fig.add_vline(x=m["age"], line_dash="dot", line_color=colors_m.get(m["type"],"#8899BB"),
                         opacity=0.6,
                         annotation_text=f"{m['icon']} {m['age']}",
                         annotation_font_color="#E8E8E8",
                         annotation_font_size=10)

        if fi_age < 99:
            fig.add_vline(x=fi_age, line_dash="solid", line_color="#4CAF50",
                         annotation_text=f"🎯 FI {fi_age}ans", annotation_font_color="#4CAF50")

        fig.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=450, margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(title="Âge", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title=f"Patrimoine ({p.currency})", gridcolor="rgba(255,255,255,0.05)"),
            yaxis2=dict(title="Épargne/an", overlaying="y", side="right", showgrid=False),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.12),
            font=dict(color="#C8D4E8"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("**Résumé Patrimonial**")
        wealth_now  = float(traj[traj["age"] == p.age]["wealth_real"].iloc[0]) if not traj.empty else p.current_net_worth
        wealth_50   = float(traj[traj["age"] == min(50, traj["age"].max())]["wealth_real"].iloc[-1])
        wealth_ret  = float(traj[traj["age"] == p.target_retirement_age]["wealth_real"].iloc[0]) if p.target_retirement_age in traj["age"].values else 0

        for label, val in [("Maintenant", wealth_now), ("À 50 ans", wealth_50), ("À la retraite", wealth_ret)]:
            st.metric(label, format_currency(val, p.currency, compact=True))

        # Savings rate gauge
        sr = p.net_savings_rate
        fig_sr = go.Figure(go.Indicator(
            mode="gauge+number",
            value=sr * 100,
            title={"text": "Taux d'épargne"},
            gauge={"axis": {"range": [0, 35]},
                   "bar": {"color": "#D4AF37" if sr >= 0.15 else "#FF9800"},
                   "steps": [
                       {"range": [0, 10], "color": "rgba(244,67,54,0.2)"},
                       {"range": [10, 20], "color": "rgba(255,152,0,0.2)"},
                       {"range": [20, 35], "color": "rgba(76,175,80,0.2)"},
                   ]},
            number={"suffix": "%"},
        ))
        fig_sr.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=160, margin=dict(l=10,r=10,t=30,b=0), font=dict(color="#C8D4E8"))
        st.plotly_chart(fig_sr, use_container_width=True)

    # Trajectory table
    with st.expander("📋 Données complètes par âge"):
        display_df = traj[["age","income_annual","expenses_annual","savings_annual","savings_rate","wealth_real","is_retired"]].copy()
        display_df.columns = ["Âge","Revenus/an","Dépenses/an","Épargne/an","Taux épargne","Patrimoine réel","Retraité"]
        for col in ["Revenus/an","Dépenses/an","Épargne/an","Patrimoine réel"]:
            display_df[col] = display_df[col].map(lambda x: format_currency(x, p.currency))
        display_df["Taux épargne"] = display_df["Taux épargne"].map(lambda x: f"{x*100:.1f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<div class="section-header">Jalons Financiers Clés</div>', unsafe_allow_html=True)
    type_colors = {"current":"#D4AF37","family":"#E8C547","real_estate":"#5CB85C","wealth":"#4A90D9","retirement":"#9B59B6"}
    for m in milestones:
        c = type_colors.get(m["type"], "#8899BB")
        wealth_at = float(traj[traj["age"] == m["age"]]["wealth_real"].iloc[0]) if m["age"] in traj["age"].values else 0
        st.markdown(f"""
        <div class="milestone-item">
            <div class="milestone-dot" style="background:{c};"></div>
            <div>
                <div class="milestone-year">{m['icon']} Âge {m['age']}</div>
                <div class="milestone-desc">{m['event']}</div>
                <div style="font-size:0.8rem; color:{c}; margin-top:2px;">
                    Patrimoine estimé : {format_currency(wealth_at, p.currency, compact=True)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    if not ret_ready:
        st.info("Données insuffisantes pour le calcul retraite.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Patrimoine à la retraite", format_currency(ret_ready["wealth_at_retirement"], p.currency, compact=True))
            st.metric("Corpus requis (règle 4%)", format_currency(ret_ready["required_corpus"], p.currency, compact=True))
        with c2:
            gap = ret_ready["gap"]
            st.metric("Gap", format_currency(abs(gap), p.currency, compact=True),
                     "✅ Excédent" if gap <= 0 else "⚠️ Déficit à combler")
            st.metric("Retrait max mensuel", format_currency(ret_ready["max_monthly_withdrawal"], p.currency))
        with c3:
            fi = fi_age
            st.metric("Liberté Financière", f"{fi} ans" if fi < 99 else "Non atteint", f"dans {fi - p.age} ans" if fi < 99 else "")
            readiness = ret_ready["readiness_pct"]
            color = "#4CAF50" if readiness >= 0.80 else ("#D4AF37" if readiness >= 0.50 else "#F44336")
            st.markdown(f"**Préparation : {readiness*100:.0f}%**")
            st.progress(min(readiness, 1.0))

        # Retirement income chart
        fig_ret = go.Figure()
        pension_income = p.total_income * 0.55  # state pension
        investment_income = ret_ready["max_monthly_withdrawal"]
        labels = ["Pension État/Caisse", "Revenus Investissements", "Gap"]
        gap_val = max(p.desired_monthly_pension - pension_income - investment_income, 0)
        values  = [pension_income, investment_income, gap_val]
        colors  = ["#4CAF50","#D4AF37","#F44336" if gap_val > 0 else "#4CAF50"]

        fig_ret.add_trace(go.Bar(
            x=labels, y=values,
            marker_color=colors,
            text=[format_currency(v, p.currency) for v in values],
            textposition="outside",
        ))
        fig_ret.add_hline(y=p.desired_monthly_pension, line_dash="dash", line_color="#E8C547",
                         annotation_text=f"Objectif: {format_currency(p.desired_monthly_pension, p.currency)}")
        fig_ret.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title="Décomposition du revenu retraite mensuel", height=350,
            font=dict(color="#C8D4E8"), margin=dict(l=0,r=0,t=40,b=0),
        )
        st.plotly_chart(fig_ret, use_container_width=True)

with tab4:
    st.markdown('<div class="section-header">Prévisions Prophet (Série Temporelle)</div>', unsafe_allow_html=True)
    forecaster = ProphetForecaster(p)

    if not ProphetForecaster.is_available():
        st.info("Prophet non installé — projection linéaire affichée. `pip install prophet` pour activer les prévisions ML.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Prévision Revenus (10 ans)**")
        fc_income = forecaster.forecast_income(120)
        fig_income = go.Figure()
        fig_income.add_trace(go.Scatter(x=fc_income["ds"], y=fc_income["yhat"], name="Prévision", line=dict(color="#D4AF37")))
        fig_income.add_trace(go.Scatter(x=fc_income["ds"], y=fc_income["yhat_upper"], name="Borne haute",
                                        line=dict(color="#D4AF37", dash="dot", width=1), showlegend=False))
        fig_income.add_trace(go.Scatter(x=fc_income["ds"], y=fc_income["yhat_lower"], name="Borne basse",
                                        line=dict(color="#D4AF37", dash="dot", width=1), fill="tonexty",
                                        fillcolor="rgba(212,175,55,0.12)", showlegend=False))
        fig_income.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                 height=280, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#C8D4E8"))
        st.plotly_chart(fig_income, use_container_width=True)

    with col_b:
        st.markdown("**Prévision Valeur Bien Immobilier (10 ans)**")
        fc_prop = forecaster.forecast_property_value(120)
        fig_prop = go.Figure()
        fig_prop.add_trace(go.Scatter(x=fc_prop["ds"], y=fc_prop["yhat"], name="Valeur", line=dict(color="#5CB85C")))
        fig_prop.add_trace(go.Scatter(x=fc_prop["ds"], y=fc_prop["yhat_upper"], name="Max",
                                      line=dict(color="#5CB85C", dash="dot", width=1), showlegend=False))
        fig_prop.add_trace(go.Scatter(x=fc_prop["ds"], y=fc_prop["yhat_lower"], name="Min",
                                      line=dict(color="#5CB85C", dash="dot", width=1), fill="tonexty",
                                      fillcolor="rgba(92,184,92,0.12)", showlegend=False))
        fig_prop.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                height=280, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#C8D4E8"))
        st.plotly_chart(fig_prop, use_container_width=True)

    st.markdown("**Prévision Patrimoine Total (30 ans)**")
    fc_wealth = forecaster.forecast_wealth_trajectory(360)
    fig_w = go.Figure()
    fig_w.add_trace(go.Scatter(x=fc_wealth["ds"], y=fc_wealth["yhat"], name="Patrimoine", line=dict(color="#D4AF37", width=2.5)))
    fig_w.add_trace(go.Scatter(x=fc_wealth["ds"], y=fc_wealth["yhat_upper"], fill=None,
                               line=dict(color="rgba(212,175,55,0.3)", width=1), showlegend=False))
    fig_w.add_trace(go.Scatter(x=fc_wealth["ds"], y=fc_wealth["yhat_lower"],
                               fill="tonexty", fillcolor="rgba(212,175,55,0.10)",
                               line=dict(color="rgba(212,175,55,0.3)", width=1), showlegend=False))
    fig_w.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=300, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#C8D4E8"),
                        yaxis=dict(title=p.currency), xaxis=dict(title="Date"))
    st.plotly_chart(fig_w, use_container_width=True)
