import React from 'react';
import AlertBadge from './AlertBadge';
import { AlertCircle, CheckCircle, Wrench } from 'lucide-react';

const AlertTable = ({ alerts = [], onAcknowledge, onResolve, showActions = true }) => {
  if (alerts.length === 0) {
    return (
      <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center">
        <CheckCircle className="w-12 h-12 text-emerald-500 mx-auto mb-3 opacity-90" />
        <h4 className="text-sm font-bold text-slate-800">No Active Fault Alerts</h4>
        <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
          All multi-modal sensors are operating within calibrated safety thresholds. Motor health is stable.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-500 uppercase font-semibold border-b border-slate-200">
            <tr>
              <th className="py-3 px-4">Severity</th>
              <th className="py-3 px-4">Fault Type</th>
              <th className="py-3 px-4">Description</th>
              <th className="py-3 px-4">Sensor Reading</th>
              <th className="py-3 px-4">Timestamp</th>
              <th className="py-3 px-4">Suggested Action</th>
              {showActions && <th className="py-3 px-4 text-right">Action</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {alerts.map((alert) => (
              <tr key={alert.id} className="hover:bg-slate-50/80 transition-colors">
                <td className="py-3 px-4 whitespace-nowrap">
                  <AlertBadge severity={alert.severity} />
                </td>
                <td className="py-3 px-4 font-semibold text-slate-800 whitespace-nowrap">
                  {alert.alert_type}
                </td>
                <td className="py-3 px-4 text-slate-700 max-w-xs">
                  {alert.description}
                </td>
                <td className="py-3 px-4 font-mono font-medium text-slate-800 whitespace-nowrap">
                  {alert.sensor_value !== null && alert.sensor_value !== undefined
                    ? alert.sensor_value
                    : '—'}
                </td>
                <td className="py-3 px-4 text-slate-500 whitespace-nowrap font-mono">
                  {new Date(alert.timestamp).toLocaleTimeString()} ({new Date(alert.timestamp).toLocaleDateString()})
                </td>
                <td className="py-3 px-4 text-slate-600 max-w-xs">
                  <div className="flex items-start gap-1.5 text-[11px] bg-slate-50 p-2 rounded border border-slate-200">
                    <Wrench className="w-3.5 h-3.5 text-blue-600 shrink-0 mt-0.5" />
                    <span>{alert.suggested_action || 'Inspect DC motor and check sensor cabling.'}</span>
                  </div>
                </td>
                {showActions && (
                  <td className="py-3 px-4 text-right whitespace-nowrap">
                    {alert.status === 'ACTIVE' ? (
                      <button
                        onClick={() => onAcknowledge && onAcknowledge(alert.id)}
                        className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded text-[11px] transition-colors border border-slate-300"
                      >
                        Acknowledge
                      </button>
                    ) : (
                      <span className="text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">
                        Acknowledged
                      </span>
                    )}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AlertTable;
