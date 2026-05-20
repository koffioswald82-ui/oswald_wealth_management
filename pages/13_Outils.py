"""
Outils Rapides — 3 calculateurs utiles au quotidien.
1. Puis-je me permettre ca ?
2. Simulateur de negociation salariale
3. Tracker de patrimoine net mensuel
"""
import streamlit as st
import sys
import os
import sqlite3
from datetime import datetime, date
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.constants import RISK_PROFILES
from utils.formatters import format_currency
import plotly.graph_objects as go

st.set_page_config(page_title="Outils Rapides — Oswald Wealth", page_icon="🔧", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("Creez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
uid = st.session_state.get("user_id")
annual_return = RISK_PROFILES.get(p.risk_tolerance, RISK_PROFILES["Modéré"])["expected_return"]
target_wealth = p.desired_monthly_pension * 12 / 0.04

# ── Inline SQLite for net worth log ──────────────────────
_DB = os.path.join(os.path.dirname(__file__), "..", "database", "oswald_wealth.db")


def _db():
    c = sqlite3.connect(_DB)
    c.row_factory = sqlite3.Row
    return c


def _ensure_nw_table():
    with _db() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS net_worth_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                log_date TEXT,
                net_worth REAL,
                note TEXT DEFAULT '',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)


def _save_nw(user_id, log_date, net_worth, note=""):
    with _db() as c:
        c.execute(
            "INSERT INTO net_worth_log (user_id, log_date, net_worth, note) VALUES (?,?,?,?)",
            (user_id, str(log_date), net_worth, note)
        )


def _load_nw(user_id):
    with _db() as c:
        rows = c.execute(
            "SELECT log_date, net_worth, note FROM net_worth_log "
            "WHERE user_id=? ORDER BY log_date ASC",
            (user_id,)
        ).fetchall()
    return [{"date": r["log_date"], "nw": r["net_worth"], "note": r["note"]} for r in rows]


_ensure_nw_table()

st.markdown(
    '<div class="hero-banner">'
    '<div class="hero-title">🔧 Outils Rapides</div>'
    '<div class="hero-subtitle">'
    'Trois calculateurs essentiels pour les decisions du quotidien.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["❓ Puis-je me permettre ?", "💼 Negociation salariale", "📈 Mon patrimoine net"])

# ══════════════════════════════════════════════════════════
# TAB 1 — PUIS-JE ME PERMETTRE CA ?
# ══════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Est-ce que je peux me permettre cet achat ?")
    st.markdown(
        "<div style='color:#8899BB; margin-bottom:20px;'>"
        "Entrez n'importe quel achat — l'app vous dit si c'est raisonnable "
        "et ce que ca vous coutera vraiment a long terme."
        "</div>",
        unsafe_allow_html=True,
    )

    col_in, col_out = st.columns([1, 1])
    with col_in:
        purchase_name = st.text_input("Quel achat ?", placeholder="Ex: Nouvel iPhone, Vacances, Voiture...")
        purchase_price = st.number_input(
            "Combien ca coute ? (" + sym + ")",
            min_value=0.0, value=800.0, step=50.0,
        )
        purchase_type = st.selectbox(
            "Type d'achat",
            ["Achat unique (paiement comptant)", "Mensualites (credit)"],
        )
        if "Mensualites" in purchase_type:
            monthly_payment = st.number_input(
                "Mensualite (" + sym + "/mois)", min_value=0.0, value=50.0, step=10.0
            )
            nb_months = st.slider("Duree (mois)", 3, 84, 24)
            total_cost = monthly_payment * nb_months
        else:
            monthly_payment = 0.0
            total_cost = purchase_price

    with col_out:
        current_savings_balance = p.current_savings + p.current_investments
        monthly_surplus = max(p.total_income - p.monthly_expenses, 0)
        months_to_save = (purchase_price / monthly_surplus) if monthly_surplus > 10 else 999

        # Can afford now?
        can_afford_now = current_savings_balance >= purchase_price * 1.2

        # Opportunity cost — what if invested instead
        years_left = max(p.target_retirement_age - p.age, 1)
        r_m = (1 + annual_return) ** (1 / 12) - 1
        n = years_left * 12
        if r_m > 0:
            opp_cost = purchase_price * (1 + r_m) ** n
        else:
            opp_cost = purchase_price * (1 + annual_return * years_left)

        # Impact on goal
        goal_impact_pct = purchase_price / target_wealth * 100 if target_wealth > 0 else 0

        # Verdict
        if can_afford_now and goal_impact_pct < 1:
            verdict_color = "#4CAF50"
            verdict_icon = "✅"
            verdict = "Oui, vous pouvez vous le permettre confortablement."
        elif can_afford_now and goal_impact_pct < 5:
            verdict_color = "#D4AF37"
            verdict_icon = "✅"
            verdict = "Oui, mais c'est consequent. Epargnez-le d'abord plutot que de prendre un credit."
        elif months_to_save <= 6:
            verdict_color = "#D4AF37"
            verdict_icon = "⏳"
            verdict = "Pas tout de suite. Mais dans " + str(round(months_to_save)) + " mois en epargnant votre surplus."
        elif months_to_save <= 18:
            verdict_color = "#FF9800"
            verdict_icon = "⚠️"
            verdict = "Dans " + str(round(months_to_save)) + " mois. Considerez si c'est vraiment prioritaire."
        else:
            verdict_color = "#F44336"
            verdict_icon = "❌"
            verdict = "Ce n'est pas le bon moment. Renforcez vos bases financieres d'abord."

        st.markdown(
            f'<div style="background:rgba(19,27,46,0.9); border:2px solid {verdict_color}; '
            f'border-radius:14px; padding:20px; margin-bottom:16px; text-align:center;">'
            f'<div style="font-size:2.5rem; margin-bottom:8px;">{verdict_icon}</div>'
            f'<div style="color:{verdict_color}; font-size:1.1rem; font-weight:700;">{verdict}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        opp_cost_fmt = format_currency(opp_cost, cur, compact=True)
        total_cost_fmt = sym + str(round(total_cost))
        months_save_display = "Maintenant" if months_to_save < 1 else str(round(months_to_save)) + " mois"

        st.markdown(
            f'<div style="background:rgba(19,27,46,0.7); border-radius:10px; padding:14px;">'
            f'<div style="display:flex; justify-content:space-between; padding:6px 0; '
            f'border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<span style="color:#8899BB;">Cout total</span>'
            f'<span style="color:#E8E8E8; font-weight:600;">{total_cost_fmt}</span>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; padding:6px 0; '
            f'border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<span style="color:#8899BB;">Atteignable sans credit dans</span>'
            f'<span style="color:#D4AF37; font-weight:600;">{months_save_display}</span>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; padding:6px 0; '
            f'border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<span style="color:#8899BB;">Impact sur objectif retraite</span>'
            f'<span style="color:#FF9800; font-weight:600;">{goal_impact_pct:.1f}%</span>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; padding:6px 0;">'
            f'<span style="color:#8899BB;">Cout d\'opportunite a {p.target_retirement_age} ans</span>'
            f'<span style="color:#F44336; font-weight:600;">{opp_cost_fmt}</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.caption(
            "Le cout d'opportunite est ce que cet argent aurait valu si investi "
            "jusqu'a votre retraite a " + str(annual_return * 100) + "% de rendement annuel."
        )


# ══════════════════════════════════════════════════════════
# TAB 2 — NEGOCIATION SALARIALE
# ══════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Simulateur de negociation salariale")
    st.markdown(
        "<div style='color:#8899BB; margin-bottom:20px;'>"
        "La negociation salariale est la decision financiere a plus fort retour sur investissement. "
        "Voyez l'impact sur toute votre carriere."
        "</div>",
        unsafe_allow_html=True,
    )

    col_sal, col_res = st.columns([1, 1])
    with col_sal:
        current_salary = st.number_input(
            "Salaire mensuel net actuel (" + sym + ")",
            min_value=0.0, value=float(p.monthly_income), step=100.0,
        )
        target_salary = st.number_input(
            "Salaire vise apres negociation (" + sym + ")",
            min_value=0.0, value=float(p.monthly_income * 1.10), step=100.0,
        )
        growth_pct = st.slider(
            "Croissance salariale annuelle attendue (%)",
            min_value=0.0, max_value=10.0, value=2.0, step=0.5,
        )
        years_career = max(p.target_retirement_age - p.age, 1)

    with col_res:
        monthly_gain = target_salary - current_salary
        if monthly_gain <= 0:
            st.info("Le salaire vise doit etre superieur au salaire actuel.")
        else:
            annual_gain = monthly_gain * 12
            r_m_sal = (1 + annual_return) ** (1 / 12) - 1
            n_sal = years_career * 12

            # Cumulative salary earned (with annual growth, compounded)
            cum_current = 0.0
            cum_target = 0.0
            sal_c = current_salary
            sal_t = target_salary
            for yr in range(years_career):
                cum_current += sal_c * 12
                cum_target += sal_t * 12
                sal_c *= (1 + growth_pct / 100)
                sal_t *= (1 + growth_pct / 100)

            lifetime_gain = cum_target - cum_current

            # If the gain is invested each month
            if r_m_sal > 0:
                invested_fv = monthly_gain * ((1 + r_m_sal) ** n_sal - 1) / r_m_sal
            else:
                invested_fv = monthly_gain * n_sal

            lifetime_fmt = format_currency(lifetime_gain, cur, compact=True)
            invested_fmt = format_currency(invested_fv, cur, compact=True)

            st.markdown(
                f'<div style="background:rgba(19,27,46,0.9); border:2px solid #4CAF50; '
                f'border-radius:14px; padding:20px; margin-bottom:12px; text-align:center;">'
                f'<div style="color:#8899BB; font-size:0.85rem;">Gain mensuel</div>'
                f'<div style="color:#4CAF50; font-size:2.5rem; font-weight:800;">'
                f'+{sym}{monthly_gain:,.0f}/mois</div>'
                f'<div style="color:#8899BB; font-size:0.85rem; margin-top:4px;">'
                f'+{sym}{annual_gain:,.0f}/an</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div style="background:rgba(19,27,46,0.7); border-radius:10px; padding:14px;">'
                f'<div style="display:flex; justify-content:space-between; padding:8px 0; '
                f'border-bottom:1px solid rgba(255,255,255,0.05);">'
                f'<span style="color:#8899BB;">Gain cumule sur {years_career} ans de carriere</span>'
                f'<span style="color:#D4AF37; font-weight:700;">{lifetime_fmt}</span>'
                f'</div>'
                f'<div style="display:flex; justify-content:space-between; padding:8px 0;">'
                f'<span style="color:#8899BB;">Si ce gain est investi</span>'
                f'<span style="color:#4CAF50; font-weight:700; font-size:1.05rem;">{invested_fmt}</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f'<div style="background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.25); '
                f'border-radius:10px; padding:12px; margin-top:10px;">'
                f'<div style="color:#D4AF37; font-weight:600; margin-bottom:4px;">'
                f'Ne jamais accepter la premiere offre</div>'
                f'<div style="color:#C8D4E8; font-size:0.88rem;">'
                f'En moyenne, une negociation salariale reussie apporte +{sym}{monthly_gain:,.0f}/mois. '
                f'Sur votre carriere, c\'est {lifetime_fmt} de revenus supplementaires — '
                f'sans changer votre style de vie.'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Chart: cumulative gain over years
            years_x = list(range(1, years_career + 1))
            cum_gains = []
            running = 0.0
            mg = monthly_gain
            for yr in years_x:
                running += mg * 12
                mg *= (1 + growth_pct / 100)
                cum_gains.append(running)

            fig_sal = go.Figure()
            fig_sal.add_trace(go.Scatter(
                x=years_x, y=cum_gains,
                fill="tozeroy", name="Gain cumule",
                line=dict(color="#4CAF50", width=2.5),
                fillcolor="rgba(76,175,80,0.12)",
            ))
            fig_sal.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=240, margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(title="Annees de carriere"),
                yaxis=dict(title="Gain cumule (" + cur + ")"),
            )
            st.plotly_chart(fig_sal, use_container_width=True)


# ══════════════════════════════════════════════════════════
# TAB 3 — TRACKER PATRIMOINE NET
# ══════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Tracker de patrimoine net")
    st.markdown(
        "<div style='color:#8899BB; margin-bottom:20px;'>"
        "Enregistrez votre patrimoine net chaque mois. "
        "Voir la courbe monter est la meilleure motivation financiere qui soit."
        "</div>",
        unsafe_allow_html=True,
    )

    nw_history = _load_nw(uid) if uid else []

    # Add entry
    col_add, col_hist = st.columns([1, 2])
    with col_add:
        st.markdown("#### Enregistrer aujourd'hui")
        today_date = st.date_input("Date", value=date.today())

        # Compute current net worth from profile as default
        default_nw = p.current_net_worth
        new_nw = st.number_input(
            "Patrimoine net (" + sym + ")",
            value=float(default_nw),
            step=100.0,
            help="Actifs (epargne + investissements + immobilier) - Dettes",
        )
        nw_note = st.text_input("Note (optionnel)", placeholder="Ex: Recu prime, rembourse credit...")
        if st.button("Enregistrer", type="primary"):
            if uid:
                _save_nw(uid, today_date, new_nw, nw_note)
                st.success("Patrimoine enregistre !")
                st.rerun()
            else:
                st.error("Selectionnez un profil.")

        st.markdown(
            "<div style='margin-top:12px; color:#8899BB; font-size:0.82rem;'>"
            "Composantes du patrimoine net :<br>"
            "Epargne + Investissements + Immobilier − Dettes"
            "</div>",
            unsafe_allow_html=True,
        )

    with col_hist:
        if not nw_history:
            st.info(
                "Aucun historique. Enregistrez votre premier point pour voir la courbe de progression."
            )
        else:
            # Chart
            dates_x = [h["date"] for h in nw_history]
            nw_y = [h["nw"] for h in nw_history]
            latest = nw_y[-1] if nw_y else 0
            first = nw_y[0] if nw_y else 0
            total_growth = latest - first
            g_color = "#4CAF50" if total_growth >= 0 else "#F44336"

            st.markdown(
                f'<div style="display:flex; gap:24px; margin-bottom:12px;">'
                f'<div>'
                f'<div style="color:#8899BB; font-size:0.8rem;">Patrimoine actuel</div>'
                f'<div style="color:#D4AF37; font-size:1.4rem; font-weight:700;">'
                f'{sym}{latest:,.0f}</div>'
                f'</div>'
                f'<div>'
                f'<div style="color:#8899BB; font-size:0.8rem;">Progression totale</div>'
                f'<div style="color:{g_color}; font-size:1.4rem; font-weight:700;">'
                f'{"+" if total_growth >= 0 else ""}{sym}{total_growth:,.0f}</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            fig_nw = go.Figure()
            fig_nw.add_trace(go.Scatter(
                x=dates_x, y=nw_y,
                mode="lines+markers",
                name="Patrimoine net",
                fill="tozeroy",
                line=dict(color="#D4AF37", width=2.5),
                fillcolor="rgba(212,175,55,0.10)",
                marker=dict(size=7, color="#D4AF37"),
            ))
            fig_nw.add_hline(
                y=target_wealth, line_dash="dash", line_color="#4CAF50",
                annotation_text="Objectif",
                annotation_font_color="#4CAF50",
            )
            fig_nw.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, margin=dict(l=0, r=0, t=10, b=0),
                yaxis=dict(title=cur),
                showlegend=False,
            )
            st.plotly_chart(fig_nw, use_container_width=True)

            # Milestones reached
            milestones_nw = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
            reached = [m for m in milestones_nw if latest >= m]
            next_ms = next((m for m in milestones_nw if latest < m), None)

            if reached:
                last_reached = reached[-1]
                st.markdown(
                    f'<div style="background:rgba(212,175,55,0.08); '
                    f'border:1px solid rgba(212,175,55,0.3); '
                    f'border-radius:10px; padding:12px; text-align:center;">'
                    f'<div style="color:#D4AF37; font-weight:600;">🏆 Jalon atteint</div>'
                    f'<div style="color:#E8E8E8; font-size:1.1rem; font-weight:700;">'
                    f'{sym}{last_reached:,.0f}</div>'
                    f'{"<div style=color:#8899BB;font-size:0.82rem;>Prochain jalon : " + sym + str(next_ms) + "</div>" if next_ms else ""}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
