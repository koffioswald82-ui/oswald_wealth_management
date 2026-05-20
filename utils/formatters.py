from utils.constants import CURRENCY_SYMBOLS

def format_currency(amount: float, currency: str = "EUR", compact: bool = False) -> str:
    symbol = CURRENCY_SYMBOLS.get(currency, currency + " ")
    if compact:
        if abs(amount) >= 1_000_000:
            return f"{symbol}{amount/1_000_000:.1f}M"
        if abs(amount) >= 1_000:
            return f"{symbol}{amount/1_000:.0f}k"
    return f"{symbol}{amount:,.0f}"

def format_percentage(value: float, decimals: int = 1) -> str:
    return f"{value * 100:.{decimals}f}%"

def format_years(years: float) -> str:
    y = int(years)
    m = int((years - y) * 12)
    if m == 0:
        return f"{y} ans"
    return f"{y} ans {m} mois"

def color_for_score(score: float, max_score: float = 1000) -> str:
    pct = score / max_score
    if pct >= 0.75:
        return "#4CAF50"
    if pct >= 0.50:
        return "#D4AF37"
    if pct >= 0.25:
        return "#FF9800"
    return "#F44336"

def score_label(score: float, max_score: float = 1000) -> str:
    pct = score / max_score
    if pct >= 0.80:
        return "Excellent"
    if pct >= 0.65:
        return "Très Bon"
    if pct >= 0.50:
        return "Bon"
    if pct >= 0.35:
        return "Satisfaisant"
    if pct >= 0.20:
        return "À Améliorer"
    return "Critique"

def risk_color(level: str) -> str:
    mapping = {
        "Faible": "#4CAF50",
        "Modéré": "#D4AF37",
        "Élevé": "#FF9800",
        "Critique": "#F44336",
    }
    return mapping.get(level, "#8899BB")
