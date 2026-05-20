"""
Country-level economic data and platform-wide constants.
Sources: OECD, Eurostat, World Bank (2024 estimates).
"""

COUNTRIES = {
    "France": {
        "currency": "EUR",
        "avg_income": 2600,
        "avg_home_price_m2": 3800,
        "inflation": 0.025,
        "mortgage_rate": 0.038,
        "child_monthly_cost": 850,
        "retirement_age": 64,
        "pension_replacement_rate": 0.55,
        "capital_gains_tax": 0.30,
        "income_tax_brackets": [(0,11294,0),(11294,28797,0.11),(28797,82341,0.30),(82341,177106,0.41),(177106,float('inf'),0.45)],
    },
    "Belgium": {
        "currency": "EUR",
        "avg_income": 2900,
        "avg_home_price_m2": 2700,
        "inflation": 0.027,
        "mortgage_rate": 0.036,
        "child_monthly_cost": 800,
        "retirement_age": 65,
        "pension_replacement_rate": 0.50,
        "capital_gains_tax": 0.30,
        "income_tax_brackets": [(0,15200,0.25),(15200,26830,0.40),(26830,46440,0.45),(46440,float('inf'),0.50)],
    },
    "Canada": {
        "currency": "CAD",
        "avg_income": 4200,
        "avg_home_price_m2": 6500,
        "inflation": 0.028,
        "mortgage_rate": 0.052,
        "child_monthly_cost": 1100,
        "retirement_age": 65,
        "pension_replacement_rate": 0.40,
        "capital_gains_tax": 0.267,
        "income_tax_brackets": [(0,53359,0.15),(53359,106717,0.205),(106717,165430,0.26),(165430,235675,0.29),(235675,float('inf'),0.33)],
    },
    "Germany": {
        "currency": "EUR",
        "avg_income": 3200,
        "avg_home_price_m2": 3200,
        "inflation": 0.024,
        "mortgage_rate": 0.040,
        "child_monthly_cost": 900,
        "retirement_age": 67,
        "pension_replacement_rate": 0.48,
        "capital_gains_tax": 0.265,
        "income_tax_brackets": [(0,10908,0),(10908,62810,0.14),(62810,277826,0.42),(277826,float('inf'),0.45)],
    },
    "United Kingdom": {
        "currency": "GBP",
        "avg_income": 2800,
        "avg_home_price_m2": 4500,
        "inflation": 0.030,
        "mortgage_rate": 0.055,
        "child_monthly_cost": 950,
        "retirement_age": 66,
        "pension_replacement_rate": 0.38,
        "capital_gains_tax": 0.20,
        "income_tax_brackets": [(0,12570,0),(12570,50270,0.20),(50270,125140,0.40),(125140,float('inf'),0.45)],
    },
    "United States": {
        "currency": "USD",
        "avg_income": 4800,
        "avg_home_price_m2": 2200,
        "inflation": 0.026,
        "mortgage_rate": 0.068,
        "child_monthly_cost": 1300,
        "retirement_age": 67,
        "pension_replacement_rate": 0.40,
        "capital_gains_tax": 0.20,
        "income_tax_brackets": [(0,11600,0.10),(11600,47150,0.12),(47150,100525,0.22),(100525,191950,0.24),(191950,243725,0.32),(243725,609350,0.35),(609350,float('inf'),0.37)],
    },
    "Switzerland": {
        "currency": "CHF",
        "avg_income": 6500,
        "avg_home_price_m2": 8500,
        "inflation": 0.015,
        "mortgage_rate": 0.020,
        "child_monthly_cost": 1200,
        "retirement_age": 65,
        "pension_replacement_rate": 0.60,
        "capital_gains_tax": 0.0,
        "income_tax_brackets": [(0,17800,0.077),(17800,float('inf'),0.115)],
    },
    "Ivory Coast": {
        "currency": "XOF",
        "avg_income": 350000,
        "avg_home_price_m2": 900000,
        "inflation": 0.035,
        "mortgage_rate": 0.075,
        "child_monthly_cost": 80000,
        "retirement_age": 60,
        "pension_replacement_rate": 0.30,
        "capital_gains_tax": 0.15,
        "income_tax_brackets": [(0,600000,0.02),(600000,1200000,0.10),(1200000,float('inf'),0.25)],
    },
    "Senegal": {
        "currency": "XOF",
        "avg_income": 280000,
        "avg_home_price_m2": 600000,
        "inflation": 0.038,
        "mortgage_rate": 0.080,
        "child_monthly_cost": 60000,
        "retirement_age": 60,
        "pension_replacement_rate": 0.25,
        "capital_gains_tax": 0.15,
        "income_tax_brackets": [(0,600000,0.05),(600000,1500000,0.20),(1500000,float('inf'),0.30)],
    },
}

