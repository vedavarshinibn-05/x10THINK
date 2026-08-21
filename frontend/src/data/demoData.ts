import { AnalysisData } from '../types';

export const demoAnalysis: AnalysisData = {
  landSuitability: 87,
  soil: {
    ph: 6.8,
    nitrogen: 45,
    phosphorus: 30,
    potassium: 120,
    organicMatter: 3.2,
    moisture: 24,
    healthScore: 84
  },
  weather: {
    currentTemp: 28,
    humidity: 72,
    rainfall: 12,
    windSpeed: 15,
    forecast: [
      { day: 'Mon', temp: 28, rainfall: 0 },
      { day: 'Tue', temp: 29, rainfall: 5 },
      { day: 'Wed', temp: 27, rainfall: 20 },
      { day: 'Thu', temp: 26, rainfall: 45 },
      { day: 'Fri', temp: 28, rainfall: 10 },
      { day: 'Sat', temp: 30, rainfall: 0 },
      { day: 'Sun', temp: 31, rainfall: 0 },
    ]
  },
  risks: [
    { id: 'r1', name: 'Drought', level: 'Low', score: 15, description: 'Low risk of drought in current season.' },
    { id: 'r2', name: 'Pest Infestation', level: 'Moderate', score: 45, description: 'Moderate risk of stem borer detected based on historical data.' },
    { id: 'r3', name: 'Flood', level: 'Low', score: 10, description: 'Elevation protects from immediate flood risks.' },
    { id: 'r4', name: 'Market Price Drop', level: 'High', score: 75, description: 'High volatility expected for tomatoes next month.' },
    { id: 'r5', name: 'Soil Erosion', level: 'Low', score: 20, description: 'Current cover crops provide good protection.' },
    { id: 'r6', name: 'Disease', level: 'Moderate', score: 50, description: 'Humidity levels favor fungal growth.' }
  ],
  crops: [
    {
      id: 'c1',
      name: 'Finger Millet (Ragi)',
      emoji: '🌾',
      suitabilityScore: 92,
      expectedYield: { min: 2.1, max: 2.8, unit: 'Tons/Ha' },
      durationDays: 110,
      waterReq: 'Low',
      revenueEst: 85000,
      costEst: 32000,
      roi: 165,
      factors: [
        { name: 'Soil pH Match', impact: 90, type: 'positive' },
        { name: 'Rainfall Pattern', impact: 85, type: 'positive' },
        { name: 'Market Demand', impact: 70, type: 'positive' },
        { name: 'Pest Threat', impact: -20, type: 'negative' }
      ]
    },
    {
      id: 'c2',
      name: 'Tomatoes',
      emoji: '🍅',
      suitabilityScore: 84,
      expectedYield: { min: 25, max: 35, unit: 'Tons/Ha' },
      durationDays: 90,
      waterReq: 'High',
      revenueEst: 350000,
      costEst: 150000,
      roi: 133,
      factors: [
        { name: 'Temperature Profile', impact: 88, type: 'positive' },
        { name: 'Soil Nitrogen', impact: 75, type: 'positive' },
        { name: 'Market Volatility', impact: -40, type: 'negative' },
        { name: 'Water Availability', impact: -15, type: 'negative' }
      ]
    },
    {
      id: 'c3',
      name: 'Maize',
      emoji: '🌽',
      suitabilityScore: 78,
      expectedYield: { min: 4.5, max: 6.0, unit: 'Tons/Ha' },
      durationDays: 120,
      waterReq: 'Moderate',
      revenueEst: 110000,
      costEst: 45000,
      roi: 144,
      factors: [
        { name: 'Solar Radiation', impact: 85, type: 'positive' },
        { name: 'Soil Drainage', impact: 70, type: 'positive' },
        { name: 'Nutrient Depletion', impact: -25, type: 'negative' }
      ]
    },
    {
      id: 'c4',
      name: 'Groundnut',
      emoji: '🥜',
      suitabilityScore: 72,
      expectedYield: { min: 1.5, max: 2.2, unit: 'Tons/Ha' },
      durationDays: 105,
      waterReq: 'Low',
      revenueEst: 125000,
      costEst: 55000,
      roi: 127,
      factors: [
        { name: 'Soil Texture', impact: 80, type: 'positive' },
        { name: 'Drought Tolerance', impact: 90, type: 'positive' },
        { name: 'Disease Risk', impact: -35, type: 'negative' }
      ]
    },
    {
      id: 'c5',
      name: 'Chili',
      emoji: '🌶️',
      suitabilityScore: 65,
      expectedYield: { min: 3.5, max: 5.0, unit: 'Tons/Ha' },
      durationDays: 150,
      waterReq: 'Moderate',
      revenueEst: 220000,
      costEst: 95000,
      roi: 131,
      factors: [
        { name: 'Profit Margin', impact: 95, type: 'positive' },
        { name: 'Pest Vulnerability', impact: -50, type: 'negative' },
        { name: 'Labor Intensive', impact: -30, type: 'negative' }
      ]
    }
  ],
  actionPlan: [
    { time: 'NOW', action: 'Apply 50kg Nitrogen based on soil deficit', icon: '🧪' },
    { time: 'THIS WEEK', action: 'Prepare land for Ragi sowing before Wed rains', icon: '🚜' },
    { time: 'THIS SEASON', action: 'Install drip irrigation for better water efficiency', icon: '💧' }
  ],
  futureClimate: [
    { year: 2024, suitability: 87 },
    { year: 2026, suitability: 85 },
    { year: 2030, suitability: 79 },
    { year: 2040, suitability: 72 }
  ]
};
