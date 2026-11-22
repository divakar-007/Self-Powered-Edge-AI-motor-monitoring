import React from 'react';
import { Bar } from 'react-chartjs-2';
import '../../utils/chartSetup';

const FFTSpectrumChart = ({ frequencies = [], amplitudes = [], dominantFreq = 50.0 }) => {
  const chartData = {
    labels: frequencies.map((f) => `${f} Hz`),
    datasets: [
      {
        label: 'Vibration Spectral Amplitude (m/s²)',
        data: amplitudes,
        backgroundColor: frequencies.map((f) =>
          Math.abs(f - dominantFreq) < 5 ? '#EF4444' : '#3B82F6'
        ),
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          title: (items) => `Frequency: ${items[0].label}`,
          label: (item) => `Amplitude: ${item.raw.toFixed(3)} m/s²`,
        },
      },
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 9 }, color: '#94A3B8', maxTicksLimit: 12 },
        title: { display: true, text: 'Frequency (Hz)', color: '#64748B', font: { size: 10 } },
      },
      y: {
        beginAtZero: true,
        grid: { color: '#F1F5F9' },
        ticks: { font: { size: 10 }, color: '#94A3B8' },
        title: { display: true, text: 'Peak Amplitude (m/s²)', color: '#64748B', font: { size: 10 } },
      },
    },
  };

  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-bold text-slate-800">Frequency Spectrum (FFT Analysis)</h4>
          <p className="text-xs text-slate-500">Fast Fourier Transform of MEMS accelerometer high-speed samples</p>
        </div>
        <div className="px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-xs font-mono font-semibold text-slate-700">
          Dominant Peak: <span className="text-rose-600 font-bold">{dominantFreq} Hz</span>
        </div>
      </div>
      <div className="h-64">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  );
};

export default FFTSpectrumChart;
