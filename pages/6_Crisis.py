"""
Simulation de Crise — Macro ET Micro.
Les vrais risques des gens ordinaires : CDD, maladie, loyer, separation...
"""
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.crisis_simulation import CrisisSimulationEngine
from engines.life_stage_engine import LifeStageEngine, MICRO_CRISES
import plotly.graph_objects as go

st.set_page_config(page_title="Simulation de Crise — Oswald Wealth", page_icon="⚡", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("Creez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
crisis_eng = CrisisSimulationEngine(p)
stage_eng = LifeStageEngine(p)

st.markdown(
    '<div class="hero-banner">'
    '<div class="hero-title">⚡ Simulation de Crise</div>'
    '<div class="hero-subtitle">'
    'Les coups durs ca arrive — voyez comment vos finances y resistent.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

tab_micro, tab_macro = st.tabs(["⚡ Crises du quotidien", "📊 Chocs financiers majeurs"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — CRISES MICRO (everyday life)
# ══════════════════════════════════════════════════════════════
with tab_micro:

    st.markdown("### Ce qui arrive vraiment aux gens — et comment vous y survivrez")
    st.markdown(
        "<div style='color:#8899BB; margin-bottom:24px;'>"
        "Pas de krach boursier abstrait. Ces scenarios sont ceux que vous pouvez vivre demain."
        "</div>",
        unsafe_allow_html=True,
    )

    # Emergency fund status first
    ef = p.emergency_fund
    ef_months = ef / p.monthly_expenses if p.monthly_expenses > 0 else 0
    ef_color = "#4CAF50" if ef_months >= 4 else ("#D4AF37" if ef_months >= 2 else "#F44336")
    ef_label = ("Solide" if ef_months >= 4 else ("Fragile" if ef_months >= 2 else "Insuffisant"))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Fonds d\'urgence</div>'
            f'<div class="kpi-value" style="color:{ef_color};">{sym}{ef:,.0f}</div>'
            f'<div style="color:{ef_color}; font-size:0.85rem;">{ef_label}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Mois de securite</div>'
            f'<div class="kpi-value" style="color:{ef_color};">{ef_months:.1f} mois</div>'
            f'<div style="color:#8899BB; font-size:0.8rem;">objectif : 4-6 mois</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c3:
        manque = max((4 - ef_months) * p.monthly_expenses, 0)
        m_color = "#4CAF50" if manque == 0 else "#FF9800"
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Il vous manque</div>'
            f'<div class="kpi-value" style="color:{m_color};">'
            f'{sym}{manque:,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.8rem;">pour atteindre 4 mois</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Crisis selector
    crisis_labels = {k: v["icon"] + " " + v["name"] for k, v in MICRO_CRISES.items()}
    selected_key = st.selectbox(
        "Choisissez un scenario de crise a simuler",
        list(MICRO_CRISES.keys()),
        format_func=lambda k: crisis_labels[k],
    )
    crisis_cfg = MICRO_CRISES[selected_key]

    # Duration slider (only for income-based crises)
    has_duration = crisis_cfg.get("duration_months_high", 0) > 0
    if has_duration and crisis_cfg["duration_months_high"] < 999:
        dur_low = crisis_cfg["duration_months_low"]
        dur_high = crisis_cfg["duration_months_high"]
        sim_duration = st.slider(
            "Duree estimee de la crise (mois)",
            min_value=dur_low, max_value=min(dur_high + 3, 12),
            value=dur_high, step=1,
        )
    else:
        sim_duration = crisis_cfg.get("duration_months_high", 1)
        if sim_duration == 999:
            sim_duration = 12

    result = stage_eng.simulate_micro_crisis(selected_key, sim_duration)

    # Crisis summary card
    sev_color = crisis_cfg["severity_color"]
    st.markdown(
        f'<div style="background:rgba(19,27,46,0.9); border:2px solid {sev_color}; '
        f'border-radius:14px; padding:20px 24px; margin:16px 0;">'
        f'<div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">'
        f'<span style="font-size:2rem;">{crisis_cfg["icon"]}</span>'
        f'<div>'
        f'<div style="font-size:1.1rem; font-weight:700; color:#E8E8E8;">{crisis_cfg["name"]}</div>'
        f'<div style="color:{sev_color}; font-size:0.85rem; font-weight:600;">Severite : {crisis_cfg["severity"]}</div>'
        f'</div>'
        f'</div>'
        f'<div style="color:#C8D4E8; font-size:0.95rem; line-height:1.6;">{crisis_cfg["description"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Impact KPIs
    st.markdown("#### Impact financier")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        monthly_deficit = result["monthly_deficit"]
        d_color = "#4CAF50" if monthly_deficit == 0 else "#F44336"
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Deficit mensuel</div>'
            f'<div class="kpi-value" style="color:{d_color};">'
            f'{sym}{monthly_deficit:,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.75rem;">/mois pendant la crise</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col2:
        total_sh = result["total_shortfall"]
        ts_color = "#4CAF50" if total_sh == 0 else ("#D4AF37" if total_sh < ef else "#F44336")
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Manque total</div>'
            f'<div class="kpi-value" style="color:{ts_color};">'
            f'{sym}{total_sh:,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.75rem;">sur toute la periode</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col3:
        runway = result["runway_months"]
        rw_color = "#4CAF50" if runway >= sim_duration else ("#D4AF37" if runway >= sim_duration * 0.5 else "#F44336")
        runway_display = str(round(runway, 1)) if runway < 999 else "Infini"
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Votre fonds tient</div>'
            f'<div class="kpi-value" style="color:{rw_color};">'
            f'{runway_display} mois</div>'
            f'<div style="color:#8899BB; font-size:0.75rem;">avec votre fonds d\'urgence</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with col4:
        rebuild = result["rebuild_months"]
        rb_display = str(rebuild) + " mois" if rebuild < 999 else "Long"
        rb_color = "#4CAF50" if rebuild <= 3 else ("#D4AF37" if rebuild <= 9 else "#FF9800")
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Temps de recuperation</div>'
            f'<div class="kpi-value" style="color:{rb_color};">{rb_display}</div>'
            f'<div style="color:#8899BB; font-size:0.75rem;">pour rebatir le fonds</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Verdict
    if result["ef_covers"]:
        verdict_color = "#4CAF50"
        verdict_icon = "✅"
        verdict = (
            "Votre fonds d'urgence couvre cette crise en entier. "
            "Vous pouvez traverser ca sans toucher a votre epargne long terme."
        )
    elif result["ef_covers_partial"]:
        verdict_color = "#D4AF37"
        verdict_icon = "⚠️"
        missing = result["missing_amount"]
        verdict = (
            "Votre fonds d'urgence couvre la moitie de cette crise. "
            "Il vous manquerait " + sym + str(round(missing)) + " — pensez a renforcer ce coussin."
        )
    else:
        verdict_color = "#F44336"
        verdict_icon = "❌"
        missing = result["missing_amount"]
        verdict = (
            "Votre fonds d'urgence est insuffisant pour cette crise. "
            "Sans renforcement, vous devrez vous endetter ou puiser dans l'epargne long terme. "
            "Priorite : constituer " + sym + str(round(missing)) + " supplementaires."
        )

    st.markdown(
        f'<div style="background:rgba(19,27,46,0.8); border-left:4px solid {verdict_color}; '
        f'border-radius:0 12px 12px 0; padding:16px 20px; margin:16px 0;">'
        f'<div style="font-size:1.2rem; margin-bottom:6px;">{verdict_icon}</div>'
        f'<div style="color:{verdict_color}; font-weight:600;">{verdict}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Allocation / aide info
    if crisis_cfg.get("has_allocation"):
        alloc_label = crisis_cfg.get("allocation_label", "")
        st.info("💡 " + alloc_label)

    # Chart: budget before vs during crisis
    st.markdown("---")
    st.markdown("#### Votre budget : avant vs pendant la crise")

    normal_income = result["income_normal"]
    crisis_income = result["income_during"]
    normal_exp = p.monthly_expenses
    crisis_exp = result["expenses_during"]
    normal_savings = max(normal_income - normal_exp, 0)
    crisis_surplus = max(crisis_income - crisis_exp, 0)

    fig = go.Figure()
    categories = ["Revenus", "Depenses", "Disponible"]
    normal_vals = [normal_income, normal_exp, normal_savings]
    crisis_vals = [crisis_income, crisis_exp, crisis_surplus]

    fig.add_trace(go.Bar(
        name="Situation normale",
        x=categories, y=normal_vals,
        marker_color="#4A90D9",
        text=[sym + str(int(v)) for v in normal_vals],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="Pendant la crise",
        x=categories, y=crisis_vals,
        marker_color=sev_color,
        text=[sym + str(int(v)) for v in crisis_vals],
        textposition="outside",
        opacity=0.85,
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        barmode="group", height=300, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.25),
        yaxis=dict(title=cur),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Action plan
    st.markdown("---")
    st.markdown("#### Plan d'action si ca arrive")
    for i, action in enumerate(crisis_cfg["actions"], 1):
        st.markdown(
            f'<div style="display:flex; gap:12px; padding:10px 14px; '
            f'background:rgba(19,27,46,0.6); border-radius:8px; margin-bottom:8px;">'
            f'<span style="color:#D4AF37; font-weight:800; font-size:1rem;">{i}.</span>'
            f'<span style="color:#C8D4E8; font-size:0.92rem;">{action}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Reminder: build emergency fund
    if ef_months < 4:
        target_ef = p.monthly_expenses * 4
        months_to_build = round((target_ef - ef) / max(p.monthly_savings, 50))
        st.markdown(
            f'<div style="background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.3); '
            f'border-radius:12px; padding:16px; margin-top:16px; text-align:center;">'
            f'<div style="color:#D4AF37; font-weight:600;">Renforcez votre fonds d\'urgence</div>'
            f'<div style="color:#C8D4E8; margin-top:6px;">'
            f'Objectif : {sym}{target_ef:,.0f} (4 mois) — '
            f'a votre rythme actuel, vous l\'atteignez en {months_to_build} mois.'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════
# TAB 2 — MACRO CRISES (existing engine)
# ══════════════════════════════════════════════════════════════
with tab_macro:

    resilience = crisis_eng.overall_resilience_score()
    res_score = resilience["total_score"]
    res_color = resilience["color"]

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        fig_res = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res_score,
            title={
                "text": "Score de Resilience : " + resilience["level"],
                "font": {"color": "#E8E8E8", "size": 14},
            },
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": res_color},
                "steps": [
                    {"range": [0,  20], "color": "rgba(244,67,54,0.2)"},
                    {"range": [20, 40], "color": "rgba(255,87,34,0.2)"},
                    {"range": [40, 60], "color": "rgba(255,152,0,0.2)"},
                    {"range": [60, 80], "color": "rgba(76,175,80,0.2)"},
                    {"range": [80,100], "color": "rgba(212,175,55,0.2)"},
                ],
            },
            number={"font": {"color": res_color, "size": 42}, "suffix": "/100"},
        ))
        fig_res.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=260,
            margin=dict(l=20, r=20, t=30, b=0), font=dict(color="#C8D4E8"),
        )
        st.plotly_chart(fig_res, use_container_width=True)

    vuln_txt = resilience["top_vulnerability"]
    st.markdown(
        f'<div style="text-align:center; margin-bottom:16px;">'
        f'<span style="color:#FF9800;">Vulnerabilite principale : '
        f'<strong style="color:{res_color};">{vuln_txt}</strong></span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Breakdown scores
    breakdown = resilience["breakdown"]
    cols = st.columns(len(breakdown))
    for i, (name, data) in enumerate(breakdown.items()):
        with cols[i]:
            sc = data.get("score", 0)
            max_sc = data.get("max_score", 20)
            s_color = "#4CAF50" if sc >= max_sc * 0.7 else ("#D4AF37" if sc >= max_sc * 0.4 else "#F44336")
            st.markdown(
                f'<div style="background:rgba(19,27,46,0.7); border:1px solid rgba(255,255,255,0.07); '
                f'border-radius:10px; padding:12px; text-align:center; margin-bottom:8px;">'
                f'<div style="color:#8899BB; font-size:0.78rem;">{name}</div>'
                f'<div style="color:{s_color}; font-size:1.3rem; font-weight:700;">'
                f'{sc:.0f}/{max_sc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # 4 macro scenarios
    macro_scenarios = [
        ("Chomage 6 mois",      crisis_eng.simulate_unemployment,   "#F44336"),
        ("Urgence medicale",    crisis_eng.simulate_medical_emergency, "#FF9800"),
        ("Krach boursier -40%", crisis_eng.simulate_market_crash,   "#D4AF37"),
        ("Inflation choc +5%",  crisis_eng.simulate_inflation_shock, "#4A90D9"),
    ]

    for title, sim_fn, color in macro_scenarios:
        with st.expander(title):
            try:
                res = sim_fn()
                impact = res.get("monthly_budget_impact", res.get("wealth_impact", 0))
                months_ok = res.get("months_until_crisis", res.get("months_solvent", 0))

                c_a, c_b = st.columns(2)
                with c_a:
                    st.markdown(
                        f'<div style="color:#C8D4E8;">'
                        f'<strong>Impact mensuel :</strong> '
                        f'<span style="color:{color};">{sym}{abs(impact):,.0f}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                with c_b:
                    st.markdown(
                        f'<div style="color:#C8D4E8;">'
                        f'<strong>Mois de couverture :</strong> '
                        f'<span style="color:{color};">{months_ok}</span>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                actions = res.get("recommendations", res.get("actions", []))
                for action in actions[:4]:
                    st.markdown(
                        f'<div style="color:#8899BB; font-size:0.85rem; '
                        f'padding:4px 0;">• {action}</div>',
                        unsafe_allow_html=True,
                    )
            except Exception:
                st.info("Completez votre profil pour simuler ce scenario.")
