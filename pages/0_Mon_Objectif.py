"""
MON OBJECTIF — La page la plus importante.
Langage simple. Calculateur inversé. Plan concret mois par mois.
"Je veux X€ à Y ans → voici exactement quoi faire."
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.goal_engine import GoalEngine
from engines.progressive_plan import ProgressivePlanEngine
from utils.formatters import format_currency
from utils.constants import RISK_PROFILES
import plotly.graph_objects as go

st.set_page_config(page_title="Mon Objectif — Oswald Wealth", page_icon="🎯", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("👈 Commencez par créer votre profil dans le menu à gauche (section **Profil**).")
    st.stop()

p   = st.session_state.profile
eng = GoalEngine(p)
cur = p.currency
sym = {"EUR":"€","USD":"$","GBP":"£","CHF":"CHF","CAD":"CA$","XOF":"FCFA"}.get(cur, cur)

# ──────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">🎯 Mon Objectif Financier</div>
    <div class="hero-subtitle">
        Dites-nous où vous voulez aller. On vous dit exactement comment y arriver.
    </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SAISIE DE L'OBJECTIF — Simple et claire
# ──────────────────────────────────────────────
st.markdown("### Je veux atteindre…")

c1, c2, c3 = st.columns(3)
with c1:
    target_wealth = st.number_input(
        f"Montant cible ({sym})",
        min_value=10_000.0,
        max_value=10_000_000.0,
        value=float(p.desired_monthly_pension * 12 / 0.04),
        step=10_000.0,
        help="La somme totale que vous voulez avoir d'ici votre retraite ou votre objectif.",
        format="%.0f",
    )
with c2:
    target_age = st.number_input(
        "À quel âge ?",
        min_value=p.age + 1,
        max_value=85,
        value=p.target_retirement_age,
        step=1,
    )
with c3:
    risk_options = list(RISK_PROFILES.keys())
    risk_choice = st.selectbox(
        "Niveau de risque de mes placements",
        risk_options,
        index=risk_options.index(p.risk_tolerance) if p.risk_tolerance in risk_options else 2,
    )

annual_return = RISK_PROFILES[risk_choice]["expected_return"]

# ──────────────────────────────────────────────
# CALCUL
# ──────────────────────────────────────────────
required = eng.required_monthly_savings(target_wealth, target_age, annual_return)
plan     = eng.build_plan(target_wealth, target_age, annual_return, required)
messages = eng.explain_in_plain_language(plan, cur)

# ──────────────────────────────────────────────
# RÉSULTAT CENTRAL
# ──────────────────────────────────────────────
st.markdown("---")

if required == 0:
    st.success("🎉 Votre patrimoine actuel suffit déjà à atteindre cet objectif sans effort supplémentaire !")
else:
    col_main, col_side = st.columns([3, 2])

    with col_main:
        # La réponse principale — grande et claire
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#131B2E,#1a2540); border:2px solid #D4AF37;
                    border-radius:16px; padding:32px; margin-bottom:24px; text-align:center;">
            <div style="color:#8899BB; font-size:0.9rem; margin-bottom:8px; text-transform:uppercase; letter-spacing:1px;">
                Pour atteindre {format_currency(target_wealth, cur, compact=True)} à {target_age} ans
            </div>
            <div style="font-size:3.2rem; font-weight:800; color:#D4AF37; line-height:1;">
                {sym}{required:,.0f} / mois
            </div>
            <div style="color:#8899BB; font-size:1rem; margin-top:12px;">
                soit <strong style="color:#E8E8E8;">{sym}{plan['daily_equivalent']:.1f} par jour</strong>
                · pendant <strong style="color:#E8E8E8;">{plan['years_left']} ans</strong>
                · au rendement <strong style="color:#D4AF37;">{annual_return*100:.1f}%/an</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Messages explicatifs
        for msg in messages:
            if msg.startswith("✅"):
                st.success(msg)
            elif msg.startswith("⚠️"):
                st.warning(msg)
            elif msg.startswith("🎉"):
                st.balloons()
                st.success(msg)
            else:
                st.markdown(f"""
                <div style="background:rgba(19,27,46,0.6); border-left:3px solid #D4AF37;
                            padding:12px 16px; border-radius:0 8px 8px 0; margin:8px 0;
                            color:#C8D4E8; font-size:0.95rem; line-height:1.6;">
                    {msg}
                </div>
                """, unsafe_allow_html=True)

    with col_side:
        # Répartition mensuelle recommandée
        st.markdown("#### Comment répartir ces épargnes ?")
        split = plan["savings_split"]
        for vehicle, amount in split.items():
            pct = amount / required if required > 0 else 0
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:10px 14px; background:rgba(19,27,46,0.6); border-radius:8px; margin-bottom:8px;">
                <div style="color:#C8D4E8; font-size:0.9rem;">{vehicle}</div>
                <div style="color:#D4AF37; font-weight:700;">{sym}{amount:.0f}/mois</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:12px; padding:12px; background:rgba(212,175,55,0.08);
                    border-radius:8px; text-align:center;">
            <div style="color:#8899BB; font-size:0.8rem;">Intérêts cette année</div>
            <div style="color:#4CAF50; font-size:1.6rem; font-weight:700;">
                +{format_currency(plan['interest_this_year'], cur, compact=True)}
            </div>
            <div style="color:#8899BB; font-size:0.75rem;">votre argent travaille pour vous</div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TRAJECTOIRE — Graphique simple
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📈 Votre patrimoine année après année")

df = eng.trajectory_dataframe(target_wealth, target_age, annual_return, required)

fig = go.Figure()

# Zone de progression
fig.add_trace(go.Scatter(
    x=df["Âge"], y=df["Patrimoine"],
    fill="tozeroy", name="Votre patrimoine",
    line=dict(color="#D4AF37", width=3),
    fillcolor="rgba(212,175,55,0.12)",
))

# Ligne objectif
fig.add_hline(
    y=target_wealth,
    line_dash="dash", line_color="#4CAF50", line_width=2,
    annotation_text=f"🎯 Objectif : {format_currency(target_wealth, cur, compact=True)}",
    annotation_font_color="#4CAF50",
    annotation_position="top right",
)

# Jalon actuel
fig.add_vline(x=p.age, line_dash="dot", line_color="#D4AF37", opacity=0.5,
              annotation_text=f"Aujourd'hui ({p.age} ans)", annotation_font_color="#D4AF37")

# Barres d'intérêts
fig.add_trace(go.Bar(
    x=df["Âge"], y=df["Intérêts annuels"],
    name="Intérêts gagnés cette année",
    marker_color="rgba(76,175,80,0.5)",
    yaxis="y2",
    opacity=0.7,
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=420, margin=dict(l=0, r=0, t=20, b=0),
    xaxis=dict(title="Votre âge", gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(title=f"Patrimoine ({cur})", gridcolor="rgba(255,255,255,0.05)"),
    yaxis2=dict(title="Intérêts/an", overlaying="y", side="right", showgrid=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.15),
    font=dict(color="#C8D4E8"),
)
st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────
# JALONS CLÉS — Tableau simple
# ──────────────────────────────────────────────
st.markdown("### 🗓️ Vos jalons clés")

milestones = plan["milestones"]
if milestones:
    cols = st.columns(len(milestones))
    for i, m in enumerate(milestones):
        pct   = min(m["wealth"] / target_wealth * 100, 100)
        color = "#4CAF50" if pct >= 100 else ("#D4AF37" if pct >= 60 else "#8899BB")
        with cols[i]:
            st.markdown(f"""
            <div style="background:rgba(19,27,46,0.8); border:1px solid rgba(212,175,55,0.2);
                        border-radius:12px; padding:16px; text-align:center;">
                <div style="font-size:1.5rem; font-weight:800; color:{color};">{m['age']} ans</div>
                <div style="font-size:1.1rem; font-weight:700; color:#E8E8E8; margin-top:4px;">
                    {format_currency(m['wealth'], cur, compact=True)}
                </div>
                <div style="font-size:0.85rem; color:{color}; margin-top:4px;">{pct:.0f}% de l'objectif</div>
                <div style="font-size:0.8rem; color:#8899BB; margin-top:6px;">
                    dont {format_currency(m['interest'], cur, compact=True)}/an d'intérêts
                </div>
            </div>
            """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TABLEAU DÉTAILLÉ — Optionnel
# ──────────────────────────────────────────────
with st.expander("📋 Voir le tableau complet année par année"):
    display = df.copy()
    display["Patrimoine"]          = display["Patrimoine"].map(lambda x: format_currency(x, cur))
    display["Intérêts annuels"]    = display["Intérêts annuels"].map(lambda x: f"+{format_currency(x, cur)}")
    display["Cotisation annuelle"] = display["Cotisation annuelle"].map(lambda x: format_currency(x, cur))
    display["% de l'objectif"]     = display["% de l'objectif"].map(lambda x: f"{x:.1f}%")
    st.dataframe(display, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# ÉTAT ACTUEL vs OBJECTIF
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Où en êtes-vous aujourd'hui ?")

progress = plan["progress_pct"]
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Patrimoine actuel", format_currency(p.current_net_worth, cur, compact=True))
with c2:
    st.metric("Objectif", format_currency(target_wealth, cur, compact=True))
with c3:
    savings_delta = "✅ Suffisant" if plan["on_track"] else f"⚠️ Manque {sym}{plan['monthly_gap']:.0f}/mois"
    st.metric("Épargne actuelle", f"{sym}{p.monthly_savings:.0f}/mois", savings_delta)

progress_color = "#4CAF50" if progress >= 0.80 else ("#D4AF37" if progress >= 0.40 else "#8899BB")
st.markdown(
    f'<div style="margin-top:8px;">'
    f'<div style="display:flex; justify-content:space-between; margin-bottom:4px;">'
    f'<span style="color:#8899BB;">Progression vers l\'objectif</span>'
    f'<span style="color:{progress_color}; font-weight:700;">{progress*100:.1f}%</span>'
    f'</div></div>',
    unsafe_allow_html=True,
)
st.progress(min(progress, 1.0))

# ──────────────────────────────────────────────
# PLAN PROGRESSIF — Choisissez votre rythme
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🗺️ Choisissez votre rythme d'épargne")
st.markdown(
    "<div style='color:#8899BB; margin-bottom:20px;'>"
    "Inutile de tout épargner dès le premier mois. "
    "Choisissez le plan qui vous correspond — vous pouvez accélérer quand vous êtes prêt(e)."
    "</div>",
    unsafe_allow_html=True,
)

pp = ProgressivePlanEngine(p)
prog_plans = pp.build_progressive_plans(target_wealth, target_age, annual_return)
prog_names = [pl["icon"] + " " + pl["name"] for pl in prog_plans]
sel_prog = st.radio("Rythme", prog_names, horizontal=True, index=1, label_visibility="collapsed")
sel_prog_plan = prog_plans[prog_names.index(sel_prog)]

months_delayed = sel_prog_plan["months_delayed"]
if months_delayed == 0:
    delay_txt = "Objectif atteint a la date prevue"
else:
    yrs_late = months_delayed // 12
    m_late = months_delayed % 12
    if yrs_late > 0 and m_late > 0:
        delay_txt = "Objectif atteint environ " + str(yrs_late) + " an(s) et " + str(m_late) + " mois plus tard"
    elif yrs_late > 0:
        delay_txt = "Objectif atteint environ " + str(yrs_late) + " an(s) plus tard"
    else:
        delay_txt = "Objectif atteint environ " + str(m_late) + " mois plus tard"

pc = sel_prog_plan["color"]
st.markdown(
    f'<div style="background:rgba(19,27,46,0.8); border:2px solid {pc}; '
    f'border-radius:12px; padding:18px 22px; margin:12px 0;">'
    f'<div style="font-size:1.1rem; font-weight:700; color:{pc}; margin-bottom:6px;">'
    f'{sel_prog_plan["icon"]} {sel_prog_plan["name"]}</div>'
    f'<div style="color:#C8D4E8; margin-bottom:8px;">{sel_prog_plan["description"]}</div>'
    f'<div style="color:#8899BB; font-size:0.85rem;">{delay_txt}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

years_left_prog = max(target_age - p.age, 1)
display_n = min(years_left_prog, 5)
yr_items = list(sel_prog_plan["year_targets"].items())[:display_n]
yr_cols = st.columns(display_n)
for i, (yr_num, yr_target) in enumerate(yr_items):
    pct_full = yr_target / required * 100 if required > 0 else 100
    yc = "#4CAF50" if pct_full >= 95 else ("#D4AF37" if pct_full >= 60 else "#4A90D9")
    age_s = p.age + yr_num - 1
    age_e = p.age + yr_num
    if yr_num == 3 and sel_prog_plan["start_pct"] < 60:
        yr_lbl = "Annee discipline"
    else:
        yr_lbl = "Annee " + str(yr_num)
    with yr_cols[i]:
        st.markdown(
            f'<div style="background:rgba(19,27,46,0.8); border:1px solid {yc}; '
            f'border-radius:10px; padding:12px; text-align:center;">'
            f'<div style="color:#8899BB; font-size:0.72rem;">{yr_lbl} · {age_s}-{age_e} ans</div>'
            f'<div style="color:{yc}; font-size:1.25rem; font-weight:800;">{sym}{yr_target:,.0f}</div>'
            f'<div style="color:#8899BB; font-size:0.72rem;">/mois</div>'
            f'<div style="color:{yc}; font-size:0.7rem; margin-top:3px;">{pct_full:.0f}% du plan complet</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
if years_left_prog > 5:
    st.caption(
        "... a partir de l'annee 6 : " + sym + str(int(required)) + "/mois jusqu'a "
        + str(target_age) + " ans."
    )
