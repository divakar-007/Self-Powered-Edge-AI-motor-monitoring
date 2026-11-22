import React from 'react';
import { ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';

const MetricCard = ({
  title,
  value,
  unit,
  icon: Icon,
  trend,
  trendDirection = 'neutral', // 'up', 'down', 'neutral'
  status = 'normal', // 'normal', 'warning', 'critical'
  subtitle,
}) => {
  const getStatusStyles = () => {
    switch (status) {
      case 'critical':
        return {
          border: 'border-rose-200',
          bg: 'bg-white',
          glow: 'ring-1 ring-rose-400/30',
          badge: 'bg-rose-50 text-rose-700 border-rose-200',
          iconBg: 'bg-rose-50 text-rose-600',
        };
      case 'warning':
        return {
          border: 'border-amber-200',
          bg: 'bg-white',
          glow: 'ring-1 ring-amber-400/30',
          badge: 'bg-amber-50 text-amber-700 border-amber-200',
          iconBg: 'bg-amber-50 text-amber-600',
        };
      default:
        return {
          border: 'border-slate-200',
          bg: 'bg-white',
          glow: '',
          badge: 'bg-emerald-50 text-emerald-700 border-emerald-200',
          iconBg: 'bg-blue-50 text-blue-600',
        };
    }
  };

  const styles = getStatusStyles();

  return (
    <div
      className={`p-5 rounded-2xl ${styles.bg} border ${styles.border} ${styles.glow} shadow-sm hover:shadow-md transition-all duration-200`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</span>
        <div className={`p-2.5 rounded-xl ${styles.iconBg} border border-slate-100`}>
          {Icon && <Icon className="w-5 h-5" />}
        </div>
      </div>

      <div className="mt-4 flex items-baseline gap-2">
        <span className="text-3xl font-extrabold text-slate-900 tracking-tight mono-metric">
          {typeof value === 'number' ? value.toFixed(2) : value}
        </span>
        {unit && <span className="text-sm font-semibold text-slate-500">{unit}</span>}
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
        <span className="text-slate-500 font-medium truncate">{subtitle || 'Live Sensor'}</span>
        {trend && (
          <div className="flex items-center gap-1 font-semibold">
            {trendDirection === 'up' && <ArrowUpRight className="w-3.5 h-3.5 text-rose-500" />}
            {trendDirection === 'down' && <ArrowDownRight className="w-3.5 h-3.5 text-emerald-500" />}
            {trendDirection === 'neutral' && <Minus className="w-3.5 h-3.5 text-slate-400" />}
            <span
              className={
                trendDirection === 'up'
                  ? 'text-rose-600'
                  : trendDirection === 'down'
                  ? 'text-emerald-600'
                  : 'text-slate-500'
              }
            >
              {trend}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