ASSET_CLASSES = {
    "Global Equities":    {"return": 0.075, "volatility": 0.16, "color": "#D4AF37"},
    "European Equities":  {"return": 0.065, "volatility": 0.15, "color": "#B8963E"},
    "Emerging Markets":   {"return": 0.085, "volatility": 0.22, "color": "#E8C547"},
    "Bonds (Gov)":        {"return": 0.030, "volatility": 0.05, "color": "#4A90D9"},
    "Bonds (Corp)":       {"return": 0.040, "volatility": 0.07, "color": "#357ABD"},
    "Real Estate (REIT)": {"return": 0.060, "volatility": 0.12, "color": "#5CB85C"},
    "Commodities":        {"return": 0.040, "volatility": 0.18, "color": "#F0AD4E"},
    "Cash":               {"return": 0.025, "volatility": 0.005,"color": "#9B9B9B"},
    "Crypto (BTC/ETH)":   {"return": 0.200, "volatility": 0.65, "color": "#FF6B35"},
    "Private Equity":     {"return": 0.110, "volatility": 0.25, "color": "#9B59B6"},
}

RISK_PROFILES = {
    "Très conservateur":  {"equities": 0.10, "bonds": 0.70, "real_estate": 0.10, "cash": 0.10, "expected_return": 0.032, "volatility": 0.04},
    "Conservateur":       {"equities": 0.25, "bonds": 0.55, "real_estate": 0.10, "cash": 0.10, "expected_return": 0.043, "volatility": 0.06},
    "Modéré":             {"equities": 0.45, "bonds": 0.35, "real_estate": 0.12, "cash": 0.08, "expected_return": 0.056, "volatility": 0.09},
    "Dynamique":          {"equities": 0.65, "bonds": 0.15, "real_estate": 0.12, "cash": 0.08, "expected_return": 0.067, "volatility": 0.13},
    "Agressif":           {"equities": 0.80, "bonds": 0.05, "real_estate": 0.10, "cash": 0.05, "expected_return": 0.076, "volatility": 0.17},
    "Très agressif":      {"equities": 0.90, "bonds": 0.00, "real_estate": 0.05, "cash": 0.05, "expected_return": 0.085, "volatility": 0.21},
}

CHILD_COST_CATEGORIES = {
    "Alimentation":       {"monthly_base": 200, "growth": 0.03},
    "Logement (part)":    {"monthly_base": 150, "growth": 0.02},
    "Santé":              {"monthly_base": 80,  "growth": 0.04},
    "Éducation":          {"monthly_base": 120, "growth": 0.035},
    "Vêtements":          {"monthly_base": 60,  "growth": 0.025},
    "Activités/Loisirs":  {"monthly_base": 100, "growth": 0.03},
    "Garde/Crèche":       {"monthly_base": 600, "growth": 0.03},
    "Transport":          {"monthly_base": 40,  "growth": 0.02},
    "Divers":             {"monthly_base": 100, "growth": 0.025},
}

HIGHER_EDUCATION_COSTS = {
    "Université publique (FR)":   {"annual_base": 3000,  "duration": 3},
    "Grande École (FR)":          {"annual_base": 12000, "duration": 5},
    "Business School Top (FR)":   {"annual_base": 20000, "duration": 5},
    "Université UK":              {"annual_base": 25000, "duration": 3},
    "Université US (State)":      {"annual_base": 22000, "duration": 4},
    "Université US (Private)":    {"annual_base": 58000, "duration": 4},
    "MBA Top (Intl)":             {"annual_base": 55000, "duration": 2},
}

INSURANCE_BENCHMARKS = {
    "life_coverage_multiplier": 10,
    "disability_coverage_pct": 0.70,
    "emergency_fund_months": 6,
    "term_life_pct_income": 0.01,
}

CAR_COSTS = {
    "Utilitaire (<15k€)":         {"purchase": 12000, "monthly_total": 400,  "depreciation_annual": 0.12},
    "Citadine (15-25k€)":         {"purchase": 20000, "monthly_total": 600,  "depreciation_annual": 0.15},
    "Berline (25-40k€)":          {"purchase": 32000, "monthly_total": 900,  "depreciation_annual": 0.18},
    "SUV Premium (40-70k€)":      {"purchase": 55000, "monthly_total": 1400, "depreciation_annual": 0.20},
    "Luxury (70k€+)":             {"purchase": 90000, "monthly_total": 2200, "depreciation_annual": 0.22},
}

CURRENCY_SYMBOLS = {
    "EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF",
    "CAD": "CA$", "XOF": "FCFA",
}
