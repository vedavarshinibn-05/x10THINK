import { CropRecommendation } from '../../types';
import { motion } from 'framer-motion';

export default function CropCard({ crop, onClick, isSelected }: { crop: CropRecommendation, onClick: () => void, isSelected: boolean }) {
  return (
    <motion.div 
      whileHover={{ scale: 1.02 }}
      className={`glass p-4 cursor-pointer transition-all duration-300 ${isSelected ? 'border-x10-green glow-green' : 'border-x10-border hover:border-gray-500'}`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{crop.emoji}</span>
          <div>
            <h3 className="font-bold text-lg">{crop.name}</h3>
            <p className="text-xs text-gray-400">{crop.durationDays} Days • {crop.waterReq} Water</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-x10-green font-bold text-xl">{crop.suitabilityScore}%</div>
          <div className="text-xs text-gray-400">Match</div>
        </div>
      </div>
      
      <div className="w-full bg-gray-800 h-2 rounded-full mt-2 overflow-hidden">
        <motion.div 
          className="bg-x10-green h-full"
          initial={{ width: 0 }}
          animate={{ width: `${crop.suitabilityScore}%` }}
          transition={{ duration: 1 }}
        />
      </div>
      
      <div className="mt-4 grid grid-cols-2 gap-2 text-sm">
        <div className="bg-black/30 p-2 rounded">
          <div className="text-gray-400 text-xs">Expected Yield</div>
          <div className="font-semibold">{crop.expectedYield.min}-{crop.expectedYield.max} {crop.expectedYield.unit}</div>
        </div>
        <div className="bg-black/30 p-2 rounded">
          <div className="text-gray-400 text-xs">Est. ROI</div>
          <div className="font-semibold text-x10-green">{crop.roi}%</div>
        </div>
      </div>
    </motion.div>
  );
}
