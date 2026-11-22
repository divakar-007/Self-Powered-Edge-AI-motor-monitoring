# System Architecture & Technical Specifications

**Project Title:** Self-Powered Multimodal MEMS Sensor Node, Edge AI and Adaptive Wireless Communication for Autonomous Industrial Monitoring

---

## 1. High-Level Architectural Model

The system strictly adheres to an industrial-grade **Three-Tier Architectural Pattern**, separating Presentation, Business Logic, and Data Persistence layers.

```mermaid
flowchart TD
    subgraph EdgeLayer["Edge Hardware Layer"]
        S1["MPU6050 (3-Axis Accel / Gyro)"]
        S2["DS18B20 (Temperature)"]
        S3["ACS712 (Current Sensor)"]
        S4["Piezo Harvester (Voltage)"]
        ESP["ESP32-S3 Microcontroller"]
        S1 -->|I2C 400kHz| ESP
        S2 -->|1-Wire Digital| ESP
        S3 -->|Conditioned ADC (10k/20k)| ESP
        S4 -->|Rectified ADC (3.3V Zener)| ESP
    end

    subgraph SimulationLayer["Simulation Pipeline"]
        SIM["Python Physics-Informed Simulator"]
    end

    subgraph BrokerLayer["Communication Broker"]
        MOSQ["Eclipse Mosquitto MQTT Broker (Port 1883)"]
    end

    subgraph AppTier["Application Tier (FastAPI)"]
        subgraph Ingestion["Ingestion & Protocol Engine"]
            MQTT_SUB["Paho MQTT Async Client"]
            REST_EP["REST Endpoints (/api/sensors/data)"]
            SIM_RUN["Async Simulator Loop"]
        end

        subgraph Core["Business Logic Engine"]
            VAL["Schema Validation (Pydantic)"]
            DSP["NumPy Signal Processing (FFT, RMS)"]
            FAULT["Rule-Based Fault Detection & Recovery Tracker"]
            TINYML["ITinyMLDetector Inference Hook"]
        end

        subgraph Broadcast["Real-Time Dispatcher"]
            WS_MGR["WebSocket Manager (/ws/sensors)"]
        end
    end

    subgraph DataTier["Data Tier"]
        SQLITE["SQLite Relational DB (Machines, Configs, Alerts)"]
        INFLUX["InfluxDB v2 Time-Series Engine (30-day Retention)"]
    end

    subgraph PresTier["Presentation Tier (React + Vite)"]
        DASH["Industrial Dashboard"]
        LIVE["Real-Time Live Telemetry"]
        FAULTS["Anomaly Diagnostics Center"]
        ENERGY["Energy Scavenging Analytics"]
        HIST["Historical Records & CSV Export"]
        SETTINGS["Calibrated Thresholds & Controls"]
    end

    ESP -->|MQTT Pub / JSON| MOSQ
    MOSQ -->|Subscribe| MQTT_SUB
    SIM -->|Async Ingest| SIM_RUN
    MQTT_SUB --> VAL
    REST_EP --> VAL
    SIM_RUN --> VAL

    VAL --> DSP
    DSP --> FAULT
    FAULT --> TINYML
    FAULT --> SQLITE
    DSP --> INFLUX
    DSP --> SQLITE

    FAULT --> WS_MGR
    DSP --> WS_MGR
    WS_MGR -->|WebSocket 1Hz| PresTier
    SQLITE <-->|REST API| PresTier
    INFLUX <-->|REST API| PresTier
```

---

## 2. Tier Details

### Tier 1: Presentation Tier (Frontend)
- **Framework**: React 18 with Vite for ultra-fast HMR and bundle optimization.
- **Styling**: Tailwind CSS configured with custom industrial dark navy (`#0F172A`), slate backgrounds, and standard alarm color codes (Green/Orange/Red).
- **Visualization**: Chart.js and `react-chartjs-2` for real-time 1Hz dynamic line charts, bar spectrums (FFT), and circular SVG gauges.
- **State Management**: Centralized `SensorContext` binding WebSocket live streams, alarm notifications, and simulation controls.
- **Pages**:
  1. *Dashboard*: Executive health summary, 6 sensor KPI cards, dynamic charts, active alarms.
  2. *Live Monitoring*: High-frequency MPU6050 6-DOF telemetry, live FFT bar chart, DS18B20 temperature, ACS712 current, and piezo voltage.
  3. *Fault Detection*: Rules-based engine diagnostic state, fault injection bench, and prescriptive maintenance recommendations.
  4. *Energy Monitoring*: Piezoelectric voltage analysis, instantaneous power calculations ($P = V^2 / R$), energy accumulator ($\mu\text{J}$), and conditioning schematic.
  5. *Historical Data*: Chronological logs, multi-sensor selector, and CSV export.
  6. *Settings*: Dynamic threshold form synced to SQLite, system connectivity diagnostics.

### Tier 2: Application Tier (Backend)
- **Framework**: FastAPI (Python 3.13) with asynchronous event loops.
- **Protocol Handlers**:
  - Paho MQTT v2 client running in a dedicated thread with auto-reconnection and non-blocking queue ingestion.
  - Native FastAPI WebSockets (`/ws/sensors`) dispatching telemetry and alerts without browser polling.
- **Signal Processing**: NumPy computing true vector RMS ($RMS = \sqrt{\frac{x^2+y^2+z^2}{3}}$), windowed FFT frequency decomposition, and ISO 10816 vibration severity zones.
- **Fault Detection Service**: State-tracking alarm engine with recovery detection, deduplication, and `ITinyMLDetector` interface for plug-and-play machine learning integration.

### Tier 3: Data Tier (Storage)
- **SQLite (Relational)**: Stores machine inventory, dynamic user-calibrated thresholds, historical alert incidents, and historical telemetry cache.
- **InfluxDB v2 (Time-Series)**: High-speed ingestion for time-stamped metrics (`vibration_x/y/z/rms`, `temperature`, `current`, `piezo_voltage`). Includes automatic 30-day retention policies.
- **Fault-Tolerant Fallback**: If InfluxDB is offline, the backend automatically maintains time-series history in SQLite so the dashboard remains 100% operational.
