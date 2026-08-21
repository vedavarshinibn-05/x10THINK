import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from typing import Dict, Any

MODEL_PATH = os.path.join(os.path.dirname(__file__), "land_suitability_model.joblib")

FEATURES = ['ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter',
            'moisture', 'temperature', 'humidity', 'rainfall', 'elevation', 'slope', 'ndvi']

def generate_synthetic_data(samples: int = 500):
    np.random.seed(42)
    data = {
        'ph': np.random.uniform(4.5, 9.0, samples),
        'nitrogen': np.random.uniform(40, 320, samples),
        'phosphorus': np.random.uniform(8, 120, samples),
        'potassium': np.random.uniform(40, 260, samples),
        'organic_matter': np.random.uniform(0.5, 6.0, samples),
        'moisture': np.random.uniform(8, 60, samples),
        'temperature': np.random.uniform(12, 42, samples),
        'humidity': np.random.uniform(25, 95, samples),
        'rainfall': np.random.uniform(150, 2200, samples),
        'elevation': np.random.uniform(0, 2500, samples),
        'slope': np.random.uniform(0, 20, samples),
        'ndvi': np.random.uniform(0.05, 0.95, samples),
    }
    df = pd.DataFrame(data)

    def calculate_label(row):
        score = 0
        # pH: ideal 6.0–7.5
        if 6.0 <= row['ph'] <= 7.5: score += 20
        elif 5.5 <= row['ph'] < 6.0 or 7.5 < row['ph'] <= 8.0: score += 10
        # Nitrogen
        if row['nitrogen'] >= 200: score += 20
        elif row['nitrogen'] >= 120: score += 10
        # Organic matter
        if row['organic_matter'] >= 2.5: score += 15
        elif row['organic_matter'] >= 1.5: score += 8
        # Temperature
        if 20 <= row['temperature'] <= 32: score += 20
        elif 15 <= row['temperature'] < 20 or 32 < row['temperature'] <= 36: score += 8
        # Rainfall
        if row['rainfall'] >= 600: score += 15
        elif row['rainfall'] >= 350: score += 7
        # Slope
        if row['slope'] <= 3: score += 10
        elif row['slope'] <= 8: score += 5

        if score >= 85: return 3   # Excellent
        elif score >= 65: return 2  # Good
        elif score >= 45: return 1  # Moderate
        else: return 0              # Poor

    df['label'] = df.apply(calculate_label, axis=1)
    return df

def train_model():
    df = generate_synthetic_data(600)
    X = df[FEATURES]
    y = df['label']
    model = RandomForestClassifier(n_estimators=150, random_state=42, max_depth=8)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

def predict(features: Dict[str, Any]) -> Dict[str, Any]:
    if not os.path.exists(MODEL_PATH):
        train_model()
    model = joblib.load(MODEL_PATH)

    # Build feature vector with defaults
    vec = {f: features.get(f, 0) for f in FEATURES}
    df = pd.DataFrame([vec])
    
    # Predict category
    pred_label = int(model.predict(df)[0])
    pred_proba = model.predict_proba(df)[0]
    
    categories = ['Poor', 'Moderate', 'Good', 'Excellent']
    category = categories[pred_label]

    # Calculate rule-based suitability score (0–100)
    ph = features.get('ph', 6.5)
    nitrogen = features.get('nitrogen', 150)
    organic_matter = features.get('organic_matter', 2.0)
    temperature = features.get('temperature', 28)
    rainfall = features.get('rainfall', 700)
    moisture = features.get('moisture', 28)
    slope = features.get('slope', 3)
    ndvi = features.get('ndvi', 0.5)
    potassium = features.get('potassium', 140)
    phosphorus = features.get('phosphorus', 30)

    scores = {
        'soil_score': 0,
        'climate_score': 0,
        'water_score': 0,
        'terrain_score': 0,
        'vegetation_score': 0,
    }

    # Soil score (pH, N, P, K, OM)
    soil = 50
    if 6.0 <= ph <= 7.5: soil += 20
    elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0: soil += 10
    if nitrogen >= 200: soil += 15
    elif nitrogen >= 120: soil += 8
    if phosphorus >= 40: soil += 8
    elif phosphorus >= 20: soil += 3
    if potassium >= 160: soil += 7
    if organic_matter >= 2.5: soil += 10
    elif organic_matter >= 1.5: soil += 5
    scores['soil_score'] = min(100, soil)

    # Climate score
    climate = 50
    if 22 <= temperature <= 32: climate += 25
    elif 18 <= temperature < 22 or 32 < temperature <= 36: climate += 12
    if rainfall >= 800: climate += 20
    elif rainfall >= 500: climate += 12
    elif rainfall >= 300: climate += 5
    if 50 <= features.get('humidity', 65) <= 80: climate += 10
    scores['climate_score'] = min(100, climate)

    # Water score
    water = 50
    if moisture >= 28: water += 20
    elif moisture >= 18: water += 10
    if rainfall >= 700: water += 20
    elif rainfall >= 400: water += 10
    water_avail = features.get('water_score', 70)
    water += (water_avail - 50) * 0.3
    scores['water_score'] = min(100, max(0, int(water)))

    # Terrain score
    terrain = 75
    if slope <= 2: terrain += 20
    elif slope <= 5: terrain += 12
    elif slope <= 10: terrain += 3
    else: terrain -= 15
    elevation = features.get('elevation', 500)
    if 0 <= elevation <= 1500: terrain += 5
    scores['terrain_score'] = min(100, max(0, terrain))

    # Vegetation score
    vegetation = 50
    if ndvi >= 0.6: vegetation += 35
    elif ndvi >= 0.4: vegetation += 20
    elif ndvi >= 0.2: vegetation += 8
    scores['vegetation_score'] = min(100, vegetation)

    # Weighted overall score
    overall = int(
        scores['soil_score'] * 0.30 +
        scores['climate_score'] * 0.25 +
        scores['water_score'] * 0.20 +
        scores['terrain_score'] * 0.15 +
        scores['vegetation_score'] * 0.10
    )
    overall = min(100, max(0, overall))

    # Map overall score to category label
    if overall >= 85: category = "Excellent"
    elif overall >= 70: category = "Good"
    elif overall >= 50: category = "Moderate"
    else: category = "Poor"

    return {
        "suitability_score": overall,
        "category": category,
        "component_scores": scores,
        "confidence": int(max(pred_proba) * 100),
        "interpretation": f"This land is rated as '{category}' for agriculture with a suitability score of {overall}/100. "
                          f"{'Excellent conditions — proceed with top crop recommendations.' if category == 'Excellent' else ''}"
                          f"{'Good land quality — most recommended crops should thrive.' if category == 'Good' else ''}"
                          f"{'Moderate potential — improvements to soil and irrigation can boost yields.' if category == 'Moderate' else ''}"
                          f"{'Poor suitability — significant intervention needed before farming.' if category == 'Poor' else ''}"
    }
