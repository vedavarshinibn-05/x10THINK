# X10THINK — AI-Powered Agriculture Land Intelligence Platform

> **Think Beyond the Land.** AI-powered land intelligence for smarter, safer and more profitable farming.

---

## Quick Start (One Command)

### Option 1: Use the batch script (Windows)
```bat
start.bat
```
This opens **both servers** and launches the browser automatically.

### Option 2: Manual

**Backend (Terminal 1):**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm install
npm run dev
```

**Open:** http://localhost:5173

---

## Demo Mode

Click **"EXPLORE DEMO"** or **"USE DEMO LOCATION"** on any page.

The demo loads **Krishnappa Farm** in Dharwad, Karnataka, India — a realistic 2.5-hectare agricultural land with complete soil, weather, crop, and risk data.

**No API keys required. Works fully offline via demo data.**

---

## Project Structure

```
x10think/
├── start.bat                    ← One-click startup
├── frontend/                    ← React + Vite + Three.js
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.tsx      ← 3D Earth landing page
│   │   │   ├── MapSelector.tsx  ← Interactive farm map
│   │   │   └── Dashboard.tsx    ← Main analysis dashboard
│   │   ├── components/
│   │   │   ├── 3d/
│   │   │   │   ├── EarthGlobe.tsx     ← Rotating 3D Earth
│   │   │   │   ├── FarmTerrain.tsx    ← 3D farm digital twin
│   │   │   │   ├── AIVisualization.tsx ← Neural network animation
│   │   │   │   └── SoilLayers.tsx     ← 3D soil layers
│   │   │   ├── ui/
│   │   │   │   ├── ScoreGauge.tsx     ← Animated score gauge
│   │   │   │   ├── CropCard.tsx       ← Crop recommendation card
│   │   │   │   ├── RiskBadge.tsx      ← Risk indicator
│   │   │   │   ├── ChatAssistant.tsx  ← X10 AI chat
│   │   │   │   └── LoadingAnimation.tsx ← AI scanning animation
│   │   │   └── layout/
│   │   │       └── Navbar.tsx         ← Navigation bar
│   │   ├── store/farmStore.ts   ← Zustand global state
│   │   ├── api/client.ts        ← Axios API client
│   │   ├── data/demoData.ts     ← Hardcoded fallback demo data
│   │   └── types/index.ts       ← TypeScript interfaces
│   └── package.json
│
└── backend/                     ← FastAPI + Python ML
    ├── main.py                  ← All API endpoints
    ├── database.py              ← SQLite schema
    ├── demo_data.py             ← Realistic demo farm data
    ├── requirements.txt
    └── ml/
        ├── land_suitability.py  ← Land suitability model
        ├── crop_recommendation.py ← Crop recommendation engine
        ├── yield_prediction.py  ← Yield estimation model
        ├── risk_prediction.py   ← Risk assessment engine
        ├── profitability.py     ← Farm economics calculator
        └── explainability.py    ← AI explainability (SHAP-style)
```

---

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| 3D Landing Page | ✅ | Rotating Earth globe with particles |
| Interactive Map | ✅ | React Leaflet with farm boundary drawing |
| 3D Farm Digital Twin | ✅ | Procedural terrain with layer selector |
| AI Land Suitability | ✅ | Random Forest ML model, 0-100 score |
| Crop Recommendations | ✅ | Top 5 crops ranked by suitability |
| Explainable AI | ✅ | SHAP-style factor importance |
| Risk Radar | ✅ | 6 risk types with Recharts RadarChart |
| Yield Prediction | ✅ | Condition-adjusted yield estimates |
| Farm Economics | ✅ | 2026 Indian market price-based ROI |
| Future Climate Simulation | ✅ | 2026/2030/2040 suitability trends |
| X10 AI Chat Assistant | ✅ | Context-aware Q&A about your farm |
| Farm Action Plan | ✅ | NOW / THIS WEEK / THIS SEASON |
| Report Generation | ✅ | PDF export via jsPDF |
| Demo Mode | ✅ | Works 100% offline |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |
| GET | `/api/demo-farm` | Complete demo farm data |
| POST | `/api/analyze-land` | Full AI analysis pipeline |
| POST | `/api/crop-recommendation` | Crop recommendations only |
| POST | `/api/yield-prediction` | Yield for specific crop |
| POST | `/api/risk-analysis` | Risk assessment |
| POST | `/api/profitability` | Farm economics |
| POST | `/api/future-climate` | Climate simulation |
| POST | `/api/chat` | AI chat assistant |
| POST | `/api/save-farm` | Save farm to DB |
| GET | `/api/farm/{id}` | Get farm by ID |
| POST | `/api/generate-report` | Generate report data |

API documentation: http://localhost:8000/docs

---

## Tech Stack

**Frontend:**
- React 18 + TypeScript + Vite
- React Three Fiber + Three.js + Drei
- Tailwind CSS + Framer Motion
- Recharts + React Leaflet
- Zustand (state management)

**Backend:**
- FastAPI + Python 3.11+
- scikit-learn (Random Forest, Gradient Boosting)
- pandas + NumPy
- SQLite (production-ready with PostgreSQL migration path)

**Design:**
- Glassmorphism dark theme
- NASA agricultural intelligence center aesthetic
- Deep green (#050a05) → bright (#00ff88) color scheme
- Responsive: Desktop, Tablet, Mobile

---

## Demo Farm Details

**Krishnappa Demo Farm** — Dharwad, Karnataka, India

| Parameter | Value |
|-----------|-------|
| Location | 15.3173°N, 75.7139°E |
| Area | 2.5 hectares |
| Elevation | 738 m |
| Soil Type | Clay Loam |
| pH | 6.8 |
| Nitrogen | 240 kg/ha |
| Annual Rainfall | 840 mm |
| Climate | Semi-Arid Tropical |
| Top Crop | Maize (91% suitability) |
| Land Score | 87/100 |

---

## Environment Variables

```env
# frontend/.env
VITE_API_URL=http://localhost:8000

# backend/.env (optional — for external APIs)
WEATHER_API_KEY=your_key_here
```

---

## Disclaimer

> AI recommendations are based on ML models trained on synthetic agricultural data.
> They are intended as decision-support tools, not guaranteed scientific predictions.
> Always consult local agricultural experts before making major farming decisions.

---

*Built for hackathon demonstration. Modular design supports integration of real agricultural datasets, satellite imagery, and IoT sensors.*
