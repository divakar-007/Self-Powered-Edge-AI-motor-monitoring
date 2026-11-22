import axios from 'axios';

const getBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) return import.meta.env.VITE_API_BASE_URL;
  if (typeof window !== 'undefined' && window.location.hostname) {
    return `http://${window.location.hostname}:8000/api`;
  }
  return 'http://127.0.0.1:8000/api';
};

const API_BASE_URL = getBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const systemService = {
  getHealth: () => api.get('/health'),
};

export const sensorService = {
  getLatestReading: () => api.get('/sensors/latest'),
  getHistory: (machineId = 'MOTOR_001', limit = 50) => 
    api.get(`/sensors/history?machine_id=${machineId}&limit=${limit}`),
  getVibrationFFT: () => api.get('/sensors/fft'),
  postSensorData: (data) => api.post('/sensors/data', data),
};

export const machineService = {
  getMachines: () => api.get('/machines'),
  getMachine: (machineId) => api.get(`/machines/${machineId}`),
  getThresholds: (machineId = 'MOTOR_001') => api.get(`/machines/${machineId}/thresholds`),
  updateThresholds: (machineId, thresholds) => api.put(`/machines/${machineId}/thresholds`, thresholds),
};

export const alertService = {
  getAlerts: (params = {}) => api.get('/alerts', { params }),
  createAlert: (alertData) => api.post('/alerts', alertData),
  acknowledgeAlert: (alertId) => api.put(`/alerts/${alertId}/acknowledge`),
  resolveAlert: (alertId) => api.put(`/alerts/${alertId}/resolve`),
};

export const analyticsService = {
  getSummary: (machineId = 'MOTOR_001') => api.get(`/analytics/summary?machine_id=${machineId}`),
  getVibrationAnalytics: (machineId = 'MOTOR_001') => api.get(`/analytics/vibration?machine_id=${machineId}`),
  getEnergyAnalytics: () => api.get('/analytics/energy'),
};

export const simulationService = {
  getStatus: () => api.get('/simulation/status'),
  startSimulation: (payload = { action: 'start', interval_seconds: 1.0 }) => 
    api.post('/simulation/start', payload),
  stopSimulation: () => api.post('/simulation/stop'),
  setMode: (mode) => api.post(`/simulation/mode?mode=${mode}`),
};

export default api;
