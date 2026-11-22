import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import wsService from '../services/websocket';
import { sensorService, alertService, simulationService } from '../services/api';

const SensorContext = createContext(null);

export const SensorProvider = ({ children }) => {
  const [latestData, setLatestData] = useState({
    device_id: 'ESP32_001',
    machine_id: 'MOTOR_001',
    timestamp: new Date().toISOString(),
    source: 'simulation',
    vibration_x: 0.0,
    vibration_y: 0.0,
    vibration_z: 0.0,
    vibration_rms: 0.0,
    gyro_x: 0.0,
    gyro_y: 0.0,
    gyro_z: 0.0,
    temperature: 0.0,
    current: 0.0,
    piezo_voltage: 0.0,
    machine_status: 'NORMAL',
    iso_zone: 'Zone A (Good)',
  });

  const [historyBuffer, setHistoryBuffer] = useState([]);
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('DISCONNECTED'); // CONNECTED, CONNECTING, DISCONNECTED
  const [simulationState, setSimulationState] = useState({
    running: true,
    mode: 'normal',
    interval_seconds: 1.0,
  });

  const maxHistoryPoints = 30;

  useEffect(() => {
    // 1. Initial REST fetch for latest readings & active alerts
    sensorService.getLatestReading()
      .then((res) => {
        if (res.data && res.data.timestamp) {
          setLatestData(res.data);
        }
      })
      .catch((err) => console.warn('Could not fetch initial reading:', err));

    sensorService.getHistory('MOTOR_001', 30)
      .then((res) => {
        if (Array.isArray(res.data)) {
          setHistoryBuffer(res.data);
        }
      })
      .catch((err) => console.warn('Could not fetch initial history:', err));

    alertService.getAlerts({ status: 'ACTIVE', limit: 10 })
      .then((res) => {
        if (Array.isArray(res.data)) {
          setActiveAlerts(res.data);
        }
      })
      .catch((err) => console.warn('Could not fetch active alerts:', err));

    simulationService.getStatus()
      .then((res) => {
        if (res.data) setSimulationState(res.data);
      })
      .catch((err) => console.warn('Could not fetch simulation status:', err));

    // 2. Connect WebSocket
    wsService.connect();

    // 3. Subscribe to real-time events
    const unsubStatus = wsService.subscribeStatus((status) => {
      setConnectionStatus(status);
    });

    const unsubSensor = wsService.subscribeSensor((newData, machineStatus, newAlerts) => {
      setLatestData(newData);
      setHistoryBuffer((prev) => {
        const next = [...prev, newData];
        if (next.length > maxHistoryPoints) {
          return next.slice(next.length - maxHistoryPoints);
        }
        return next;
      });

      if (newAlerts && newAlerts.length > 0) {
        setActiveAlerts((prev) => {
          const ids = new Set(prev.map((a) => a.id));
          const additions = newAlerts.filter((a) => !ids.has(a.id));
          return [...additions, ...prev];
        });
      }
    });

    const unsubAlert = wsService.subscribeAlert((alert) => {
      setActiveAlerts((prev) => {
        if (prev.some((a) => a.id === alert.id)) return prev;
        return [alert, ...prev];
      });
    });

    const unsubRecovery = wsService.subscribeRecovery((recoveredTypes) => {
      setActiveAlerts((prev) => prev.filter((a) => !recoveredTypes.includes(a.alert_type)));
    });

    return () => {
      unsubStatus();
      unsubSensor();
      unsubAlert();
      unsubRecovery();
      wsService.disconnect();
    };
  }, []);

  const changeSimulationMode = async (mode) => {
    try {
      const res = await simulationService.setMode(mode);
      setSimulationState((prev) => ({ ...prev, mode }));
      return res.data;
    } catch (err) {
      console.error('Error changing simulation mode:', err);
      throw err;
    }
  };

  const toggleSimulation = async () => {
    try {
      if (simulationState.running) {
        await simulationService.stopSimulation();
        setSimulationState((prev) => ({ ...prev, running: false }));
      } else {
        await simulationService.startSimulation({ action: 'start', interval_seconds: 1.0 });
        setSimulationState((prev) => ({ ...prev, running: true }));
      }
    } catch (err) {
      console.error('Error toggling simulation:', err);
    }
  };

  return (
    <SensorContext.Provider
      value={{
        latestData,
        historyBuffer,
        activeAlerts,
        connectionStatus,
        simulationState,
        changeSimulationMode,
        toggleSimulation,
      }}
    >
      {children}
    </SensorContext.Provider>
  );
};

export const useSensor = () => {
  const context = useContext(SensorContext);
  if (!context) {
    throw new Error('useSensor must be used within a SensorProvider');
  }
  return context;
};
