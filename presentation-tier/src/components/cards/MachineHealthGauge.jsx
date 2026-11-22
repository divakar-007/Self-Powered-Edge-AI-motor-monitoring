import React from 'react';
import { Activity, AlertTriangle, ShieldCheck } from 'lucide-react';

const MachineHealthGauge = ({ healthScore = 95, status = 'NORMAL', activeAlertsCount = 0 }) => {
  const getColors = () => {
    if (status === 'CRITICAL' || healthScore < 60) {
      return {
        text: 'text-rose-600',
        stroke: '#EF4444',
        bg: 'bg-rose-50',
        border: 'border-rose-200',
        label: 'CRITICAL ATTENTION',
      };
    } else if (status === 'WARNING' || healthScore < 85) {
      return {
        text: 'text-amber-600',
        stroke: '#F59E0B',
        bg: 'bg-amber-50',
        border: 'border-amber-200',
        label: 'WARNING CONDITION',
      };
    }
    return {
      text: 'text-emerald-600',
      stroke: '#10B981',
      bg: 'bg-emerald-50',
      border: 'border-emerald-200',
      label: 'OPTIMAL HEALTH',
    };
  };

  const colors = getColors();
  const radius = 64;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (healthScore / 100) * circumference;

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className="p-2 rounded-lg bg-blue-50 text-blue-600">
            <Activity className="w-5 h-5" />
          </span>
          <div>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
              Overall Motor Health Index
            </h3>
            <p className="text-xs text-slate-500">Autonomous Edge AI & Multi-Modal Fusion</p>
          </div>
        </div>

        <div className="mt-4 space-y-2">
          <div className="flex items-center gap-2">
            <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${colors.bg} ${colors.text} border ${colors.border}`}>
              {colors.label}
            </span>
            <span className="text-xs text-slate-500 font-medium">
              {activeAlertsCount === 0 ? 'No active threshold faults' : `${activeAlertsCount} active abnormal conditions`}
            </span>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            Composite health calculated from 3-axis vibration acceleration RMS, DS18B20 core temperature, ACS712 current load, and piezoelectric kinetic harvesting amplitude.
          </p>
        </div>
      </div>

      {/* Circular Gauge */}
      <div className="relative flex items-center justify-center">
        <svg className="w-36 h-36 transform -rotate-90">
          <circle
            cx="72"
            cy="72"
            r={radius}
            stroke="#E2E8F0"
            strokeWidth="12"
            fill="transparent"
          />
          <circle
            cx="72"
            cy="72"
            r={radius}
            stroke={colors.stroke}
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-700 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center">
          <span className={`text-3xl font-black ${colors.text} mono-metric`}>
            {Math.round(healthScore)}%
          </span>
          <span className="text-[10px] font-bold text-slate-400 tracking-wider">HEALTH</span>
        </div>
      </div>
    </div>
  );
};

export default MachineHealthGauge;
