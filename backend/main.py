from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import json

from database import init_db
from demo_data import DEMO_FARM
from ml import land_suitability, crop_recommendation, yield_prediction, risk_prediction, profitability, explainability

app = FastAPI(
    title="X10THINK API",
    description="AI-Powered Agriculture Land Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()
    land_suitability.train_model()
    crop_recommendation.train_model()
    yield_prediction.train_model()
    print("X10THINK backend started. DB initialized. ML models ready.")

# ────────────────────────────────────────────────────────────────────────
# HEALTH
# ────────────────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "X10THINK API", "version": "1.0.0"}

# ────────────────────────────────────────────────────────────────────────
# DEMO FARM
# ────────────────────────────────────────────────────────────────────────
@app.get("/api/demo-farm")
async def get_demo_farm():
    return DEMO_FARM

# ────────────────────────────────────────────────────────────────────────
# LAND ANALYSIS (main endpoint — runs full pipeline)
# ────────────────────────────────────────────────────────────────────────
class FarmAnalysisRequest(BaseModel):
    area_hectares: float = 1.0
    features: Dict[str, Any]
    selected_crop: Optional[str] = None

@app.post("/api/analyze-land")
async def analyze_land(request: FarmAnalysisRequest):
    try:
        f = request.features
        area = request.area_hectares

        # 1. Land suitability
        suitability = land_suitability.predict(f)

        # 2. Crop recommendations (top 5)
        recommendations = crop_recommendation.predict(f)

        # 3. Risk analysis
        risks = risk_prediction.predict_risks(f)

        # 4. Yield + profitability for each recommended crop
        for rec in recommendations:
            yp = yield_prediction.predict(rec['crop_name'], f)
            prof = profitability.estimate_profitability(rec['crop_name'], area, yp)
            rec['yield_prediction'] = yp
            rec['profitability'] = prof

        # 5. Explainability for top crop
        top_crop = request.selected_crop or recommendations[0]['crop_name'] if recommendations else "MAIZE"
        explanation = explainability.generate_explanation(f, top_crop)

        # 6. Action plan
        action_plan = _generate_action_plan(suitability, recommendations, risks, f)

        return {
            "analysis_id": str(uuid.uuid4()),
            "demo_mode": False,
            "suitability": suitability,
            "recommendations": recommendations,
            "risks": risks,
            "explanation": explanation,
            "action_plan": action_plan,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

# ────────────────────────────────────────────────────────────────────────
# INDIVIDUAL ENDPOINTS
# ────────────────────────────────────────────────────────────────────────
class CropRecRequest(BaseModel):
    features: Dict[str, Any]

@app.post("/api/crop-recommendation")
async def recommend_crop(request: CropRecRequest):
    recs = crop_recommendation.predict(request.features)
    return {"recommendations": recs}

class YieldRequest(BaseModel):
    crop_name: str
    features: Dict[str, Any]

@app.post("/api/yield-prediction")
async def predict_yield(request: YieldRequest):
    return yield_prediction.predict(request.crop_name, request.features)

class RiskRequest(BaseModel):
    features: Dict[str, Any]

@app.post("/api/risk-analysis")
async def analyze_risks(request: RiskRequest):
    return risk_prediction.predict_risks(request.features)

class ProfitabilityRequest(BaseModel):
    crop_name: str
    area_hectares: float = 1.0
    yield_data: Dict[str, Any]
    market_price_override: Optional[float] = None

@app.post("/api/profitability")
async def estimate_profit(request: ProfitabilityRequest):
    return profitability.estimate_profitability(
        request.crop_name, request.area_hectares,
        request.yield_data, request.market_price_override
    )

class ExplainRequest(BaseModel):
    features: Dict[str, Any]
    crop_name: str = "MAIZE"

@app.post("/api/explain")
async def explain_recommendation(request: ExplainRequest):
    return explainability.generate_explanation(request.features, request.crop_name)

# ────────────────────────────────────────────────────────────────────────
# WEATHER (demo fallback)
# ────────────────────────────────────────────────────────────────────────
class WeatherRequest(BaseModel):
    latitude: float
    longitude: float

@app.post("/api/weather")
async def get_weather(request: WeatherRequest):
    # In production, call a real weather API here
    return {**DEMO_FARM['weather'], "source": "demo", "note": "Demo weather data. Integrate a real API for production."}

# ────────────────────────────────────────────────────────────────────────
# FARM CRUD
# ────────────────────────────────────────────────────────────────────────
@app.get("/api/farm/{farm_id}")
async def get_farm(farm_id: str):
    if farm_id == DEMO_FARM['id']:
        return DEMO_FARM
    raise HTTPException(status_code=404, detail="Farm not found")

class SaveFarmRequest(BaseModel):
    data: Dict[str, Any]

@app.post("/api/save-farm")
async def save_farm(request: SaveFarmRequest):
    farm_id = str(uuid.uuid4())
    # In production, save to DB here
    return {"status": "success", "farm_id": farm_id, "message": "Farm saved successfully."}

# ────────────────────────────────────────────────────────────────────────
# AI CHAT ASSISTANT
# ────────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    context: Dict[str, Any] = {}

@app.post("/api/chat")
async def chat_assistant(request: ChatRequest):
    msg = request.message.lower().strip()
    ctx = request.context

    # Extract context values
    top_crop = ctx.get("top_crop", "MAIZE")
    suit_score = ctx.get("suitability_score", 87)
    soil_ph = ctx.get("ph", 6.8)
    nitrogen = ctx.get("nitrogen", 240)
    rainfall = ctx.get("rainfall", 840)
    temp = ctx.get("temperature", 28)
    risks = ctx.get("risks", {})
    location = ctx.get("location", "your farm")

    def get_highest_risk():
        if not risks: return "pest"
        return max(risks, key=lambda k: {"LOW": 0, "MODERATE": 1, "HIGH": 2, "CRITICAL": 3}.get(risks.get(k, {}).get("level", "LOW"), 0))

    # Rule-based response engine
    if any(w in msg for w in ['best crop', 'what crop', 'which crop', 'recommend', 'grow', 'plant']):
        response = (f"Based on your soil and climate analysis, **{top_crop}** is the best crop for {location}. "
                    f"It has a suitability score of {suit_score}%. Your soil pH of {soil_ph} and nitrogen level of "
                    f"{nitrogen} kg/ha are particularly favorable for {top_crop}. "
                    f"Groundnut and Millet are also strong alternatives.")

    elif any(w in msg for w in ['why', 'reason', 'explain', 'how', 'maize', 'recommended']):
        response = (f"AI recommended **{top_crop}** for these key reasons:\n\n"
                    f"✅ **Soil pH {soil_ph}** — Ideal range (6.0–7.5) for nutrient absorption\n"
                    f"✅ **Nitrogen {nitrogen} kg/ha** — High nitrogen supports strong vegetative growth\n"
                    f"✅ **Temperature {temp}°C** — Within optimal growing range\n"
                    f"✅ **Rainfall {rainfall} mm/year** — Adequate for {top_crop} without heavy irrigation\n\n"
                    f"The AI analyzed 12 land parameters to arrive at this recommendation.")

    elif any(w in msg for w in ['risk', 'danger', 'threat', 'problem', 'concern']):
        top_risk = get_highest_risk()
        risk_info = risks.get(top_risk, {})
        risk_level = risk_info.get('level', 'MODERATE') if isinstance(risk_info, dict) else 'MODERATE'
        response = (f"Your biggest risk is **{top_risk.replace('_', ' ').title()}** (Level: {risk_level}). "
                    f"Drought and flood risks are LOW given your rainfall pattern. "
                    f"Pest risk is MODERATE — monitor for stem borers especially during early crop stages. "
                    f"Heat stress is MODERATE — consider shade nets during peak summer months.")

    elif any(w in msg for w in ['yield', 'harvest', 'production', 'output']):
        response = (f"For **{top_crop}**, your farm is expected to yield approximately **4.8 tons per hectare** "
                    f"over a 100-day growing period. Based on your soil nitrogen ({nitrogen} kg/ha) and moisture levels, "
                    f"the yield range is 3.5–6.5 t/ha depending on management practices. "
                    f"Proper irrigation during the flowering stage is critical for maximizing yield.")

    elif any(w in msg for w in ['profit', 'money', 'cost', 'revenue', 'earn', 'economics', 'income']):
        response = (f"For 2.5 hectares of **{top_crop}** at current 2026 market prices:\n\n"
                    f"💰 **Estimated Revenue**: ₹2,40,000\n"
                    f"💸 **Input Costs**: ₹1,12,500\n"
                    f"📈 **Potential Profit**: ₹1,27,500\n"
                    f"🔄 **ROI**: ~113%\n\n"
                    f"Actual profits depend on market price fluctuations and farm management quality.")

    elif any(w in msg for w in ['soil', 'ph', 'nitrogen', 'phosphorus', 'potassium', 'fertility']):
        response = (f"Your soil profile at {location}:\n\n"
                    f"🧪 **pH**: {soil_ph} — Good (ideal range 6.0–7.5)\n"
                    f"🌱 **Nitrogen**: {nitrogen} kg/ha — High (excellent for leafy growth)\n"
                    f"🔬 **Phosphorus**: 32 kg/ha — Moderate (consider applying DAP)\n"
                    f"⚡ **Potassium**: 180 kg/ha — Good\n"
                    f"🌿 **Organic Matter**: 2.8% — Good\n\n"
                    f"**Recommendation**: Apply 20 kg/ha phosphorus to bring it to the optimal range.")

    elif any(w in msg for w in ['water', 'irrigation', 'rainfall', 'drought', 'moisture']):
        response = (f"Your farm's water situation:\n\n"
                    f"🌧️ **Annual Rainfall**: {rainfall} mm — Moderate-Good\n"
                    f"💧 **Current Soil Moisture**: 31% — Optimal\n"
                    f"🚰 **Irrigation Source**: Borewell + Canal\n"
                    f"⚠️ **Water Risk**: LOW\n\n"
                    f"For {top_crop}, you'll need about 600 mm/season. "
                    f"Your rainfall covers most of this. Supplemental irrigation needed during dry spells.")

    elif any(w in msg for w in ['improve', 'better', 'increase', 'enhance', 'fertilize']):
        response = (f"Here are the top ways to improve your farm's productivity:\n\n"
                    f"1. 🧪 **Apply DAP (Diammonium Phosphate)** — 20 kg/ha to fix phosphorus deficit\n"
                    f"2. 💧 **Install drip irrigation** — Save 40% water, improve root zone moisture\n"
                    f"3. 🌿 **Add organic compost** — 5 tons/ha to boost microbial activity\n"
                    f"4. 🔄 **Practice crop rotation** — Alternate with legumes next season\n"
                    f"5. 📊 **Monitor soil monthly** — Track pH and nitrogen levels regularly")

    elif any(w in msg for w in ['weather', 'temperature', 'climate', 'rain', 'forecast']):
        response = (f"Current weather at {location}:\n\n"
                    f"🌡️ **Temperature**: {temp}°C — Normal for this season\n"
                    f"💧 **Humidity**: 72%\n"
                    f"🌧️ **Today's Rainfall**: 12 mm\n"
                    f"💨 **Wind**: 14 km/h\n\n"
                    f"7-day forecast shows mixed conditions with moderate rainfall mid-week. "
                    f"Good conditions for {top_crop} germination if planting this week.")

    elif any(w in msg for w in ['future', 'climate change', '2030', '2040', 'scenario']):
        response = (f"Climate simulation for your land:\n\n"
                    f"📅 **2026**: {top_crop} suitability 91% — Current conditions\n"
                    f"📅 **2030**: Expected 84% — Temperature +1.2°C, rainfall -5%\n"
                    f"📅 **2040**: Expected 72% — Temperature +2.5°C, rainfall -15%\n\n"
                    f"⚠️ **Trend**: Increasing heat stress and reduced rainfall projected. "
                    f"Consider transitioning to drought-tolerant varieties like Millet or Sorghum by 2030.")

    elif any(w in msg for w in ['hello', 'hi', 'hey', 'help', 'start', 'what can you']):
        response = (f"Hello! I'm **X10 AI**, your personal farm intelligence assistant. 🌱\n\n"
                    f"I've analyzed your farm at {location} and I'm ready to help. You can ask me:\n\n"
                    f"🌾 \"Which crop should I grow?\"\n"
                    f"🧪 \"How is my soil quality?\"\n"
                    f"⚠️ \"What are my biggest risks?\"\n"
                    f"💰 \"How profitable is maize?\"\n"
                    f"💧 \"How much water does my farm need?\"\n"
                    f"🔮 \"What will my land look like in 2030?\"")

    else:
        response = (f"Based on my analysis of your farm at {location} (Suitability: {suit_score}/100), "
                    f"I can provide insights on crops, soil, weather, risks, yield, and profitability. "
                    f"Try asking: 'What's my best crop?', 'What are my risks?', or 'How can I improve my soil?'")

    return {
        "response": response,
        "suggested_questions": [
            "Why did you recommend this crop?",
            "What is my biggest risk?",
            "How can I improve my soil?",
            "What yield can I expect?",
            "How profitable is this crop?"
        ]
    }

# ────────────────────────────────────────────────────────────────────────
# FUTURE CLIMATE SIMULATION
# ────────────────────────────────────────────────────────────────────────
class ClimateRequest(BaseModel):
    features: Dict[str, Any]

@app.post("/api/future-climate")
async def future_climate(request: ClimateRequest):
    f = request.features
    base_temp = f.get('temperature', 28)
    base_rain = f.get('rainfall', 840)

    crops_2026 = crop_recommendation.predict(f)

    def simulate_year(temp_delta, rain_factor, year):
        sim_features = {**f, 'temperature': base_temp + temp_delta, 'rainfall': base_rain * rain_factor}
        sim_crops = crop_recommendation.predict(sim_features)
        crop_map = {c['crop_name']: c['suitability_pct'] for c in sim_crops}
        return {
            "year": year,
            "temperature": round(base_temp + temp_delta, 1),
            "rainfall_mm": round(base_rain * rain_factor),
            "temperature_delta": f"+{temp_delta}°C",
            "rainfall_change": f"{round((rain_factor - 1) * 100)}%",
            "crop_suitability": crop_map,
            "note": "Simulated scenario — not a guaranteed forecast."
        }

    y2026 = simulate_year(0, 1.0, 2026)
    y2030 = simulate_year(1.2, 0.95, 2030)
    y2040 = simulate_year(2.5, 0.85, 2040)

    # Build trend lines for top 5 crops
    top_crops = [c['crop_name'] for c in crops_2026[:5]]
    trends = {}
    for crop in top_crops:
        trends[crop] = {
            "2026": y2026['crop_suitability'].get(crop, 70),
            "2030": y2030['crop_suitability'].get(crop, 65),
            "2040": y2040['crop_suitability'].get(crop, 58),
        }

    # Find crops that become more suitable
    emerging_crops = []
    for crop in top_crops:
        if trends[crop]["2040"] > trends[crop]["2026"]:
            emerging_crops.append(crop)

    return {
        "scenarios": {"2026": y2026, "2030": y2030, "2040": y2040},
        "trends": trends,
        "emerging_crops": emerging_crops,
        "declining_crops": [c for c in top_crops if c not in emerging_crops],
        "disclaimer": (
            "⚠️ This is a simulation based on moderate climate change projections. "
            "Actual conditions may differ. Consult agricultural experts for long-term planning."
        )
    }

# ────────────────────────────────────────────────────────────────────────
# FARM COMPARISON
# ────────────────────────────────────────────────────────────────────────
class CompareRequest(BaseModel):
    farm_a: Dict[str, Any]
    farm_b: Dict[str, Any]

@app.post("/api/compare-farms")
async def compare_farms(request: CompareRequest):
    suit_a = land_suitability.predict(request.farm_a.get('features', {}))
    suit_b = land_suitability.predict(request.farm_b.get('features', {}))
    risk_a = risk_prediction.predict_risks(request.farm_a.get('features', {}))
    risk_b = risk_prediction.predict_risks(request.farm_b.get('features', {}))
    return {
        "farm_a": {"name": request.farm_a.get("name", "Farm A"), "suitability": suit_a, "risk": risk_a},
        "farm_b": {"name": request.farm_b.get("name", "Farm B"), "suitability": suit_b, "risk": risk_b},
    }

# ────────────────────────────────────────────────────────────────────────
# REPORT GENERATION
# ────────────────────────────────────────────────────────────────────────
class ReportRequest(BaseModel):
    analysis_id: str
    farm_data: Dict[str, Any] = {}

@app.post("/api/generate-report")
async def generate_report(request: ReportRequest):
    return {
        "report_id": request.analysis_id,
        "generated_at": "2026-08-20",
        "summary": "X10THINK Farm Intelligence Report",
        "farm_data": request.farm_data,
        "status": "success",
        "message": "Report data ready. Use frontend PDF generation to download."
    }

# ────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ────────────────────────────────────────────────────────────────────────
def _generate_action_plan(suitability, recommendations, risks, features):
    top_crop = recommendations[0]['crop_name'] if recommendations else "MAIZE"
    top_suit = recommendations[0]['suitability_pct'] if recommendations else 85
    risk_data = risks.get('risks', {})

    now_actions = [
        f"✅ Confirm land selection — suitability score is {suitability['suitability_score']}/100",
        f"🧪 Conduct soil test to verify pH ({features.get('ph', 6.8)}) and nutrient levels",
        "💧 Check irrigation source availability and repair any infrastructure",
    ]

    if features.get('phosphorus', 30) < 40:
        now_actions.append("🌱 Apply 20 kg/ha DAP (diammonium phosphate) to fix phosphorus deficit")

    week_actions = [
        f"🌾 Source certified {top_crop} seeds from a registered dealer",
        "📋 Create a farm calendar for planting, fertilizing, and harvesting dates",
        "💧 Test borewell/canal water quality for irrigation suitability",
        "🔧 Prepare land: deep ploughing, bed preparation, and drainage channels",
    ]

    season_actions = [
        f"🌱 Plant {top_crop} as primary crop — expected yield: {recommendations[0].get('yield_prediction', {}).get('expected_yield', 4.8) if recommendations else 4.8} t/ha",
        "📊 Monitor soil moisture weekly throughout the season",
        "🐛 Watch for pest signs (especially stem borers) during early vegetative stage",
        "💦 Schedule irrigation based on crop growth stage and rainfall",
        "📈 Track input costs for accurate profitability assessment at harvest",
    ]

    if risk_data.get('drought', {}).get('level') in ['HIGH', 'CRITICAL']:
        season_actions.insert(0, "🚨 URGENT: Install drip irrigation — high drought risk detected")

    return {
        "NOW": now_actions,
        "THIS_WEEK": week_actions,
        "THIS_SEASON": season_actions,
        "primary_crop": top_crop,
        "confidence": f"{top_suit}%",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
