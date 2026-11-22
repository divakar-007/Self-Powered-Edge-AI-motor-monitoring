# Database Design & Schema Specifications

The MEMS Industrial Monitoring System uses a dual-database architecture:
1. **SQLite (Relational)** for machine metadata, user configurations, and fault history.
2. **InfluxDB (Time-Series)** for high-frequency numerical sensor telemetry.

---

## 1. SQLite Relational Schema

```
+--------------------------------------------------------------+
|                          machines                            |
+--------------------+--------------+--------------------------+
| id (PK)            | VARCHAR(50)  | Machine tag (e.g. MOTOR_001)|
| machine_name       | VARCHAR(100) | Human-readable name      |
| device_id          | VARCHAR(50)  | Paired edge device ID    |
| motor_type         | VARCHAR(100) | Motor specification      |
| installation_date  | DATETIME     | Commissioning timestamp  |
| status             | VARCHAR(20)  | NORMAL, WARNING, CRITICAL|
+--------------------+--------------+--------------------------+
                                | 1
                                |
             +------------------+------------------+
             | 1:N                                 | 1:N
             v                                     v
+-------------------------------+   +-------------------------------+
|     sensor_configurations     |   |            alerts             |
+-------------------------------+   +-------------------------------+
| id (PK, Auto)  | INTEGER      |   | id (PK, Auto)  | INTEGER      |
| machine_id(FK) | VARCHAR(50)  |   | machine_id(FK) | VARCHAR(50)  |
| sensor_name    | VARCHAR(50)  |   | alert_type     | VARCHAR(50)  |
| warning_th     | FLOAT        |   | severity       | VARCHAR(20)  |
| critical_th    | FLOAT        |   | description    | VARCHAR(255) |
| calibration_val| FLOAT        |   | sensor_value   | FLOAT        |
| updated_at     | DATETIME     |   | timestamp      | DATETIME     |
+-------------------------------+   | status         | VARCHAR(20)  |
                                    +-------------------------------+

+--------------------------------------------------------------+
|                       sensor_readings                        |
+--------------------+--------------+--------------------------+
| id (PK, Auto)      | INTEGER      | Primary Key              |
| device_id          | VARCHAR(50)  | ESP32 ID (e.g. ESP32_001)|
| machine_id         | VARCHAR(50)  | Machine ID               |
| timestamp          | DATETIME     | UTC ISO timestamp        |
| source             | VARCHAR(20)  | "hardware" or "simulation"|
| vibration_x        | FLOAT        | Accel X (m/s²)           |
| vibration_y        | FLOAT        | Accel Y (m/s²)           |
| vibration_z        | FLOAT        | Accel Z (m/s²)           |
| vibration_rms      | FLOAT        | Computed Vector RMS      |
| gyro_x             | FLOAT        | Angular rate X (rad/s)   |
| gyro_y             | FLOAT        | Angular rate Y (rad/s)   |
| gyro_z             | FLOAT        | Angular rate Z (rad/s)   |
| temperature        | FLOAT        | DS18B20 Temp (°C)        |
| current            | FLOAT        | ACS712 Current (A)       |
| piezo_voltage      | FLOAT        | Rectified Piezo (V)      |
+--------------------+--------------+--------------------------+
```

---

## 2. InfluxDB Time-Series Model

- **Organization**: `mems_org`
- **Bucket**: `motor_telemetry`
- **Retention**: 30 days (`30d`)
- **Measurement**: `motor_sensor_data`

### Index Tags (Indexed for high-speed queries)
- `device_id`: Tag identifying edge hardware node (e.g., `ESP32_001`)
- `machine_id`: Tag identifying industrial motor (e.g., `MOTOR_001`)
- `source`: Tag identifying provenance (`hardware` vs `simulation`)

### Fields (Stored numerical measurements)
- `vibration_x`: Float (m/s²)
- `vibration_y`: Float (m/s²)
- `vibration_z`: Float (m/s²)
- `vibration_rms`: Float (m/s²)
- `gyro_x`: Float (rad/s)
- `gyro_y`: Float (rad/s)
- `gyro_z`: Float (rad/s)
- `temperature`: Float (°C)
- `current`: Float (A)
- `piezo_voltage`: Float (V)

### High-Frequency Waveform Policy
In compliance with requirements, high-frequency raw waveform bursts are processed in memory for live FFT decomposition and spectral bin generation rather than serialized as thousands of individual InfluxDB fields, avoiding database bloating.
