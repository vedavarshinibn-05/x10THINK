import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Canvas } from '@react-three/fiber';
import { motion, AnimatePresence } from 'framer-motion';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { useFarmStore } from '../store/farmStore';
import FarmTerrain from '../components/3d/FarmTerrain';
import SoilLayers from '../components/3d/SoilLayers';
import ScoreGauge from '../components/ui/ScoreGauge';
import CropCard from '../components/ui/CropCard';
import RiskBadge from '../components/ui/RiskBadge';
import ChatAssistant from '../components/ui/ChatAssistant';
import DemoNotice from '../components/ui/DemoNotice';
import jsPDF from 'jspdf';

export default function Dashboard() {
  const navigate = useNavigate();
  const { farmData, analysisData, selectedCrop, setSelectedCrop, isDemoMode } = useFarmStore();
  const [terrainLayer, setTerrainLayer] = useState('LAND');
  const [climateYear, setClimateYear] = useState(2024);

  useEffect(() => {
    if (!farmData || !analysisData) {
      navigate('/map');
    }
  }, [farmData, analysisData, navigate]);

  if (!farmData || !analysisData) return null;

  const currentCrop = analysisData.crops.find(c => c.id === selectedCrop) || analysisData.crops[0];

  const handleExport = () => {
    const doc = new jsPDF();
    doc.setFont("helvetica", "bold");
    doc.setFontSize(22);
    doc.setTextColor(0, 200, 100);
    doc.text("X10THINK - Farm Intelligence Report", 20, 20);
    
    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.setFont("helvetica", "normal");
    doc.text(`Farm: ${farmData.name}`, 20, 40);
    doc.text(`Location: ${farmData.location.lat.toFixed(4)}, ${farmData.location.lng.toFixed(4)}`, 20, 50);
    doc.text(`Area: ${farmData.areaSize} Hectares`, 20, 60);
    
    doc.text(`Overall Suitability: ${analysisData.landSuitability}/100`, 20, 80);
    doc.text(`Soil Health: ${analysisData.soil.healthScore}/100`, 20, 90);
    
    doc.setFont("helvetica", "bold");
    doc.text("Top Crop Recommendation:", 20, 110);
    doc.setFont("helvetica", "normal");
    doc.text(`Crop: ${currentCrop.name}`, 20, 120);
    doc.text(`Expected Yield: ${currentCrop.expectedYield.min} - ${currentCrop.expectedYield.max} ${currentCrop.expectedYield.unit}`, 20, 130);
    doc.text(`Estimated ROI: ${currentCrop.roi}%`, 20, 140);
    
    doc.save("x10think-farm-report.pdf");
  };

  return (
    <div className="flex-1 flex flex-col pb-24">
      <DemoNotice />
      
      {/* 1. 3D Digital Twin Section */}
      <section className="relative h-[50vh] border-b border-x10-border">
        <div className="absolute inset-0 z-0">
          <Canvas camera={{ position: [0, 20, 30], fov: 45 }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 20, 10]} intensity={1} color="#ffffff" />
            <FarmTerrain layer={terrainLayer} />
          </Canvas>
        </div>
        
        {/* Terrain Controls overlay */}
        <div className="absolute top-4 left-4 z-10">
          <div className="glass p-4 rounded-xl flex flex-col gap-2">
            <h3 className="text-xs text-x10-green font-mono uppercase font-bold tracking-wider mb-2">Data Layers</h3>
            {['LAND', 'SOIL', 'WATER', 'RISK'].map(layer => (
              <button 
                key={layer}
                onClick={() => setTerrainLayer(layer)}
                className={`px-4 py-2 text-xs font-bold rounded ${terrainLayer === layer ? 'bg-x10-green text-black' : 'bg-black/50 text-gray-300 hover:bg-gray-800'}`}
              >
                {layer}
              </button>
            ))}
          </div>
        </div>

        {/* Key Stats overlay */}
        <div className="absolute bottom-0 w-full z-10 bg-gradient-to-t from-[#050a05] to-transparent pt-20 pb-4 px-6 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">{farmData.name}</h1>
            <p className="text-gray-400 font-mono text-sm">{farmData.location.lat.toFixed(4)}, {farmData.location.lng.toFixed(4)} | {farmData.areaSize} Hectares</p>
          </div>
          <button onClick={handleExport} className="glass px-4 py-2 text-sm font-bold hover:bg-x10-green hover:text-black transition-colors border-x10-green text-x10-green">
            GENERATE REPORT
          </button>
        </div>
      </section>

      {/* Main Content Grid */}
      <div className="max-w-7xl mx-auto w-full px-4 py-8 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column (Scores & Soil) */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="glass p-6 rounded-xl flex justify-around">
            <ScoreGauge score={analysisData.landSuitability} label="Land Score" />
            <ScoreGauge score={analysisData.soil.healthScore} label="Soil Health" delay={0.2} />
          </div>

          <div className="glass p-6 rounded-xl flex flex-col">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-x10-green">
              <span className="text-xl">🪨</span> SOIL INTELLIGENCE
            </h3>
            
            <div className="h-40 mb-4 relative bg-black/30 rounded-lg overflow-hidden border border-x10-border">
               <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
                  <ambientLight intensity={0.5} />
                  <directionalLight position={[2, 2, 2]} />
                  <SoilLayers />
               </Canvas>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm mt-2">
              <div className="bg-black/40 p-2 rounded border border-x10-border/50">
                <span className="text-gray-400 text-xs block">pH Level</span>
                <span className="font-bold text-lg text-white">{analysisData.soil.ph}</span>
              </div>
              <div className="bg-black/40 p-2 rounded border border-x10-border/50">
                <span className="text-gray-400 text-xs block">Moisture</span>
                <span className="font-bold text-lg text-white">{analysisData.soil.moisture}%</span>
              </div>
              <div className="bg-black/40 p-2 rounded border border-x10-border/50">
                <span className="text-gray-400 text-xs block">Nitrogen (N)</span>
                <span className="font-bold text-lg text-white">{analysisData.soil.nitrogen} mg/kg</span>
              </div>
              <div className="bg-black/40 p-2 rounded border border-x10-border/50">
                <span className="text-gray-400 text-xs block">Organic Matter</span>
                <span className="font-bold text-lg text-white">{analysisData.soil.organicMatter}%</span>
              </div>
            </div>
          </div>

          <div className="glass p-6 rounded-xl">
             <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-x10-blue">
              <span className="text-xl">☁️</span> WEATHER INSIGHTS
            </h3>
            <div className="flex justify-between items-center mb-6">
              <div className="text-4xl font-bold">{analysisData.weather.currentTemp}°C</div>
              <div className="text-right">
                <div className="text-sm text-gray-400">Humidity: {analysisData.weather.humidity}%</div>
                <div className="text-sm text-gray-400">Rainfall: {analysisData.weather.rainfall}mm</div>
              </div>
            </div>
            <div className="h-32 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={analysisData.weather.forecast}>
                  <XAxis dataKey="day" stroke="#6b7280" fontSize={10} tickLine={false} axisLine={false} />
                  <Tooltip cursor={{fill: 'rgba(255,255,255,0.1)'}} contentStyle={{backgroundColor: '#111c11', borderColor: '#1a3a1a'}}/>
                  <Bar dataKey="rainfall" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Center Column (Crops & Econ) */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <div className="glass p-6 rounded-xl">
             <div className="flex justify-between items-center mb-6">
               <h3 className="text-xl font-bold flex items-center gap-2 text-x10-green">
                <span className="text-xl">🌱</span> CROP RECOMMENDATIONS
              </h3>
              <span className="text-xs bg-x10-green/20 text-x10-green px-2 py-1 rounded">AI SORTED</span>
             </div>
             
             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
               {analysisData.crops.slice(0,3).map(crop => (
                 <CropCard 
                   key={crop.id} 
                   crop={crop} 
                   isSelected={selectedCrop === crop.id}
                   onClick={() => setSelectedCrop(crop.id)} 
                 />
               ))}
             </div>

             {/* Deep Dive for Selected Crop */}
             <AnimatePresence mode="wait">
              <motion.div 
                key={currentCrop.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="bg-black/40 rounded-xl p-6 border border-x10-border"
              >
                <h4 className="font-bold text-lg mb-4 border-b border-x10-border pb-2 flex items-center justify-between">
                  <span>{currentCrop.emoji} {currentCrop.name} Intelligence</span>
                  <span className="text-x10-green">ROI: {currentCrop.roi}%</span>
                </h4>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* AI Explainability */}
                  <div>
                    <h5 className="text-sm font-bold text-gray-400 mb-3 uppercase tracking-wider">AI Decision Factors</h5>
                    <div className="space-y-3">
                      {currentCrop.factors.map((f, i) => (
                        <div key={i}>
                          <div className="flex justify-between text-xs mb-1">
                            <span>{f.name}</span>
                            <span className={f.type === 'positive' ? 'text-green-400' : 'text-red-400'}>
                              {f.type === 'positive' ? '+' : ''}{f.impact}%
                            </span>
                          </div>
                          <div className="w-full bg-gray-800 h-1.5 rounded-full overflow-hidden">
                            <div 
                              className={`h-full ${f.type === 'positive' ? 'bg-green-500' : 'bg-red-500'}`}
                              style={{ width: `${Math.abs(f.impact)}%` }}
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Economics */}
                  <div>
                     <h5 className="text-sm font-bold text-gray-400 mb-3 uppercase tracking-wider">Economics (Per Ha)</h5>
                     <div className="space-y-2">
                       <div className="flex justify-between items-center bg-black/50 p-2 rounded">
                         <span className="text-sm text-gray-300">Est. Cost</span>
                         <span className="font-bold text-red-400">₹{currentCrop.costEst.toLocaleString()}</span>
                       </div>
                       <div className="flex justify-between items-center bg-black/50 p-2 rounded">
                         <span className="text-sm text-gray-300">Est. Revenue</span>
                         <span className="font-bold text-x10-green">₹{currentCrop.revenueEst.toLocaleString()}</span>
                       </div>
                       <div className="flex justify-between items-center bg-black/50 p-2 rounded border border-x10-green/30 mt-2">
                         <span className="text-sm font-bold">Net Profit</span>
                         <span className="font-bold text-x10-green text-lg">₹{(currentCrop.revenueEst - currentCrop.costEst).toLocaleString()}</span>
                       </div>
                     </div>
                  </div>
                </div>
              </motion.div>
             </AnimatePresence>
          </div>

          {/* Bottom row: Risks and Action Plan */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass p-6 rounded-xl">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-x10-amber">
                <span className="text-xl">⚠️</span> RISK RADAR
              </h3>
              
              <div className="h-48 w-full mb-4">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="70%" data={analysisData.risks}>
                    <PolarGrid stroke="#1a3a1a" />
                    <PolarAngleAxis dataKey="name" tick={{fill: '#9ca3af', fontSize: 10}} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                    <Radar name="Risk" dataKey="score" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              
              <div className="flex flex-col gap-2">
                {analysisData.risks.filter(r => r.level === 'High' || r.level === 'Moderate').slice(0,2).map(r => (
                  <RiskBadge key={r.id} risk={r} />
                ))}
              </div>
            </div>

            <div className="glass p-6 rounded-xl flex flex-col">
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-white">
                <span className="text-xl">📋</span> ACTION PLAN
              </h3>
              <div className="flex-1 overflow-y-auto pr-2 space-y-4">
                {analysisData.actionPlan.map((action, i) => (
                  <div key={i} className="flex gap-4 items-start bg-black/30 p-3 rounded-lg border border-x10-border">
                    <div className="text-2xl mt-1">{action.icon}</div>
                    <div>
                      <div className="text-xs font-bold text-x10-green mb-1">{action.time}</div>
                      <div className="text-sm text-gray-200">{action.action}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Future Climate */}
          <div className="glass p-6 rounded-xl">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2 text-purple-400">
              <span className="text-xl">🔮</span> FUTURE CLIMATE SIMULATION
            </h3>
            <p className="text-sm text-gray-400 mb-6">Projected land suitability based on global climate models (SSP2-4.5).</p>
            
            <div className="h-48 w-full">
               <ResponsiveContainer width="100%" height="100%">
                <LineChart data={analysisData.futureClimate}>
                  <XAxis dataKey="year" stroke="#6b7280" />
                  <YAxis domain={[0, 100]} stroke="#6b7280" />
                  <Tooltip contentStyle={{backgroundColor: '#111c11', borderColor: '#1a3a1a'}} />
                  <Line type="monotone" dataKey="suitability" stroke="#a855f7" strokeWidth={3} dot={{r: 6, fill: '#a855f7', stroke: '#000', strokeWidth: 2}} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

        </div>
      </div>
      
      <ChatAssistant />
    </div>
  );
}
