import numpy as np
from typing import Dict, Any

def generate_explanation(features: Dict[str, Any], crop_name: str = "MAIZE") -> Dict[str, Any]:
    """
    Generate SHAP-style feature importance explanation for AI recommendation.
    Returns human-readable positive and negative factors.
    """
    ph = features.get("ph", 6.5)
    nitrogen = features.get("nitrogen", 180)
    phosphorus = features.get("phosphorus", 30)
    potassium = features.get("potassium", 150)
    organic_matter = features.get("organic_matter", 2.5)
    moisture = features.get("moisture", 30)
    temperature = features.get("temperature", 28)
    humidity = features.get("humidity", 65)
    rainfall = features.get("rainfall", 800)
    ndvi = features.get("ndvi", 0.5)
    slope = features.get("slope", 2.0)
    elevation = features.get("elevation", 500)

    positive_factors = []
    negative_factors = []

    # pH scoring
    if 6.0 <= ph <= 7.5:
        positive_factors.append({"factor": "Soil pH", "value": f"{ph}", "impact": +18, "reason": f"pH {ph} is ideal for most crops (6.0–7.5 optimal range)"})
    elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:
        negative_factors.append({"factor": "Soil pH", "value": f"{ph}", "impact": -8, "reason": f"pH {ph} is slightly outside optimal range; liming or sulfur application recommended"})
    else:
        negative_factors.append({"factor": "Soil pH", "value": f"{ph}", "impact": -20, "reason": f"pH {ph} is too extreme; major soil amendment required"})

    # Nitrogen
    if nitrogen >= 200:
        positive_factors.append({"factor": "Nitrogen Level", "value": f"{nitrogen} kg/ha", "impact": +16, "reason": f"High nitrogen ({nitrogen} kg/ha) strongly supports vegetative growth"})
    elif nitrogen >= 120:
        positive_factors.append({"factor": "Nitrogen Level", "value": f"{nitrogen} kg/ha", "impact": +8, "reason": f"Adequate nitrogen ({nitrogen} kg/ha) for moderate crop growth"})
    else:
        negative_factors.append({"factor": "Nitrogen Level", "value": f"{nitrogen} kg/ha", "impact": -12, "reason": f"Low nitrogen ({nitrogen} kg/ha); apply urea or organic compost"})

    # Temperature
    if 22 <= temperature <= 32:
        positive_factors.append({"factor": "Temperature", "value": f"{temperature}°C", "impact": +16, "reason": f"Temperature {temperature}°C is in the optimal growing range (22–32°C)"})
    elif temperature > 35:
        negative_factors.append({"factor": "Temperature", "value": f"{temperature}°C", "impact": -14, "reason": f"High temperature ({temperature}°C) causes heat stress; shade nets recommended"})
    else:
        negative_factors.append({"factor": "Temperature", "value": f"{temperature}°C", "impact": -8, "reason": f"Temperature {temperature}°C may slow growth; consider season timing"})

    # Rainfall
    if rainfall >= 600:
        positive_factors.append({"factor": "Annual Rainfall", "value": f"{rainfall} mm", "impact": +14, "reason": f"Good rainfall ({rainfall} mm) reduces irrigation burden"})
    elif rainfall >= 400:
        positive_factors.append({"factor": "Annual Rainfall", "value": f"{rainfall} mm", "impact": +6, "reason": f"Moderate rainfall ({rainfall} mm); supplemental irrigation advised"})
    else:
        negative_factors.append({"factor": "Annual Rainfall", "value": f"{rainfall} mm", "impact": -10, "reason": f"Low rainfall ({rainfall} mm); extensive irrigation infrastructure needed"})

    # Soil Moisture
    if 25 <= moisture <= 40:
        positive_factors.append({"factor": "Soil Moisture", "value": f"{moisture}%", "impact": +12, "reason": f"Soil moisture {moisture}% is in optimal field capacity range (25–40%)"})
    elif moisture < 15:
        negative_factors.append({"factor": "Soil Moisture", "value": f"{moisture}%", "impact": -10, "reason": f"Critically low moisture ({moisture}%); drought stress risk"})
    else:
        positive_factors.append({"factor": "Soil Moisture", "value": f"{moisture}%", "impact": +5, "reason": f"Moisture {moisture}% is acceptable; monitor during dry spells"})

    # Organic Matter
    if organic_matter >= 2.5:
        positive_factors.append({"factor": "Organic Matter", "value": f"{organic_matter}%", "impact": +10, "reason": f"Good organic matter ({organic_matter}%) improves soil structure and fertility"})
    else:
        negative_factors.append({"factor": "Organic Matter", "value": f"{organic_matter}%", "impact": -6, "reason": f"Low organic matter ({organic_matter}%); add compost or green manure"})

    # Phosphorus
    if phosphorus >= 40:
        positive_factors.append({"factor": "Phosphorus", "value": f"{phosphorus} kg/ha", "impact": +8, "reason": f"Good phosphorus level ({phosphorus} kg/ha) supports root development"})
    elif phosphorus >= 20:
        negative_factors.append({"factor": "Phosphorus", "value": f"{phosphorus} kg/ha", "impact": -4, "reason": f"Moderate phosphorus ({phosphorus} kg/ha); apply DAP fertilizer for boost"})
    else:
        negative_factors.append({"factor": "Phosphorus", "value": f"{phosphorus} kg/ha", "impact": -12, "reason": f"Critically low phosphorus ({phosphorus} kg/ha); major fertilization needed"})

    # NDVI (vegetation health)
    if ndvi >= 0.6:
        positive_factors.append({"factor": "Vegetation Health (NDVI)", "value": f"{ndvi:.2f}", "impact": +10, "reason": f"High NDVI ({ndvi:.2f}) indicates healthy land currently producing good biomass"})
    elif ndvi >= 0.4:
        positive_factors.append({"factor": "Vegetation Health (NDVI)", "value": f"{ndvi:.2f}", "impact": +4, "reason": f"Moderate NDVI ({ndvi:.2f}); moderate vegetation coverage"})
    else:
        negative_factors.append({"factor": "Vegetation Health (NDVI)", "value": f"{ndvi:.2f}", "impact": -8, "reason": f"Low NDVI ({ndvi:.2f}); land may be degraded or barren"})

    # Slope
    if slope <= 3:
        positive_factors.append({"factor": "Terrain Slope", "value": f"{slope}°", "impact": +8, "reason": f"Nearly flat terrain ({slope}°) — excellent for mechanized farming and irrigation"})
    elif slope <= 8:
        positive_factors.append({"factor": "Terrain Slope", "value": f"{slope}°", "impact": +3, "reason": f"Gentle slope ({slope}°) — manageable with contour farming techniques"})
    else:
        negative_factors.append({"factor": "Terrain Slope", "value": f"{slope}°", "impact": -12, "reason": f"Steep slope ({slope}°) — high erosion risk; terracing recommended"})

    # Sort by absolute impact
    positive_factors.sort(key=lambda x: abs(x["impact"]), reverse=True)
    negative_factors.sort(key=lambda x: abs(x["impact"]), reverse=True)

    total_positive = sum(f["impact"] for f in positive_factors)
    total_negative = sum(f["impact"] for f in negative_factors)
    net_score = min(100, max(0, 50 + total_positive + total_negative))

    return {
        "crop_name": crop_name,
        "ai_confidence": net_score,
        "positive_factors": positive_factors[:6],
        "negative_factors": negative_factors[:4],
        "summary": f"AI recommends {crop_name} based on {len(positive_factors)} favorable conditions. "
                   f"Main strengths: {positive_factors[0]['factor'] if positive_factors else 'N/A'} and "
                   f"{positive_factors[1]['factor'] if len(positive_factors) > 1 else 'good soil structure'}. "
                   f"{'Key concern: ' + negative_factors[0]['factor'] if negative_factors else 'No major concerns identified.'}",
        "farmer_message": f"Your land is well-suited for {crop_name}. "
                          f"{'Improve ' + ', '.join([f['factor'] for f in negative_factors[:2]]) + ' for better results.' if negative_factors else 'Conditions are excellent!'}"
    }
