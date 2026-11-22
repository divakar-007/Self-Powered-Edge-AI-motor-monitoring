import React, { useState, useEffect } from 'react';
import {
  Bell,
  Wifi,
  WifiOff,
  Clock,
  ShieldCheck,
  AlertTriangle,
  User,
  ExternalLink
} from 'lucide-react';
import { useSensor } from '../../context/SensorContext';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const { connectionStatus, latestData, activeAlerts } = useSensor();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showAlertDropdown, setShowAlertDropdown] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const getStatusBadge = () => {
    if (connectionStatus === 'CONNECTED') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Live WebSocket</span>
        </div>
      );
    } else if (connectionStatus === 'CONNECTING') {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-amber-500 animate-spin"></span>
          <span>Connecting...</span>
        </div>
      );
    } else {
      return (
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-xs font-semibold">
          <WifiOff className="w-3.5 h-3.5 text-rose-500" />
          <span>Offline</span>
        </div>
      );
    }
  };

  const getMachineHealthBadge = () => {
    const status = latestData.machine_status || 'NORMAL';
    if (status === 'CRITICAL') {
      return (
        <span className="px-2.5 py-1 rounded-full bg-rose-100 text-rose-800 text-xs font-bold border border-rose-300">
          STATUS: CRITICAL
        </span>
      );
    } else if (status === 'WARNING') {
      return (
        <span className="px-2.5 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-bold border border-amber-300">
          STATUS: WARNING
        </span>
      );
    }
    return (
      <span className="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold border border-emerald-300">
        STATUS: HEALTHY
      </span>
    );
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200 fixed top-0 right-0 left-64 z-20 px-6 flex items-center justify-between shadow-sm">
      {/* Title & Machine ID */}
      <div className="flex items-center gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-800 tracking-tight">
            Industrial DC Motor Health Monitoring
          </h2>
          <div className="flex items-center gap-2 text-xs text-slate-500 font-medium">
            <span>Machine: <strong className="text-slate-700">{latestData.machine_id}</strong></span>
            <span>•</span>
            <span>Device: <strong className="text-slate-700">{latestData.device_id}</strong></span>
          </div>
        </div>

        {getMachineHealthBadge()}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        {/* Connection Status */}
        {getStatusBadge()}

        {/* Local Clock */}
        <div className="hidden md:flex items-center gap-1.5 text-xs font-mono text-slate-600 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
          <Clock className="w-3.5 h-3.5 text-slate-400" />
          <span>{currentTime.toLocaleTimeString()}</span>
          <span className="text-slate-400">|</span>
          <span>{currentTime.toLocaleDateString()}</span>
        </div>

        {/* Notifications */}
        <div className="relative">
          <button
            onClick={() => setShowAlertDropdown(!showAlertDropdown)}
            className="relative p-2 text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors border border-slate-200"
            title="Active Notifications"
          >
            <Bell className="w-4 h-4" />
            {activeAlerts.length > 0 && (
              <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white shadow">
                {activeAlerts.length}
              </span>
            )}
          </button>

          {/* Alert Popover */}
          {showAlertDropdown && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-xl border border-slate-200 py-2 z-50 animate-in fade-in slide-in-from-top-2">
              <div className="px-4 py-2 border-b border-slate-100 flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800">Active Fault Notifications</span>
                <span className="text-[10px] font-semibold text-rose-600 bg-rose-50 px-2 py-0.5 rounded-full">
                  {activeAlerts.length} Active
                </span>
              </div>
              <div className="max-h-64 overflow-y-auto divide-y divide-slate-100">
                {activeAlerts.length === 0 ? (
                  <div className="px-4 py-6 text-center text-xs text-slate-500">
                    <ShieldCheck className="w-8 h-8 text-emerald-500 mx-auto mb-2 opacity-80" />
                    All motor operating parameters are normal.
                  </div>
                ) : (
                  activeAlerts.slice(0, 5).map((alert) => (
                    <div key={alert.id} className="p-3 hover:bg-slate-50 transition-colors">
                      <div className="flex items-center justify-between">
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                          alert.severity === 'CRITICAL' ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'
                        }`}>
                          {alert.severity}
                        </span>
                        <span className="text-[10px] text-slate-400">
                          {new Date(alert.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                      <p className="text-xs text-slate-700 mt-1 line-clamp-2">{alert.description}</p>
                    </div>
                  ))
                )}
              </div>
              <div className="px-3 py-1.5 border-t border-slate-100 bg-slate-50 text-center">
                <Link
                  to="/faults"
                  onClick={() => setShowAlertDropdown(false)}
                  className="text-xs font-semibold text-blue-600 hover:text-blue-800 inline-flex items-center gap-1"
                >
                  View Fault Monitoring Center <ExternalLink className="w-3 h-3" />
                </Link>
              </div>
            </div>
          )}
        </div>

        {/* User / Engineer Tag */}
        <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
          <div className="w-8 h-8 rounded-full bg-blue-100 border border-blue-200 flex items-center justify-center text-blue-700 font-bold text-xs">
            EN
          </div>
          <div className="hidden lg:block text-left text-xs">
            <div className="font-semibold text-slate-700 leading-tight">Plant Engineer</div>
            <div className="text-[10px] text-slate-400">Supervisor</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
