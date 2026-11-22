import React, { useState, useEffect } from 'react';
import {
  History as HistoryIcon,
  Download,
  Filter,
  Calendar,
  Layers,
  ArrowUpDown,
  RefreshCw
} from 'lucide-react';
import { Line } from 'react-chartjs-2';
import { sensorService, alertService } from '../services/api';
import '../utils/chartSetup';

const HistoryPage = () => {
  const [historyData, setHistoryData] = useState([]);
  const [selectedSensor, setSelectedSensor] = useState('vibration_rms');
  const [recordLimit, setRecordLimit] = useState(50);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, [recordLimit]);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await sensorService.getHistory('MOTOR_001', recordLimit);
      if (Array.isArray(res.data)) {
        setHistoryData(res.data);
      }
    } catch (err) {
      console.error('Error fetching sensor history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportCSV = () => {
    if (historyData.length === 0) return;

    const headers = [
      'Timestamp',
      'Device_ID',
      'Machine_ID',
      'Source',
      'Vibration_X(m/s2)',
      'Vibration_Y(m/s2)',
      'Vibration_Z(m/s2)',
      'Vibration_RMS(m/s2)',
      'Temperature(C)',
      'Current(A)',
      'Piezo_Voltage(V)',
    ];

    const rows = historyData.map((d) => [
      d.timestamp,
      d.device_id,
      d.machine_id,
      d.source,
      d.vibration_x,
      d.vibration_y,
      d.vibration_z,
      d.vibration_rms,
      d.temperature,
      d.current,
      d.piezo_voltage,
    ]);

    const csvContent =
      'data:text/csv;charset=utf-8,' +
      [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `motor_telemetry_history_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Sensor Config for graph
  const sensorConfigs = {
    vibration_rms: {
      label: 'Vibration RMS (m/s²)',
      color: '#2563EB',
      bg: 'rgba(37, 99, 235, 0.1)',
      unit: 'm/s²',
    },
    temperature: {
      label: 'Temperature (°C)',
      color: '#F97316',
      bg: 'rgba(249, 115, 22, 0.1)',
      unit: '°C',
    },
    current: {
      label: 'Current (A)',
      color: '#10B981',
      bg: 'rgba(16, 185, 129, 0.1)',
      unit: 'A',
    },
    piezo_voltage: {
      label: 'Piezoelectric Output (V)',
      color: '#06B6D4',
      bg: 'rgba(6, 182, 212, 0.1)',
      unit: 'V',
    },
  };

  const activeConfig = sensorConfigs[selectedSensor] || sensorConfigs.vibration_rms;

  const chartLabels = historyData.map((d) => {
    const dt = new Date(d.timestamp);
    return `${dt.getHours().toString().padStart(2, '0')}:${dt.getMinutes().toString().padStart(2, '0')}:${dt.getSeconds().toString().padStart(2, '0')}`;
  });

  const chartData = {
    labels: chartLabels,
    datasets: [
      {
        label: activeConfig.label,
        data: historyData.map((d) => d[selectedSensor] || 0),
        borderColor: activeConfig.color,
        backgroundColor: activeConfig.bg,
        borderWidth: 2,
        tension: 0.2,
        fill: true,
        pointRadius: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top', labels: { font: { size: 11 } } },
      tooltip: { mode: 'index', intersect: false },
    },
    scales: {
      x: { grid: { display: false }, ticks: { font: { size: 10 }, color: '#94A3B8', maxTicksLimit: 10 } },
      y: {
        grid: { color: '#F1F5F9' },
        ticks: { font: { size: 10 }, color: '#94A3B8' },
        title: { display: true, text: activeConfig.unit, color: '#64748B', font: { size: 11 } },
      },
    },
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Historical Telemetry & Audit Logs
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Query time-series telemetry records stored in SQLite and InfluxDB
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchHistory}
            disabled={loading}
            className="px-3 py-2 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 inline-flex items-center gap-1.5 shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button
            onClick={handleExportCSV}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-blue-600 text-white hover:bg-blue-700 inline-flex items-center gap-2 shadow-sm shadow-blue-600/20"
          >
            <Download className="w-3.5 h-3.5" />
            Export to CSV
          </button>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
            <Filter className="w-4 h-4 text-slate-400" />
            <span>Select Metric:</span>
          </div>

          <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl">
            <button
              onClick={() => setSelectedSensor('vibration_rms')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                selectedSensor === 'vibration_rms'
                  ? 'bg-white text-blue-700 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Vibration RMS
            </button>
            <button
              onClick={() => setSelectedSensor('temperature')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                selectedSensor === 'temperature'
                  ? 'bg-white text-amber-700 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Temperature
            </button>
            <button
              onClick={() => setSelectedSensor('current')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                selectedSensor === 'current'
                  ? 'bg-white text-emerald-700 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Current
            </button>
            <button
              onClick={() => setSelectedSensor('piezo_voltage')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                selectedSensor === 'piezo_voltage'
                  ? 'bg-white text-cyan-700 shadow-sm'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Piezo Voltage
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500">Record Depth:</span>
          <select
            value={recordLimit}
            onChange={(e) => setRecordLimit(Number(e.target.value))}
            className="text-xs font-semibold bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 outline-none"
          >
            <option value={20}>Last 20 Samples</option>
            <option value={50}>Last 50 Samples</option>
            <option value={100}>Last 100 Samples</option>
            <option value={200}>Last 200 Samples</option>
          </select>
        </div>
      </div>

      {/* Historical Trend Chart */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <h3 className="text-sm font-bold text-slate-800 mb-4">{activeConfig.label} – Chronological Timeline</h3>
        <div className="h-72">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* Historical Records Table */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between">
          <h4 className="text-sm font-bold text-slate-800">
            Raw Telemetry Table ({historyData.length} records)
          </h4>
          <span className="text-xs text-slate-500 font-mono">Machine: MOTOR_001</span>
        </div>

        <div className="overflow-x-auto max-h-96 overflow-y-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200 sticky top-0 z-10">
              <tr>
                <th className="py-2.5 px-4">Timestamp</th>
                <th className="py-2.5 px-4">Source</th>
                <th className="py-2.5 px-4">Vib X</th>
                <th className="py-2.5 px-4">Vib Y</th>
                <th className="py-2.5 px-4">Vib Z</th>
                <th className="py-2.5 px-4">Vib RMS</th>
                <th className="py-2.5 px-4">Temp (°C)</th>
                <th className="py-2.5 px-4">Current (A)</th>
                <th className="py-2.5 px-4">Piezo (V)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
              {historyData.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                  <td className="py-2 px-4 text-slate-600 whitespace-nowrap">
                    {new Date(row.timestamp).toLocaleTimeString()} ({new Date(row.timestamp).toLocaleDateString()})
                  </td>
                  <td className="py-2 px-4 whitespace-nowrap">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-sans font-semibold ${
                      row.source === 'hardware' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'
                    }`}>
                      {row.source}
                    </span>
                  </td>
                  <td className="py-2 px-4 text-slate-700">{row.vibration_x?.toFixed(2)}</td>
                  <td className="py-2 px-4 text-slate-700">{row.vibration_y?.toFixed(2)}</td>
                  <td className="py-2 px-4 text-slate-700">{row.vibration_z?.toFixed(2)}</td>
                  <td className="py-2 px-4 font-bold text-blue-700">{row.vibration_rms?.toFixed(2)}</td>
                  <td className="py-2 px-4 font-bold text-amber-700">{row.temperature?.toFixed(1)}</td>
                  <td className="py-2 px-4 font-bold text-emerald-700">{row.current?.toFixed(2)}</td>
                  <td className="py-2 px-4 font-bold text-cyan-700">{row.piezo_voltage?.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default HistoryPage;
