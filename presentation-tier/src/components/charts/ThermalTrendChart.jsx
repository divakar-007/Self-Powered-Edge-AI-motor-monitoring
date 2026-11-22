import React from 'react';
import { Line } from 'react-chartjs-2';
import '../../utils/chartSetup';

const ThermalTrendChart = ({ dataPoints = [], warningThreshold = 45.0, criticalThreshold = 60.0 }) => {
  const labels = dataPoints.map((dp) => {
    const d = new Date(dp.timestamp);
    return `${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Motor Temperature (°C)',
        data: dataPoints.map((dp) => dp.temperature || 0),
        borderColor: '#F97316',
        backgroundColor: 'rgba(249, 115, 22, 0.1)',
        borderWidth: 2.5,
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
      {
        label: 'Warning (45°C)',
        data: dataPoints.map(() => warningThreshold),
        borderColor: '#F59E0B',
        borderWidth: 1.5,
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false,
      },
      {
        label: 'Critical (60°C)',
        data: dataPoints.map(() => criticalThreshold),
        borderColor: '#EF4444',
        borderWidth: 1.5,
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false,
      },
    ],
  };

  const options = {
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
        ticks: { font: { size: 10 }, color: '#94A3B8', maxTicksLimit: 8 },
      },
      y: {
        min: 20,
        suggestedMax: 70,
        grid: { color: '#F1F5F9' },
        ticks: { font: { size: 10 }, color: '#94A3B8' },
        title: { display: true, text: '°C', color: '#64748B', font: { size: 11 } },
      },
    },
  };

  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-800">Motor Temperature History (DS18B20)</h4>
          <p className="text-xs text-slate-500">Continuous surface casing thermal dissipation profile</p>
        </div>
      </div>
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default ThermalTrendChart;
