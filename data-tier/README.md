# Data Tier – MEMS Industrial Monitoring System

This tier implements a high-performance **Hybrid Relational & Time-Series Data Architecture** optimized for industrial motor health telemetry and supervisory control.

---

## 1. Architecture Overview

```
                      +-----------------------------+
                      | Application Tier (FastAPI)  |
                      +--------------+--------------+
                                     |
               +---------------------+---------------------+
               |                                           |
               v                                           v
    +----------------------+                    +----------------------+
    | SQLite Database      |                    | InfluxDB v2          |
    | (Relational Store)   |                    | (Time-Series Engine) |
    +----------------------+                    +----------------------+
    - Machine Metadata                          - High-Frequency Telemetry
    - Threshold Configurations                  - Metric Tags (device, machine)
    - Alert History & Audits                    - 30-Day Auto Retention
    - Offline Historical Cache                  - Flux Query Optimized
```

---

## 2. SQLite (Relational Store)

- **File Path**: `data-tier/sqlite/mems_industrial.db`
- **ORM**: SQLAlchemy 2.0+
- **Purpose**:
  1. Relational machine profiles, motor models, and installation records.
  2. Dynamic threshold settings (Warning and Critical boundaries) editable via Settings.
  3. Actionable fault alerts with timestamps, severity levels, and acknowledgment logs.
  4. Local persistence cache for sensor readings ensuring full application functionality without Docker.

### Tables
1. **`machines`**: `id` (PK), `machine_name`, `device_id`, `motor_type`, `installation_date`, `status`
2. **`sensor_configurations`**: `id` (PK), `machine_id` (FK), `sensor_name`, `warning_threshold`, `critical_threshold`, `calibration_value`, `updated_at`
3. **`alerts`**: `id` (PK), `machine_id` (FK), `alert_type`, `severity`, `description`, `sensor_value`, `timestamp`, `status`
4. **`sensor_readings`**: `id` (PK), `device_id`, `machine_id`, `timestamp`, `source`, `vibration_x/y/z/rms`, `gyro_x/y/z`, `temperature`, `current`, `piezo_voltage`

---

## 3. InfluxDB (Time-Series Store)

- **Bucket**: `motor_telemetry`
- **Measurement**: `motor_sensor_data`
- **Retention**: 30 days
- **Tags**:
  - `device_id`: e.g., `ESP32_001`
  - `machine_id`: e.g., `MOTOR_001`
  - `source`: `hardware` or `simulation`
- **Fields**:
  - `vibration_x`, `vibration_y`, `vibration_z`, `vibration_rms` (m/s²)
  - `gyro_x`, `gyro_y`, `gyro_z` (rad/s)
  - `temperature` (°C)
  - `current` (A)
  - `piezo_voltage` (V)

---

## 4. Fault Tolerance & Fallback

If Docker or InfluxDB is unavailable, the backend automatically logs the condition and seamlessly routes time-series reads and writes to the local SQLite historical table. The system never crashes or halts ingestion when time-series storage is offline.
