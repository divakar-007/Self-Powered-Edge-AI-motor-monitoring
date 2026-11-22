import React from 'react';

const AlertBadge = ({ severity = 'NORMAL', text }) => {
  const sev = (severity || 'NORMAL').toUpperCase();

  if (sev === 'CRITICAL') {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-300">
        <span className="w-1.5 h-1.5 rounded-full bg-rose-600 animate-pulse"></span>
        {text || 'CRITICAL'}
      </span>
    );
  }

  if (sev === 'WARNING') {
    return (
      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300">
        <span className="w-1.5 h-1.5 rounded-full bg-amber-600"></span>
        {text || 'WARNING'}
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
      <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
      {text || 'NORMAL'}
    </span>
  );
};

export default AlertBadge;
