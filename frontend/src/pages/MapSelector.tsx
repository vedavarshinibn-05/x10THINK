import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import { useNavigate } from 'react-router-dom';
import { useFarmStore } from '../store/farmStore';
import { analyzeLand } from '../api/client';
import LoadingAnimation from '../components/ui/LoadingAnimation';
import L from 'leaflet';

// Fix leaflet icon
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

function MapEvents({ onLocationSelect }: { onLocationSelect: (lat: number, lng: number) => void }) {
  useMapEvents({
    click(e) {
      onLocationSelect(e.latlng.lat, e.latlng.lng);
    },
  });
  return null;
}

export default function MapSelector() {
  const [position, setPosition] = useState<{lat: number, lng: number} | null>(null);
  const [area, setArea] = useState(2.5);
  const navigate = useNavigate();
  const { setAnalyzing, setFarmData, setAnalysisData, loadDemoFarm, isAnalyzing } = useFarmStore();

  const handleAnalyze = async () => {
    if (!position) return;
    setAnalyzing(true);
    
    try {
      const result = await analyzeLand({ lat: position.lat, lng: position.lng, areaSize: area });
      setFarmData(result.farm);
      setAnalysisData(result.analysis);
      navigate('/dashboard');
    } catch (e) {
      console.error(e);
      setAnalyzing(false);
    }
  };

  const handleDemo = async () => {
    await loadDemoFarm();
    navigate('/dashboard');
  };

  if (isAnalyzing) return <LoadingAnimation />;

  return (
    <div className="flex-1 flex flex-col md:flex-row relative">
      {/* Sidebar Panel */}
      <div className="w-full md:w-96 glass m-4 z-[1000] flex flex-col absolute md:relative top-0 left-0">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-2 text-x10-green text-glow">LAND SELECTOR</h2>
          <p className="text-gray-400 text-sm mb-6">Click on the map to select your farm location for AI analysis.</p>

          <div className="space-y-4 mb-8">
            <div className="bg-black/50 p-4 rounded border border-x10-border">
              <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">Coordinates</label>
              <div className="font-mono text-sm">
                {position ? `${position.lat.toFixed(4)}, ${position.lng.toFixed(4)}` : 'No location selected'}
              </div>
            </div>

            <div className="bg-black/50 p-4 rounded border border-x10-border">
              <label className="text-xs text-gray-400 uppercase tracking-wider block mb-1">Area (Hectares)</label>
              <input 
                type="number" 
                value={area} 
                onChange={(e) => setArea(Number(e.target.value))}
                className="w-full bg-transparent border-b border-x10-border focus:border-x10-green outline-none py-1 font-mono"
              />
            </div>
          </div>

          <button 
            onClick={handleAnalyze}
            disabled={!position}
            className={`w-full py-4 rounded font-bold text-lg transition-all ${position ? 'bg-x10-green text-black shadow-glow-green hover:bg-green-400' : 'bg-gray-800 text-gray-500 cursor-not-allowed'}`}
          >
            ANALYZE FARM
          </button>
          
          <div className="mt-6 text-center">
            <span className="text-gray-500 text-sm">or</span>
          </div>
          
          <button 
            onClick={handleDemo}
            className="w-full mt-4 py-3 border border-x10-green text-x10-green rounded font-bold hover:bg-x10-green/10 transition-colors"
          >
            USE DEMO LOCATION
          </button>
        </div>
      </div>

      {/* Map Area */}
      <div className="flex-1 h-[calc(100vh-64px)] z-0">
        <MapContainer 
          center={[15.3173, 75.7139]} // Karnataka approx center
          zoom={6} 
          style={{ height: '100%', width: '100%', background: '#0a0f0a' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            className="map-tiles"
          />
          <MapEvents onLocationSelect={(lat, lng) => setPosition({lat, lng})} />
          {position && (
            <Marker position={[position.lat, position.lng]}>
              <Popup>
                Selected Location <br />
                {position.lat.toFixed(4)}, {position.lng.toFixed(4)}
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>

      {/* Map dark mode css override injected */}
      <style>{`
        .leaflet-layer,
        .leaflet-control-zoom-in,
        .leaflet-control-zoom-out,
        .leaflet-control-attribution {
          filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
        }
      `}</style>
    </div>
  );
}
