import { useFarmStore } from '../../store/farmStore';

export default function DemoNotice() {
  const { isDemoMode } = useFarmStore();

  if (!isDemoMode) return null;

  return (
    <div className="bg-x10-amber/20 border-b border-x10-amber/30 text-x10-amber px-4 py-2 text-center text-sm font-medium z-40 relative">
      ⚠️ DEMO MODE ACTIVE - Showing simulated data for showcase purposes. Some AI features use pre-calculated results.
    </div>
  );
}
