import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SensorProvider } from './context/SensorContext';
import Layout from './components/layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import LiveMonitoring from './pages/LiveMonitoring';
import FaultDetection from './pages/FaultDetection';
import EnergyMonitoring from './pages/EnergyMonitoring';
import HistoryPage from './pages/History';
import SettingsPage from './pages/Settings';

function App() {
  return (
    <SensorProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/live" element={<LiveMonitoring />} />
            <Route path="/faults" element={<FaultDetection />} />
            <Route path="/energy" element={<EnergyMonitoring />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </Router>
    </SensorProvider>
  );
}

export default App;
