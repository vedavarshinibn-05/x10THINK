import { motion } from 'framer-motion';

export default function LoadingAnimation({ message = "ANALYZING SATELLITE DATA..." }: { message?: string }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-x10-dark/90 backdrop-blur-sm">
      <div className="flex flex-col items-center">
        <div className="relative w-32 h-32 mb-8">
          <motion.div 
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="absolute inset-0 rounded-full border-t-2 border-r-2 border-x10-green shadow-glow-green"
          />
          <motion.div 
            animate={{ rotate: -360 }}
            transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            className="absolute inset-4 rounded-full border-b-2 border-l-2 border-x10-blue"
          />
          <div className="absolute inset-0 flex items-center justify-center text-x10-green font-mono text-xs">
            AI CORE
          </div>
        </div>
        
        <h2 className="text-xl font-mono text-x10-green tracking-widest text-glow mb-4">{message}</h2>
        
        <div className="w-64 h-1 bg-gray-800 rounded overflow-hidden">
          <motion.div 
            className="h-full bg-x10-green"
            initial={{ width: "0%" }}
            animate={{ width: "100%" }}
            transition={{ duration: 3, repeat: Infinity }}
          />
        </div>
        
        <div className="mt-8 grid grid-cols-2 gap-4 text-xs font-mono text-gray-500">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-x10-green rounded-full animate-pulse"></div>
            CONNECTING NEURAL NET
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-x10-green rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
            FETCHING WEATHER
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-x10-green rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
            SCANNING SOIL DATA
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-x10-green rounded-full animate-pulse" style={{animationDelay: '0.6s'}}></div>
            COMPUTING YIELD
          </div>
        </div>
      </div>
    </div>
  );
}
