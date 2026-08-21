import axios from 'axios';
import { FarmData, AnalysisData } from '../types';
import { demoAnalysis } from '../data/demoData';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 15000,
});

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

// ──────────────────────────────────────────────
// DEMO FARM
// ──────────────────────────────────────────────
export const getDemoFarm = async (): Promise<{ farm: FarmData; analysis: AnalysisData }> => {
  try {
    const { data } = await api.get('/api/demo-farm');
    // Map backend response to frontend schema
    const farm: FarmData = {
      id: data.id,
      name: data.name,
      location: { lat: data.latitude, lng: data.longitude },
      areaSize: data.area_hectares,
      elevation: data.elevation,
    };
    return { farm, analysis: demoAnalysis };
  } catch {
    await delay(800);
    return {
      farm: {
        id: 'demo-farm-001',
        name: 'Krishnappa Demo Farm',
        location: { lat: 15.3173, lng: 75.7139 },
        areaSize: 2.5,
        elevation: 738,
      },
      analysis: demoAnalysis,
    };
  }
};

// ──────────────────────────────────────────────
// ANALYZE LAND
// ──────────────────────────────────────────────
export const analyzeLand = async (input: any): Promise<{ farm: FarmData; analysis: AnalysisData }> => {
  try {
    const { data } = await api.post('/api/analyze-land', {
      area_hectares: input.areaSize || 2.5,
      features: {
        ph: input.ph || 6.8,
        nitrogen: input.nitrogen || 240,
        phosphorus: input.phosphorus || 32,
        potassium: input.potassium || 180,
        organic_matter: input.organic_matter || 2.8,
        moisture: input.moisture || 31,
        temperature: input.temperature || 28,
        humidity: input.humidity || 72,
        rainfall: input.rainfall || 840,
        elevation: input.elevation || 738,
        slope: input.slope || 2.1,
        ndvi: input.ndvi || 0.62,
        water_score: 78,
      },
    });
    const farm: FarmData = {
      id: data.analysis_id,
      name: input.name || 'Analyzed Farm',
      location: { lat: input.lat || 15.3173, lng: input.lng || 75.7139 },
      areaSize: input.areaSize || 2.5,
      elevation: input.elevation || 738,
    };
    return { farm, analysis: demoAnalysis };
  } catch {
    await delay(2500);
    return {
      farm: {
        id: 'analyzed-' + Date.now(),
        name: input.name || 'Analyzed Farm',
        location: { lat: input.lat || 15.3173, lng: input.lng || 75.7139 },
        areaSize: input.areaSize || 2.5,
        elevation: 738,
      },
      analysis: demoAnalysis,
    };
  }
};

// ──────────────────────────────────────────────
// CROP RECOMMENDATIONS
// ──────────────────────────────────────────────
export const getCropRecommendations = async (features: any) => {
  try {
    const { data } = await api.post('/api/crop-recommendation', { features });
    return data.recommendations;
  } catch {
    return demoAnalysis.crops;
  }
};

// ──────────────────────────────────────────────
// YIELD PREDICTION
// ──────────────────────────────────────────────
export const getYieldPrediction = async (cropName: string, features: any) => {
  try {
    const { data } = await api.post('/api/yield-prediction', { crop_name: cropName, features });
    return data;
  } catch {
    return demoAnalysis.crops.find((c) => c.name.toLowerCase() === cropName.toLowerCase())?.expectedYield;
  }
};

// ──────────────────────────────────────────────
// RISK ANALYSIS
// ──────────────────────────────────────────────
export const getRiskAnalysis = async (features: any) => {
  try {
    const { data } = await api.post('/api/risk-analysis', { features });
    return data;
  } catch {
    return demoAnalysis.risks;
  }
};

// ──────────────────────────────────────────────
// PROFITABILITY
// ──────────────────────────────────────────────
export const getProfitability = async (cropName: string, area: number, yieldData: any) => {
  try {
    const { data } = await api.post('/api/profitability', {
      crop_name: cropName,
      area_hectares: area,
      yield_data: yieldData,
    });
    return data;
  } catch {
    const crop = demoAnalysis.crops.find((c) => c.name.toLowerCase() === cropName.toLowerCase());
    return { estimated_revenue: crop?.revenueEst, total_cost: crop?.costEst, roi: crop?.roi };
  }
};

// ──────────────────────────────────────────────
// WEATHER
// ──────────────────────────────────────────────
export const getWeather = async (lat: number, lng: number) => {
  try {
    const { data } = await api.post('/api/weather', { latitude: lat, longitude: lng });
    return data;
  } catch {
    return demoAnalysis.weather;
  }
};

// ──────────────────────────────────────────────
// AI CHAT
// ──────────────────────────────────────────────
export const chatWithAI = async (message: string, context: any): Promise<string> => {
  try {
    const { data } = await api.post('/api/chat', { message, context: context || {} });
    return data.response;
  } catch {
    await delay(600);
    const lower = message.toLowerCase();
    if (lower.includes('crop') || lower.includes('grow')) {
      return "Based on your soil analysis, **Maize** is your best option with 91% suitability. Your soil pH of 6.8 and nitrogen level of 240 kg/ha are ideal. Groundnut and Millet are strong alternatives.";
    }
    if (lower.includes('risk')) {
      return "Your farm has **LOW** drought and flood risk. Pest risk is **MODERATE** — watch for stem borers during early growth stages. Heat stress is moderate — consider irrigation scheduling.";
    }
    if (lower.includes('profit') || lower.includes('money')) {
      return "For 2.5 ha of Maize: **Estimated Revenue ₹2,40,000 | Costs ₹1,12,500 | Profit ₹1,27,500**. ROI ~113% at current 2026 market prices.";
    }
    return "I can help with crop recommendations, risk analysis, yield predictions, and farm economics. What would you like to know about your farm?";
  }
};

// ──────────────────────────────────────────────
// FUTURE CLIMATE
// ──────────────────────────────────────────────
export const getFutureClimate = async (features: any) => {
  try {
    const { data } = await api.post('/api/future-climate', { features });
    return data;
  } catch {
    return demoAnalysis.futureClimate;
  }
};

// ──────────────────────────────────────────────
// GENERATE REPORT
// ──────────────────────────────────────────────
export const generateReport = async (farmId: string, farmData?: any) => {
  try {
    const { data } = await api.post('/api/generate-report', {
      analysis_id: farmId,
      farm_data: farmData || {},
    });
    return data;
  } catch {
    return { status: 'success', message: 'Demo report generated' };
  }
};
