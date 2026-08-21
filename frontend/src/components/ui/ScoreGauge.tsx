import { motion } from 'framer-motion';

export default function ScoreGauge({ score, label, delay = 0 }: { score: number; label: string; delay?: number }) {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let color = '#00ff88'; // green
  if (score < 50) color = '#ef4444'; // red
  else if (score < 80) color = '#f59e0b'; // amber

  return (
    <div className="flex flex-col items-center justify-center p-4 glass">
      <div className="relative w-32 h-32 flex items-center justify-center">
        <svg className="transform -rotate-90 w-full h-full">
          <circle
            cx="64"
            cy="64"
            r={radius}
            stroke="rgba(255,255,255,0.1)"
            strokeWidth="8"
            fill="transparent"
          />
          <motion.circle
            cx="64"
            cy="64"
            r={radius}
            stroke={color}
            strokeWidth="8"
            fill="transparent"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, delay, ease: "easeOut" }}
            style={{ strokeLinecap: "round", filter: `drop-shadow(0 0 8px ${color})` }}
          />
        </svg>
        <div className="absolute text-3xl font-bold text-white drop-shadow-md">
          {score}
        </div>
      </div>
      <p className="mt-2 text-sm font-medium text-gray-300 uppercase tracking-widest">{label}</p>
    </div>
  );
}
