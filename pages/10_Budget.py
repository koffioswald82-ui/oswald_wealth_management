"""
MON BUDGET — Suivi mensuel mois par mois.
Règle 50/30/20. Historique persistant. Plan progressif d'épargne.
"""
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.budget_engine import BudgetEngine, BUDGET_CATEGORIES
from engines.progressive_plan import ProgressivePlanEngine, MONTH_FR
from database.db_manager import DatabaseManager
from utils.constants import RISK_PROFILES
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(page_title="Mon Budget — Oswald Wealth", page_icon="💳", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("👈 Créez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
bud = BudgetEngine(p)
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
db = DatabaseManager()
db.initialize()
uid = st.session_state.get("user_id")
annual_return = RISK_PROFILES.get(p.risk_tolerance, RISK_PROFILES["Modéré"])["expected_return"]
target_wealth = p.desired_monthly_pension * 12 / 0.04
pp = ProgressivePlanEngine(p)
today = datetime.now()

savings_history = db.load_savings_history(uid) if uid else []

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">💳 Mon Budget Mensuel</div>
    <div class="hero-subtitle">
        Suivez vos dépenses mois par mois. Chaque euro épargné vous rapproche de votre objectif.
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📅 Ce Mois-ci", "📈 Mon Plan d'Épargne", "📊 Historique"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — CE MOIS-CI
# ══════════════════════════════════════════════════════════════
with tab1:
    col_sel, col_income = st.columns([2, 3])
    with col_sel:
        sel_year = st.selectbox(
            "Année", [today.year - 1, today.year, today.year + 1],
            index=1, key="sel_year"
        )
        sel_month = st.selectbox(
            "Mois", list(range(1, 13)),
            format_func=lambda m: MONTH_FR[m],
            index=today.month - 1, key="sel_month"
        )
    with col_income:
        st.markdown(
            f'<div style="background:rgba(19,27,46,0.8); border:1px solid rgba(212,175,55,0.2);'
            f'border-radius:12px; padding:16px 24px; margin-top:8px;">'
            f'<span style="color:#8899BB;">Revenu mensuel : </span>'
            f'<span style="color:#D4AF37; font-size:1.4rem; font-weight:700;">{sym}{p.total_income:,.0f}</span>'
            f'<span style="color:#8899BB; font-size:0.85rem;"> · Règle 50/30/20</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    month_label = MONTH_FR[sel_month] + " " + str(sel_year)
    saved_budget = db.load_monthly_budget(uid, sel_year, sel_month) if uid else {}

    st.markdown("---")

    quick_mode = st.toggle("⚡ Mode rapide — tout était comme prévu ce mois-ci", value=False)

    actual_spending = {}

    if quick_mode:
        rec = bud.recommended_budget()
        for group_data in rec.values():
            for cat, data in group_data.items():
                actual_spending[cat] = saved_budget.get(cat, data["recommended"])
        st.info("Budget rempli avec les montants recommandés. Enregistrez pour valider le mois.")
    else:
        st.markdown(f"### Dépenses réelles — {month_label}")
        st.markdown(
            "<div style='color:#8899BB; font-size:0.85rem; margin-bottom:16px;'>"
            "Modifiez uniquement les catégories qui ont changé — les autres sont pré-remplis "
            "avec votre budget habituel ou les montants recommandés."
            "</div>",
            unsafe_allow_html=True,
        )

        for group_name, cats in BUDGET_CATEGORIES.items():
            if "Essentiels" in group_name:
                group_color = "#D4AF37"
            elif "Envies" in group_name:
                group_color = "#4A90D9"
            else:
                group_color = "#4CAF50"

            st.markdown(
                f'<div style="border-left:4px solid {group_color}; padding-left:12px; margin:20px 0 12px;">'
                f'<span style="font-size:1.05rem; font-weight:600; color:{group_color};">{group_name}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

            cols = st.columns(3)
            for i, (cat_name, cat_data) in enumerate(cats.items()):
                rec_amount = round(p.total_income * cat_data["pct"])
                saved_val = saved_budget.get(cat_name, float(rec_amount))
                with cols[i % 3]:
                    val = st.number_input(
                        cat_name,
                        min_value=0.0,
                        max_value=float(p.total_income * 2),
                        value=float(saved_val),
                        step=10.0,
                        key=f"bgt_{sel_year}_{sel_month}_{cat_name}",
                    )
                    actual_spending[cat_name] = val

    analysis = bud.analyze_budget(actual_spending)

    col_save, _ = st.columns([1, 3])
    with col_save:
        if st.button("💾 Enregistrer " + month_label, use_container_width=True, type="primary"):
            if uid:
                db.save_monthly_budget(uid, sel_year, sel_month, actual_spending)
                plan_target = pp.full_required_monthly(
                    target_wealth, p.target_retirement_age, annual_return
                )
                db.save_savings_entry(
                    uid, sel_year, sel_month,
                    round(plan_target), round(analysis["total_savings"])
                )
                st.success("Budget " + month_label + " enregistré !")
                st.rerun()
            else:
                st.error("Sélectionnez un profil d'abord.")

    st.markdown("---")
    st.markdown("### Bilan du mois")

    score = analysis["compliance_score"]
    score_color = "#4CAF50" if score >= 75 else ("#D4AF37" if score >= 50 else "#F44336")
    score_label = ("Excellent" if score >= 75
                   else ("Bon" if score >= 50 else ("À améliorer" if score >= 30 else "Critique")))
    surplus = analysis["surplus"]
    s_color = "#4CAF50" if surplus >= 0 else "#F44336"
    surplus_label = "Surplus" if surplus >= 0 else "Déficit"
    sav_pct = analysis["ratio_savings"]
    sav_color = "#4CAF50" if sav_pct >= 0.18 else ("#D4AF37" if sav_pct >= 0.10 else "#F44336")
    total = analysis["total_actual"]
    t_color = "#4CAF50" if total <= p.total_income else "#F44336"
    total_savings_fmt = format_currency(analysis["total_savings"], cur, compact=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Score budget</div>'
            f'<div class="kpi-value" style="color:{score_color};">{score:.0f}/100</div>'
            f'<div style="color:{score_color}; font-size:0.85rem;">{score_label}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">{surplus_label}</div>'
            f'<div class="kpi-value" style="color:{s_color};">{sym}{abs(surplus):,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.8rem;">ce mois</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Épargné</div>'
            f'<div class="kpi-value" style="color:{sav_color};">{sav_pct*100:.0f}%</div>'
            f'<div style="color:#8899BB; font-size:0.8rem;">{total_savings_fmt} · cible 20%</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f'<div class="kpi-card">'
            f'<div class="kpi-label">Total dépensé</div>'
            f'<div class="kpi-value" style="color:{t_color};">{sym}{total:,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.8rem;">sur {sym}{p.total_income:,.0f}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    msg = bud.simple_budget_message(analysis, cur)
    if "✅" in msg:
        st.success(msg)
    elif "⚠️" in msg:
        st.warning(msg)
    else:
        st.error(msg)

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**Répartition réelle vs recommandée**")
        cats_bar = ["🏠 Besoins", "🎯 Envies", "💰 Épargne"]
        actual_vals = [
            analysis["ratio_essential"] * 100,
            analysis["ratio_lifestyle"] * 100,
            analysis["ratio_savings"] * 100,
        ]
        target_vals = [50, 30, 20]
        bar_colors = [
            "#4CAF50" if abs(a - t) <= 5 else ("#FF9800" if abs(a - t) <= 10 else "#F44336")
            for a, t in zip(actual_vals, target_vals)
        ]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Votre répartition", x=cats_bar, y=actual_vals,
            marker_color=bar_colors,
            text=[f"{v:.0f}%" for v in actual_vals], textposition="outside",
        ))
        fig.add_trace(go.Scatter(
            name="Cible 50/30/20", x=cats_bar, y=target_vals, mode="markers+lines",
            line=dict(color="#D4AF37", dash="dash", width=2),
            marker=dict(size=10, color="#D4AF37"),
        ))
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=280, margin=dict(l=0, r=0, t=20, b=0),
            yaxis=dict(range=[0, 70]),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.3),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("**Détail par catégorie**")
        for cat, data in analysis["breakdown"].items():
            pct_used = data["pct_used"]
            bar_color = "#4CAF50" if pct_used <= 1.0 else ("#FF9800" if pct_used <= 1.20 else "#F44336")
            ca, cb, cc = st.columns([3, 4, 1])
            with ca:
                st.markdown(
                    f'<div style="font-size:0.82rem; color:#C8D4E8; padding-top:4px;">{cat}</div>',
                    unsafe_allow_html=True,
                )
            with cb:
                st.progress(min(pct_used, 1.5) / 1.5)
            with cc:
                st.markdown(
                    f'<div style="color:{bar_color}; font-size:0.85rem; font-weight:700;">'
                    f'{data["status"]}</div>',
                    unsafe_allow_html=True,
                )

    opps = bud.top_savings_opportunities(actual_spending)
    if opps:
        st.markdown("---")
        st.markdown("### 🎯 Où économiser pour progresser vers votre objectif ?")
        for opp in opps:
            impact = bud.budget_goal_impact(
                opp["monthly_saving"], target_wealth,
                p.target_retirement_age, annual_return
            )
            fv_fmt = format_currency(impact["future_value"], cur, compact=True)
            st.markdown(
                f'<div class="insight-card warning" style="margin-bottom:10px;">'
                f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                f'<div>'
                f'<div style="font-weight:600; color:#FF9800;">{opp["category"]}</div>'
                f'<div style="color:#C8D4E8; font-size:0.9rem; margin-top:4px;">'
                f'Vous dépensez {sym}{opp["actual"]:,.0f} · recommandé {sym}{opp["recommended"]:,.0f}'
                f' · économie possible <strong style="color:#FF9800;">{sym}{opp["monthly_saving"]:,.0f}/mois</strong>'
                f'</div>'
                f'</div>'
                f'<div style="text-align:right; min-width:160px;">'
                f'<div style="color:#4CAF50; font-weight:700; font-size:1rem;">+{fv_fmt}</div>'
                f'<div style="color:#8899BB; font-size:0.8rem;">à votre objectif final</div>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════
# TAB 2 — MON PLAN D'ÉPARGNE
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Choisissez votre rythme d'épargne")
    st.markdown(
        "<div style='color:#8899BB; margin-bottom:20px;'>"
        "Pas besoin d'épargner tout d'un coup. Choisissez un plan adapté à votre situation — "
        "vous pourrez accélérer quand vous serez prêt(e)."
        "</div>",
        unsafe_allow_html=True,
    )

    plans = pp.build_progressive_plans(target_wealth, p.target_retirement_age, annual_return)
    required = pp.full_required_monthly(target_wealth, p.target_retirement_age, annual_return)
    plan_names = [pl["icon"] + " " + pl["name"] for pl in plans]

    sel_plan_idx = st.radio(
        "Plan", plan_names, horizontal=True,
        index=0, label_visibility="collapsed"
    )
    selected_plan = plans[plan_names.index(sel_plan_idx)]

    months_delayed = selected_plan["months_delayed"]
    if months_delayed == 0:
        delay_text = "Objectif atteint à la date prévue"
    else:
        yrs_late = months_delayed // 12
        m_late = months_delayed % 12
        if yrs_late > 0 and m_late > 0:
            delay_text = "Objectif atteint environ " + str(yrs_late) + " an(s) et " + str(m_late) + " mois plus tard"
        elif yrs_late > 0:
            delay_text = "Objectif atteint environ " + str(yrs_late) + " an(s) plus tard"
        else:
            delay_text = "Objectif atteint environ " + str(m_late) + " mois plus tard"

    st.markdown(
        f'<div style="background:rgba(19,27,46,0.8); border:2px solid {selected_plan["color"]}; '
        f'border-radius:12px; padding:20px; margin:16px 0;">'
        f'<div style="font-size:1.2rem; font-weight:700; color:{selected_plan["color"]}; margin-bottom:8px;">'
        f'{selected_plan["icon"]} {selected_plan["name"]}</div>'
        f'<div style="color:#C8D4E8; margin-bottom:10px;">{selected_plan["description"]}</div>'
        f'<div style="color:#8899BB; font-size:0.85rem;">{delay_text}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("#### Combien épargner chaque année ?")
    years_left = max(p.target_retirement_age - p.age, 1)
    display_years = min(years_left, 5)
    year_items = list(selected_plan["year_targets"].items())[:display_years]
    year_cols = st.columns(display_years)

    for i, (yr_num, yr_target) in enumerate(year_items):
        pct_of_full = yr_target / required * 100 if required > 0 else 100
        c = "#4CAF50" if pct_of_full >= 95 else ("#D4AF37" if pct_of_full >= 60 else "#4A90D9")
        age_start = p.age + yr_num - 1
        age_end = p.age + yr_num
        if yr_num == 3 and selected_plan["start_pct"] < 60:
            yr_label = "Année discipline"
        else:
            yr_label = "Année " + str(yr_num)
        with year_cols[i]:
            st.markdown(
                f'<div style="background:rgba(19,27,46,0.8); border:1px solid {c}; '
                f'border-radius:10px; padding:14px; text-align:center; margin-bottom:8px;">'
                f'<div style="color:#8899BB; font-size:0.72rem;">'
                f'{yr_label} · {age_start}→{age_end} ans</div>'
                f'<div style="color:{c}; font-size:1.3rem; font-weight:800;">{sym}{yr_target:,.0f}</div>'
                f'<div style="color:#8899BB; font-size:0.72rem;">/mois</div>'
                f'<div style="color:{c}; font-size:0.72rem; margin-top:4px;">{pct_of_full:.0f}% du plan complet</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if years_left > 5:
        st.caption(
            "... à partir de l'année 6 et jusqu'à " + str(p.target_retirement_age)
            + " ans : " + sym + str(int(required)) + "/mois."
        )

    st.markdown("---")
    st.markdown("#### Votre situation actuelle")

    catchup = pp.catch_up_analysis(savings_history, annual_return)
    status_colors = {
        "excellent": "#4CAF50", "good": "#D4AF37",
        "warning": "#FF9800", "discipline_year": "#F44336", "on_track": "#4CAF50",
    }
    sc = status_colors.get(catchup["status"], "#8899BB")

    catchup_detail = ""
    if catchup["shortfall"] > 0:
        catchup_detail = (
            f'<div style="margin-top:10px; color:#C8D4E8; font-size:0.9rem;">'
            f'Retard total : <strong style="color:#FF9800;">{sym}{catchup["shortfall"]:,.0f}</strong>'
            f' · Rattrapage suggéré : <strong style="color:#D4AF37;">'
            f'+{sym}{catchup["catch_up_monthly"]:,.0f}/mois</strong>'
            f'</div>'
        )

    st.markdown(
        f'<div style="background:rgba(19,27,46,0.8); border-left:4px solid {sc}; '
        f'border-radius:0 12px 12px 0; padding:16px 20px; margin:8px 0;">'
        f'<div style="color:{sc}; font-weight:600; font-size:1rem;">{catchup["message"]}</div>'
        f'{catchup_detail}'
        f'</div>',
        unsafe_allow_html=True,
    )

    if not savings_history:
        st.info(
            "Aucun mois enregistré pour l'instant. "
            "Renseignez votre budget dans l'onglet 'Ce Mois-ci' pour voir votre suivi ici."
        )


# ══════════════════════════════════════════════════════════════
# TAB 3 — HISTORIQUE
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Votre historique d'épargne")

    if not savings_history:
        st.info(
            "Aucun historique enregistré. "
            "Commencez par renseigner votre budget du mois dans l'onglet 'Ce Mois-ci'."
        )
    else:
        recap = pp.yearly_recap(savings_history)
        if recap:
            st.markdown("#### Bilan par année")
            for yr in recap:
                pct = yr["achievement_pct"]
                st.markdown(
                    f'<div style="background:rgba(19,27,46,0.8); border:1px solid rgba(255,255,255,0.08); '
                    f'border-radius:10px; padding:14px 20px; margin-bottom:10px; '
                    f'display:flex; justify-content:space-between; align-items:center;">'
                    f'<div>'
                    f'<div style="color:#E8E8E8; font-weight:700;">{yr["year"]}</div>'
                    f'<div style="color:#8899BB; font-size:0.82rem;">{yr["months"]} mois enregistrés</div>'
                    f'</div>'
                    f'<div style="text-align:center;">'
                    f'<div style="color:#C8D4E8;">Objectif : {sym}{yr["target_total"]:,.0f}</div>'
                    f'<div style="color:#D4AF37; font-weight:700;">Réalisé : {sym}{yr["actual_total"]:,.0f}</div>'
                    f'</div>'
                    f'<div style="text-align:right;">'
                    f'<div style="color:{yr["label_color"]}; font-size:1.4rem; font-weight:800;">{pct:.0f}%</div>'
                    f'<div style="color:{yr["label_color"]}; font-size:0.85rem;">'
                    f'{yr["label_icon"]} {yr["label"]}</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("#### Épargne réelle vs objectif — mois par mois")

        labels = [MONTH_FR[h["month"]][:3] + " " + str(h["year"]) for h in savings_history]
        targets = [h["target"] for h in savings_history]
        actuals = [h["actual"] for h in savings_history]
        bar_colors_hist = [
            "#4CAF50" if a >= t else ("#FF9800" if a >= t * 0.75 else "#F44336")
            for a, t in zip(actuals, targets)
        ]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Épargne réelle", x=labels, y=actuals, marker_color=bar_colors_hist,
        ))
        fig2.add_trace(go.Scatter(
            name="Objectif du plan", x=labels, y=targets, mode="lines+markers",
            line=dict(color="#D4AF37", dash="dash", width=2),
            marker=dict(size=8, color="#D4AF37"),
        ))
        fig2.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            yaxis=dict(title="Épargne (" + cur + ")"),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.3),
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.markdown("#### Cumul de votre épargne dans le temps")

        cum_target = 0.0
        cum_actual = 0.0
        cum_labels, cum_targets_list, cum_actuals_list = [], [], []
        for h in savings_history:
            cum_target += h["target"]
            cum_actual += h["actual"]
            cum_labels.append(MONTH_FR[h["month"]][:3] + " " + str(h["year"]))
            cum_targets_list.append(cum_target)
            cum_actuals_list.append(cum_actual)

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=cum_labels, y=cum_actuals_list, name="Votre épargne cumulée",
            fill="tozeroy", line=dict(color="#4CAF50", width=2.5),
            fillcolor="rgba(76,175,80,0.12)",
        ))
        fig3.add_trace(go.Scatter(
            x=cum_labels, y=cum_targets_list, name="Objectif cumulé",
            line=dict(color="#D4AF37", dash="dash", width=2),
        ))
        fig3.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=260, margin=dict(l=0, r=0, t=10, b=0),
            legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.3),
        )
        st.plotly_chart(fig3, use_container_width=True)
