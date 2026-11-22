import React, { useState, useEffect } from 'react';
import {
  AlertTriangle,
  ShieldCheck,
  Cpu,
  Layers,
  Wrench,
  Sliders,
  CheckCircle,
  HelpCircle,
  Sparkles
} from 'lucide-react';
import { useSensor } from '../context/SensorContext';
import AlertBadge from '../components/alerts/AlertBadge';
import AlertTable from '../components/alerts/AlertTable';
import { alertService, machineService } from '../services/api';

const FaultDetection = () => {
  const { latestData, activeAlerts, changeSimulationMode, simulationState } = useSensor();
  const [allAlerts, setAllAlerts] = useState([]);
  const [thresholds, setThresholds] = useState({
    vibration: { warning: 3.0, critical: 5.0 },
    temperature: { warning: 45.0, critical: 60.0 },
    current: { warning: 1.0, critical: 1.5 },
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAlerts();
    machineService.getThresholds('MOTOR_001')
      .then((res) => {
        if (res.data) setThresholds(res.data);
      })
      .catch((e) => console.warn('Could not load thresholds:', e));
  }, []);

  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const res = await alertService.getAlerts({ limit: 50 });
      if (Array.isArray(res.data)) {
        setAllAlerts(res.data);
      }
    } catch (err) {
      console.error('Error fetching alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (id) => {
    try {
      await alertService.acknowledgeAlert(id);
      fetchAlerts();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Fault Detection & Anomaly Diagnostics
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Rule-based threshold boundary verification with TinyML edge inference interface
          </p>
        </div>

        <div className="flex items-center gap-2">
          <AlertBadge
            severity={latestData.machine_status}
            text={`SYSTEM STATE: ${latestData.machine_status || 'NORMAL'}`}
          />
        </div>
      </div>

      {/* TinyML Edge Architecture Status Card (Transparent & Honest) */}
      <div className="bg-gradient-to-r from-navy-900 to-slate-900 text-white p-6 rounded-2xl border border-slate-800 shadow-md">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 rounded-xl bg-blue-600/30 border border-blue-500/40 text-blue-400">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold tracking-wide">
                  Edge AI / TinyML Architecture Interface
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  Ready for Model Training
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                The application implements a clean abstract adapter pattern (<code className="text-cyan-300">ITinyMLDetector</code>). The active engine uses deterministic calibrated industrial threshold safety rules. Once physical motor run-to-failure vibration datasets are collected, a quantized TensorFlow Lite / Micro TinyML model can be plugged in without refactoring.
              </p>
            </div>
          </div>
          <div className="shrink-0 flex flex-col items-end">
            <span className="text-xs text-slate-400">Active Engine:</span>
            <span className="text-sm font-bold text-emerald-400 font-mono">Calibrated Rule Matrix</span>
          </div>
        </div>
      </div>

      {/* Active Faults & Anomaly Trigger Injector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Active Fault Status */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h4 className="text-sm font-bold text-slate-800">Active Anomalies ({activeAlerts.length})</h4>
            <span className="text-xs text-slate-500">Auto-recovery with alert deduplication</span>
          </div>

          {activeAlerts.length === 0 ? (
            <div className="py-8 text-center">
              <ShieldCheck className="w-12 h-12 text-emerald-500 mx-auto mb-2 opacity-90" />
              <p className="text-sm font-semibold text-slate-800">All Motor Conditions Within Tolerances</p>
              <p className="text-xs text-slate-500 mt-1">
                No vibration peaks, thermal runaways, or overcurrent spikes detected.
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {activeAlerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-4 rounded-xl border ${
                    alert.severity === 'CRITICAL'
                      ? 'bg-rose-50/60 border-rose-200'
                      : 'bg-amber-50/60 border-amber-200'
                  } space-y-2`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <AlertBadge severity={alert.severity} />
                      <span className="text-xs font-bold text-slate-800 uppercase">{alert.alert_type}</span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-500">
                      {new Date(alert.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-xs text-slate-700 leading-relaxed font-medium">{alert.description}</p>
                  <div className="p-2.5 rounded-lg bg-white border border-slate-200 text-xs text-slate-600 flex items-start gap-2">
                    <Wrench className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                    <div>
                      <strong className="text-slate-800">Prescribed Action:</strong> {alert.suggested_action}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right: Real-time Anomaly Injector */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
              <Sliders className="w-4 h-4 text-blue-600" />
              <h4 className="text-sm font-bold text-slate-800">Fault Injection Testbench</h4>
            </div>
            <p className="text-xs text-slate-500 mt-2 leading-relaxed">
              Trigger specific mechanical, electrical, and thermal failure modes to verify automated rule detection, WebSocket alerting, and recovery.
            </p>

            <div className="mt-4 space-y-2">
              <button
                onClick={() => changeSimulationMode('normal')}
                className={`w-full text-left p-3 rounded-xl border text-xs font-semibold flex items-center justify-between transition-all ${
                  simulationState.mode === 'normal'
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-800'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <span>Normal Balanced Operation</span>
                <span className="text-[10px] text-slate-400 font-mono">RMS &lt; 1.8 m/s²</span>
              </button>

              <button
                onClick={() => changeSimulationMode('high_vibration')}
                className={`w-full text-left p-3 rounded-xl border text-xs font-semibold flex items-center justify-between transition-all ${
                  simulationState.mode === 'high_vibration'
                    ? 'bg-amber-50 border-amber-300 text-amber-800'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <span>Bearing Defect & Vibration Spike</span>
                <span className="text-[10px] text-amber-600 font-mono">&gt; 4.8 m/s²</span>
              </button>

              <button
                onClick={() => changeSimulationMode('overheating')}
                className={`w-full text-left p-3 rounded-xl border text-xs font-semibold flex items-center justify-between transition-all ${
                  simulationState.mode === 'overheating'
                    ? 'bg-rose-50 border-rose-300 text-rose-800'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <span>Cooling Failure & Thermal Runaway</span>
                <span className="text-[10px] text-rose-600 font-mono">&gt; 64 °C</span>
              </button>

              <button
                onClick={() => changeSimulationMode('high_current')}
                className={`w-full text-left p-3 rounded-xl border text-xs font-semibold flex items-center justify-between transition-all ${
                  simulationState.mode === 'high_current'
                    ? 'bg-amber-50 border-amber-300 text-amber-800'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <span>Mechanical Jam / Overcurrent</span>
                <span className="text-[10px] text-amber-600 font-mono">&gt; 1.6 A</span>
              </button>

              <button
                onClick={() => changeSimulationMode('multi_fault')}
                className={`w-full text-left p-3 rounded-xl border text-xs font-semibold flex items-center justify-between transition-all ${
                  simulationState.mode === 'multi_fault'
                    ? 'bg-purple-50 border-purple-300 text-purple-800'
                    : 'bg-slate-50 hover:bg-slate-100 border-slate-200 text-slate-700'
                }`}
              >
                <span>Compound Multi-Condition Breakdown</span>
                <span className="text-[10px] text-purple-600 font-mono">Multi-Modal</span>
              </button>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500">
            Current Mode: <strong className="text-slate-800 uppercase font-mono">{simulationState.mode}</strong>
          </div>
        </div>
      </div>

      {/* Historical Alert Log */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-800">Historical Fault Event Records</h3>
          <button
            onClick={fetchAlerts}
            className="text-xs font-semibold text-blue-600 hover:text-blue-800"
          >
            Refresh Log
          </button>
        </div>
        <AlertTable alerts={allAlerts} onAcknowledge={handleAcknowledge} />
      </div>
    </div>
  );
};

export default FaultDetection;
