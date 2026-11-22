import React from 'react';
import { Line } from 'react-chartjs-2';
import '../../utils/chartSetup';

const LiveVibrationChart = ({ dataPoints = [], warningThreshold = 3.0, criticalThreshold = 5.0 }) => {
  const labels = dataPoints.map((dp) => {
    const d = new Date(dp.timestamp);
    return `${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Vibration RMS (m/s²)',
        data: dataPoints.map((dp) => dp.vibration_rms || 0),
        borderColor: '#2563EB',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        borderWidth: 2.5,
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
      {
        label: 'Z-Axis (m/s²)',
        data: dataPoints.map((dp) => dp.vibration_z || 0),
        borderColor: '#06B6D4',
        borderWidth: 1.5,
        borderDash: [4, 4],
        tension: 0.2,
        fill: false,
        pointRadius: 0,
      },
      {
        label: 'Warning Limit (3.0 m/s²)',
        data: dataPoints.map(() => warningThreshold),
        borderColor: '#F59E0B',
        borderWidth: 1.5,
        borderDash: [6, 6],
        pointRadius: 0,
        fill: false,
      },
      {
        label: 'Critical Limit (5.0 m/s²)',
        data: dataPoints.map(() => criticalThreshold),
        borderColor: '#EF4444',
        borderWidth: 1.5,
        borderDash: [6, 6],
        pointRadius: 0,
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false, // Performance for 1Hz real-time stream
    plugins: {
      legend: {
        position: 'top',
        labels: {
          boxWidth: 12,
          font: { size: 11, family: 'Inter' },
          color: '#475569',
        },
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 10 }, color: '#94A3B8', maxTicksLimit: 8 },
      },
      y: {
        min: 0,
        suggestedMax: 6,
        grid: { color: '#F1F5F9' },
        ticks: { font: { size: 10 }, color: '#94A3B8' },
        title: { display: true, text: 'm/s²', color: '#64748B', font: { size: 11 } },
      },
    },
  };

  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-800">Live Vibration Dynamics (MPU6050)</h4>
          <p className="text-xs text-slate-500">Continuous vector RMS and vertical axis acceleration</p>
        </div>
        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
          WebSocket Live
        </span>
      </div>
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default LiveVibrationChart;
