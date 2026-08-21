import numpy as np
from typing import Dict, Any, List

# Crop profiles: optimal ranges for each parameter
CROP_PROFILES = {
    "MAIZE": {
        "emoji": "🌽",
        "ph_min": 5.8, "ph_max": 7.2,
        "nitrogen_min": 150, "temp_min": 21, "temp_max": 32,
        "rainfall_min": 500, "moisture_min": 25, "moisture_max": 45,
        "water_req": "Moderate (500-700mm)",
        "duration_days": 100,
        "description": "High-yield grain crop ideal for warm, well-drained soils with good nitrogen supply.",
        "growing_season": "June–November",
        "category": "Cereal",
    },
    "GROUNDNUT": {
        "emoji": "🥜",
        "ph_min": 5.5, "ph_max": 7.0,
        "nitrogen_min": 80, "temp_min": 22, "temp_max": 35,
        "rainfall_min": 400, "moisture_min": 20, "moisture_max": 40,
        "water_req": "Low-Moderate (400-600mm)",
        "duration_days": 120,
        "description": "Legume crop that fixes nitrogen; excellent for sandy loam and clay loam soils.",
        "growing_season": "June–October",
        "category": "Legume",
    },
    "MILLET": {
        "emoji": "🌾",
        "ph_min": 5.5, "ph_max": 7.5,
        "nitrogen_min": 60, "temp_min": 24, "temp_max": 38,
        "rainfall_min": 250, "moisture_min": 15, "moisture_max": 35,
        "water_req": "Low (250-400mm)",
        "duration_days": 75,
        "description": "Highly drought-tolerant cereal. Thrives in semi-arid regions with poor soil.",
        "growing_season": "June–September",
        "category": "Cereal",
    },
    "SOYBEAN": {
        "emoji": "🫘",
        "ph_min": 6.0, "ph_max": 7.0,
        "nitrogen_min": 80, "temp_min": 20, "temp_max": 30,
        "rainfall_min": 500, "moisture_min": 28, "moisture_max": 50,
        "water_req": "Moderate (500-700mm)",
        "duration_days": 110,
        "description": "Protein-rich legume that improves soil nitrogen. Good for tropical climates.",
        "growing_season": "July–November",
        "category": "Legume",
    },
    "SUNFLOWER": {
        "emoji": "🌻",
        "ph_min": 6.0, "ph_max": 7.5,
        "nitrogen_min": 100, "temp_min": 20, "temp_max": 33,
        "rainfall_min": 400, "moisture_min": 20, "moisture_max": 40,
        "water_req": "Low-Moderate (400-600mm)",
        "duration_days": 90,
        "description": "Oil-seed crop resistant to heat and mild drought. Well-drained soils preferred.",
        "growing_season": "October–January",
        "category": "Oil Seed",
    },
    "COTTON": {
        "emoji": "🪴",
        "ph_min": 5.8, "ph_max": 7.5,
        "nitrogen_min": 100, "temp_min": 25, "temp_max": 38,
        "rainfall_min": 500, "moisture_min": 25, "moisture_max": 45,
        "water_req": "Moderate-High (600-900mm)",
        "duration_days": 150,
        "description": "Cash crop for warm climates; requires long frost-free season and good drainage.",
        "growing_season": "June–December",
        "category": "Cash Crop",
    },
    "SORGHUM": {
        "emoji": "🌿",
        "ph_min": 5.5, "ph_max": 7.5,
        "nitrogen_min": 80, "temp_min": 23, "temp_max": 38,
        "rainfall_min": 300, "moisture_min": 18, "moisture_max": 38,
        "water_req": "Low (300-500mm)",
        "duration_days": 90,
        "description": "Versatile drought-tolerant cereal suitable for dryland farming.",
        "growing_season": "June–October",
        "category": "Cereal",
    },
    "WHEAT": {
        "emoji": "🌾",
        "ph_min": 6.0, "ph_max": 7.5,
        "nitrogen_min": 100, "temp_min": 12, "temp_max": 24,
        "rainfall_min": 300, "moisture_min": 20, "moisture_max": 40,
        "water_req": "Low-Moderate (350-500mm)",
        "duration_days": 120,
        "description": "Winter cereal suitable for cooler climates and fertile, well-drained soils.",
        "growing_season": "November–March",
        "category": "Cereal",
    },
}

def score_crop(crop_name: str, features: Dict[str, Any]) -> float:
    """Score a crop from 0-100 based on how well the farm features match optimal conditions."""
    profile = CROP_PROFILES.get(crop_name)
    if not profile:
        return 50.0

    ph = features.get('ph', 6.5)
    nitrogen = features.get('nitrogen', 150)
    temperature = features.get('temperature', 28)
    rainfall = features.get('rainfall', 700)
    moisture = features.get('moisture', 30)

    score = 0.0

    # pH match (0-25 points)
    if profile['ph_min'] <= ph <= profile['ph_max']:
        score += 25
    elif profile['ph_min'] - 0.5 <= ph <= profile['ph_max'] + 0.5:
        score += 15
    elif profile['ph_min'] - 1.0 <= ph <= profile['ph_max'] + 1.0:
        score += 7

    # Nitrogen (0-20 points)
    if nitrogen >= profile['nitrogen_min'] * 1.5:
        score += 20
    elif nitrogen >= profile['nitrogen_min']:
        score += 14
    elif nitrogen >= profile['nitrogen_min'] * 0.7:
        score += 7

    # Temperature (0-25 points)
    if profile['temp_min'] <= temperature <= profile['temp_max']:
        score += 25
    elif profile['temp_min'] - 3 <= temperature <= profile['temp_max'] + 3:
        score += 14
    elif profile['temp_min'] - 6 <= temperature <= profile['temp_max'] + 6:
        score += 6

    # Rainfall (0-20 points)
    if rainfall >= profile['rainfall_min'] * 1.5:
        score += 20
    elif rainfall >= profile['rainfall_min']:
        score += 14
    elif rainfall >= profile['rainfall_min'] * 0.7:
        score += 7

    # Moisture (0-10 points)
    if profile['moisture_min'] <= moisture <= profile['moisture_max']:
        score += 10
    elif profile['moisture_min'] - 5 <= moisture <= profile['moisture_max'] + 10:
        score += 5

    return round(min(100, score), 1)

def predict(features: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return ranked crop recommendations with suitability scores and details."""
    results = []
    for crop_name, profile in CROP_PROFILES.items():
        suit = score_crop(crop_name, features)
        results.append({
            "crop_name": crop_name,
            "emoji": profile["emoji"],
            "suitability_pct": suit,
            "category": profile["category"],
            "description": profile["description"],
            "growing_season": profile["growing_season"],
            "water_requirement": profile["water_req"],
            "duration_days": profile["duration_days"],
            "details": {
                "soil_compatibility": f"Optimal pH {profile['ph_min']}–{profile['ph_max']}; needs {profile['nitrogen_min']}+ kg/ha nitrogen",
                "temperature_range": f"{profile['temp_min']}–{profile['temp_max']}°C",
                "rainfall_requirement": f"Minimum {profile['rainfall_min']} mm/year",
                "water_requirement": profile["water_req"],
            }
        })

    results.sort(key=lambda x: x['suitability_pct'], reverse=True)
    for i, r in enumerate(results):
        r['rank'] = i + 1

    return results[:5]

def train_model():
    """Stub — scoring is rule-based, no model file needed."""
    pass
