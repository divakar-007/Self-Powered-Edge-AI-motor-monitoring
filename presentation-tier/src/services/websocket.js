class WebSocketService {
  constructor() {
    this.ws = null;
    const host = (typeof window !== 'undefined' && window.location.hostname) ? window.location.hostname : '127.0.0.1';
    this.url = import.meta.env.VITE_WS_URL || `ws://${host}:8000/ws/sensors`;
    this.subscribers = {
      sensor: new Set(),
      alert: new Set(),
      recovery: new Set(),
      status: new Set(),
    };
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 30;
    this.reconnectInterval = 2000;
    this.reconnectTimer = null;
    this.isConnected = false;
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this._notifyStatus('CONNECTING');

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this._notifyStatus('CONNECTED');
        console.log('[WebSocket] Connected to Application Tier Live Feed');
      };

      this.ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          this._handleMessage(payload);
        } catch (err) {
          console.error('[WebSocket] Error parsing message JSON:', err);
        }
      };

      this.ws.onclose = () => {
        this.isConnected = false;
        this._notifyStatus('DISCONNECTED');
        console.warn('[WebSocket] Disconnected from server. Scheduling reconnect...');
        this._scheduleReconnect();
      };

      this.ws.onerror = (error) => {
        console.warn('[WebSocket] Error encountered:', error);
        this.ws.close();
      };
    } catch (e) {
      console.error('[WebSocket] Connection failed:', e);
      this._scheduleReconnect();
    }
  }

  _scheduleReconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);

    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(10000, this.reconnectInterval * Math.min(this.reconnectAttempts, 5));
      this.reconnectTimer = setTimeout(() => {
        console.log(`[WebSocket] Attempting reconnect (#${this.reconnectAttempts})...`);
        this.connect();
      }, delay);
    }
  }

  _handleMessage(payload) {
    if (!payload || !payload.type) return;

    if (payload.type === 'SENSOR_UPDATE') {
      this.subscribers.sensor.forEach((cb) => cb(payload.data, payload.machine_status, payload.alerts));
    } else if (payload.type === 'NEW_ALERT') {
      this.subscribers.alert.forEach((cb) => cb(payload.alert));
    } else if (payload.type === 'ALERT_RECOVERY') {
      this.subscribers.recovery.forEach((cb) => cb(payload.recovered_types, payload.machine_id));
    }
  }

  _notifyStatus(status) {
    this.subscribers.status.forEach((cb) => cb(status));
  }

  subscribeSensor(callback) {
    this.subscribers.sensor.add(callback);
    return () => this.subscribers.sensor.delete(callback);
  }

  subscribeAlert(callback) {
    this.subscribers.alert.add(callback);
    return () => this.subscribers.alert.delete(callback);
  }

  subscribeRecovery(callback) {
    this.subscribers.recovery.add(callback);
    return () => this.subscribers.recovery.delete(callback);
  }

  subscribeStatus(callback) {
    this.subscribers.status.add(callback);
    callback(this.isConnected ? 'CONNECTED' : 'DISCONNECTED');
    return () => this.subscribers.status.delete(callback);
  }

  disconnect() {
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.isConnected = false;
  }
}

export const wsService = new WebSocketService();
export default wsService;
