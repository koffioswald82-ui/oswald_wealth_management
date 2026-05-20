"""
AI Coaching Engine — Personalized, impact-quantified financial insights.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from engines.ai_coaching import AICoachingEngine
from utils.formatters import format_currency
from app.config import ANTHROPIC_API_KEY

st.set_page_config(page_title="Coaching IA — Oswald Wealth", page_icon="🤖", layout="wide")
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if not st.session_state.get("profile"):
    st.warning("⚠️ Créez votre profil d'abord.")
    st.stop()

p      = st.session_state.profile
coach  = AICoachingEngine(p)

st.markdown(f'<div class="hero-banner"><div class="hero-title">🤖 AI Financial Coach</div><div class="hero-subtitle">Conseils personnalisés avec impact chiffré — {p.name}</div></div>', unsafe_allow_html=True)

insights = coach.generate_all_insights()

# Category filter
categories = list(set(i["category"] for i in insights))
all_cats   = ["Tous"] + sorted(categories)
selected_cat = st.selectbox("Filtrer par catégorie", all_cats)

if selected_cat != "Tous":
    filtered_insights = [i for i in insights if i["category"] == selected_cat]
else:
    filtered_insights = insights

# Stats row
type_counts = {"critical": 0, "warning": 0, "success": 0, "info": 0}
for i in insights:
    type_counts[i.get("type","info")] += 1

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Critiques</div>
    <div class="kpi-value" style="color:#F44336;">{type_counts['critical']}</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Alertes</div>
    <div class="kpi-value" style="color:#FF9800;">{type_counts['warning']}</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Positifs</div>
    <div class="kpi-value" style="color:#4CAF50;">{type_counts['success']}</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Informations</div>
    <div class="kpi-value" style="color:#4A90D9;">{type_counts['info']}</div></div>""", unsafe_allow_html=True)

st.markdown("---")

# Display insights
if not filtered_insights:
    st.success("✅ Aucune alerte dans cette catégorie — situation saine !")
else:
    for insight in filtered_insights:
        itype = insight.get("type", "info")
        type_config = {
            "critical": ("danger", "🚨", "#F44336"),
            "warning":  ("warning", "⚠️", "#FF9800"),
            "success":  ("success", "✅", "#4CAF50"),
            "info":     ("", "💡", "#4A90D9"),
        }
        css_class, icon, color = type_config.get(itype, ("", "ℹ️", "#8899BB"))

        actions_html = ""
        if insight.get("actions"):
            actions_html = "<ul style='margin:8px 0 0 16px; color:#C8D4E8;'>" + "".join(f"<li>{a}</li>" for a in insight["actions"]) + "</ul>"

        impact_html = ""
        if insight.get("impact"):
            impact_html = f'<div class="insight-impact">💰 {insight["impact"]}</div>'

        st.markdown(f"""
        <div class="insight-card {css_class}" style="margin-bottom:16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span style="font-size:1.2rem;">{icon}</span>
                <span style="font-weight:600; color:{color}; font-size:1rem;">{insight['title']}</span>
                <span style="font-size:0.7rem; background:rgba(255,255,255,0.05); padding:2px 8px; border-radius:10px; color:#8899BB;">{insight['category']}</span>
            </div>
            <div class="insight-text">{insight['text']}</div>
            {actions_html}
            {impact_html}
        </div>
        """, unsafe_allow_html=True)

# ---- Claude AI Analysis (optional) ----
st.markdown("---")
st.markdown('<div class="section-header">🤖 Analyse Approfondie par Claude AI</div>', unsafe_allow_html=True)

api_key_input = st.text_input(
    "Clé API Anthropic (optionnel — pour analyse IA avancée)",
    value=ANTHROPIC_API_KEY,
    type="password",
    placeholder="sk-ant-...",
    help="Votre clé reste locale, jamais partagée."
)

if st.button("Générer l'analyse IA personnalisée", type="primary"):
    if not api_key_input:
        st.warning("Saisissez votre clé Anthropic pour activer l'analyse Claude.")
    else:
        with st.spinner("Claude analyse votre profil..."):
            analysis = coach.claude_ai_analysis(api_key_input)
        if analysis:
            st.markdown(f"""
            <div style="background:rgba(19,27,46,0.9); border:1px solid rgba(212,175,55,0.3); border-radius:12px; padding:24px; margin-top:16px;">
                <div style="font-size:0.8rem; color:#D4AF37; margin-bottom:12px; font-weight:600;">ANALYSE CLAUDE AI</div>
                <div style="color:#E8E8E8; line-height:1.7; white-space:pre-wrap;">{analysis}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Analyse non disponible. Vérifiez votre clé API.")
