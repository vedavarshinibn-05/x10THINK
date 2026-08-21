import { Link, useLocation } from 'react-router-dom';
import { useFarmStore } from '../../store/farmStore';

export default function Navbar() {
  const location = useLocation();
  const { isDemoMode } = useFarmStore();

  return (
    <nav className="fixed top-0 w-full z-50 glass rounded-none border-b border-x10-border border-l-0 border-r-0 border-t-0 px-6 py-4 flex items-center justify-between">
      <Link to="/" className="flex items-center gap-2">
        <span className="text-2xl font-bold gradient-text tracking-wider">X10THINK</span>
      </Link>
      
      <div className="flex items-center gap-6">
        <Link 
          to="/dashboard" 
          className={`text-sm font-medium transition-colors hover:text-x10-green ${location.pathname === '/dashboard' ? 'text-x10-green text-glow' : 'text-gray-300'}`}
        >
          Dashboard
        </Link>
        <Link 
          to="/map" 
          className={`text-sm font-medium transition-colors hover:text-x10-green ${location.pathname === '/map' ? 'text-x10-green text-glow' : 'text-gray-300'}`}
        >
          Map
        </Link>
        
        {isDemoMode && (
          <span className="px-3 py-1 text-xs font-bold text-x10-dark bg-x10-amber rounded-full shadow-glow-amber">
            DEMO MODE
          </span>
        )}
        
        <Link 
          to="/map"
          className="px-4 py-2 bg-x10-green text-x10-dark font-semibold rounded hover:bg-green-400 transition-all shadow-glow-green"
        >
          START ANALYSIS
        </Link>
      </div>
    </nav>
  );
}
