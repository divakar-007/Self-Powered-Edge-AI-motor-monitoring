import React from 'react';
import { Line } from 'react-chartjs-2';
import '../../utils/chartSetup';

const CurrentTrendChart = ({ dataPoints = [], warningThreshold = 1.0, criticalThreshold = 1.5 }) => {
  const labels = dataPoints.map((dp) => {
    const d = new Date(dp.timestamp);
    return `${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`;
  });

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Measured Current (Amperes)',
        data: dataPoints.map((dp) => dp.current || 0),
        borderColor: '#10B981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderWidth: 2.5,
        tension: 0.3,
        fill: true,
        pointRadius: 2,
      },
      {
        label: 'Warning (1.0 A)',
        data: dataPoints.map(() => warningThreshold),
        borderColor: '#F59E0B',
        borderWidth: 1.5,
        borderDash: [5, 5],
        pointRadius: 0,
        fill: false,
      },
      {
        label: 'Critical (1.5 A)',
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
        min: 0,
        suggestedMax: 2.5,
        grid: { color: '#F1F5F9' },
        ticks: { font: { size: 10 }, color: '#94A3B8' },
        title: { display: true, text: 'Amperes (A)', color: '#64748B', font: { size: 11 } },
      },
    },
  };

  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-800">Current Consumption Trend (ACS712)</h4>
          <p className="text-xs text-slate-500">
            <span className="font-semibold text-emerald-700">Measured Value:</span> True analog Hall-effect current draw
          </p>
        </div>
      </div>
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default CurrentTrendChart;
