import React, { useState } from 'react';
import {
  Activity,
  Thermometer,
  Zap,
  BatteryCharging,
  Cpu,
  Wifi,
  Radio,
  Play,
  Pause,
  AlertTriangle,
  RotateCcw
} from 'lucide-react';
import { useSensor } from '../context/SensorContext';
import MetricCard from '../components/cards/MetricCard';
import MachineHealthGauge from '../components/cards/MachineHealthGauge';
import LiveVibrationChart from '../components/charts/LiveVibrationChart';
import ThermalTrendChart from '../components/charts/ThermalTrendChart';
import CurrentTrendChart from '../components/charts/CurrentTrendChart';
import AlertTable from '../components/alerts/AlertTable';
import { alertService } from '../services/api';

const Dashboard = () => {
  const {
    latestData,
    historyBuffer,
    activeAlerts,
    connectionStatus,
    simulationState,
    changeSimulationMode,
    toggleSimulation,
  } = useSensor();

  const [simLoading, setSimLoading] = useState(false);

  const handleModeSwitch = async (mode) => {
    setSimLoading(true);
    try {
      await changeSimulationMode(mode);
    } catch (err) {
      console.error(err);
    } finally {
      setSimLoading(false);
    }
  };

  const handleAcknowledgeAlert = async (id) => {
    try {
      await alertService.acknowledgeAlert(id);
    } catch (err) {
      console.error(err);
    }
  };

  const getMetricStatus = (metric, val) => {
    if (metric === 'vibration') {
      if (val >= 5.0) return 'critical';
      if (val >= 3.0) return 'warning';
      return 'normal';
    }
    if (metric === 'temperature') {
      if (val >= 60.0) return 'critical';
      if (val >= 45.0) return 'warning';
      return 'normal';
    }
    if (metric === 'current') {
      if (val >= 1.5) return 'critical';
      if (val >= 1.0) return 'warning';
      return 'normal';
    }
    if (metric === 'piezo') {
      if (val >= 4.2) return 'warning';
      return 'normal';
    }
    return 'normal';
  };

  const vibRms = latestData.vibration_rms || 0;
  const temp = latestData.temperature || 0;
  const current = latestData.current || 0;
  const piezoV = latestData.piezo_voltage || 0;

  // Approximate health score from active status
  let healthScore = 98;
  if (latestData.machine_status === 'CRITICAL') healthScore = 42;
  else if (latestData.machine_status === 'WARNING') healthScore = 78;

  return (
    <div className="space-y-6">
      {/* Top Banner: Anomaly Injector Toolbar for Prototype Evaluation */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-blue-50 text-blue-600">
            <Radio className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Prototype Simulation Control Panel
            </h3>
            <p className="text-[11px] text-slate-500">
              Active Mode: <strong className="text-blue-600 uppercase font-mono">{simulationState.mode}</strong>
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => handleModeSwitch('normal')}
            disabled={simLoading}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              simulationState.mode === 'normal'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            Normal Motor
          </button>
          <button
            onClick={() => handleModeSwitch('high_vibration')}
            disabled={simLoading}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              simulationState.mode === 'high_vibration'
                ? 'bg-amber-600 text-white shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            High Vibration
          </button>
          <button
            onClick={() => handleModeSwitch('overheating')}
            disabled={simLoading}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              simulationState.mode === 'overheating'
                ? 'bg-rose-600 text-white shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            Overheating
          </button>
          <button
            onClick={() => handleModeSwitch('high_current')}
            disabled={simLoading}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              simulationState.mode === 'high_current'
                ? 'bg-amber-600 text-white shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            High Current
          </button>
          <button
            onClick={() => handleModeSwitch('multi_fault')}
            disabled={simLoading}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              simulationState.mode === 'multi_fault'
                ? 'bg-purple-600 text-white shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
          >
            Compound Multi-Fault
          </button>

          <button
            onClick={toggleSimulation}
            className="ml-2 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 text-white hover:bg-slate-900 inline-flex items-center gap-1.5"
          >
            {simulationState.running ? (
              <>
                <Pause className="w-3.5 h-3.5" /> Pause Feed
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" /> Resume Feed
              </>
            )}
          </button>
        </div>
      </div>

      {/* 6 Sensor Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {/* 1. Vibration Level */}
        <MetricCard
          title="Vibration RMS"
          value={vibRms}
          unit="m/s²"
          icon={Activity}
          status={getMetricStatus('vibration', vibRms)}
          subtitle={latestData.iso_zone?.split(' ')[0] || 'ISO Zone'}
          trend={vibRms > 3.0 ? '+Elevated' : 'Stable'}
          trendDirection={vibRms > 3.0 ? 'up' : 'neutral'}
        />

        {/* 2. Temperature */}
        <MetricCard
          title="Temperature"
          value={temp}
          unit="°C"
          icon={Thermometer}
          status={getMetricStatus('temperature', temp)}
          subtitle="DS18B20 Surface"
          trend={temp > 45 ? '+Rising' : 'Nominal'}
          trendDirection={temp > 45 ? 'up' : 'neutral'}
        />

        {/* 3. Electrical Current */}
        <MetricCard
          title="Current Draw"
          value={current}
          unit="A"
          icon={Zap}
          status={getMetricStatus('current', current)}
          subtitle="ACS712 Measured"
          trend={current > 1.0 ? '+High Load' : 'Normal'}
          trendDirection={current > 1.0 ? 'up' : 'neutral'}
        />

        {/* 4. Piezoelectric Voltage */}
        <MetricCard
          title="Piezo Voltage"
          value={piezoV}
          unit="V"
          icon={BatteryCharging}
          status={getMetricStatus('piezo', piezoV)}
          subtitle="Kinetic Harvester"
          trend={piezoV > 2.0 ? 'Active' : 'Idle'}
          trendDirection="neutral"
        />

        {/* 5. Machine Health Status */}
        <MetricCard
          title="Machine Status"
          value={latestData.machine_status || 'NORMAL'}
          icon={Cpu}
          status={latestData.machine_status === 'CRITICAL' ? 'critical' : latestData.machine_status === 'WARNING' ? 'warning' : 'normal'}
          subtitle={`Node: ${latestData.device_id}`}
        />

        {/* 6. Device Connection Status */}
        <MetricCard
          title="Device Link"
          value={connectionStatus}
          icon={Wifi}
          status={connectionStatus === 'CONNECTED' ? 'normal' : 'warning'}
          subtitle={latestData.source === 'hardware' ? 'ESP32 MQTT Link' : 'Simulator Link'}
        />
      </div>

      {/* Health Gauge & Operational Metadata */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <MachineHealthGauge
            healthScore={healthScore}
            status={latestData.machine_status}
            activeAlertsCount={activeAlerts.length}
          />
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Motor Operating Parameters
            </h4>
            <div className="mt-3 space-y-2.5 text-xs">
              <div className="flex items-center justify-between pb-1.5 border-b border-slate-100">
                <span className="text-slate-500">Machine Model</span>
                <span className="font-semibold text-slate-800">DC Brushed Motor (Line 1)</span>
              </div>
              <div className="flex items-center justify-between pb-1.5 border-b border-slate-100">
                <span className="text-slate-500">Data Source</span>
                <span className="font-semibold text-blue-600 uppercase font-mono">{latestData.source}</span>
              </div>
              <div className="flex items-center justify-between pb-1.5 border-b border-slate-100">
                <span className="text-slate-500">ISO 10816 Zone</span>
                <span className="font-semibold text-slate-800">{latestData.iso_zone || 'Zone A (Good)'}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Last Telemetry Packet</span>
                <span className="font-mono text-slate-700 font-medium">
                  {latestData.timestamp ? new Date(latestData.timestamp).toLocaleTimeString() : '—'}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-500 flex items-center justify-between">
            <span>Buffer Samples: {historyBuffer.length}</span>
            <span className="flex items-center gap-1 text-emerald-600 font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-ping"></span>
              Streaming Live
            </span>
          </div>
        </div>
      </div>

      {/* Real-time Dynamic Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <LiveVibrationChart dataPoints={historyBuffer} />
        <ThermalTrendChart dataPoints={historyBuffer} />
        <CurrentTrendChart dataPoints={historyBuffer} />
      </div>

      {/* Recent Alerts Section */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            <h3 className="text-base font-bold text-slate-800">Recent Fault Alerts & Anomaly Records</h3>
          </div>
          <span className="text-xs text-slate-500">
            Showing latest active alarms with rule-based severity
          </span>
        </div>
        <AlertTable alerts={activeAlerts} onAcknowledge={handleAcknowledgeAlert} />
      </div>
    </div>
  );
};

export default Dashboard;
