"""Model selected plans, without treating modeled cost as a market quote."""
from decimal import Decimal, ROUND_CEILING


def estimate(plan, monthly_units, peak_daily_units=0):
    if isinstance(monthly_units, bool) or not isinstance(monthly_units, int) or not 0 <= monthly_units <= 10_000_000:
        raise ValueError("Monthly units must be an integer between 0 and 10,000,000.")
    if not isinstance(peak_daily_units, int) or not 0 <= peak_daily_units <= monthly_units:
        raise ValueError("Peak daily units must be between zero and monthly units.")
    if plan.get("daily_limit") is not None and peak_daily_units > plan["daily_limit"]:
        return {"available": False, "reason": "The workload exceeds this plan's daily allowance."}
    excess = max(0, monthly_units - plan["included"])
    if excess and plan.get("overage_per_1000") is None:
        return {"available": False, "reason": "This plan does not allow the modeled overage."}
    # The source must explicitly establish whether billing uses whole buckets.
    units = Decimal(excess) / 1000
    if plan["rounding"] == "bucket":
        units = units.to_integral_value(rounding=ROUND_CEILING)
    elif plan["rounding"] != "proportional":
        raise ValueError("Unknown billing rounding policy.")
    overage = units * Decimal(plan.get("overage_per_1000") or "0")
    base = Decimal(plan["base"])
    return {"available": True, "base": base, "overage": overage, "total": base + overage, "excess": excess}


def best_volume_tier(plan, monthly_units, peak_daily_units=0):
    """Choose among supplied volume tiers of the same edition, not providers."""
    candidates = []
    for tier in plan.get("tiers", [{}]):
        variant = {**plan, **tier}
        result = estimate(variant, monthly_units, peak_daily_units)
        if result["available"]:
            candidates.append({**result, "included": variant["included"]})
    if not candidates:
        return estimate(plan, monthly_units, peak_daily_units)
    return min(candidates, key=lambda r: (r["total"], -r["included"]))
