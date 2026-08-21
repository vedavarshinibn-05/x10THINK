import { Canvas } from '@react-three/fiber';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import EarthGlobe from '../components/3d/EarthGlobe';
import { useFarmStore } from '../store/farmStore';

export default function Landing() {
  const navigate = useNavigate();
  const { loadDemoFarm } = useFarmStore();

  const handleDemo = async () => {
    await loadDemoFarm();
    navigate('/dashboard');
  };

  const features = [
    { title: "3D Farm Digital Twin", icon: "🌍", desc: "Visualize your entire farm terrain, water flow, and vegetation in real-time 3D." },
    { title: "AI Crop Intelligence", icon: "🧬", desc: "Neural networks analyze 50+ soil and weather parameters to recommend the perfect crops." },
    { title: "Risk Prediction", icon: "⚠️", desc: "Early warning system for pests, diseases, and extreme weather events." },
    { title: "Yield Estimation", icon: "📈", desc: "Highly accurate harvest predictions based on historical and real-time data." },
    { title: "Future Climate Simulation", icon: "🌡️", desc: "See how climate change will affect your land in 2030, 2040, and beyond." },
    { title: "Farm Economics", icon: "💰", desc: "Real-time profitability calculations and ROI projections." }
  ];

  return (
    <div className="min-h-screen bg-[#050a05] text-white overflow-x-hidden pt-16">
      
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center">
        <div className="absolute inset-0 z-0 opacity-80">
          <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
            <ambientLight intensity={0.2} />
            <directionalLight position={[5, 3, 5]} intensity={1.5} color="#00ff88" />
            <EarthGlobe />
          </Canvas>
        </div>

        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto mt-[-10vh]">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
          >
            <h1 className="text-6xl md:text-8xl font-bold mb-4 gradient-text tracking-tighter">
              X10THINK
            </h1>
            <h2 className="text-2xl md:text-4xl font-light mb-6 text-gray-300">
              Think Beyond the Land.
            </h2>
            <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
              AI-powered land intelligence for smarter, safer and more profitable farming. Transform agricultural data into actionable 3D insights.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <button 
                onClick={() => navigate('/map')}
                className="px-8 py-4 bg-x10-green text-black font-bold text-lg rounded shadow-glow-green hover:bg-green-400 transition-all hover:scale-105"
              >
                ANALYZE MY LAND
              </button>
              <button 
                onClick={handleDemo}
                className="px-8 py-4 bg-transparent border-2 border-x10-green text-x10-green font-bold text-lg rounded shadow-[inset_0_0_20px_rgba(0,255,136,0.2)] hover:bg-x10-green/10 transition-all hover:scale-105"
              >
                EXPLORE DEMO
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-6 max-w-7xl mx-auto relative z-10 bg-[#050a05]">
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold mb-4">Why X10THINK?</h2>
          <div className="w-24 h-1 bg-x10-green mx-auto rounded shadow-glow-green"></div>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((f, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="glass p-8 hover:-translate-y-2 transition-transform duration-300 hover:shadow-glow-green border-x10-border"
            >
              <div className="text-4xl mb-4">{f.icon}</div>
              <h3 className="text-xl font-bold mb-3 text-x10-green">{f.title}</h3>
              <p className="text-gray-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-x10-surface relative z-10 border-y border-x10-border">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { label: "Crops Analyzed", val: "500+" },
            { label: "AI Accuracy", val: "98%" },
            { label: "Farms Supported", val: "10,000+" },
            { label: "Countries", val: "50+" },
          ].map((stat, i) => (
            <motion.div 
              key={i}
              initial={{ scale: 0.8, opacity: 0 }}
              whileInView={{ scale: 1, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <div className="text-4xl md:text-5xl font-bold text-x10-green mb-2 text-glow">{stat.val}</div>
              <div className="text-gray-400 font-medium uppercase tracking-wider text-sm">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6 text-center relative z-10 bg-[#050a05]">
        <div className="max-w-3xl mx-auto glass p-12 relative overflow-hidden">
          <div className="absolute top-[-50%] left-[-50%] w-[200%] h-[200%] bg-[radial-gradient(ellipse_at_center,rgba(0,255,136,0.1)_0%,transparent_50%)]"></div>
          <h2 className="text-4xl font-bold mb-6 relative z-10">Ready to transform your farm?</h2>
          <p className="text-xl text-gray-400 mb-10 relative z-10">
            Experience the future of agriculture today. Our interactive demo shows you exactly what X10THINK can do.
          </p>
          <button 
            onClick={handleDemo}
            className="relative z-10 px-10 py-5 bg-x10-green text-black font-bold text-xl rounded shadow-glow-green hover:bg-green-400 transition-all hover:scale-105"
          >
            START X10THINK DEMO
          </button>
        </div>
      </section>

    </div>
  );
}
