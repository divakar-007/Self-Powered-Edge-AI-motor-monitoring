import React, { useState, useEffect } from 'react';
import {
  Settings as SettingsIcon,
  Save,
  CheckCircle2,
  AlertTriangle,
  Server,
  Database,
  Radio,
  Wifi,
  Cpu,
  RefreshCw
} from 'lucide-react';
import { useSensor } from '../context/SensorContext';
import { machineService, systemService } from '../services/api';

const SettingsPage = () => {
  const { latestData, connectionStatus, simulationState, changeSimulationMode } = useSensor();

  const [thresholds, setThresholds] = useState({
    vibration: { warning: 3.0, critical: 5.0 },
    temperature: { warning: 45.0, critical: 60.0 },
    current: { warning: 1.0, critical: 1.5 },
    piezo_voltage: { warning: 3.8, critical: 4.5 },
  });

  const [healthStatus, setHealthStatus] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    machineService.getThresholds('MOTOR_001')
      .then((res) => {
        if (res.data) setThresholds(res.data);
      })
      .catch((e) => console.warn('Could not fetch thresholds:', e));

    fetchSystemHealth();
  }, []);

  const fetchSystemHealth = async () => {
    try {
      const res = await systemService.getHealth();
      setHealthStatus(res.data);
    } catch (e) {
      console.warn('Could not fetch system health:', e);
    }
  };

  const handleThresholdChange = (sensor, field, val) => {
    setThresholds((prev) => ({
      ...prev,
      [sensor]: {
        ...prev[sensor],
        [field]: parseFloat(val) || 0,
      },
    }));
  };

  const handleSaveThresholds = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveSuccess(false);
    try {
      await machineService.updateThresholds('MOTOR_001', thresholds);
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to update thresholds:', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            System Configuration & Threshold Calibrations
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Calibrate safety boundaries, configure machine tags, and inspect tier connectivity
          </p>
        </div>

        {saveSuccess && (
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold animate-in fade-in">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            Thresholds successfully saved and synced to SQLite!
          </div>
        )}
      </div>

      {/* Grid: Thresholds Form & Machine Identity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <SettingsIcon className="w-5 h-5 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-800">
                Rule-Based Fault Detection Thresholds
              </h3>
            </div>
            <span className="text-xs text-slate-500">Live Backend Application Tier Sync</span>
          </div>

          <form onSubmit={handleSaveThresholds} className="space-y-5">
            {/* 1. Vibration */}
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-slate-800">Vibration RMS Thresholds (m/s²)</span>
                  <p className="text-[11px] text-slate-500">Based on ISO 10816-3 industrial severity standard</p>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-100 text-blue-800">MPU6050</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[11px] font-semibold text-amber-700 mb-1">
                    Warning Threshold (m/s²)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={thresholds.vibration?.warning || 3.0}
                    onChange={(e) => handleThresholdChange('vibration', 'warning', e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-white border border-slate-200 rounded-lg outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-rose-700 mb-1">
                    Critical Threshold (m/s²)
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={thresholds.vibration?.critical || 5.0}
                    onChange={(e) => handleThresholdChange('vibration', 'critical', e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-white border border-slate-200 rounded-lg outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500"
                  />
                </div>
              </div>
            </div>

            {/* 2. Temperature */}
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-slate-800">Motor Temperature Limits (°C)</span>
                  <p className="text-[11px] text-slate-500">Stator winding insulation safety boundaries</p>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-100 text-amber-800">DS18B20</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[11px] font-semibold text-amber-700 mb-1">
                    Warning Threshold (°C)
                  </label>
                  <input
                    type="number"
                    step="0.5"
                    value={thresholds.temperature?.warning || 45.0}
                    onChange={(e) => handleThresholdChange('temperature', 'warning', e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-white border border-slate-200 rounded-lg outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-rose-700 mb-1">
                    Critical Limit (°C)
                  </label>
                  <input
                    type="number"
                    step="0.5"
                    value={thresholds.temperature?.critical || 60.0}
                    onChange={(e) => handleThresholdChange('temperature', 'critical', e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-white border border-slate-200 rounded-lg outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500"
                  />
                </div>
              </div>
            </div>

            {/* 3. Current */}
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-slate-800">Electrical Current Draw Limits (A)</span>
                  <p className="text-[11px] text-slate-500">Overcurrent and mechanical jam detection</p>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-100 text-emerald-800">ACS712</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-[11px] font-semibold text-amber-700 mb-1">
                    Warning Threshold (A)
                  </label>
                  <input
                    type="number"
                    step="0.05"
                    value={thresholds.current?.warning || 1.0}
                    onChange={(e) => handleThresholdChange('current', 'warning', e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-white border border-slate-200 rounded-lg outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-rose-700 mb-1">
                    Critical Overcurrent (A)
                  </label>
                  <input
                    type="number"
                    step="0.05"
                    value={thresholds.current?.critical || 1.5}
                    onChange={(e) => handleThresholdChange('current', 'critical', e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-white border border-slate-200 rounded-lg outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500"
                  />
                </div>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="submit"
                disabled={saving}
                className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs inline-flex items-center gap-2 shadow-md shadow-blue-600/20"
              >
                <Save className="w-4 h-4" />
                {saving ? 'Saving...' : 'Save Thresholds to SQLite'}
              </button>
            </div>
          </form>
        </div>

        {/* Right: Identifiers & Data Source */}
        <div className="space-y-6">
          {/* Machine & Hardware IDs */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-slate-800 pb-2 border-b border-slate-100">
              Hardware & Edge Node Identity
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-400 font-semibold mb-1">Machine Identifier</label>
                <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 font-mono font-bold text-slate-800">
                  {latestData.machine_id}
                </div>
              </div>

              <div>
                <label className="block text-slate-400 font-semibold mb-1">Edge Device Identifier</label>
                <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 font-mono font-bold text-slate-800">
                  {latestData.device_id}
                </div>
              </div>

              <div>
                <label className="block text-slate-400 font-semibold mb-1">Active Pipeline Source</label>
                <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between">
                  <span className="font-semibold text-slate-700 uppercase font-mono">{latestData.source}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-700">
                    Dual Mode Ready
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* MQTT Broker Configuration Info */}
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
            <h3 className="text-sm font-bold text-slate-800 pb-2 border-b border-slate-100 flex items-center gap-2">
              <Radio className="w-4 h-4 text-emerald-600" />
              Mosquitto MQTT Information
            </h3>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Broker Host</span>
                <span className="font-mono font-semibold text-slate-800">localhost</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Broker Port</span>
                <span className="font-mono font-semibold text-slate-800">1883</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Sensor Topic</span>
                <span className="font-mono text-[10px] text-blue-600">mems/motor001/sensors</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Status Topic</span>
                <span className="font-mono text-[10px] text-blue-600">mems/motor001/status</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Diagnostics / Health Panel */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Server className="w-5 h-5 text-blue-600" />
            <h3 className="text-sm font-bold text-slate-800">
              Three-Tier Subsystem Health & Diagnostics
            </h3>
          </div>
          <button
            onClick={fetchSystemHealth}
            className="text-xs font-semibold text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Re-check Status
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* 1. Presentation Tier */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-700">Presentation Tier</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            </div>
            <div className="mt-2 text-xs font-semibold text-slate-900">React + Vite</div>
            <p className="text-[11px] text-slate-500 mt-1">Dashboard live in browser</p>
          </div>

          {/* 2. Application Tier */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-700">Application Tier</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            </div>
            <div className="mt-2 text-xs font-semibold text-slate-900">FastAPI + Uvicorn</div>
            <p className="text-[11px] text-slate-500 mt-1">REST API & WebSocket Broadcast</p>
          </div>

          {/* 3. SQLite Relational Store */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-700">Relational Store</span>
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            </div>
            <div className="mt-2 text-xs font-semibold text-slate-900">SQLite (SQLAlchemy)</div>
            <p className="text-[11px] text-slate-500 mt-1">Machines, alerts, configurations</p>
          </div>

          {/* 4. Time-Series Store */}
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-700">Time-Series Engine</span>
              <span className={`w-2 h-2 rounded-full ${healthStatus?.data_tier?.influxdb?.connected ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
            </div>
            <div className="mt-2 text-xs font-semibold text-slate-900">
              {healthStatus?.data_tier?.influxdb?.connected ? 'InfluxDB v2 Connected' : 'SQLite Local Fallback'}
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              {healthStatus?.data_tier?.influxdb?.connected ? 'High-speed 30-day bucket' : 'Active offline cache'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
