from typing import Dict, Any

# 2026 Indian Market Prices (INR per ton)
MARKET_PRICES = {
    "MAIZE":     20000,
    "GROUNDNUT": 55000,
    "MILLET":    22000,
    "SOYBEAN":   45000,
    "SUNFLOWER": 60000,
    "COTTON":    75000,
    "SORGHUM":   20000,
    "WHEAT":     25000,
}

# Cost templates per hectare (INR)
COST_TEMPLATES = {
    "MAIZE":     {"seed": 4500,  "fertilizer": 8000,  "irrigation": 5000, "labor": 14000, "other": 3500},
    "GROUNDNUT": {"seed": 7000,  "fertilizer": 7000,  "irrigation": 4500, "labor": 13000, "other": 3000},
    "MILLET":    {"seed": 2000,  "fertilizer": 4500,  "irrigation": 2500, "labor": 10000, "other": 2000},
    "SOYBEAN":   {"seed": 5000,  "fertilizer": 8500,  "irrigation": 5000, "labor": 13000, "other": 3500},
    "SUNFLOWER": {"seed": 4000,  "fertilizer": 6500,  "irrigation": 4000, "labor": 11000, "other": 2500},
    "COTTON":    {"seed": 5500,  "fertilizer": 12000, "irrigation": 8000, "labor": 18000, "other": 4500},
    "SORGHUM":   {"seed": 1500,  "fertilizer": 5000,  "irrigation": 2500, "labor": 10000, "other": 2000},
    "WHEAT":     {"seed": 3500,  "fertilizer": 8000,  "irrigation": 4500, "labor": 12000, "other": 2500},
}

def estimate_profitability(
    crop_name: str,
    area_hectares: float,
    yield_data: Dict[str, Any],
    market_price_override: float = None
) -> Dict[str, Any]:
    crop = crop_name.upper()
    template = COST_TEMPLATES.get(crop, COST_TEMPLATES["MAIZE"])
    market_price = market_price_override or MARKET_PRICES.get(crop, 20000)

    expected_yield = yield_data.get("expected_yield", 3.0)  # t/ha
    yield_min = yield_data.get("yield_min", expected_yield * 0.8)
    yield_max = yield_data.get("yield_max", expected_yield * 1.2)

    # Scale costs by area
    seed_cost       = round(template["seed"]       * area_hectares)
    fertilizer_cost = round(template["fertilizer"] * area_hectares)
    irrigation_cost = round(template["irrigation"] * area_hectares)
    labor_cost      = round(template["labor"]      * area_hectares)
    other_cost      = round(template["other"]      * area_hectares)
    total_cost      = seed_cost + fertilizer_cost + irrigation_cost + labor_cost + other_cost

    # Revenue
    total_yield     = round(expected_yield * area_hectares, 2)
    revenue         = round(total_yield * market_price)
    revenue_min     = round(yield_min * area_hectares * market_price)
    revenue_max     = round(yield_max * area_hectares * market_price)
    profit          = revenue - total_cost
    profit_min      = revenue_min - total_cost
    profit_max      = revenue_max - total_cost
    roi_pct         = round((profit / total_cost) * 100, 1) if total_cost > 0 else 0
    break_even_yield= round(total_cost / market_price, 2)

    return {
        "crop_name": crop,
        "area_hectares": area_hectares,
        "market_price_inr_per_ton": market_price,
        "costs": {
            "seed":        seed_cost,
            "fertilizer":  fertilizer_cost,
            "irrigation":  irrigation_cost,
            "labor":       labor_cost,
            "other":       other_cost,
            "total":       total_cost,
        },
        "revenue": {
            "expected_yield_tons": total_yield,
            "estimated_revenue":  revenue,
            "revenue_min":        revenue_min,
            "revenue_max":        revenue_max,
        },
        "profit": {
            "potential_return":   profit,
            "return_min":         profit_min,
            "return_max":         profit_max,
            "roi_percent":        roi_pct,
            "break_even_yield_tons": break_even_yield,
        },
        "disclaimer": (
            "These are estimates based on 2026 market prices and typical input costs in India. "
            "Actual profits may vary due to market price fluctuations, weather, and management practices."
        )
    }
