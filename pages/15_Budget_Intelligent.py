"""
Budget Intelligent — Analyse poste par poste avec conseils hyper-concrets.
Chaque euro de dépense est optimisable. Voyez exactement combien vous pouvez récupérer.
"""
import streamlit as st
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.budget_optimizer import BudgetOptimizer
import plotly.graph_objects as go

st.set_page_config(
    page_title="Budget Intelligent — Oswald Wealth",
    page_icon="🔍",
    layout="wide",
)
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("Créez votre profil d'abord.")
    st.stop()

p = st.session_state.profile
cur = p.currency
sym = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "CAD": "CA$", "XOF": "FCFA"}.get(cur, cur)
opt = BudgetOptimizer(p)
TIPS = opt.tips
ctx = opt.context
CATEGORY_ORDER = list(TIPS.keys())
is_ci = (cur == "XOF")

# ── Hero avec badge pays ──────────────────────────────────────
flag = ctx["flag"]
country = ctx["country"]
st.markdown(
    f'<div class="hero-banner">'
    f'<div class="hero-title">🔍 Budget Intelligent</div>'
    f'<div class="hero-subtitle">'
    f'Conseils adaptés à la réalité de <strong>{flag} {country}</strong> — '
    f'prix réels, services locaux, habitudes locales. '
    f'Pas des généralités : votre vie, votre argent.'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# Bannière CI spécifique
if is_ci:
    st.markdown(
        '<div style="background:linear-gradient(135deg, rgba(255,140,0,0.12), rgba(0,160,0,0.08)); '
        'border:1px solid rgba(255,140,0,0.3); border-radius:14px; padding:18px 22px; margin-bottom:20px;">'
        '<div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">'
        '<span style="font-size:2rem;">🇨🇮</span>'
        '<div>'
        '<div style="color:#FFA500; font-weight:700; font-size:1rem;">Adapté à la Côte d\'Ivoire</div>'
        '<div style="color:#C8D4E8; font-size:0.85rem;">'
        'Prix en FCFA, marchés vivriers, gbaka, maquis, Mobile Money, tontines — '
        'les vraies réalités du quotidien ivoirien.'
        '</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# ── Saisie des dépenses ───────────────────────────────────────
st.markdown("### Vos dépenses mensuelles réelles")
st.markdown(
    '<div style="color:#8899BB; font-size:0.85rem; margin-bottom:16px;">'
    "Renseignez ce que vous dépensez <strong>réellement</strong> chaque mois. "
    "Plus vous êtes précis, plus les conseils sont pertinents."
    "</div>",
    unsafe_allow_html=True,
)

# Pre-fill from profile if available
monthly_income = p.monthly_income or (300000 if is_ci else 3000)
if is_ci:
    default_spending = {
        "Alimentation": round(monthly_income * 0.20),
        "Transport": round(monthly_income * 0.12),
        "Logement": round(monthly_income * 0.28),
        "Mobile Money": round(monthly_income * 0.03),
        "Tontine & Épargne locale": round(monthly_income * 0.08),
        "Abonnements": round(monthly_income * 0.04),
        "Santé": round(monthly_income * 0.05),
        "Loisirs": round(monthly_income * 0.05),
        "Banque & Finances": round(monthly_income * 0.02),
    }
else:
    default_spending = {
        "Alimentation": round(monthly_income * 0.15),
        "Transport": round(monthly_income * 0.10),
        "Logement": round(monthly_income * 0.30),
        "Abonnements": round(monthly_income * 0.05),
    "Santé": round(monthly_income * 0.04),
    "Loisirs": round(monthly_income * 0.07),
    "Vêtements": round(monthly_income * 0.03),
    "Banque & Finances": round(monthly_income * 0.02),
}

if "spending_inputs" not in st.session_state:
    st.session_state.spending_inputs = dict(default_spending)

col_a, col_b = st.columns(2)
spending = {}
for i, cat in enumerate(CATEGORY_ORDER):
    cfg = TIPS[cat]
    col = col_a if i % 2 == 0 else col_b
    with col:
        step_val = 1000 if is_ci else 10
        val = st.number_input(
            f"{cfg['icon']} {cat}",
            min_value=0,
            max_value=int(monthly_income * 2),
            value=int(st.session_state.spending_inputs.get(cat, default_spending.get(cat, 0))),
            step=step_val,
            key=f"spend_{cat}",
        )
        spending[cat] = val
        st.session_state.spending_inputs[cat] = val

total_declared = sum(spending.values())
total_income = monthly_income

# ── KPI global ────────────────────────────────────────────────
st.markdown("---")
k1, k2, k3, k4 = st.columns(4)

potential_saving = opt.total_potential_monthly_saving(spending)
years_to_retirement = max(1, p.target_retirement_age - p.age)
wealth_impact = opt.wealth_impact(potential_saving, years_to_retirement)

with k1:
    pct_income = total_declared / total_income * 100 if total_income > 0 else 0
    pct_color = "#4CAF50" if pct_income < 80 else ("#FF9800" if pct_income < 95 else "#F44336")
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Dépenses déclarées</div>'
        f'<div class="metric-value" style="color:{pct_color};">{sym}{total_declared:,.0f}</div>'
        f'<div style="color:#8899BB; font-size:0.78rem;">{pct_income:.0f}% de votre revenu</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Économies potentielles/mois</div>'
        f'<div class="metric-value" style="color:#D4AF37;">{sym}{potential_saving:,.0f}</div>'
        f'<div style="color:#8899BB; font-size:0.78rem;">si vous appliquez les conseils</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Impact patrimoine à {p.target_retirement_age} ans</div>'
        f'<div class="metric-value" style="color:#4CAF50;">{sym}{wealth_impact:,.0f}</div>'
        f'<div style="color:#8899BB; font-size:0.78rem;">si économies investies à 7%/an</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with k4:
    quick = opt.quick_wins(spending)
    qs = sum(t["estimated_saving"] for t in quick)
    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Quick wins (effort minimal)</div>'
        f'<div class="metric-value" style="color:#2196F3;">{sym}{qs:,.0f}/mois</div>'
        f'<div style="color:#8899BB; font-size:0.78rem;">{len(quick)} conseils très faciles à appliquer</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# ── Quick wins highlight ──────────────────────────────────────
if quick:
    st.markdown("---")
    st.markdown(
        '<div style="background:rgba(33,150,243,0.06); border:1px solid #2196F3; '
        'border-radius:14px; padding:20px 24px; margin-bottom:8px;">'
        '<div style="color:#2196F3; font-weight:700; font-size:1.05rem; margin-bottom:12px;">'
        '⚡ Vos Quick Wins — résultats immédiats, effort minimal</div>',
        unsafe_allow_html=True,
    )
    qw_cols = st.columns(min(len(quick), 3))
    for qi, tip in enumerate(quick[:3]):
        with qw_cols[qi]:
            st.markdown(
                f'<div style="background:rgba(19,27,46,0.8); border-radius:10px; padding:14px; text-align:center;">'
                f'<div style="font-size:1.4rem;">{tip["category_icon"]}</div>'
                f'<div style="color:#C8D4E8; font-weight:600; font-size:0.85rem; margin:6px 0;">'
                f'{tip["title"]}</div>'
                f'<div style="color:#2196F3; font-size:1.1rem; font-weight:800;">'
                f'{sym}{tip["estimated_saving"]}/mois</div>'
                f'<div style="color:#8899BB; font-size:0.72rem; margin-top:4px;">'
                f'Effort : {tip["effort"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

# ── Graphique répartition + potentiel ────────────────────────
st.markdown("---")
st.markdown("### Où va votre argent — et combien récupérer")

chart_col, chart_col2 = st.columns(2)
with chart_col:
    labels = [f"{TIPS[c]['icon']} {c}" for c in CATEGORY_ORDER if spending.get(c, 0) > 0]
    values = [spending[c] for c in CATEGORY_ORDER if spending.get(c, 0) > 0]
    colors = [TIPS[c]["color"] for c in CATEGORY_ORDER if spending.get(c, 0) > 0]

    fig_pie = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.42,
        marker=dict(colors=colors, line=dict(color="#0A0E1A", width=2)),
        textfont=dict(color="white", size=11),
        hovertemplate="%{label}<br>%{value:.0f} " + cur + "/mois<br>%{percent}<extra></extra>",
    ))
    fig_pie.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=24, b=0), height=300,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#C8D4E8", size=10)),
        font=dict(color="#C8D4E8"),
        title=dict(text="Répartition actuelle", font=dict(color="#C8D4E8", size=13)),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    cats_with_savings = []
    savings_vals = []
    savings_colors = []
    for cat in CATEGORY_ORDER:
        if spending.get(cat, 0) > 0:
            result = opt.analyze_category(cat, spending[cat])
            best_saving = max((t["estimated_saving"] for t in result.get("tips", [])), default=0)
            if best_saving > 0:
                cats_with_savings.append(f"{TIPS[cat]['icon']} {cat}")
                savings_vals.append(best_saving)
                savings_colors.append(TIPS[cat]["color"])

    fig_bar = go.Figure(go.Bar(
        x=savings_vals, y=cats_with_savings,
        orientation="h",
        marker=dict(color=savings_colors, opacity=0.85),
        text=[f"{sym}{v}" for v in savings_vals],
        textposition="outside",
        textfont=dict(color="#C8D4E8", size=10),
    ))
    fig_bar.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=60, t=24, b=0), height=300,
        xaxis=dict(title=f"{cur}/mois", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        font=dict(color="#C8D4E8"),
        title=dict(text="Potentiel d'économie mensuel par poste", font=dict(color="#C8D4E8", size=13)),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Analyse détaillée par catégorie ──────────────────────────
st.markdown("---")
st.markdown("### Analyse détaillée — poste par poste")
st.markdown(
    '<div style="color:#8899BB; font-size:0.85rem; margin-bottom:20px;">'
    "Cliquez sur chaque poste pour voir les conseils personnalisés avec exemples de prix réels."
    "</div>",
    unsafe_allow_html=True,
)

for cat in CATEGORY_ORDER:
    amount = spending.get(cat, 0)
    if amount <= 0:
        continue

    cfg = TIPS[cat]
    result = opt.analyze_category(cat, amount)
    total_pot = result.get("total_potential_saving", 0)
    pot_pct = total_pot / amount * 100 if amount > 0 else 0
    benchmark_pct = cfg["benchmark_pct"]
    is_over_benchmark = (amount / total_income) > benchmark_pct * 1.2 if total_income > 0 else False

    over_badge = ""
    if is_over_benchmark:
        benchmark_amount = round(total_income * benchmark_pct)
        over_badge = (
            f'<span style="background:rgba(244,67,54,0.15); color:#F44336; '
            f'font-size:0.7rem; font-weight:600; padding:2px 7px; border-radius:99px; margin-left:8px;">'
            f'Au-dessus repère ({sym}{benchmark_amount}/mois)</span>'
        )

    with st.expander(
        f"{cfg['icon']}  {cat} — {sym}{amount:,.0f}/mois  |  Potentiel : {sym}{total_pot:,.0f}/mois ({pot_pct:.0f}%)",
        expanded=(cat == "Alimentation"),
    ):
        # Sub-header
        bench_txt = f"Repère conseillé : {sym}{round(total_income * benchmark_pct):,}/mois ({round(benchmark_pct*100)}% du revenu)"
        st.markdown(
            f'<div style="display:flex; justify-content:space-between; align-items:center; '
            f'margin-bottom:16px; flex-wrap:wrap; gap:8px;">'
            f'<div style="color:#8899BB; font-size:0.82rem;">{bench_txt}{over_badge}</div>'
            f'<div style="color:{cfg["color"]}; font-weight:700; font-size:0.95rem;">'
            f'Économies totales possibles : {sym}{total_pot}/mois = {sym}{total_pot*12:,.0f}/an</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Tips
        for tip in result.get("tips", []):
            tip_saving = tip["estimated_saving"]
            tip_pct = tip_saving / amount * 100 if amount > 0 else 0

            qw_badge = ""
            if tip.get("quick_win"):
                qw_badge = (
                    '<span style="background:rgba(33,150,243,0.15); color:#2196F3; '
                    'font-size:0.65rem; font-weight:700; padding:1px 6px; border-radius:99px; margin-left:6px;">'
                    'QUICK WIN</span>'
                )

            examples_html = ""
            for ex in tip.get("examples", []):
                examples_html += (
                    f'<div style="display:flex; gap:8px; padding:5px 0; '
                    f'border-bottom:1px solid rgba(255,255,255,0.04);">'
                    f'<span style="color:#D4AF37; min-width:14px;">→</span>'
                    f'<span style="color:#C8D4E8; font-size:0.82rem;">{ex}</span>'
                    f'</div>'
                )

            actions_html = ""
            for j, act in enumerate(tip.get("actions", []), 1):
                actions_html += (
                    f'<div style="display:flex; gap:8px; padding:4px 0;">'
                    f'<span style="color:#4CAF50; font-weight:700; min-width:16px;">{j}.</span>'
                    f'<span style="color:#C8D4E8; font-size:0.82rem;">{act}</span>'
                    f'</div>'
                )

            effort_color = tip["effort_color"]
            impact_color = tip["impact_color"]

            st.markdown(
                f'<div style="background:rgba(19,27,46,0.75); border:1px solid rgba(255,255,255,0.06); '
                f'border-left:3px solid {cfg["color"]}; border-radius:10px; '
                f'padding:16px 18px; margin-bottom:12px;">'

                # Title row
                f'<div style="display:flex; justify-content:space-between; '
                f'align-items:flex-start; margin-bottom:10px; flex-wrap:wrap; gap:8px;">'
                f'<div>'
                f'<span style="font-weight:700; color:#E8E8E8; font-size:0.95rem;">{tip["title"]}</span>'
                f'{qw_badge}'
                f'</div>'
                f'<div style="text-align:right;">'
                f'<div style="color:{cfg["color"]}; font-size:1.05rem; font-weight:800;">'
                f'{sym}{tip_saving}/mois</div>'
                f'<div style="color:#8899BB; font-size:0.72rem;">-{tip_pct:.0f}% sur ce poste</div>'
                f'</div>'
                f'</div>'

                # Badges effort / impact
                f'<div style="display:flex; gap:10px; margin-bottom:10px; flex-wrap:wrap;">'
                f'<span style="background:rgba(19,27,46,0.9); border:1px solid {effort_color}; '
                f'color:{effort_color}; font-size:0.7rem; padding:2px 8px; border-radius:99px;">'
                f'Effort : {tip["effort"]}</span>'
                f'<span style="background:rgba(19,27,46,0.9); border:1px solid {impact_color}; '
                f'color:{impact_color}; font-size:0.7rem; padding:2px 8px; border-radius:99px;">'
                f'Impact : {tip["impact"]}</span>'
                f'</div>'

                # Description
                f'<div style="color:#9AABCC; font-size:0.85rem; margin-bottom:12px; '
                f'font-style:italic; border-left:2px solid rgba(255,255,255,0.1); '
                f'padding-left:10px;">{tip["description"]}</div>'

                # Examples
                f'<div style="margin-bottom:12px;">'
                f'<div style="color:#D4AF37; font-size:0.75rem; font-weight:600; '
                f'text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">'
                f'Exemples concrets</div>'
                f'{examples_html}'
                f'</div>'

                # Actions
                f'<div>'
                f'<div style="color:#4CAF50; font-size:0.75rem; font-weight:600; '
                f'text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">'
                f'Actions immédiates</div>'
                f'{actions_html}'
                f'</div>'

                f'</div>',
                unsafe_allow_html=True,
            )

        # Food special: restaurant vs maison calculator
        if cat == "Alimentation":
            calc_title = "🍳 Calculateur : Maquis vs Maison" if is_ci else "🍳 Calculateur : Resto vs Maison"
            lbl_resto = ctx["restaurant_label"].capitalize()
            lbl_home = ctx["home_label"].capitalize()
            step_calc = 1000 if is_ci else 10
            max_calc = int(amount) + (100000 if is_ci else 1000)
            default_resto = min(int(amount * 0.4), 150000 if is_ci else 300)
            default_grocery = min(int(amount * 0.6), 200000 if is_ci else 400)
            st.markdown(
                f'<div style="background:rgba(76,175,80,0.05); border:1px solid rgba(76,175,80,0.2); '
                f'border-radius:10px; padding:16px 18px; margin-top:4px;">'
                f'<div style="color:#4CAF50; font-weight:700; font-size:0.9rem; margin-bottom:12px;">'
                f'{calc_title}</div>',
                unsafe_allow_html=True,
            )
            fc1, fc2 = st.columns(2)
            with fc1:
                resto_budget = st.number_input(
                    f"Budget {lbl_resto} ({sym}/mois)",
                    min_value=0, max_value=max_calc,
                    value=default_resto,
                    step=step_calc, key="calc_resto",
                )
            with fc2:
                grocery_budget = st.number_input(
                    f"Budget courses alimentaires ({sym}/mois)",
                    min_value=0, max_value=max_calc,
                    value=default_grocery,
                    step=step_calc, key="calc_grocery",
                )

            meal = opt.meal_cost_comparison(float(resto_budget), float(grocery_budget))
            if meal["potential_saving"] > 0:
                n_meals = meal["restaurant_meals_count"]
                home_cost_val = meal["home_equivalent_cost"]
                saving_m = meal["potential_saving"]
                cost_resto = meal["cost_per_restaurant_meal"]
                cost_home = meal["cost_per_home_meal"]
                st.markdown(
                    f'<div style="display:flex; gap:24px; flex-wrap:wrap; margin-top:10px;">'
                    f'<div style="text-align:center;">'
                    f'<div style="color:#8899BB; font-size:0.75rem;">{lbl_resto} (estimé)</div>'
                    f'<div style="color:#F44336; font-size:1.1rem; font-weight:700;">'
                    f'{n_meals} repas × {sym}{cost_resto:,.0f}</div>'
                    f'</div>'
                    f'<div style="text-align:center;">'
                    f'<div style="color:#8899BB; font-size:0.75rem;">Même nombre — {lbl_home}</div>'
                    f'<div style="color:#4CAF50; font-size:1.1rem; font-weight:700;">'
                    f'{sym}{home_cost_val:,.0f} total ({sym}{cost_home:,.0f}/repas)</div>'
                    f'</div>'
                    f'<div style="text-align:center;">'
                    f'<div style="color:#8899BB; font-size:0.75rem;">Économie possible</div>'
                    f'<div style="color:#D4AF37; font-size:1.3rem; font-weight:800;">'
                    f'{sym}{saving_m:,.0f}/mois</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

# ── Plan d'action personnalisé ────────────────────────────────
st.markdown("---")
st.markdown("### Mon plan d'action personnalisé")
st.markdown(
    '<div style="color:#8899BB; font-size:0.85rem; margin-bottom:16px;">'
    "Voici votre feuille de route optimisation, classée du plus simple au plus impactant."
    "</div>",
    unsafe_allow_html=True,
)

all_opps = opt.top_opportunities(spending, n=12)
if all_opps:
    cumulative = 0
    for rank, tip in enumerate(all_opps, 1):
        cumulative += tip["estimated_saving"]
        rank_color = "#D4AF37" if rank <= 3 else ("#4CAF50" if rank <= 6 else "#8899BB")
        qw = "⚡ " if tip.get("quick_win") else ""
        effort_color = tip["effort_color"]

        st.markdown(
            f'<div style="display:flex; align-items:flex-start; gap:14px; '
            f'padding:12px 16px; background:rgba(19,27,46,0.7); '
            f'border-radius:10px; margin-bottom:8px; '
            f'border-left:3px solid {rank_color};">'
            f'<div style="min-width:28px; height:28px; border-radius:50%; '
            f'background:{rank_color}; display:flex; align-items:center; justify-content:center; '
            f'color:#0A0E1A; font-weight:800; font-size:0.8rem;">{rank}</div>'
            f'<div style="flex:1;">'
            f'<div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">'
            f'<div>'
            f'<span style="color:#E8E8E8; font-weight:600; font-size:0.9rem;">'
            f'{qw}{tip["category_icon"]} {tip["title"]}</span>'
            f'<span style="color:{effort_color}; font-size:0.72rem; margin-left:8px;">'
            f'effort : {tip["effort"]}</span>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<span style="color:{rank_color}; font-weight:700;">{sym}{tip["estimated_saving"]}/mois</span>'
            f'<span style="color:#8899BB; font-size:0.75rem; margin-left:8px;">'
            f'Cumulé : {sym}{cumulative}/mois</span>'
            f'</div>'
            f'</div>'
            f'<div style="color:#8899BB; font-size:0.8rem; margin-top:4px;">'
            f'{tip["description"][:100]}...</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

# ── Impact patrimoine si économies investies ─────────────────
st.markdown("---")
st.markdown("### Et si vous investissiez ces économies ?")

inv_col1, inv_col2 = st.columns(2)
with inv_col1:
    monthly_to_invest = st.slider(
        "Économies réalisées à investir chaque mois",
        min_value=0,
        max_value=int(potential_saving) + 50,
        value=int(potential_saving * 0.6),
        step=10,
    )
with inv_col2:
    inv_years = st.slider(
        "Pendant combien d'années ?",
        min_value=1,
        max_value=40,
        value=min(years_to_retirement, 20),
    )

years_range = list(range(1, inv_years + 1))
fv_curve = [opt.wealth_impact(monthly_to_invest, y) for y in years_range]
total_invested = monthly_to_invest * inv_years * 12
final_fv = fv_curve[-1] if fv_curve else 0
gain = final_fv - total_invested

fig_inv = go.Figure()
fig_inv.add_trace(go.Scatter(
    x=years_range, y=fv_curve,
    fill="tozeroy", name="Valeur patrimoniale",
    line=dict(color="#D4AF37", width=2.5),
    fillcolor="rgba(212,175,55,0.10)",
    hovertemplate="Année %{x}<br>Valeur : " + sym + "%{y:,.0f}<extra></extra>",
))
fig_inv.add_trace(go.Scatter(
    x=years_range,
    y=[monthly_to_invest * 12 * y for y in years_range],
    name="Capital versé (sans intérêts)",
    line=dict(color="#8899BB", width=1.5, dash="dot"),
    hovertemplate="Année %{x}<br>Versé : " + sym + "%{y:,.0f}<extra></extra>",
))
fig_inv.update_layout(
    template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=280, margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(title="Années", gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(title=cur, gridcolor="rgba(255,255,255,0.05)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#C8D4E8")),
    font=dict(color="#C8D4E8"),
)
st.plotly_chart(fig_inv, use_container_width=True)

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(
        f'<div class="metric-card" style="text-align:center;">'
        f'<div class="metric-label">Capital versé</div>'
        f'<div class="metric-value">{sym}{total_invested:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with r2:
    st.markdown(
        f'<div class="metric-card" style="text-align:center;">'
        f'<div class="metric-label">Valeur finale (7%/an)</div>'
        f'<div class="metric-value" style="color:#D4AF37;">{sym}{final_fv:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
with r3:
    st.markdown(
        f'<div class="metric-card" style="text-align:center;">'
        f'<div class="metric-label">Gains des intérêts composés</div>'
        f'<div class="metric-value" style="color:#4CAF50;">{sym}{gain:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f'<div style="background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.3); '
    f'border-radius:10px; padding:14px 18px; margin-top:12px; color:#C8D4E8; font-size:0.88rem;">'
    f'💡 <strong style="color:#D4AF37;">La vraie valeur des économies quotidiennes</strong> : '
    f'économiser {sym}{monthly_to_invest}/mois en optimisant vos dépenses, puis investir cette somme, '
    f'vous rapporte {sym}{gain:,.0f} d\'intérêts supplémentaires sur {inv_years} ans. '
    f'Chaque café à 3 € préparé chez vous plutôt qu\'acheté = 3 € qui, investis, deviennent bien plus.'
    f'</div>',
    unsafe_allow_html=True,
)
