"""
Prophet Forecasting Engine
Time-series forecasting for income, property values, and wealth trajectory.
Prophet is optional — falls back to linear projection if not installed.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from models.user_profile import UserProfile
from utils.constants import COUNTRIES

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False


class ProphetForecaster:

    def __init__(self, profile: UserProfile):
        self.p    = profile
        self.cd   = COUNTRIES.get(profile.country, COUNTRIES["France"])

    def _make_history(self, base_value: float, growth_rate: float,
                      volatility: float, months_back: int = 36) -> pd.DataFrame:
        """
        Synthesise plausible historical data for a given metric.
        We don't have real history, so we back-project with noise.
        """
        rng   = np.random.default_rng(hash(self.p.name) % (2**31))
        dates = pd.date_range(end=datetime.today(), periods=months_back, freq="MS")
        vals  = [base_value / (1 + growth_rate) ** ((months_back - i) / 12) for i in range(months_back)]
        noise = rng.normal(0, volatility, months_back)
        vals  = np.array(vals) * (1 + noise)
        return pd.DataFrame({"ds": dates, "y": vals})

    def _linear_fallback(self, base: float, growth: float, periods: int, freq: str = "MS") -> pd.DataFrame:
        """Simple linear projection when Prophet is unavailable."""
        future_dates = pd.date_range(start=datetime.today(), periods=periods, freq=freq)
        vals = [base * (1 + growth) ** (i / 12) for i in range(periods)]
        return pd.DataFrame({
            "ds": future_dates,
            "yhat": vals,
            "yhat_lower": [v * 0.85 for v in vals],
            "yhat_upper": [v * 1.15 for v in vals],
        })

    def forecast_income(self, periods_months: int = 120) -> pd.DataFrame:
        """Forecast monthly income over the next <periods_months> months."""
        base    = self.p.total_income
        growth  = self.p.salary_growth_pct / 12

        if not PROPHET_AVAILABLE:
            return self._linear_fallback(base, self.p.salary_growth_pct, periods_months)

        history = self._make_history(base, self.p.salary_growth_pct, volatility=0.03)

        model = Prophet(
            changepoint_prior_scale=0.05,
            seasonality_mode="multiplicative",
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False,
        )
        # Add salary growth as a custom regressor proxy via seasonality
        model.fit(history)
        future   = model.make_future_dataframe(periods=periods_months, freq="MS")
        forecast = model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods_months).reset_index(drop=True)

    def forecast_property_value(self, periods_months: int = 120) -> pd.DataFrame:
        """Forecast property value appreciation."""
        base         = self.p.target_property_value
        country_data = COUNTRIES.get(self.p.country, COUNTRIES["France"])
        appre_rate   = 0.03  # historical average

        if not PROPHET_AVAILABLE:
            return self._linear_fallback(base, appre_rate, periods_months)

        history = self._make_history(base, appre_rate, volatility=0.06, months_back=48)

        model = Prophet(
            changepoint_prior_scale=0.1,
            seasonality_mode="additive",
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
        )
        model.add_seasonality(name="quarterly", period=91.25, fourier_order=3)
        model.fit(history)
        future   = model.make_future_dataframe(periods=periods_months, freq="MS")
        forecast = model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods_months).reset_index(drop=True)

    def forecast_wealth_trajectory(self, periods_months: int = 360) -> pd.DataFrame:
        """Forecast total wealth using trend + Monte Carlo noise."""
        from utils.financial_math import future_value

        base     = max(self.p.current_net_worth, 1000)
        monthly  = self.p.monthly_savings
        ret      = 0.065

        if not PROPHET_AVAILABLE:
            # Build from compound growth
            vals = []
            w = base
            dates = pd.date_range(start=datetime.today(), periods=periods_months, freq="MS")
            for i in range(periods_months):
                w = w * (1 + ret / 12) + monthly
                vals.append(w)
            std = [v * 0.10 for v in vals]  # ±10% confidence interval
            return pd.DataFrame({
                "ds": dates,
                "yhat": vals,
                "yhat_lower": [v - s for v, s in zip(vals, std)],
                "yhat_upper": [v + s for v, s in zip(vals, std)],
            })

        # Build synthetic history (past 5 years)
        history = self._make_history(base, ret, volatility=0.08, months_back=60)

        model = Prophet(
            changepoint_prior_scale=0.15,
            seasonality_mode="multiplicative",
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False,
        )
        model.fit(history)
        future   = model.make_future_dataframe(periods=periods_months, freq="MS")
        forecast = model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods_months).reset_index(drop=True)

    @staticmethod
    def is_available() -> bool:
        return PROPHET_AVAILABLE
