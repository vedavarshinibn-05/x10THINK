import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import MapSelector from './pages/MapSelector';
import Dashboard from './pages/Dashboard';
import Navbar from './components/layout/Navbar';

function App() {
  return (
    <div className="min-h-screen bg-x10-dark text-white flex flex-col">
      <Navbar />
      <main className="flex-1 flex flex-col relative pt-16">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/map" element={<MapSelector />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
