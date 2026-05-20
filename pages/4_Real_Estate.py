"""
Real Estate Wealth Engine — Affordability, Rent vs Buy, Investment Property.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.real_estate import RealEstateEngine
from utils.formatters import format_currency, format_percentage
from utils.constants import COUNTRIES
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Immobilier — Oswald Wealth", page_icon="🏡", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p   = st.session_state.profile
re  = RealEstateEngine(p)
cd  = COUNTRIES.get(p.country, COUNTRIES["France"])

st.markdown(f'<div class="hero-banner"><div class="hero-title">🏡 Moteur Immobilier</div><div class="hero-subtitle">Accessibilité · Louer vs Acheter · Investissement Locatif — {p.name}</div></div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏦 Accessibilité", "⚖️ Louer vs Acheter", "📋 Amortissement", "🏢 Investissement Locatif"])

with tab1:
    st.markdown('<div class="section-header">Analyse d\'Accessibilité</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        prop_val   = st.number_input(f"Valeur du bien ({p.currency})", 50000.0, 5_000_000.0, float(p.target_property_value), step=5000.0)
        down_pct   = st.slider("Apport personnel (%)", 5, 50, 20) / 100
        mort_rate  = st.slider("Taux d'intérêt (%)", 0.5, 10.0, float(cd["mortgage_rate"]*100), 0.05) / 100
        mort_years = st.slider("Durée du prêt (ans)", 5, 30, 25)

    afford = re.affordability_analysis(prop_val, down_pct)

    with c2:
        # Affordability KPIs
        dti_color   = "#4CAF50" if afford["dti_with_mortgage"] <= 0.28 else ("#D4AF37" if afford["dti_with_mortgage"] <= 0.35 else "#F44336")
        stress_color= "#4CAF50" if afford["dti_stressed"] <= 0.40 else "#F44336"

        kpis = [
            ("Mensualité", format_currency(afford["monthly_payment"], p.currency), "Normal"),
            ("Mensualité stress +2%", format_currency(afford["monthly_payment_stress"], p.currency), "Stress test"),
            ("DTI avec crédit", f"{afford['dti_with_mortgage']*100:.1f}%", "Max 35%"),
            ("DTI stressé", f"{afford['dti_stressed']*100:.1f}%", "Max 40%"),
            ("LTV", f"{afford['ltv']*100:.0f}%", "Loan-To-Value"),
            ("Apport requis", format_currency(afford["down_payment_required"], p.currency), ""),
        ]
        cols = st.columns(3)
        for i, (label, val, note) in enumerate(kpis):
            with cols[i % 3]:
                st.metric(label, val, note)

        # Overall verdict
        if afford["is_affordable"]:
            st.success(f"✅ **Ce bien est accessible** avec votre profil financier actuel. DTI projeté : {afford['dti_with_mortgage']*100:.1f}%")
        else:
            st.error(f"❌ **Ce bien dépasse vos capacités** (DTI {afford['dti_with_mortgage']*100:.1f}% > 35%). Réduire le bien ou augmenter l'apport.")

        if afford["is_stressed_affordable"]:
            st.success("✅ Résistance au stress test +2% : OK")
        else:
            st.warning("⚠️ Ce bien deviendrait problématique si les taux montent de +2%")

    # Down payment savings timeline
    st.markdown('<div class="section-header">Délai d\'Accumulation de l\'Apport</div>', unsafe_allow_html=True)
    gap   = afford["current_savings_gap"]
    months = afford["months_to_down_payment"]
    if gap <= 0:
        st.success(f"✅ Vous disposez déjà de l'apport requis ({format_currency(afford['down_payment_required'], p.currency)}) !")
    else:
        st.info(f"Il vous faudra **{months:.0f} mois ({months/12:.1f} ans)** pour accumuler l'apport manquant de {format_currency(gap, p.currency)}.")
        # Visual savings progress
        progress_months = list(range(int(months) + 2))
        savings_path = [p.current_savings + p.monthly_savings * m for m in progress_months]
        target_line  = [afford["down_payment_required"]] * len(progress_months)
        fig_savings = go.Figure()
        fig_savings.add_trace(go.Scatter(x=progress_months, y=savings_path, name="Épargne projetée",
                                         line=dict(color="#D4AF37", width=2), fill="tozeroy",
                                         fillcolor="rgba(212,175,55,0.10)"))
        fig_savings.add_trace(go.Scatter(x=progress_months, y=target_line, name=f"Apport cible",
                                         line=dict(color="#4CAF50", dash="dash")))
        fig_savings.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   height=280, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#C8D4E8"),
                                   xaxis=dict(title="Mois"), yaxis=dict(title=p.currency))
        st.plotly_chart(fig_savings, use_container_width=True)

    # Ideal timing
    st.markdown('<div class="section-header">Timing Optimal d\'Achat</div>', unsafe_allow_html=True)
    timing = re.ideal_purchase_timing()
    st.markdown(f"**Âge optimal calculé : {timing['optimal_age']} ans** (basé sur apport + DTI disponibles)")

with tab2:
    st.markdown('<div class="section-header">Analyse Louer vs Acheter (NPV)</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        rvb_years = st.slider("Horizon d'analyse (années)", 5, 30, 15)
        appreciation = st.slider("Appréciation annuelle du bien (%)", -2.0, 8.0, 3.0, 0.5) / 100
    with c2:
        monthly_rent_input = st.number_input(f"Loyer mensuel actuel ({p.currency})", 100.0, 10_000.0, float(p.current_rent), step=50.0)

    rvb = re.rent_vs_buy()
    rvb_custom = {**rvb}  # use computed version

    rec_color = "#4CAF50" if rvb["recommendation"] == "Acheter" else "#4A90D9"
    st.markdown(f"""
    <div class="kpi-card" style="text-align:center; margin:16px 0;">
        <div class="kpi-label">Recommandation</div>
        <div style="font-size:2rem; font-weight:700; color:{rec_color};">
            {'🏡 Acheter' if rvb['recommendation'] == 'Acheter' else '🏠 Louer'}
        </div>
        <div style="color:#C8D4E8; margin-top:8px;">
            Avantage NPV : {format_currency(rvb['advantage'], p.currency, compact=True)} en faveur de l'option recommandée
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("NPV Achat", format_currency(rvb["buy_npv"], p.currency, compact=True))
    with c2: st.metric("NPV Location", format_currency(rvb["rent_npv"], p.currency, compact=True))
    with c3: st.metric(f"Valeur bien dans {rvb_years} ans", format_currency(rvb["final_home_value"], p.currency, compact=True))
    with c4: st.metric("Coût total location", format_currency(abs(rvb["total_rent_cost"]), p.currency, compact=True))

    # Appreciation scenarios
    st.markdown('<div class="section-header">Scénarios d\'Appréciation</div>', unsafe_allow_html=True)
    appre_df = re.property_appreciation_scenarios(rvb_years)
    fig_appre = go.Figure()
    for _, row in appre_df.iterrows():
        fig_appre.add_trace(go.Bar(
            x=[row["Scénario"]],
            y=[row[f"Plus-value brute"]],
            name=row["Scénario"],
            text=[format_currency(row[f"Plus-value brute"], p.currency, compact=True)],
            textposition="outside",
        ))
    fig_appre.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             height=320, font=dict(color="#C8D4E8"), showlegend=False,
                             title=f"Plus-value potentielle sur {rvb_years} ans")
    st.plotly_chart(fig_appre, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">Tableau d\'Amortissement</div>', unsafe_allow_html=True)
    amort = re.amortization_summary(prop_val if 'prop_val' in dir() else p.target_property_value)
    fig_amort = go.Figure()
    fig_amort.add_trace(go.Bar(x=amort["year"], y=amort["interest_paid"], name="Intérêts", marker_color="#F44336", opacity=0.8))
    fig_amort.add_trace(go.Bar(x=amort["year"], y=amort["principal_paid"], name="Capital remboursé", marker_color="#4CAF50", opacity=0.8))
    fig_amort.add_trace(go.Scatter(x=amort["year"], y=amort["equity"], name="Equity cumulée",
                                    line=dict(color="#D4AF37", width=2.5), yaxis="y2"))
    fig_amort.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        barmode="stack", height=380, font=dict(color="#C8D4E8"),
        xaxis=dict(title="Année"),
        yaxis=dict(title=f"Paiement ({p.currency})"),
        yaxis2=dict(title="Equity", overlaying="y", side="right"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_amort, use_container_width=True)

    amort_display = amort.copy()
    for col in ["total_paid","interest_paid","principal_paid","balance_end","equity"]:
        amort_display[col] = amort_display[col].map(lambda x: format_currency(x, p.currency))
    amort_display.columns = ["Année","Total payé","Intérêts","Capital","Capital restant","Equity"]
    st.dataframe(amort_display, use_container_width=True, hide_index=True)

with tab4:
    st.markdown('<div class="section-header">Analyse Investissement Locatif</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        inv_price = st.number_input(f"Prix d'achat ({p.currency})", 50000.0, 5_000_000.0, 200000.0, step=5000.0)
        inv_rent  = st.number_input(f"Loyer mensuel brut ({p.currency})", 100.0, 20_000.0, 900.0, step=50.0)
    with c2:
        vacancy   = st.slider("Taux de vacance (%)", 0, 20, 5) / 100
        mgmt_fees = st.slider("Frais de gestion (%)", 0, 15, 8) / 100

    if st.button("Analyser l'investissement", type="primary"):
        analysis = re.investment_property_analysis(inv_price, inv_rent, vacancy, mgmt_fees)

        kpis = [
            ("Loyer net effectif/mois", format_currency(analysis["monthly_rent_effective"], p.currency)),
            ("Rendement brut", format_percentage(analysis["gross_yield"])),
            ("Rendement net", format_percentage(analysis["net_yield"])),
            ("Cash-flow mensuel", format_currency(analysis["monthly_cash_flow"], p.currency)),
            ("Cash-flow annuel", format_currency(analysis["annual_cash_flow"], p.currency)),
            ("DSCR", f"{analysis['dscr']:.2f}"),
        ]
        cols = st.columns(3)
        for i, (label, val) in enumerate(kpis):
            with cols[i % 3]:
                st.metric(label, val)

        if analysis["is_investment_viable"]:
            st.success("✅ Investissement viable : DSCR ≥ 1.2 et rendement net ≥ 4%")
        else:
            st.warning("⚠️ Investissement limite : revoir le prix ou le loyer pour améliorer la rentabilité")

        if analysis["is_cash_flow_positive"]:
            st.success(f"✅ Cash-flow positif de {format_currency(analysis['monthly_cash_flow'], p.currency)}/mois")
        else:
            st.error(f"❌ Cash-flow négatif de {format_currency(analysis['monthly_cash_flow'], p.currency)}/mois — effort d'épargne mensuel requis")

        proj = analysis["projection"]
        fig_proj = go.Figure()
        fig_proj.add_trace(go.Scatter(x=proj["Année"], y=proj["Valeur bien"], name="Valeur bien",
                                      line=dict(color="#5CB85C", width=2)))
        fig_proj.add_trace(go.Scatter(x=proj["Année"], y=proj["Equity estimée"], name="Equity",
                                      line=dict(color="#D4AF37", width=2)))
        fig_proj.add_trace(go.Bar(x=proj["Année"], y=proj["Loyer mensuel net"], name="Loyer net/mois",
                                   marker_color="rgba(76,175,80,0.4)", yaxis="y2"))
        fig_proj.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                height=320, font=dict(color="#C8D4E8"),
                                yaxis2=dict(overlaying="y", side="right"),
                                legend=dict(bgcolor="rgba(0,0,0,0)"),
                                title="Projection sur 10 ans")
        st.plotly_chart(fig_proj, use_container_width=True)
