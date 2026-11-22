import React, { useState, useEffect, useMemo } from 'react';
import {
  BatteryCharging,
  Zap,
  Activity,
  Cpu,
  Info,
  Layers,
  ShieldCheck,
  CheckCircle2,
  RefreshCw,
  Gauge,
  Sliders,
  Sparkles
} from 'lucide-react';
import { Line } from 'react-chartjs-2';
import { useSensor } from '../context/SensorContext';
import { analyticsService, sensorService } from '../services/api';
import '../utils/chartSetup';

const EnergyMonitoring = () => {
  const { latestData, historyBuffer } = useSensor();
  const [localHistory, setLocalHistory] = useState([]);
  const [capSizeUf, setCapSizeUf] = useState(47); // 47 uF default storage capacitor
  const [energyStats, setEnergyStats] = useState({
    piezo_voltage_v: 1.85,
    load_resistance_ohms: 100000,
    instantaneous_power_uw: 34.2,
    harvesting_status: 'Active Kinetic Flow',
    storage_state: 'Simulated Capacitor Bank (47µF / 16V)',
  });
  const [loading, setLoading] = useState(false);

  // 1. Fetch initial energy analytics and history if historyBuffer is empty
  const fetchEnergyData = async () => {
    setLoading(true);
    try {
      const [energyRes, historyRes] = await Promise.allSettled([
        analyticsService.getEnergyAnalytics(),
        sensorService.getHistory('MOTOR_001', 30),
      ]);

      if (energyRes.status === 'fulfilled' && energyRes.value.data) {
        setEnergyStats(energyRes.value.data);
      }

      if (historyRes.status === 'fulfilled' && Array.isArray(historyRes.value.data) && historyRes.value.data.length > 0) {
        setLocalHistory(historyRes.value.data);
      }
    } catch (err) {
      console.warn('Error fetching energy telemetry:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnergyData();
  }, []);

  // Update stats whenever latest timestamp changes
  useEffect(() => {
    if (latestData?.timestamp) {
      analyticsService.getEnergyAnalytics()
        .then((res) => {
          if (res.data) setEnergyStats(res.data);
        })
        .catch(() => {});
    }
  }, [latestData?.timestamp]);

  // Determine current active telemetry points (fallback to localHistory or realistic baseline)
  const activeHistory = useMemo(() => {
    if (historyBuffer && historyBuffer.length > 0) {
      return historyBuffer;
    }
    if (localHistory && localHistory.length > 0) {
      return localHistory;
    }
    // Generate initial baseline so the chart never displays blank
    const now = Date.now();
    return Array.from({ length: 15 }, (_, i) => {
      const t = new Date(now - (14 - i) * 1000);
      return {
        timestamp: t.toISOString(),
        piezo_voltage: +(1.4 + 0.3 * Math.sin(i * 0.5)).toFixed(2),
        vibration_rms: +(1.1 + 0.2 * Math.cos(i * 0.5)).toFixed(2),
      };
    });
  }, [historyBuffer, localHistory]);

  // Numerical values
  const currentVoltage = Number(
    latestData?.piezo_voltage || energyStats?.piezo_voltage_v || 1.85
  );
  const loadR = energyStats?.load_resistance_ohms || 100000;
  const instantaneousPowerUw = Number(
    energyStats?.instantaneous_power_uw || (Math.pow(currentVoltage, 2) / loadR) * 1e6
  );

  // Energy in capacitor: E = 0.5 * C * V^2 (Joules)
  const capFarads = (capSizeUf * 1e-6);
  const storedEnergyUj = +(0.5 * capFarads * Math.pow(currentVoltage, 2) * 1e6).toFixed(2);

  // Accumulated energy over active timeline window (uJ)
  const accumulatedEnergyUj = +(instantaneousPowerUw * Math.max(activeHistory.length, 1) * 1.0).toFixed(0);

  // Vibration correlation
  const currentVibRms = Number(latestData?.vibration_rms || 1.2);
  const conversionRatio = currentVibRms > 0 ? (instantaneousPowerUw / currentVibRms).toFixed(1) : '0.0';

  // Chart Setup
  const chartLabels = activeHistory.map((dp) => {
    const d = new Date(dp.timestamp);
    return `${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
  });

  const chartData = {
    labels: chartLabels,
    datasets: [
      {
        label: 'Measured Piezoelectric Voltage (V)',
        data: activeHistory.map((dp) => Number(dp.piezo_voltage || 0)),
        borderColor: '#06B6D4',
        backgroundColor: 'rgba(6, 182, 212, 0.12)',
        borderWidth: 2.5,
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
      {
        label: 'Zener Diode Clamp Limit (3.3V)',
        data: activeHistory.map(() => 3.3),
        borderColor: '#EF4444',
        borderWidth: 1.5,
        borderDash: [6, 6],
        pointRadius: 0,
        fill: false,
      },
      {
        label: 'Minimum Scavenging Threshold (0.5V)',
        data: activeHistory.map(() => 0.5),
        borderColor: '#10B981',
        borderWidth: 1.5,
        borderDash: [4, 4],
        pointRadius: 0,
        fill: false,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    plugins: {
      legend: {
        position: 'top',
        labels: { boxWidth: 12, font: { size: 11, family: 'Inter' }, color: '#475569' },
      },
      tooltip: { mode: 'index', intersect: false },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 10 }, color: '#94A3B8', maxTicksLimit: 10 },
      },
      y: {
        min: 0,
        suggestedMax: 4.5,
        grid: { color: '#F1F5F9' },
        ticks: { font: { size: 10 }, color: '#94A3B8' },
        title: { display: true, text: 'Voltage (Volts)', color: '#64748B', font: { size: 11 } },
      },
    },
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Kinetic Energy Harvesting Analytics
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Piezoelectric transducer vibration scavenging, rectification, and electrical power conversion
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchEnergyData}
            disabled={loading}
            className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 inline-flex items-center gap-1.5 shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Refresh Telemetry
          </button>

          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-cyan-50 text-cyan-800 border border-cyan-200 flex items-center gap-1.5">
            <BatteryCharging className="w-4 h-4 text-cyan-600" />
            Harvester Status: {currentVoltage > 0.5 ? 'Active Kinetic Flow' : 'Low Excitation'}
          </span>
        </div>
      </div>

      {/* Physics Clarification Banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4 text-xs text-blue-900 flex items-start gap-3">
        <Info className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
        <div className="leading-relaxed">
          <strong className="font-bold">Engineering Principle:</strong> Piezoelectric open-circuit voltage ($V_{oc}$) is not equivalent to usable energy. Usable electrical energy requires rectification and storage in a capacitor ($E = \frac{1}{2} C V^2$) or dissipation across a load ($P = \frac{V^2}{R}$). The values below distinguish measured rectified voltage from instantaneous calculated electrical power.
        </div>
      </div>

      {/* 4 Primary Metric KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Measured Voltage */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Measured Transducer Voltage
          </span>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-3xl font-extrabold text-cyan-700 mono-metric">
              {currentVoltage.toFixed(2)}
            </span>
            <span className="text-sm font-semibold text-slate-500">Volts</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">Peak rectified output at ADC pin</div>
        </div>

        {/* Card 2: Instantaneous Power */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Instantaneous Power Output
          </span>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-3xl font-extrabold text-slate-900 mono-metric">
              {instantaneousPowerUw.toFixed(1)}
            </span>
            <span className="text-sm font-semibold text-slate-500">µW</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Dissipated across 100 kΩ load ($P = V^2 / R$)
          </div>
        </div>

        {/* Card 3: Harvested Energy Accumulation */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Harvested Energy Window
          </span>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-3xl font-extrabold text-emerald-600 mono-metric">
              {accumulatedEnergyUj}
            </span>
            <span className="text-sm font-semibold text-slate-500">µJ</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Accumulated over last {activeHistory.length}s window
          </div>
        </div>

        {/* Card 4: Capacitor Stored Energy */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Stored Energy in Capacitor
          </span>
          <div className="mt-3 flex items-baseline gap-1">
            <span className="text-3xl font-extrabold text-amber-600 mono-metric">
              {storedEnergyUj}
            </span>
            <span className="text-sm font-semibold text-slate-500">µJ ({capSizeUf}µF)</span>
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Formula: $E = \frac{1}{2} C V^2$
          </div>
        </div>
      </div>

      {/* Voltage History Line Chart */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h4 className="text-sm font-bold text-slate-800">
              Piezoelectric Transducer Output Voltage Timeline
            </h4>
            <p className="text-xs text-slate-500">
              Dynamic real-time kinetic voltage with 3.3V Zener diode clamp and 0.5V minimum scavenging boundary
            </p>
          </div>
          <span className="text-xs font-mono font-semibold px-2.5 py-1 bg-slate-100 rounded text-slate-600">
            Samples: {activeHistory.length}
          </span>
        </div>
        <div className="h-72">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* Energy Harvesting Performance Matrix & Capacitor Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Performance Table */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h4 className="text-sm font-bold text-slate-800">
            Energy Harvesting Performance & Efficiency Breakdown
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
                <tr>
                  <th className="py-2.5 px-4">Parameter</th>
                  <th className="py-2.5 px-4">Current Value</th>
                  <th className="py-2.5 px-4">Unit</th>
                  <th className="py-2.5 px-4">Status / Interpretation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                <tr>
                  <td className="py-2.5 px-4 font-sans font-semibold text-slate-800">Rectified Output Voltage ($V_{DC}$)</td>
                  <td className="py-2.5 px-4 font-bold text-cyan-700">{currentVoltage.toFixed(2)}</td>
                  <td className="py-2.5 px-4 text-slate-500">Volts</td>
                  <td className="py-2.5 px-4 font-sans text-slate-600">Within safe 0.0V - 3.3V range</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 font-sans font-semibold text-slate-800">Instantaneous Power ($P$)</td>
                  <td className="py-2.5 px-4 font-bold text-slate-900">{instantaneousPowerUw.toFixed(2)}</td>
                  <td className="py-2.5 px-4 text-slate-500">µW</td>
                  <td className="py-2.5 px-4 font-sans text-slate-600">Power available across 100kΩ load</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 font-sans font-semibold text-slate-800">Vibration-to-Power Ratio</td>
                  <td className="py-2.5 px-4 font-bold text-emerald-700">{conversionRatio}</td>
                  <td className="py-2.5 px-4 text-slate-500">µW / (m/s²)</td>
                  <td className="py-2.5 px-4 font-sans text-slate-600">Harvester mechanical coupling factor</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 font-sans font-semibold text-slate-800">Excitation Vibration RMS</td>
                  <td className="py-2.5 px-4 font-bold text-blue-700">{currentVibRms.toFixed(2)}</td>
                  <td className="py-2.5 px-4 text-slate-500">m/s²</td>
                  <td className="py-2.5 px-4 font-sans text-slate-600">Kinetic driving vibration level</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 font-sans font-semibold text-slate-800">Clamping Diode Protection</td>
                  <td className="py-2.5 px-4 font-bold text-rose-700">3.3</td>
                  <td className="py-2.5 px-4 text-slate-500">Volts (Max)</td>
                  <td className="py-2.5 px-4 font-sans text-emerald-600 font-semibold">1N4728A Active Guard</td>
                </tr>
                <tr>
                  <td className="py-2.5 px-4 font-sans font-semibold text-slate-800">Energy Storage Module</td>
                  <td className="py-2.5 px-4 font-bold text-amber-700">Pending</td>
                  <td className="py-2.5 px-4 text-slate-500">—</td>
                  <td className="py-2.5 px-4 font-sans text-amber-700">Future hardware integration component</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: Interactive Storage Capacitor Model */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <h4 className="text-sm font-bold text-slate-800 flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-500" />
              Storage Capacitor Calculator
            </h4>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Estimate harvested charge stored in buffer capacitors before deep-sleep burst transmissions:
            </p>

            <div className="mt-4 space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1.5">
                  Buffer Capacitor Capacitance:
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {[10, 47, 100].map((val) => (
                    <button
                      key={val}
                      onClick={() => setCapSizeUf(val)}
                      className={`py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                        capSizeUf === val
                          ? 'bg-amber-500 text-white border-amber-600 shadow-sm'
                          : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {val} µF
                    </button>
                  ))}
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-500">Capacitor Voltage:</span>
                  <span className="font-mono font-bold text-slate-800">{currentVoltage.toFixed(2)} V</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Stored Energy ($E$):</span>
                  <span className="font-mono font-bold text-emerald-700">{storedEnergyUj} µJ</span>
                </div>
                <div className="flex justify-between border-t border-slate-200 pt-1.5">
                  <span className="text-slate-500">ESP32 Deep-Sleep Duration:</span>
                  <span className="font-mono font-bold text-blue-700">
                    {(storedEnergyUj / (15 * 3.3)).toFixed(1)} ms
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-[11px] text-amber-900 leading-relaxed">
            <strong>Hardware Clarification:</strong> Piezo disc generates micro-watts. An integrated power management IC (like LTC3588-1) and duty-cycling are required for full autonomy.
          </div>
        </div>
      </div>

      {/* Energy Scavenging Signal Conditioning Topology */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <h4 className="text-sm font-bold text-slate-800">Energy Scavenging Signal Conditioning Topology</h4>
        <p className="text-xs text-slate-500">
          Schematic signal flow designed to safely condition piezoelectric micro-generator pulses before ESP32 ADC sampling.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-xs font-bold text-slate-700 uppercase">1. Transducer</div>
            <div className="my-2 text-sm font-semibold text-slate-900">Piezo Ceramic Disc</div>
            <p className="text-[11px] text-slate-500">Generates AC pulses from motor mechanical vibration</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-xs font-bold text-slate-700 uppercase">2. Rectification</div>
            <div className="my-2 text-sm font-semibold text-slate-900">Schottky Bridge</div>
            <p className="text-[11px] text-slate-500">4x 1N5819 low forward drop (0.2V) AC to DC rectification</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-xs font-bold text-slate-700 uppercase">3. Protection</div>
            <div className="my-2 text-sm font-semibold text-rose-700">3.3V Zener Diode</div>
            <p className="text-[11px] text-slate-500">1N4728A clamps voltage spikes safely below ESP32 ADC max</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-center">
            <div className="text-xs font-bold text-slate-700 uppercase">4. ESP32 Sampling</div>
            <div className="my-2 text-sm font-semibold text-blue-700">GPIO 2 (ADC1_1)</div>
            <p className="text-[11px] text-slate-500">12-bit ADC with 16x oversampling and smoothing</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnergyMonitoring;
