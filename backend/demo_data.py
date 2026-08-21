DEMO_FARM = {
    'id': 'demo-farm-001',
    'name': 'Krishnappa Demo Farm',
    'location': 'Dharwad, Karnataka, India',
    'latitude': 15.3173,
    'longitude': 75.7139,
    'area_hectares': 2.5,
    'elevation': 738,  # meters
    'soil': {
        'ph': 6.8,
        'nitrogen': 240,  # kg/ha
        'phosphorus': 32,
        'potassium': 180,
        'organic_matter': 2.8,
        'moisture': 31,
        'texture': 'Clay Loam',
        'color': 'Dark Brown',
        'health_score': 84
    },
    'weather': {
        'temperature': 28,
        'humidity': 72,
        'rainfall': 12,
        'wind_speed': 14,
        'uv_index': 6,
        'cloud_cover': 35,
        'forecast': [
            {'day': 'Today', 'temp': 28, 'rainfall': 12, 'humidity': 72},
            {'day': 'Tomorrow', 'temp': 29, 'rainfall': 0, 'humidity': 65},
            {'day': 'Day 3', 'temp': 30, 'rainfall': 0, 'humidity': 60},
            {'day': 'Day 4', 'temp': 28, 'rainfall': 15, 'humidity': 75},
            {'day': 'Day 5', 'temp': 27, 'rainfall': 25, 'humidity': 80},
            {'day': 'Day 6', 'temp': 27, 'rainfall': 5, 'humidity': 78},
            {'day': 'Day 7', 'temp': 28, 'rainfall': 0, 'humidity': 70},
        ]
    },
    'terrain': {
        'slope': 2.1,
        'aspect': 'South-East',
        'drainage': 'Good',
        'flood_risk': 'Low'
    },
    'vegetation': {
        'ndvi': 0.62,
        'health': 'Good',
        'coverage': 68
    },
    'water': {
        'availability': 'Moderate-High',
        'groundwater_depth': 8.5,
        'irrigation_source': 'Borewell + Canal',
        'water_score': 78
    },
    'climate': {
        'type': 'Semi-Arid Tropical',
        'annual_rainfall': 840,
        'growing_season': 'June-November',
        'frost_risk': 'None'
    },
    'recommendations': [
        {
            'crop_name': 'MAIZE',
            'suitability_pct': 91,
            'details': 'Optimal soil pH and nitrogen levels.',
            'yield': {'expected': 4.8, 'min': 4.2, 'max': 5.5, 'unit': 't/ha'},
            'profitability': {'cost': 45000, 'revenue': 96000, 'return': 51000}
        },
        {
            'crop_name': 'GROUNDNUT',
            'suitability_pct': 87,
            'details': 'Good texture, needs slight phosphorus boost.',
            'yield': {'expected': 2.1, 'min': 1.8, 'max': 2.4, 'unit': 't/ha'},
            'profitability': {'cost': 38000, 'revenue': 80000, 'return': 42000}
        },
        {
            'crop_name': 'MILLET',
            'suitability_pct': 82,
            'details': 'Excellent drought resistance.',
            'yield': {'expected': 1.8, 'min': 1.5, 'max': 2.1, 'unit': 't/ha'},
            'profitability': {'cost': 25000, 'revenue': 60000, 'return': 35000}
        },
        {
            'crop_name': 'SOYBEAN',
            'suitability_pct': 79,
            'details': 'Adequate climate, needs moisture control.',
            'yield': {'expected': 2.5, 'min': 2.0, 'max': 3.0, 'unit': 't/ha'},
            'profitability': {'cost': 40000, 'revenue': 85000, 'return': 45000}
        },
        {
            'crop_name': 'SUNFLOWER',
            'suitability_pct': 76,
            'details': 'Requires well-drained soil.',
            'yield': {'expected': 1.5, 'min': 1.2, 'max': 1.8, 'unit': 't/ha'},
            'profitability': {'cost': 30000, 'revenue': 70000, 'return': 40000}
        }
    ],
    'risks': {
        'drought': 'LOW',
        'flood': 'LOW',
        'heat': 'MODERATE',
        'water': 'LOW',
        'pest': 'MODERATE',
        'soil_degradation': 'LOW'
    },
    'feature_importance': {
        'positive': ['Soil pH (6.8)', 'Nitrogen (240 kg/ha)', 'Drainage (Good)'],
        'negative': ['Phosphorus (32 kg/ha)']
    },
    'action_plan': [
        'Apply 20kg/ha Phosphorus basal dose',
        'Ensure irrigation during flowering stage',
        'Monitor for stem borer in early stages'
    ]
}
