# Application Tier – REST & WebSocket API Documentation

The FastAPI backend exposes interactive OpenAPI / Swagger documentation at `/docs` and ReDoc at `/redoc`.

---

## 1. System Health & Diagnostics

### `GET /api/health`
Returns system status, active database connections (SQLite and InfluxDB), and MQTT link status.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-11-22T19:30:00Z",
  "application_tier": {
    "status": "UP",
    "version": "1.0.0",
    "environment": "development"
  },
  "data_tier": {
    "sqlite": { "status": "UP", "path": ".../data-tier/sqlite/mems_industrial.db" },
    "influxdb": { "connected": true, "url": "http://localhost:8086", "bucket": "motor_telemetry" }
  },
  "communication": {
    "mqtt": { "connected": true, "broker_host": "localhost", "broker_port": 1883 },
    "websocket_connections": 2
  }
}
```

---

## 2. Sensor Telemetry Endpoints

### `GET /api/sensors/latest`
Fetches the most recent sensor reading.

**Response (200 OK):**
```json
{
  "device_id": "ESP32_001",
  "machine_id": "MOTOR_001",
  "timestamp": "2026-11-22T19:30:00Z",
  "source": "simulation",
  "vibration_x": 1.15,
  "vibration_y": 0.82,
  "vibration_z": 2.34,
  "vibration_rms": 1.56,
  "gyro_x": 0.045,
  "gyro_y": -0.012,
  "gyro_z": 0.088,
  "temperature": 38.4,
  "current": 0.58,
  "piezo_voltage": 1.75,
  "machine_status": "NORMAL",
  "iso_zone": "Zone A (Good - Optimal Operating Condition)"
}
```

### `GET /api/sensors/history?machine_id=MOTOR_001&limit=50`
Retrieves chronological telemetry points for trending and analysis.

### `POST /api/sensors/data`
Ingestion endpoint for ESP32 hardware or HTTP gateways.
Runs readings through validation, fault detection, and database storage.

**Request Payload:**
```json
{
  "device_id": "ESP32_001",
  "machine_id": "MOTOR_001",
  "source": "hardware",
  "sensors": {
    "vibration_x": 1.2,
    "vibration_y": 0.9,
    "vibration_z": 2.4,
    "gyro_x": 0.02,
    "gyro_y": 0.01,
    "gyro_z": 0.04,
    "temperature": 39.2,
    "current": 0.62,
    "piezo_voltage": 1.85
  }
}
```

### `GET /api/sensors/fft`
Returns computed Fast Fourier Transform spectral bins and dominant frequency.

---

## 3. Machine & Configuration Endpoints

### `GET /api/machines`
Returns list of registered industrial motors.

### `GET /api/machines/{machine_id}`
Returns metadata and active alert count for a specific machine.

### `GET /api/machines/{machine_id}/thresholds`
Fetches current warning and critical safety thresholds.

### `PUT /api/machines/{machine_id}/thresholds`
Updates threshold limits and synchronizes live fault detection engine.

---

## 4. Fault Alerts Endpoints

### `GET /api/alerts?machine_id=MOTOR_001&status=ACTIVE&limit=50`
Retrieves fault alert log filterable by severity (`WARNING`, `CRITICAL`) and status.

### `POST /api/alerts`
Creates an edge-triggered hardware fault alert.

### `PUT /api/alerts/{id}/acknowledge`
Marks an alert as acknowledged by plant operator.

---

## 5. Prototype Simulation Endpoints

- `POST /api/simulation/start`: Starts simulated multi-modal telemetry generation.
- `POST /api/simulation/stop`: Halts simulated telemetry loop.
- `GET /api/simulation/status`: Checks simulator operational status and packet counts.
- `POST /api/simulation/mode?mode=MODE`: Injects anomaly conditions:
  - `normal`: Nominal motor operation
  - `high_vibration`: Bearing defects, imbalance
  - `overheating`: Cooling failure, thermal runaway
  - `high_current`: Mechanical jam, overload
  - `multi_fault`: Compound catastrophic breakdown

---

## 6. Real-Time WebSocket Protocol

### `ws://localhost:8000/ws/sensors`
Bi-directional real-time communication channel.

#### Broadcast Payload Types:
1. **`SENSOR_UPDATE`**:
   Broadcasts every second with new sensor values, RMS calculation, machine status, and new alerts.
2. **`NEW_ALERT`**:
   Emitted immediately upon threshold breach with prescribed maintenance action.
3. **`ALERT_RECOVERY`**:
   Emitted when a previously abnormal sensor value returns to safe tolerances.
