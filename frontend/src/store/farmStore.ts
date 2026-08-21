import { create } from 'zustand';
import { FarmData, AnalysisData } from '../types';
import { getDemoFarm, analyzeLand } from '../api/client';
import { demoAnalysis } from '../data/demoData';

interface FarmStore {
  farmData: FarmData | null;
  analysisData: AnalysisData | null;
  selectedCrop: string | null;
  isDemoMode: boolean;
  isAnalyzing: boolean;
  setFarmData: (data: FarmData | null) => void;
  setAnalysisData: (data: AnalysisData | null) => void;
  setSelectedCrop: (crop: string | null) => void;
  setDemoMode: (demo: boolean) => void;
  setAnalyzing: (analyzing: boolean) => void;
  loadDemoFarm: () => Promise<void>;
}

export const useFarmStore = create<FarmStore>((set) => ({
  farmData: null,
  analysisData: null,
  selectedCrop: null,
  isDemoMode: false,
  isAnalyzing: false,
  setFarmData: (data) => set({ farmData: data }),
  setAnalysisData: (data) => set({ analysisData: data }),
  setSelectedCrop: (crop) => set({ selectedCrop: crop }),
  setDemoMode: (demo) => set({ isDemoMode: demo }),
  setAnalyzing: (analyzing) => set({ isAnalyzing: analyzing }),
  loadDemoFarm: async () => {
    set({ isAnalyzing: true });
    try {
      const { farm, analysis } = await getDemoFarm();
      set({
        farmData: farm,
        analysisData: analysis,
        isDemoMode: true,
        isAnalyzing: false,
        selectedCrop: analysis.crops[0].id
      });
    } catch (e) {
      // Fallback
      set({
        farmData: {
          id: 'demo-1',
          name: 'Demo Farm, Karnataka',
          location: { lat: 12.9716, lng: 77.5946 },
          areaSize: 2.5,
          elevation: 920
        },
        analysisData: demoAnalysis,
        isDemoMode: true,
        isAnalyzing: false,
        selectedCrop: demoAnalysis.crops[0].id
      });
    }
  }
}));
