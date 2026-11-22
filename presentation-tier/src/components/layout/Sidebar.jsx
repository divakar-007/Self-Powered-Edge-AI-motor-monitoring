import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Activity,
  AlertTriangle,
  Zap,
  History,
  Settings,
  Cpu,
  Radio
} from 'lucide-react';
import { useSensor } from '../../context/SensorContext';

const navigationItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Live Monitoring', path: '/live', icon: Activity },
  { name: 'Fault Detection', path: '/faults', icon: AlertTriangle, hasAlertBadge: true },
  { name: 'Energy Monitoring', path: '/energy', icon: Zap },
  { name: 'Historical Data', path: '/history', icon: History },
  { name: 'Settings', path: '/settings', icon: Settings },
];

const Sidebar = () => {
  const { activeAlerts, latestData } = useSensor();

  return (
    <aside className="w-64 bg-navy-900 border-r border-slate-800 flex flex-col h-screen fixed left-0 top-0 z-30 select-none">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 gap-3 border-b border-slate-800/80 bg-navy-950/40">
        <div className="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-600/30">
          <Cpu className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-white font-bold text-sm tracking-wide leading-tight">MEMS MONITOR</h1>
          <p className="text-xs text-slate-400 font-mono">Autonomous Node</p>
        </div>
      </div>

      {/* Edge Node Status Summary Pill */}
      <div className="mx-4 my-4 p-3 rounded-xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="relative flex h-2.5 w-2.5">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
              latestData.source === 'hardware' ? 'bg-emerald-400' : 'bg-cyan-400'
            }`}></span>
            <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${
              latestData.source === 'hardware' ? 'bg-emerald-500' : 'bg-cyan-500'
            }`}></span>
          </div>
          <div>
            <div className="text-xs font-semibold text-slate-200">
              {latestData.source === 'hardware' ? 'ESP32-S3 Physical' : 'Simulation Mode'}
            </div>
            <div className="text-[10px] text-slate-400 font-mono">ID: {latestData.device_id}</div>
          </div>
        </div>
        <Radio className="w-4 h-4 text-slate-400" />
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 space-y-1.5 overflow-y-auto pt-2">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20 font-semibold'
                    : 'text-slate-300 hover:bg-slate-800/70 hover:text-white'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <Icon className="w-4 h-4" />
                <span>{item.name}</span>
              </div>

              {item.hasAlertBadge && activeAlerts.length > 0 && (
                <span className="px-2 py-0.5 text-xs font-bold bg-rose-500 text-white rounded-full animate-pulse shadow-sm">
                  {activeAlerts.length}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Machine Architecture Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-navy-950/40">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Three-Tier System</span>
          <span className="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">v1.0.0</span>
        </div>
        <div className="mt-1 text-[11px] text-slate-500 truncate">
          Motor: {latestData.machine_id}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
