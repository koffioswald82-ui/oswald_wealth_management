"""
Debt Engine — Avalanche (high rate first) vs Snowball (low balance first).
Shows interest saved, time to debt-free, and wealth impact of freed payments.
"""
import copy


class DebtEngine:

    @staticmethod
    def payoff_schedule(debts: list, strategy: str = "avalanche",
                         extra_monthly: float = 0) -> dict:
        """
        debts: [{"name":str, "balance":float, "rate_annual":float, "min_payment":float}]
        Returns month-by-month schedule until all debts paid.
        """
        work = copy.deepcopy(debts)
        if strategy == "avalanche":
            work.sort(key=lambda d: -d["rate_annual"])
        else:
            work.sort(key=lambda d: d["balance"])

        month = 0
        total_interest = 0
        max_months = 600
        schedule = []
        payoff_order = []
        paid_names = set()

        while any(d["balance"] > 0.01 for d in work) and month < max_months:
            month += 1
            month_interest = 0.0

            # Accrue interest
            for d in work:
                if d["balance"] > 0.01:
                    rate_m = d["rate_annual"] / 12
                    interest = d["balance"] * rate_m
                    d["balance"] += interest
                    month_interest += interest
                    total_interest += interest

            # Pay minimums on all debts
            for d in work:
                if d["balance"] > 0.01:
                    pmt = min(d["min_payment"], d["balance"])
                    d["balance"] = max(d["balance"] - pmt, 0.0)

            # Apply extra to priority debt (first non-zero in sorted order)
            remaining = extra_monthly
            for d in work:
                if d["balance"] > 0.01 and remaining > 0:
                    applied = min(remaining, d["balance"])
                    d["balance"] = max(d["balance"] - applied, 0.0)
                    remaining -= applied
                    break

            # Record payoffs this month
            for d in work:
                if d["balance"] <= 0.01 and d["name"] not in paid_names:
                    paid_names.add(d["name"])
                    payoff_order.append({"name": d["name"], "month": month})

            schedule.append({
                "month": month,
                "balances": {d["name"]: max(d["balance"], 0.0) for d in work},
                "interest": month_interest,
            })

        return {
            "strategy": strategy,
            "total_months": month,
            "total_interest": total_interest,
            "payoff_order": payoff_order,
            "schedule": schedule,
        }

    @staticmethod
    def compare_strategies(debts: list, extra_monthly: float = 0) -> dict:
        av = DebtEngine.payoff_schedule(debts, "avalanche", extra_monthly)
        sn = DebtEngine.payoff_schedule(debts, "snowball", extra_monthly)
        winner = "avalanche" if av["total_interest"] <= sn["total_interest"] else "snowball"
        return {
            "avalanche": av,
            "snowball": sn,
            "winner": winner,
            "interest_saved": abs(sn["total_interest"] - av["total_interest"]),
            "months_diff": abs(av["total_months"] - sn["total_months"]),
        }

    @staticmethod
    def minimum_only(debts: list) -> dict:
        return DebtEngine.payoff_schedule(debts, "avalanche", extra_monthly=0)

    @staticmethod
    def investment_impact(monthly_freed: float, years: int,
                           annual_return: float = 0.07) -> float:
        """Future value if freed payment is redirected to investment."""
        r_m = (1 + annual_return) ** (1 / 12) - 1
        n = years * 12
        if r_m > 0:
            return monthly_freed * ((1 + r_m) ** n - 1) / r_m
        return monthly_freed * n

    @staticmethod
    def total_debt_cost(debts: list) -> dict:
        """Current total balance and annual interest cost."""
        total_balance = sum(d["balance"] for d in debts)
        annual_interest = sum(d["balance"] * d["rate_annual"] for d in debts)
        return {"total_balance": total_balance, "annual_interest": annual_interest}
