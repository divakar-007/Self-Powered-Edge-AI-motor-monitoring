import React, { useState, useEffect } from 'react';
import {
  Activity,
  Compass,
  Thermometer,
  Zap,
  BatteryCharging,
  Layers,
  Radio,
  CheckCircle2,
  RefreshCw
} from 'lucide-react';
import { useSensor } from '../context/SensorContext';
import { sensorService } from '../services/api';
import LiveVibrationChart from '../components/charts/LiveVibrationChart';
import ThermalTrendChart from '../components/charts/ThermalTrendChart';
import CurrentTrendChart from '../components/charts/CurrentTrendChart';
import FFTSpectrumChart from '../components/charts/FFTSpectrumChart';

const LiveMonitoring = () => {
  const { latestData, historyBuffer } = useSensor();
  const [fftData, setFftData] = useState({
    frequencies: [],
    amplitudes: [],
    dominant_frequency_hz: 50.0,
  });

  useEffect(() => {
    // Poll FFT spectrum periodically or fetch on update
    const fetchFFT = async () => {
      try {
        const res = await sensorService.getVibrationFFT();
        if (res.data) setFftData(res.data);
      } catch (e) {
        console.warn('Error fetching FFT spectrum:', e);
      }
    };

    fetchFFT();
    const interval = setInterval(fetchFFT, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            Real-Time Multi-Modal Telemetry
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Synchronous streaming feeds from MPU6050, DS18B20, ACS712, and Piezo Transducer
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
            1 Hz WebSocket Pipeline
          </span>
        </div>
      </div>

      {/* SENSOR 1: MPU6050 Tri-Axis Accelerometer & Gyroscope */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-50 text-blue-600">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-800">
                MPU6050 – Tri-Axial Vibration & Motion MEMS
              </h3>
              <p className="text-xs text-slate-500">I2C Fast Mode (400kHz) • ±8g Range • 500 dps Gyro</p>
            </div>
          </div>
          <span className="text-xs font-mono font-semibold text-slate-600 bg-slate-100 px-2.5 py-1 rounded">
            Calculated RMS: <strong className="text-blue-700">{latestData.vibration_rms?.toFixed(2) || '0.00'} m/s²</strong>
          </span>
        </div>

        {/* 6 Degrees of Freedom Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="text-[10px] uppercase font-bold text-slate-400">Accel X</div>
            <div className="text-lg font-bold text-slate-800 mono-metric">
              {latestData.vibration_x?.toFixed(2) || '0.00'} <span className="text-xs font-normal text-slate-400">m/s²</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="text-[10px] uppercase font-bold text-slate-400">Accel Y</div>
            <div className="text-lg font-bold text-slate-800 mono-metric">
              {latestData.vibration_y?.toFixed(2) || '0.00'} <span className="text-xs font-normal text-slate-400">m/s²</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="text-[10px] uppercase font-bold text-slate-400">Accel Z (Vertical)</div>
            <div className="text-lg font-bold text-blue-600 mono-metric">
              {latestData.vibration_z?.toFixed(2) || '0.00'} <span className="text-xs font-normal text-slate-400">m/s²</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="text-[10px] uppercase font-bold text-slate-400">Gyro X</div>
            <div className="text-lg font-bold text-slate-800 mono-metric">
              {latestData.gyro_x?.toFixed(3) || '0.000'} <span className="text-xs font-normal text-slate-400">rad/s</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="text-[10px] uppercase font-bold text-slate-400">Gyro Y</div>
            <div className="text-lg font-bold text-slate-800 mono-metric">
              {latestData.gyro_y?.toFixed(3) || '0.000'} <span className="text-xs font-normal text-slate-400">rad/s</span>
            </div>
          </div>
          <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div className="text-[10px] uppercase font-bold text-slate-400">Gyro Z</div>
            <div className="text-lg font-bold text-slate-800 mono-metric">
              {latestData.gyro_z?.toFixed(3) || '0.000'} <span className="text-xs font-normal text-slate-400">rad/s</span>
            </div>
          </div>
        </div>

        {/* Charts: Live Vibration Line + FFT Spectrum */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-2">
          <LiveVibrationChart dataPoints={historyBuffer} />
          <FFTSpectrumChart
            frequencies={fftData.frequencies}
            amplitudes={fftData.amplitudes}
            dominantFreq={fftData.dominant_frequency_hz}
          />
        </div>
      </div>

      {/* SENSOR 2 & 3: DS18B20 Temperature & ACS712 Current */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* DS18B20 */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-amber-50 text-amber-600">
                <Thermometer className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-800">DS18B20 – Digital Thermal Probe</h3>
                <p className="text-xs text-slate-500">1-Wire Digital Bus • 0.0625°C Resolution</p>
              </div>
            </div>
            <span className="text-lg font-extrabold text-amber-600 mono-metric">
              {latestData.temperature?.toFixed(1) || '0.0'} °C
            </span>
          </div>
          <ThermalTrendChart dataPoints={historyBuffer} />
        </div>

        {/* ACS712 */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-emerald-50 text-emerald-600">
                <Zap className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-800">ACS712 – Hall-Effect Current Sensor</h3>
                <p className="text-xs text-slate-500">Conditioned ADC • 2:3 Voltage Divider (3.3V Protected)</p>
              </div>
            </div>
            <span className="text-lg font-extrabold text-emerald-600 mono-metric">
              {latestData.current?.toFixed(2) || '0.00'} A
            </span>
          </div>
          <CurrentTrendChart dataPoints={historyBuffer} />
        </div>
      </div>

      {/* SENSOR 4: Piezoelectric Transducer & Kinetic Harvesting */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-50 text-cyan-600">
              <BatteryCharging className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-800">
                Piezoelectric Transducer & Energy Harvester
              </h3>
              <p className="text-xs text-slate-500">
                Kinetic Vibration Energy Conversion • Full-Bridge Rectified & Zener Clamped
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold px-2.5 py-1 rounded bg-cyan-50 text-cyan-800 border border-cyan-200">
              Harvesting: {latestData.piezo_voltage > 0.5 ? 'Active Kinetic Excitation' : 'Idle'}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Measured Output Voltage</span>
            <div className="text-2xl font-black text-cyan-700 mono-metric my-2">
              {latestData.piezo_voltage?.toFixed(2) || '0.00'} V
            </div>
            <span className="text-[11px] text-slate-500">True clamped analog voltage across rectifier</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Estimated Instantaneous Power</span>
            <div className="text-2xl font-black text-slate-800 mono-metric my-2">
              {((Math.pow(latestData.piezo_voltage || 0, 2) / 100000.0) * 1e6).toFixed(1)} µW
            </div>
            <span className="text-[11px] text-slate-500">Calculated over 100kΩ simulated test load ($P=V^2/R$)</span>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase">Energy Storage Hardware Status</span>
            <div className="text-base font-bold text-slate-700 my-2 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              Future Hardware Module
            </div>
            <span className="text-[11px] text-slate-500">
              Storage measurement unavailable until storage supercapacitor circuitry is physically wired.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveMonitoring;
