import sqlite3
import json
from datetime import datetime

DATABASE_URL = "x10think.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS farms (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        name TEXT,
        latitude REAL,
        longitude REAL,
        area_hectares REAL,
        boundary_geojson TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS soil_data (
        id TEXT PRIMARY KEY,
        farm_id TEXT,
        ph REAL,
        nitrogen REAL,
        phosphorus REAL,
        potassium REAL,
        organic_matter REAL,
        moisture REAL,
        texture TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farm_id) REFERENCES farms (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id TEXT PRIMARY KEY,
        farm_id TEXT,
        temperature REAL,
        humidity REAL,
        rainfall REAL,
        wind_speed REAL,
        uv_index REAL,
        forecast_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farm_id) REFERENCES farms (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analyses (
        id TEXT PRIMARY KEY,
        farm_id TEXT,
        suitability_score REAL,
        soil_score REAL,
        climate_score REAL,
        water_score REAL,
        terrain_score REAL,
        vegetation_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (farm_id) REFERENCES farms (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crop_recommendations (
        id TEXT PRIMARY KEY,
        analysis_id TEXT,
        crop_name TEXT,
        suitability_pct REAL,
        rank INTEGER,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id TEXT PRIMARY KEY,
        analysis_id TEXT,
        drought_risk TEXT,
        flood_risk TEXT,
        heat_stress TEXT,
        water_stress TEXT,
        pest_risk TEXT,
        soil_degradation TEXT,
        details_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS yield_predictions (
        id TEXT PRIMARY KEY,
        analysis_id TEXT,
        crop_name TEXT,
        expected_yield REAL,
        yield_min REAL,
        yield_max REAL,
        duration_days INTEGER,
        water_req REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profitability_estimates (
        id TEXT PRIMARY KEY,
        analysis_id TEXT,
        crop_name TEXT,
        seed_cost REAL,
        fertilizer_cost REAL,
        irrigation_cost REAL,
        labor_cost REAL,
        other_cost REAL,
        total_cost REAL,
        expected_revenue REAL,
        potential_return REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (analysis_id) REFERENCES analyses (id)
    )
    ''')

    conn.commit()
    conn.close()
