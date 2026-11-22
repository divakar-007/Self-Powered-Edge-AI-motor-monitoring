# Self-Powered Multimodal MEMS Sensor Node, Edge AI and Adaptive Wireless Communication for Autonomous Industrial Monitoring

![Industrial IoT](https://img.shields.io/badge/Architecture-Three--Tier-blue.svg)
![Frontend](https://img.shields.io/badge/Presentation--Tier-React_18_+_Vite_+_Tailwind-61DAFB.svg)
![Backend](https://img.shields.io/badge/Application--Tier-FastAPI_+_Python_3.13-009688.svg)
![Database](https://img.shields.io/badge/Data--Tier-SQLite_+_InfluxDB-003B57.svg)
![Microcontroller](https://img.shields.io/badge/Edge--Hardware-ESP32--S3-E7352C.svg)

An industrial-grade IoT condition monitoring system developed to monitor the real-time operational health of industrial DC electric motors. The system captures multimodal sensor data (vibration, angular velocity, temperature, electrical current, and piezoelectric harvested voltage), processes high-frequency signals using FFT decomposition, executes rule-based anomaly detection, logs time-series data, and broadcasts telemetry to an interactive web dashboard via WebSockets.

---

## 1. Project Objective

- **Autonomous Motor Health Supervisory Control**: Monitor small DC motors using multimodal MEMS sensors to detect mechanical unbalance, bearing defects, thermal runaway, and electrical overcurrent before catastrophic failure occurs.
- **Strict Three-Tier Separation**:
  1. **Presentation Tier (Frontend)**: React.js, Vite, Tailwind CSS, Chart.js, Lucide Icons.
  2. **Application Tier (Backend)**: FastAPI, Uvicorn, SQLAlchemy, Paho MQTT, WebSockets, NumPy.
  3. **Data Tier (Databases)**: SQLite (relational) + InfluxDB v2 (time-series).
- **Physical & Simulated Dual Pipeline**: Runs out-of-the-box with a high-fidelity physics-informed sensor simulator, and accepts physical ESP32-S3 hardware via MQTT without requiring code redesign.
- **Safe Electrical Conditioning**: Complete conditioning schematics for ACS712 current measurement (voltage divider) and piezoelectric kinetic scavenging (Schottky bridge with 3.3V Zener protection).

---

## 2. System Architecture

```
                                  THREE-TIER SYSTEM TOPOLOGY

   +----------------------------------------------------------------------------------------+
   |                                 PRESENTATION TIER                                      |
   |   React.js 18  •  Vite  •  Tailwind CSS  •  Chart.js  •  React-Router  •  Lucide Icons |
   |                                                                                        |
   |   [Dashboard]  [Live Telemetry]  [Fault Diagnostics]  [Energy Scavenging]  [History]  |
   +---------------------------------------▲------------------------------------------------+
                                           │ WebSocket (ws://localhost:8000/ws/sensors)
                                           │ REST API  (http://localhost:8000/api)
   +---------------------------------------▼------------------------------------------------+
   |                                  APPLICATION TIER                                      |
   |                        FastAPI (Python 3.13) + Uvicorn ASGI Server                     |
   |                                                                                        |
   |  • REST Controllers: /api/sensors, /api/machines, /api/alerts, /api/analytics          |
   |  • WebSocket Dispatcher: Broadcasts 1Hz live readings & threshold alarms              |
   |  • Signal Processing Engine: NumPy Vector RMS, Peak-to-Peak, 64-pt FFT Spectrum       |
   |  • Fault Detection Service: Rule-based boundary evaluator & deduplicated state tracker |
   |  • Edge AI Interface: ITinyMLDetector hook prepared for quantized ML model weights     |
   |  • Background Sensor Simulator: Dynamic thermal inertia & 5 anomaly injection modes    |
   |  • Paho MQTT Client: Subscribes to topics on Mosquitto broker                          |
   +---------------------------------------▲------------------------------------------------+
                                           │
                    +----------------------+----------------------+
                    │                                             │
   +----------------▼--------------------+       +----------------▼--------------------+
   |             DATA TIER               |       |             DATA TIER               |
   |         SQLite Relational DB        |       |       InfluxDB v2 Time-Series       |
   |  • Machines & Motor Models          |       |  • Measurement: motor_sensor_data   |
   |  • Calibrated Warning/Critical Limits|      |  • 30-Day Auto Retention Policy     |
   |  • Historical Alert Records         |       |  • Indexed tags: device_id, machine |
   |  • Local Telemetry Cache            |       |  • High-speed time-bucket queries   |
   +-------------------------------------+       +-------------------------------------+
                    ▲                                             ▲
                    │                                             │
   +----------------┴─────────────────────────────────────────────┴--------------------+
   |                             COMMUNICATION & EDGE FIRMWARE                         |
   |                                                                                   |
   |     [ESP32-S3 Microcontroller Node]               [Mosquitto MQTT Broker]        |
   |     • MPU6050: 3-Axis Accel / Gyro (I2C)     --->  • Port: 1883                   |
   |     • DS18B20: Digital Temperature (OneWire)       • Topic: mems/motor001/sensors |
   |     • ACS712: Current (Conditioned ADC)            • Topic: mems/motor001/status  |
   |     • Piezo Transducer: Voltage (Zener ADC)        • Topic: mems/motor001/alerts  |
   +-----------------------------------------------------------------------------------+
```

---

## 3. Technology Stack

| Layer | Technologies | Role in System |
| :--- | :--- | :--- |
| **Presentation Tier** | React 18, Vite, Tailwind CSS | Industrial dashboard UI, responsiveness, theme |
| | Chart.js, react-chartjs-2 | Dynamic live streaming graphs and FFT bar spectrum |
| | Lucide React, Axios | Icons, REST communication with backend |
| **Application Tier** | FastAPI, Uvicorn, Pydantic | Asynchronous REST endpoints and request validation |
| | NumPy | Digital signal processing, Vector RMS, and FFT decomposition |
| | Paho MQTT v2 | Asynchronous MQTT subscriber and publisher |
| | Python Asyncio & WebSockets | 1Hz low-latency live telemetry broadcast |
| **Data Tier** | SQLite & SQLAlchemy 2.0 | Relational store for machines, thresholds, alerts |
| | InfluxDB v2 | Time-series historical telemetry engine |
| | Docker Compose | Mosquitto MQTT broker and InfluxDB containerization |
| **Device Firmware** | ESP32-S3, C++, Arduino Core | Hardware acquisition, ADC oversampling, JSON serialization |

---

## 4. Complete Project Directory Structure

```
MEMS-INDUSTRIAL-MONITORING/
├── presentation-tier/              # Tier 1: Frontend Dashboard
│   ├── public/                     # Static web assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/             # Sidebar, Navbar, Main Layout
│   │   │   ├── cards/              # Metric KPI cards & Circular Health Gauge
│   │   │   ├── charts/             # Vibration RMS, Thermal, Current, FFT charts
│   │   │   ├── alerts/             # Severity badges and Alert tables
│   │   │   └── common/             # Reusable UI controls
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Main executive overview & anomaly injector
│   │   │   ├── LiveMonitoring.jsx  # 6-DOF MPU6050, Temp, Current, Piezo telemetry
│   │   │   ├── FaultDetection.jsx  # Anomaly diagnostics & prescriptive maintenance
│   │   │   ├── EnergyMonitoring.jsx# Piezoelectric kinetic conversion & power
│   │   │   ├── History.jsx         # Historical audit table and CSV export
│   │   │   └── Settings.jsx        # Safety threshold calibrations & diagnostics
│   │   ├── services/
│   │   │   ├── api.js              # Axios REST client endpoints
│   │   │   └── websocket.js        # Reconnecting WebSocket manager
│   │   ├── context/
│   │   │   └── SensorContext.jsx   # Global React sensor state provider
│   │   ├── utils/
│   │   │   └── chartSetup.js       # Chart.js component registrations
│   │   ├── App.jsx                 # Client router configuration
│   │   ├── main.jsx                # React DOM entry point
│   │   └── index.css               # Tailwind CSS declarations
│   ├── package.json
│   └── vite.config.js
│
├── application-tier/               # Tier 2: Backend Application
│   ├── app/
│   │   ├── routes/
│   │   │   ├── sensor_routes.py    # /api/sensors/* & /api/simulation/*
│   │   │   ├── machine_routes.py   # /api/machines/* & thresholds
│   │   │   ├── alert_routes.py     # /api/alerts/* & acknowledgments
│   │   │   └── analytics_routes.py # /api/analytics/* & /api/health
│   │   ├── services/
│   │   │   ├── sensor_service.py   # Central ingestion pipeline & caches
│   │   │   ├── fault_detection.py  # Rule engine, deduplication, ITinyMLDetector
│   │   │   └── analytics_service.py# RMS, FFT, ISO 10816 zone classification
│   │   ├── mqtt/
│   │   │   ├── mqtt_client.py      # Paho MQTT thread & connection manager
│   │   │   └── mqtt_handler.py     # Topic routing and async loop scheduling
│   │   ├── websocket/
│   │   │   └── websocket_manager.py# Client connection & broadcast manager
│   │   ├── database/
│   │   │   ├── sqlite_database.py  # SQLAlchemy engine & session manager
│   │   │   └── influx_database.py  # InfluxDB client & fallback handler
│   │   ├── schemas/
│   │   │   └── sensor_schema.py    # Pydantic models for incoming & outgoing JSON
│   │   ├── models/
│   │   │   ├── machine.py          # SQLAlchemy Machine & Configuration models
│   │   │   ├── alert.py            # SQLAlchemy Alert incident model
│   │   │   └── sensor_reading.py   # SQLAlchemy historical telemetry table
│   │   ├── simulator/
│   │   │   └── sensor_simulator.py # Physics-informed DC motor telemetry generator
│   │   ├── config.py               # Environment configuration settings
│   │   └── main.py                 # FastAPI application & lifespan manager
│   ├── requirements.txt
│   └── .env.example
│
├── data-tier/                      # Tier 3: Databases & Storage
│   ├── sqlite/
│   │   └── mems_industrial.db      # Local SQLite database file
│   ├── influxdb/                   # InfluxDB data & config volume directory
│   └── README.md
│
├── device-firmware/                # Edge Hardware Firmware
│   └── esp32-s3/
│       ├── esp32_s3_mems_node.ino  # Production Arduino C++ sketch for ESP32-S3
│       ├── config.h                # Pinouts, WiFi, and MQTT broker definitions
│       └── README.md               # Flashing & compilation guide
│
├── infrastructure/                 # Containerized Broker & Time-Series Stack
│   ├── docker-compose.yml          # Mosquitto & InfluxDB services
│   └── mosquitto/
│       └── config/
│           └── mosquitto.conf      # MQTT broker configuration
│
├── docs/                           # Technical Documentation
│   ├── architecture.md             # System architecture & Mermaid flowcharts
│   ├── database-design.md          # Relational & Time-Series data dictionary
│   ├── api-documentation.md        # Full REST API & WebSocket specifications
│   ├── hardware-connections.md     # Wiring tables & signal conditioning schematics
│   └── installation-guide.md       # Step-by-step setup guide
│
├── .gitignore
└── README.md
```

---

## 5. Quickstart & Installation

### Step 1: Run Backend (Application Tier)
```powershell
cd MEMS-INDUSTRIAL-MONITORING/application-tier

# Create virtual environment (if not already created)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Start FastAPI application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Backend Health Check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

### Step 2: Run Frontend (Presentation Tier)
Open a new terminal:
```powershell
cd MEMS-INDUSTRIAL-MONITORING/presentation-tier

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```
- Open your browser at: **[http://localhost:5173](http://localhost:5173)**

---

## 6. How to Run the Simulator & Anomaly Testing

The simulator starts automatically on backend launch. You can inject anomalies dynamically either from the **Dashboard UI toolbar** or via REST commands:

```powershell
# Injected high vibration (Bearing wear simulation)
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=high_vibration" -Method Post

# Inject motor overheating (Cooling failure simulation)
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=overheating" -Method Post

# Inject high electrical current (Mechanical jam simulation)
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=high_current" -Method Post

# Inject compound multi-modal anomaly
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=multi_fault" -Method Post

# Return to normal balanced operation
Invoke-RestMethod -Uri "http://localhost:8000/api/simulation/mode?mode=normal" -Method Post
```

---

## 7. MQTT Topics & Message Schema

### Topics:
- `mems/motor001/sensors`: Published by edge device (ESP32-S3) with multi-modal sensor values.
- `mems/motor001/status`: Device heartbeat, firmware version, and IP.
- `mems/motor001/alerts`: Hardware-level edge alerts.

### Sensor JSON Schema:
```json
{
  "device_id": "ESP32_001",
  "machine_id": "MOTOR_001",
  "source": "hardware",
  "sensors": {
    "vibration_x": 1.25,
    "vibration_y": 0.88,
    "vibration_z": 2.45,
    "gyro_x": 0.05,
    "gyro_y": -0.02,
    "gyro_z": 0.08,
    "temperature": 39.5,
    "current": 0.65,
    "piezo_voltage": 2.10
  }
}
```

---

## 8. Physical ESP32-S3 Hardware Integration

When you are ready to connect physical hardware:
1. Open `device-firmware/esp32-s3/config.h`.
2. Configure your WiFi credentials and your computer's local IP address under `MQTT_BROKER_IP`.
3. Wire the sensors according to the schematics in `docs/hardware-connections.md` (ensuring the 10k/20k voltage divider on the ACS712 output and the 3.3V Zener diode across the Piezo transducer).
4. Flash the sketch `device-firmware/esp32-s3/esp32_s3_mems_node.ino` using the Arduino IDE.
5. In `infrastructure/`, run `docker-compose up -d` to start Mosquitto.
6. The backend automatically switches to displaying `"source": "hardware"` telemetry on the dashboard!
