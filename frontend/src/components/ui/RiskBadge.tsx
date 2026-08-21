import { Risk } from '../../types';

export default function RiskBadge({ risk }: { risk: Risk }) {
  const colors = {
    Low: 'bg-green-500/20 text-green-400 border-green-500/30',
    Moderate: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
    High: 'bg-red-500/20 text-red-400 border-red-500/30'
  };

  return (
    <div className={`p-3 rounded-lg border ${colors[risk.level]} flex flex-col gap-1`}>
      <div className="flex justify-between items-center">
        <span className="font-bold">{risk.name}</span>
        <span className="text-xs uppercase px-2 py-0.5 rounded-full bg-black/40">{risk.level}</span>
      </div>
      <p className="text-sm opacity-80 mt-1">{risk.description}</p>
    </div>
  );
}
