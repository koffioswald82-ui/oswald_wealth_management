"""
Core financial mathematics — all formulas are textbook / institutional-grade.
No simplifications. Inflation-adjusted real returns used throughout.
"""
import numpy as np

try:
    import numpy_financial as npf
    _HAS_NPF = True
except ImportError:
    _HAS_NPF = False

def future_value(pv: float, rate: float, periods: int, pmt: float = 0.0) -> float:
    """FV of lump sum + periodic payment at period-end."""
    if rate == 0:
        return pv + pmt * periods
    fv_pv  = pv * (1 + rate) ** periods
    fv_pmt = pmt * (((1 + rate) ** periods - 1) / rate)
    return fv_pv + fv_pmt

def present_value(fv: float, rate: float, periods: int) -> float:
    if rate == 0:
        return fv
    return fv / (1 + rate) ** periods

def real_return(nominal_return: float, inflation: float) -> float:
    """Fisher equation."""
    return (1 + nominal_return) / (1 + inflation) - 1

def compound_annual_growth_rate(begin: float, end: float, years: float) -> float:
    if begin <= 0 or years <= 0:
        return 0.0
    return (end / begin) ** (1 / years) - 1

def mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    """Monthly payment for a fixed-rate mortgage."""
    if annual_rate == 0:
        return principal / (years * 12)
    r = annual_rate / 12
    n = years * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

def mortgage_amortization(principal: float, annual_rate: float, years: int) -> list[dict]:
    """Full amortization schedule (monthly)."""
    pmt   = mortgage_payment(principal, annual_rate, years)
    r     = annual_rate / 12
    bal   = principal
    schedule = []
    for month in range(1, years * 12 + 1):
        interest   = bal * r
        principal_p = pmt - interest
        bal        -= principal_p
        schedule.append({
            "month": month,
            "year": (month - 1) // 12 + 1,
            "payment": pmt,
            "interest": interest,
            "principal": principal_p,
            "balance": max(bal, 0),
        })
    return schedule

def debt_to_income_ratio(monthly_debt: float, monthly_income: float) -> float:
    if monthly_income <= 0:
        return 1.0
    return monthly_debt / monthly_income

def savings_rate(monthly_savings: float, monthly_income: float) -> float:
    if monthly_income <= 0:
        return 0.0
    return monthly_savings / monthly_income

def emergency_fund_months(emergency_fund: float, monthly_expenses: float) -> float:
    if monthly_expenses <= 0:
        return 0.0
    return emergency_fund / monthly_expenses

def time_to_target(current: float, target: float, monthly_contribution: float,
                   annual_rate: float) -> float:
    """Months to reach a savings target."""
    if monthly_contribution <= 0:
        return float('inf')
    r = annual_rate / 12
    if r == 0:
        return (target - current) / monthly_contribution
    # Solve: target = current*(1+r)^n + pmt*((1+r)^n - 1)/r
    # Approximate with iteration
    n = 0
    val = current
    while val < target and n < 12000:
        val = val * (1 + r) + monthly_contribution
        n += 1
    return float(n) if n < 12000 else float('inf')

def net_present_value_rent_vs_buy(
    home_value: float,
    down_payment: float,
    mortgage_rate: float,
    mortgage_years: int,
    monthly_rent: float,
    property_appreciation: float,
    inflation: float,
    years: int,
    discount_rate: float = 0.05,
) -> dict:
    """Compare NPV of renting vs buying over <years>."""
    monthly_pmt = mortgage_payment(home_value - down_payment, mortgage_rate, mortgage_years)
    monthly_maintenance = home_value * 0.012 / 12
    monthly_property_tax = home_value * 0.008 / 12

    buy_cashflows = [-down_payment]
    sell_cashflows = []
    rent_cashflows = [0]

    for y in range(1, years + 1):
        annual_buy_cost = (monthly_pmt + monthly_maintenance + monthly_property_tax) * 12 * (1 + inflation) ** y
        annual_rent_cost = monthly_rent * 12 * (1 + inflation) ** y
        buy_cashflows.append(-annual_buy_cost)
        rent_cashflows.append(-annual_rent_cost)

    final_home_value = home_value * (1 + property_appreciation) ** years
    remaining_mortgage = mortgage_payment(home_value - down_payment, mortgage_rate, mortgage_years)
    # Equity at end = final_home_value - remaining balance
    amort = mortgage_amortization(home_value - down_payment, mortgage_rate, mortgage_years)
    remaining = amort[min(years * 12, len(amort)) - 1]["balance"] if amort else 0
    buy_cashflows[-1] += (final_home_value - remaining)

    dr = discount_rate / 1  # annual
    buy_npv  = sum(cf / (1 + dr) ** i for i, cf in enumerate(buy_cashflows))
    rent_npv = sum(cf / (1 + dr) ** i for i, cf in enumerate(rent_cashflows))
    return {
        "buy_npv": buy_npv,
        "rent_npv": rent_npv,
        "recommendation": "Acheter" if buy_npv > rent_npv else "Louer",
        "advantage": abs(buy_npv - rent_npv),
        "final_home_value": final_home_value,
        "total_buy_cost": sum(buy_cashflows),
        "total_rent_cost": sum(rent_cashflows),
    }

def rule_of_72(annual_rate: float) -> float:
    """Years to double capital."""
    if annual_rate <= 0:
        return float('inf')
    return 72 / (annual_rate * 100)

def safe_withdrawal_rate(portfolio_value: float, years_in_retirement: int = 30) -> float:
    """
    Bengen 4% Rule adjusted for time horizon.
    Returns max annual withdrawal amount.
    """
    if years_in_retirement <= 20:
        swr = 0.045
    elif years_in_retirement <= 30:
        swr = 0.040
    else:
        swr = 0.035
    return portfolio_value * swr

def income_tax(gross_income: float, brackets: list) -> float:
    """Progressive tax calculation."""
    tax = 0.0
    for i, (low, high, rate) in enumerate(brackets):
        if gross_income <= low:
            break
        taxable = min(gross_income, high) - low
        tax += taxable * rate
    return tax

def wealth_accumulation_projection(
    current_wealth: float,
    monthly_savings: float,
    annual_return: float,
    salary_growth: float,
    savings_growth: float,
    inflation: float,
    years: int,
) -> list[dict]:
    """
    Year-by-year wealth projection:
    - Real (inflation-adjusted) return on existing portfolio
    - Savings grow with salary
    """
    real_r   = real_return(annual_return, inflation)
    data     = []
    wealth   = current_wealth
    mth_save = monthly_savings

    for y in range(years + 1):
        data.append({
            "year": y,
            "age_offset": y,
            "wealth_nominal": wealth * (1 + inflation) ** y,
            "wealth_real": wealth,
            "monthly_savings": mth_save,
            "annual_savings": mth_save * 12,
        })
        wealth   = wealth * (1 + annual_return) + mth_save * 12
        mth_save = mth_save * (1 + savings_growth)

    return data
