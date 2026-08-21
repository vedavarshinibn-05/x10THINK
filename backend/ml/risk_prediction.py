import numpy as np
from typing import Dict, Any

RISK_LEVELS = ["LOW", "MODERATE", "HIGH", "CRITICAL"]

def _score_to_level(score: int) -> str:
    if score <= 25: return "LOW"
    elif score <= 50: return "MODERATE"
    elif score <= 75: return "HIGH"
    return "CRITICAL"

def predict_risks(features: Dict[str, Any]) -> Dict[str, Any]:
    rainfall = features.get('rainfall', 700)
    temperature = features.get('temperature', 28)
    moisture = features.get('moisture', 30)
    slope = features.get('slope', 3)
    humidity = features.get('humidity', 65)
    ndvi = features.get('ndvi', 0.5)
    elevation = features.get('elevation', 500)
    ph = features.get('ph', 6.5)
    organic_matter = features.get('organic_matter', 2.5)
    potassium = features.get('potassium', 150)

    risks = {}

    # --- DROUGHT RISK ---
    drought_score = 0
    if rainfall < 400: drought_score += 40
    elif rainfall < 600: drought_score += 20
    if moisture < 18: drought_score += 35
    elif moisture < 25: drought_score += 15
    if temperature > 35: drought_score += 20
    elif temperature > 32: drought_score += 10
    drought_score = min(100, drought_score)
    risks['drought'] = {
        "level": _score_to_level(drought_score),
        "score": drought_score,
        "description": "Risk of insufficient water supply for crops during dry periods.",
        "causes": [] if drought_score < 25 else (
            ["Low annual rainfall", "High evapotranspiration"] if rainfall < 500 else
            ["Low soil moisture reserves"]
        ),
        "prevention": [
            "Install drip irrigation system",
            "Mulch soil to reduce evaporation",
            "Use drought-tolerant crop varieties",
            "Monitor soil moisture weekly"
        ] if drought_score > 25 else ["Current conditions are favorable. Maintain regular monitoring."]
    }

    # --- FLOOD RISK ---
    flood_score = 0
    if rainfall > 1500: flood_score += 40
    elif rainfall > 1000: flood_score += 20
    if slope < 1: flood_score += 30
    elif slope < 2: flood_score += 15
    if moisture > 50: flood_score += 25
    elif moisture > 40: flood_score += 10
    flood_score = min(100, flood_score)
    risks['flood'] = {
        "level": _score_to_level(flood_score),
        "score": flood_score,
        "description": "Risk of waterlogging or surface flooding damaging crop roots.",
        "causes": [] if flood_score < 25 else ["Heavy seasonal rainfall", "Low slope with poor drainage"],
        "prevention": [
            "Construct field drainage channels",
            "Raise bed planting technique",
            "Install surface runoff management"
        ] if flood_score > 25 else ["Drainage conditions are satisfactory."]
    }

    # --- HEAT STRESS RISK ---
    heat_score = 0
    if temperature > 38: heat_score += 50
    elif temperature > 34: heat_score += 30
    elif temperature > 31: heat_score += 15
    if humidity < 40: heat_score += 25
    elif humidity < 55: heat_score += 10
    heat_score = min(100, heat_score)
    risks['heat_stress'] = {
        "level": _score_to_level(heat_score),
        "score": heat_score,
        "description": "Risk of high temperatures reducing crop photosynthesis and yield.",
        "causes": [] if heat_score < 25 else [f"High temperature ({temperature}°C)", "Low humidity"],
        "prevention": [
            "Use shade nets during peak summer",
            "Schedule irrigation for early morning",
            "Choose heat-tolerant varieties",
            "Apply reflective mulch"
        ] if heat_score > 25 else ["Temperature is within normal range for most crops."]
    }

    # --- WATER STRESS RISK ---
    water_score = 0
    if moisture < 15: water_score += 45
    elif moisture < 22: water_score += 25
    if rainfall < 300: water_score += 40
    elif rainfall < 500: water_score += 20
    water_score = min(100, water_score)
    risks['water_stress'] = {
        "level": _score_to_level(water_score),
        "score": water_score,
        "description": "Risk of insufficient water available to crops at critical growth stages.",
        "causes": [] if water_score < 25 else ["Low soil moisture", "Insufficient rainfall distribution"],
        "prevention": [
            "Install soil moisture sensors",
            "Schedule irrigation based on crop stages",
            "Use efficient water-saving techniques"
        ] if water_score > 25 else ["Water availability is adequate for most crops."]
    }

    # --- PEST RISK ---
    pest_score = 30  # baseline
    if humidity > 75: pest_score += 25
    elif humidity > 65: pest_score += 15
    if temperature > 28 and humidity > 60: pest_score += 20
    if ndvi > 0.65: pest_score += 10  # dense vegetation attracts pests
    pest_score = min(100, pest_score)
    risks['pest'] = {
        "level": _score_to_level(pest_score),
        "score": pest_score,
        "description": "Risk of crop damage from insects, fungi, or disease outbreaks.",
        "causes": ["High humidity creating favorable conditions for fungal growth"] if humidity > 65 else [],
        "prevention": [
            "Regular scouting for pest signs",
            "Use integrated pest management (IPM)",
            "Apply neem-based biopesticides preventively",
            "Maintain field hygiene and crop rotation"
        ]
    }

    # --- SOIL DEGRADATION RISK ---
    soil_score = 0
    if organic_matter < 1.5: soil_score += 35
    elif organic_matter < 2.0: soil_score += 15
    if slope > 8: soil_score += 35
    elif slope > 4: soil_score += 15
    if ph < 5.5 or ph > 8.0: soil_score += 25
    if potassium < 80: soil_score += 20
    soil_score = min(100, soil_score)
    risks['soil_degradation'] = {
        "level": _score_to_level(soil_score),
        "score": soil_score,
        "description": "Risk of progressive loss of soil fertility and structure over time.",
        "causes": [] if soil_score < 25 else (
            ["Low organic matter reducing microbial activity"] if organic_matter < 2.0 else []
        ) + (["Steep slope causing erosion"] if slope > 6 else []),
        "prevention": [
            "Add organic compost every season",
            "Practice crop rotation",
            "Use cover crops during off-season",
            "Minimize tillage"
        ] if soil_score > 25 else ["Soil health is currently well-maintained."]
    }

    # Overall risk summary
    all_scores = [v['score'] for v in risks.values()]
    overall_score = int(np.mean(all_scores))
    overall_level = _score_to_level(overall_score)

    return {
        "overall_risk_level": overall_level,
        "overall_risk_score": overall_score,
        "risks": risks,
        "summary": f"Overall farm risk is {overall_level} ({overall_score}/100). "
                   f"{'Farm conditions are well-managed.' if overall_score <= 25 else ''}"
                   f"{'Monitor highlighted areas and follow prevention guidelines.' if 25 < overall_score <= 50 else ''}"
                   f"{'Immediate action recommended on high-risk areas.' if overall_score > 50 else ''}"
    }
