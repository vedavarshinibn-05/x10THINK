export interface FarmData {
  id: string;
  name: string;
  location: { lat: number; lng: number };
  areaSize: number; // in hectares
  elevation: number;
}

export interface SoilData {
  ph: number;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  organicMatter: number;
  moisture: number;
  healthScore: number;
}

export interface WeatherData {
  currentTemp: number;
  humidity: number;
  rainfall: number;
  windSpeed: number;
  forecast: { day: string; temp: number; rainfall: number }[];
}

export interface Risk {
  id: string;
  name: string;
  level: 'Low' | 'Moderate' | 'High';
  score: number; // 0-100
  description: string;
}

export interface CropRecommendation {
  id: string;
  name: string;
  emoji: string;
  suitabilityScore: number;
  expectedYield: { min: number; max: number; unit: string };
  durationDays: number;
  waterReq: string;
  revenueEst: number;
  costEst: number;
  roi: number;
  factors: { name: string; impact: number; type: 'positive' | 'negative' }[];
}

export interface AnalysisData {
  landSuitability: number;
  soil: SoilData;
  weather: WeatherData;
  risks: Risk[];
  crops: CropRecommendation[];
  actionPlan: { time: string; action: string; icon: string }[];
  futureClimate: { year: number; suitability: number }[];
}

export interface FarmInput {
  lat: number;
  lng: number;
  areaSize: number;
}
