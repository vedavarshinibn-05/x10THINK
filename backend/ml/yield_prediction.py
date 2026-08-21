import numpy as np
from typing import Dict, Any

# Yield lookup table (t/ha): crop -> (min, expected, max, duration_days, water_req_mm)
YIELD_DATA = {
    "MAIZE":     {"min": 3.5, "expected": 4.8, "max": 6.5, "duration": 100, "water_mm": 600, "unit": "t/ha"},
    "GROUNDNUT": {"min": 1.6, "expected": 2.1, "max": 2.8, "duration": 120, "water_mm": 500, "unit": "t/ha"},
    "MILLET":    {"min": 1.2, "expected": 1.8, "max": 2.4, "duration": 75,  "water_mm": 350, "unit": "t/ha"},
    "SOYBEAN":   {"min": 1.8, "expected": 2.5, "max": 3.2, "duration": 110, "water_mm": 600, "unit": "t/ha"},
    "SUNFLOWER": {"min": 1.0, "expected": 1.5, "max": 2.0, "duration": 90,  "water_mm": 500, "unit": "t/ha"},
    "COTTON":    {"min": 1.5, "expected": 2.2, "max": 3.0, "duration": 150, "water_mm": 750, "unit": "t/ha"},
    "SORGHUM":   {"min": 1.5, "expected": 2.0, "max": 2.8, "duration": 90,  "water_mm": 400, "unit": "t/ha"},
    "WHEAT":     {"min": 2.5, "expected": 3.5, "max": 4.5, "duration": 120, "water_mm": 450, "unit": "t/ha"},
}

def _adjust_for_conditions(base_yield: float, features: Dict[str, Any]) -> float:
    """Apply multiplicative factors based on field conditions."""
    factor = 1.0
    moisture = features.get('moisture', 30)
    nitrogen = features.get('nitrogen', 150)
    rainfall = features.get('rainfall', 700)
    ph = features.get('ph', 6.5)
    ndvi = features.get('ndvi', 0.5)

    # Moisture factor
    if moisture < 15: factor *= 0.70
    elif moisture < 22: factor *= 0.85
    elif 25 <= moisture <= 45: factor *= 1.05
    elif moisture > 55: factor *= 0.90

    # Nitrogen factor
    if nitrogen < 80: factor *= 0.75
    elif nitrogen < 150: factor *= 0.90
    elif nitrogen >= 220: factor *= 1.08

    # Rainfall factor
    if rainfall < 300: factor *= 0.75
    elif rainfall < 500: factor *= 0.90
    elif rainfall >= 900: factor *= 1.05

    # pH factor
    if 6.0 <= ph <= 7.2: factor *= 1.03
    elif ph < 5.5 or ph > 8.0: factor *= 0.80

    # NDVI (existing land health)
    if ndvi >= 0.6: factor *= 1.05
    elif ndvi < 0.3: factor *= 0.90

    return round(factor, 3)

def predict(crop_name: str, features: Dict[str, Any]) -> Dict[str, Any]:
    crop = crop_name.upper()
    data = YIELD_DATA.get(crop, YIELD_DATA["MAIZE"])
    
    factor = _adjust_for_conditions(data['expected'], features)
    
    adjusted_expected = round(data['expected'] * factor, 2)
    adjusted_min = round(data['min'] * max(0.8, factor - 0.1), 2)
    adjusted_max = round(data['max'] * min(1.2, factor + 0.1), 2)

    return {
        "crop_name": crop,
        "expected_yield": adjusted_expected,
        "yield_min": adjusted_min,
        "yield_max": adjusted_max,
        "unit": data["unit"],
        "duration_days": data["duration"],
        "water_requirement_mm": data["water_mm"],
        "adjustment_factor": factor,
        "influencing_factors": {
            "moisture": features.get('moisture', 30),
            "nitrogen": features.get('nitrogen', 150),
            "rainfall": features.get('rainfall', 700),
            "ph": features.get('ph', 6.5),
        },
        "notes": (
            f"Expected yield of {adjusted_expected} t/ha over {data['duration']} days. "
            f"Range: {adjusted_min}–{adjusted_max} t/ha depending on management practices. "
            f"Water requirement: {data['water_mm']} mm/season."
        )
    }

def train_model():
    """Rule-based model — no training needed."""
    pass
