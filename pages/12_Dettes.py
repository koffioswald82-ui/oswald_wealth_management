"""
Gestion des Dettes — Avalanche vs Boule de neige.
Montre le chemin le plus court et le moins cher vers la liberte financiere.
"""
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.debt_engine import DebtEngine
from utils.formatters import format_currency
from utils.constants import RISK_PROFILES
import plotly.graph_objects as go

st.set_page_config(page_title="Mes Dettes — Oswald Wealth", page_icon="💳", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("Creez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
annual_return = RISK_PROFILES.get(p.risk_tolerance, RISK_PROFILES["Modéré"])["expected_return"]

st.markdown(
    '<div class="hero-banner">'
    '<div class="hero-title">💳 Mes Dettes</div>'
    '<div class="hero-subtitle">'
    'Chaque euro de dette vous coute de l\'argent chaque mois. '
    'Voici le chemin le plus rapide vers la liberte financiere.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ── Session state for debt list ───────────────────────────
if "debts" not in st.session_state:
    # Pre-fill from profile if they have debt declared
    if p.current_debt > 0:
        st.session_state.debts = [{
            "name": "Ma dette principale",
            "balance": float(p.current_debt),
            "rate_annual": 0.06,
            "min_payment": float(p.monthly_debt_payment) if p.monthly_debt_payment > 0 else round(p.current_debt * 0.02),
        }]
    else:
        st.session_state.debts = []

st.markdown("### Entrez vos dettes")
st.markdown(
    "<div style='color:#8899BB; font-size:0.88rem; margin-bottom:12px;'>"
    "Incluez TOUTES vos dettes : credit conso, auto, etudiant, decouvert, BNPL..."
    "</div>",
    unsafe_allow_html=True,
)

# Add new debt form
with st.expander("➕ Ajouter une dette", expanded=len(st.session_state.debts) == 0):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        new_name = st.text_input("Nom de la dette", placeholder="Ex: Credit conso Cetelem")
    with col2:
        new_balance = st.number_input("Capital restant (" + sym + ")", min_value=0.0, value=1000.0, step=100.0)
    with col3:
        new_rate = st.number_input("Taux annuel (%)", min_value=0.0, max_value=100.0, value=8.0, step=0.5)
    with col4:
        new_min = st.number_input("Paiement minimum/mois (" + sym + ")", min_value=1.0, value=max(round(new_balance * 0.02), 20.0), step=10.0)
    if st.button("Ajouter cette dette", type="primary"):
        if new_name and new_balance > 0:
            st.session_state.debts.append({
                "name": new_name,
                "balance": float(new_balance),
                "rate_annual": float(new_rate) / 100,
                "min_payment": float(new_min),
            })
            st.rerun()

# Show existing debts
if not st.session_state.debts:
    st.info("Aucune dette ajoutee. Vous etes libre(e) — ou renseignez vos dettes ci-dessus.")
    st.stop()

# Debt table
st.markdown("#### Vos dettes actuelles")
total_balance = sum(d["balance"] for d in st.session_state.debts)
annual_interest_cost = sum(d["balance"] * d["rate_annual"] for d in st.session_state.debts)
monthly_interest_cost = annual_interest_cost / 12

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Total des dettes</div>'
        f'<div class="kpi-value" style="color:#F44336;">{sym}{total_balance:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Interets payes / mois</div>'
        f'<div class="kpi-value" style="color:#FF9800;">{sym}{monthly_interest_cost:,.0f}</div>'
        f'<div style="color:#8899BB; font-size:0.8rem;">{sym}{annual_interest_cost:,.0f} par an</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c3:
    total_min = sum(d["min_payment"] for d in st.session_state.debts)
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Paiements minimum / mois</div>'
        f'<div class="kpi-value" style="color:#D4AF37;">{sym}{total_min:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

to_remove = None
for i, d in enumerate(st.session_state.debts):
    rate_pct = d["rate_annual"] * 100
    rate_color = "#F44336" if rate_pct > 10 else ("#FF9800" if rate_pct > 5 else "#4CAF50")
    col_a, col_b, col_c, col_d, col_e = st.columns([3, 2, 2, 2, 1])
    with col_a:
        st.markdown(
            f'<div style="font-size:0.9rem; color:#E8E8E8; padding-top:8px;">'
            f'<strong>{d["name"]}</strong></div>',
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f'<div style="font-size:0.9rem; color:#F44336; padding-top:8px;">'
            f'{sym}{d["balance"]:,.0f}</div>',
            unsafe_allow_html=True,
        )
    with col_c:
        st.markdown(
            f'<div style="font-size:0.9rem; color:{rate_color}; padding-top:8px;">'
            f'{rate_pct:.1f}%/an</div>',
            unsafe_allow_html=True,
        )
    with col_d:
        st.markdown(
            f'<div style="font-size:0.9rem; color:#D4AF37; padding-top:8px;">'
            f'{sym}{d["min_payment"]:,.0f}/mois</div>',
            unsafe_allow_html=True,
        )
    with col_e:
        if st.button("🗑️", key="del_" + str(i)):
            to_remove = i

if to_remove is not None:
    st.session_state.debts.pop(to_remove)
    st.rerun()

# ── Strategy selector ─────────────────────────────────────
st.markdown("---")
st.markdown("### Choisissez votre strategie de remboursement")

col_strat, col_extra = st.columns([2, 2])
with col_strat:
    strategy_choice = st.radio(
        "Strategie",
        ["Avalanche (taux le plus eleve en premier)", "Boule de neige (dette la plus petite en premier)"],
        help="Avalanche = economise le plus d'interets. Boule de neige = motivation psychologique plus rapide.",
    )
    strategy = "avalanche" if "Avalanche" in strategy_choice else "snowball"

with col_extra:
    extra = st.slider(
        "Paiement supplementaire / mois (" + sym + ")",
        min_value=0, max_value=int(p.total_income * 0.3),
        value=0, step=25,
        help="Chaque euro supplementaire accelere dramatiquement le remboursement.",
    )

# ── Results ───────────────────────────────────────────────
st.markdown("---")

comparison = DebtEngine.compare_strategies(st.session_state.debts, extra_monthly=extra)
chosen = comparison["avalanche"] if strategy == "avalanche" else comparison["snowball"]
other = comparison["snowball"] if strategy == "avalanche" else comparison["avalanche"]

months = chosen["total_months"]
years_n = months // 12
months_rem = months % 12
total_int = chosen["total_interest"]

if years_n > 0 and months_rem > 0:
    time_label = str(years_n) + " ans et " + str(months_rem) + " mois"
elif years_n > 0:
    time_label = str(years_n) + " ans"
else:
    time_label = str(months_rem) + " mois"

# Savings vs minimum only
min_only = DebtEngine.minimum_only(st.session_state.debts)
interest_saved = min_only["total_interest"] - total_int
months_saved = min_only["total_months"] - months

st.markdown("#### Resultats avec votre strategie")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Libre de dettes dans</div>'
        f'<div class="kpi-value" style="color:#4CAF50;">{time_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Total interets payes</div>'
        f'<div class="kpi-value" style="color:#F44336;">{sym}{total_int:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c3:
    gain_color = "#4CAF50" if interest_saved > 0 else "#8899BB"
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Economies vs paiements min.</div>'
        f'<div class="kpi-value" style="color:{gain_color};">{sym}{max(interest_saved,0):,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with c4:
    years_to_invest = max(p.target_retirement_age - p.age - months // 12, 1)
    total_freed = sum(d["min_payment"] for d in st.session_state.debts) + extra
    invest_fv = DebtEngine.investment_impact(total_freed, years_to_invest, annual_return)
    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-label">Si on investit ces {sym}{total_freed:,.0f}/mois apres</div>'
        f'<div class="kpi-value" style="color:#D4AF37;">'
        f'{format_currency(invest_fv, cur, compact=True)}</div>'
        f'<div style="color:#8899BB; font-size:0.75rem;">potentiel sur {years_to_invest} ans</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# Payoff order
if chosen["payoff_order"]:
    st.markdown("#### Ordre de liberation")
    order_cols = st.columns(len(chosen["payoff_order"]))
    for i, po in enumerate(chosen["payoff_order"]):
        m = po["month"]
        y = m // 12
        mr = m % 12
        if y > 0 and mr > 0:
            when = str(y) + "a " + str(mr) + "m"
        elif y > 0:
            when = str(y) + " ans"
        else:
            when = str(mr) + " mois"
        with order_cols[i]:
            st.markdown(
                f'<div style="background:rgba(19,27,46,0.8); border:1px solid rgba(212,175,55,0.2); '
                f'border-radius:10px; padding:12px; text-align:center;">'
                f'<div style="color:#D4AF37; font-size:1.3rem; font-weight:800;">#{i+1}</div>'
                f'<div style="color:#E8E8E8; font-size:0.88rem;">{po["name"]}</div>'
                f'<div style="color:#4CAF50; font-size:0.82rem; margin-top:4px;">'
                f'Solde dans {when}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

# ── Payoff chart ──────────────────────────────────────────
st.markdown("---")
st.markdown("#### Evolution de vos soldes dans le temps")

if chosen["schedule"]:
    debt_names = list(st.session_state.debts[0]["name"] and
                      [d["name"] for d in st.session_state.debts])
    debt_names = [d["name"] for d in st.session_state.debts]
    colors_debt = ["#F44336", "#FF9800", "#D4AF37", "#4A90D9", "#9C27B0", "#4CAF50"]

    fig = go.Figure()
    for idx, dname in enumerate(debt_names):
        months_x = [s["month"] for s in chosen["schedule"]]
        balances_y = [s["balances"].get(dname, 0) for s in chosen["schedule"]]
        fig.add_trace(go.Scatter(
            x=months_x, y=balances_y,
            name=dname,
            fill="tozeroy",
            line=dict(color=colors_debt[idx % len(colors_debt)], width=2),
            fillcolor=colors_debt[idx % len(colors_debt)].replace(")", ", 0.15)").replace("rgb", "rgba") if "rgb" in colors_debt[idx % len(colors_debt)] else colors_debt[idx % len(colors_debt)] + "26",
        ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=300, margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(title="Mois", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(title="Solde (" + cur + ")", gridcolor="rgba(255,255,255,0.05)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.3),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Avalanche vs Snowball comparison ─────────────────────
st.markdown("---")
st.markdown("#### Avalanche vs Boule de neige — comparaison directe")

av = comparison["avalanche"]
sn = comparison["snowball"]
winner = comparison["winner"]

av_months = av["total_months"]
sn_months = sn["total_months"]
av_label = str(av_months // 12) + "a " + str(av_months % 12) + "m"
sn_label = str(sn_months // 12) + "a " + str(sn_months % 12) + "m"

col_av, col_sn = st.columns(2)
with col_av:
    av_border = "border:2px solid #4CAF50" if winner == "avalanche" else "border:1px solid rgba(255,255,255,0.08)"
    best_badge = '<div style="color:#4CAF50; font-size:0.75rem; font-weight:700;">Recommande — economise le plus</div>' if winner == "avalanche" else ""
    st.markdown(
        f'<div style="background:rgba(19,27,46,0.8); {av_border}; border-radius:12px; padding:16px;">'
        f'{best_badge}'
        f'<div style="font-size:1.05rem; font-weight:700; color:#4A90D9; margin-bottom:8px;">Avalanche</div>'
        f'<div style="color:#C8D4E8;">Taux le plus eleve en premier</div>'
        f'<div style="color:#E8E8E8; font-size:1.2rem; font-weight:700; margin-top:8px;">{sym}{av["total_interest"]:,.0f} d\'interets</div>'
        f'<div style="color:#8899BB; font-size:0.85rem;">Libre dans {av_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

with col_sn:
    sn_border = "border:2px solid #4CAF50" if winner == "snowball" else "border:1px solid rgba(255,255,255,0.08)"
    best_badge_sn = '<div style="color:#4CAF50; font-size:0.75rem; font-weight:700;">Recommande — motivation plus rapide</div>' if winner == "snowball" else ""
    st.markdown(
        f'<div style="background:rgba(19,27,46,0.8); {sn_border}; border-radius:12px; padding:16px;">'
        f'{best_badge_sn}'
        f'<div style="font-size:1.05rem; font-weight:700; color:#FF9800; margin-bottom:8px;">Boule de neige</div>'
        f'<div style="color:#C8D4E8;">Solde le plus petit en premier</div>'
        f'<div style="color:#E8E8E8; font-size:1.2rem; font-weight:700; margin-top:8px;">{sym}{sn["total_interest"]:,.0f} d\'interets</div>'
        f'<div style="color:#8899BB; font-size:0.85rem;">Libre dans {sn_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

if comparison["interest_saved"] > 50:
    st.markdown(
        f'<div style="background:rgba(76,175,80,0.08); border:1px solid rgba(76,175,80,0.3); '
        f'border-radius:10px; padding:14px; margin-top:12px; text-align:center;">'
        f'<div style="color:#4CAF50; font-weight:600;">'
        f'L\'avalanche vous economise {sym}{comparison["interest_saved"]:,.0f} par rapport a la boule de neige'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
