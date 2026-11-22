# -*- coding: utf-8 -*-
"""
ch4_design.py - Chapter 4: Design Overview
"""

CHAPTER_4_TITLE = "CHAPTER 4: DESIGN OVERVIEW"

SECTIONS = [
    {
        "number": "4.1",
        "title": "Design Overview",
        "content": """The design of an autonomous industrial condition monitoring system demands an integrated approach bridging micro-machined physical transducers, analog signal conditioning electronics, real-time embedded firmware, asynchronous network protocols, and scalable multi-tier software architectures.

The design philosophy adopted in this project emphasizes four core engineering principles:
1. Architectural Decoupling: Strict separation of concerns between presentation, business logic/DSP, and data persistence, guaranteeing that changes to visualization or storage components do not disrupt real-time data acquisition.
2. Signal Integrity and Electrical Safety: Careful voltage level translation and transient over-voltage clamping to protect 3.3V CMOS microcontroller inputs from 5V analog sensor rails and high-voltage AC piezoelectric spikes.
3. Computational Efficiency at the Edge: Leveraging the dual-core architecture of the ESP32-S3 to isolate high-speed deterministic sensor polling from non-deterministic wireless networking routines.
4. Deterministic Anomaly Detection: Implementing internationally standardized mechanical vibration guidelines (ISO 10816-3) alongside multi-parameter thermal and electrical envelopes to deliver trustworthy, repeatable fault diagnostics."""
    },
    {
        "number": "4.2",
        "title": "Three-Tier System Architecture",
        "content": """The complete software infrastructure is engineered strictly according to an enterprise Three-Tier Architectural Topology (Figure 4.1):

1. Tier 1: Presentation Layer (Frontend)
   - Technologies: React.js 18, Vite build tool, Tailwind CSS utility framework, Chart.js, react-chartjs-2, and Lucide React icons.
   - Responsibilities: Renders a responsive, modern single-page monitoring interface accessible across desktop workstations, industrial panel PCs, and mobile devices. Manages persistent WebSocket client connections, maintains rolling data buffers for 5-10 Hz canvas chart streaming, calculates visual gauge angles, displays ISO 10816-3 status badges, and formats tabular historical logs.
   - Key Views: Executive Dashboard, Live Monitoring (high-speed tri-axial waveforms and FFT spectrum), Fault Detection Center (prescriptive diagnosis), Energy Harvesting Analytics, Historical Data Analytics (date-range filtering and CSV export), and System Settings (broker/threshold configurations).

2. Tier 2: Application Layer (Backend & Processing)
   - Technologies: Python 3.11, FastAPI web framework, Uvicorn ASGI server, Pydantic data schemas, Paho MQTT asynchronous client, and NumPy / SciPy digital signal processing libraries.
   - Responsibilities: Operates as the central intelligence engine. Subscribes to raw MQTT telemetry from the Mosquitto broker, validates JSON payloads, executes DSP routines (FFT spectral decomposition, peak-to-peak amplitude, and RMS velocity integration), evaluates multi-parameter fault thresholds, manages persistent WebSocket broadcasting pools, serves REST API endpoints, and orchestrates database transactions.
   - TinyML Extensibility: Encapsulates an abstract inference interface (ITinyMLDetector) providing a standardized integration slot for future on-device or edge-accelerated machine learning models.

3. Tier 3: Data Layer (Database & Persistence)
   - Technologies: SQLite 3 relational database with SQLAlchemy Object-Relational Mapping (ORM), alongside InfluxDB 2.0 time-series database engine.
   - Responsibilities: Provides robust dual-model persistence. The relational engine (SQLite) maintains machine profiles, sensor configurations, and audit-trailed fault events with full ACID transaction guarantees. The time-series engine (InfluxDB) provides optimized, columnar storage for high-velocity continuous sensor streams, enabling rapid historical aggregation and trend analysis."""
    },
    {
        "number": "4.3",
        "title": "Data Flow Diagram",
        "content": """The logical movement and transformation of telemetry throughout the system is formally specified through Data Flow Diagrams:

1. Level 0 Data Flow Diagram (Context-Level DFD - Figure 4.2):
At the context level, the entire system is represented as a single central process: "Autonomous Industrial Monitoring System". The external entities interacting with this process comprise:
- Physical DC Motor Testbed: Provides mechanical vibration, acoustic strain, casing temperature, and electrical current to the system.
- Industrial Plant Operator / Maintenance Engineer: Receives real-time streaming charts, ISO 10816 health status badges, and fault alerts; issues configuration commands and threshold adjustment parameters.
- External MQTT Broker: Acts as an asynchronous message bus routing raw sensor JSON packets into the system.

2. Level 1 Data Flow Diagram (Subsystem Decomposed DFD - Figure 4.3):
The Level 1 DFD decomposes the system into four major operational processes:
- Process 1.0 (Sensor Acquisition & Edge Ingestion): Samples physical transducers, executes ADC conversions, structures JSON strings, and publishes to MQTT topic "industrial/mems/data".
- Process 2.0 (Signal Processing & Feature Extraction): Consumes MQTT messages, validates Pydantic schemas, and computes mathematical metrics: vector acceleration magnitude, peak-to-peak amplitude, RMS velocity, and FFT frequency bins.
- Process 3.0 (Fault Classification & Alert Generation): Compares computed features against ISO 10816-3 vibration limits, thermal envelopes, and electrical over-current limits; logs anomalies into the Fault Event database.
- Process 4.0 (Visualization & Client Streaming): Pushes real-time telemetry packets across WebSocket connections to connected browser clients and executes REST queries against historical database tables."""
    },
    {
        "number": "4.4",
        "title": "Hardware Architecture",
        "content": """The hardware architecture (Figure 4.4 and Figure 4.5) centers on the Espressif ESP32-S3-WROOM-1 microcontroller module mounted on a custom prototyping carrier board.

Microcontroller Specifications:
- Processor Core: Dual-core 32-bit Xtensa LX7 operating at 240 MHz clock frequency.
- Memory: 512 KB internal SRAM, 384 KB ROM, 8 MB external Quad-SPI Flash memory.
- Vector Instructions: Hardware acceleration for 16-bit integer and floating-point vector matrix operations, tailored for embedded DSP and neural networks.
- Wireless Radio: Integrated 2.4 GHz 802.11b/g/n Wi-Fi baseband and Bluetooth 5 (LE).
- Peripherals: Two 12-bit Successive Approximation Register (SAR) Analog-to-Digital Converters (ADC), two I2C bus controllers, dedicated hardware timers, and 45 programmable General Purpose Input/Output (GPIO) lines.

Power Architecture and Pin Allocations:
The edge node is powered via a regulated 5V USB power rail. An onboard low-dropout (LDO) linear regulator generates a stable 3.3V system rail with <15 mV ripple to power the ESP32-S3 SoC, the MPU6050 sensor, and the DS18B20 digital thermal probe. The ACS712 current transducer is powered from the 5V rail to ensure correct internal Hall-effect biasing. Table 4.1 details the complete hardware pin assignment and electrical characteristics."""
    },
    {
        "number": "4.5",
        "title": "Software Architecture",
        "content": """The software architecture (Figure 5.2 and Figure 5.3) is designed using modern modular software patterns:

Frontend Component Architecture (React.js):
- Root Module: App.jsx initializes the application, mounts global layout structures, and configures the client-side router.
- State Management: React useState and useEffect hooks manage local view states, while a centralized useWebSocket hook maintains a persistent WebSocket connection to ws://localhost:8000/ws/sensors with automatic exponential-backoff reconnection logic.
- Presentation Views: Six independent view modules (Dashboard, LiveMonitoring, FaultDetection, EnergyMonitoring, History, Settings) decouple UI concerns.
- Charting Layer: Chart.js canvas elements are integrated via react-chartjs-2, utilizing downsampled rolling window arrays (100 samples) to prevent DOM memory leaks and ensure smooth 60 FPS UI rendering.

Backend Application Architecture (FastAPI):
- ASGI Server: Uvicorn manages high-concurrency asynchronous I/O over HTTP/1.1 and WebSockets.
- Router Hierarchy: Modular API routers handle health checks, real-time telemetry queries, historical record retrieval, alert logs, and system configuration.
- Service Layer Pattern: Decoupled service classes encapsulate core business logic:
  - MqttService: Handles asynchronous connection, topic subscriptions, message deserialization, and network reconnects.
  - SensorService: Manages telemetry routing, in-memory rolling buffers, and database persistence.
  - DspService: Executes numerical signal processing algorithms (NumPy FFT, RMS integration).
  - FaultService: Implements ISO 10816-3 threshold evaluation and rule-based diagnostic alerts.
  - ConnectionManager: Maintains active WebSocket client connections and broadcasts telemetry packets asynchronously."""
    },
    {
        "number": "4.6",
        "title": "Database Design",
        "content": """The data tier adopts a hybrid persistence strategy combining relational and time-series database models to balance structured relational integrity with high-throughput time-series logging:

1. Relational Persistence (SQLite via SQLAlchemy ORM):
Relational storage is utilized for entities requiring strict schema enforcement, unique constraints, and referential integrity:
- machines Table: Stores asset metadata including unique asset identifier, machine name, equipment model, rated operating speed (RPM), baseline vibration levels, and commissioning timestamps.
- fault_events Table: Audits all detected anomaly events, recording timestamp, machine ID, fault severity (WARNING, CRITICAL), fault category (VIBRATION, OVERCURRENT, OVERHEAT), trigger values, threshold limits, and operator acknowledgment status.
- sensor_readings Table: Stores downsampled periodic telemetry records for long-term historical reporting and audit compliance.

2. Time-Series Persistence (InfluxDB Engine):
For high-velocity raw telemetry, an InfluxDB client writes timestamped data points into the bucket "mems_telemetry" under measurement "machine_sensors". Tags index machine_id and sensor_id, while field values store ax, ay, az, gx, gy, gz, temperature, current, and piezo_voltage. InfluxDB's columnar compression (TSM engine) allows storing millions of high-frequency data points with minimal disk storage consumption."""
    },
    {
        "number": "4.7",
        "title": "Project Requirements",
        "content": """The hardware and software specifications required to construct, deploy, and operate the complete autonomous industrial monitoring system are detailed below."""
    },
    {
        "number": "4.7.1",
        "title": "Software Requirements",
        "content": """The software tools, runtime environments, libraries, and frameworks utilized across the three tiers comprise:
- Operating System: Microsoft Windows 11 / Ubuntu Linux 22.04 LTS (x86_64).
- Embedded Toolchain: Arduino IDE v2.3.2 with ESP32 Board Support Package (BSP) v3.0.5, ArduinoJson v7.0.4, Adafruit MPU6050 v2.2.6, DallasTemperature v3.9.0, OneWire v2.3.7, and PubSubClient v2.8.0.
- Application Runtime: Python 3.11.9 (64-bit).
- Backend Frameworks: FastAPI v0.115.5, Uvicorn v0.32.1, Pydantic v2.10.2, SQLAlchemy v2.0.36, Paho-MQTT v2.1.0, NumPy v2.1.3, SciPy v1.14.1, and InfluxDB-client v1.47.0.
- Frontend Runtime: Node.js v20.18.0 LTS and npm v10.8.2.
- Frontend Frameworks: React.js v18.3.1, Vite v5.4.11, Tailwind CSS v3.4.15, Chart.js v4.4.7, react-chartjs-2 v5.2.0, and Lucide React v0.460.0.
- Messaging & Database Services: Eclipse Mosquitto MQTT Broker v2.0.18, InfluxDB v2.7.10, and SQLite v3.45.1.
- Containerization: Docker Desktop v27.3.1 with Docker Compose v2.29.7."""
    },
    {
        "number": "4.7.2",
        "title": "Hardware Requirements",
        "content": """The physical hardware components, sensors, transducers, and experimental testbed apparatus comprise:
- Microcontroller Board: Espressif ESP32-S3-WROOM-1 DevKit (dual-core 240 MHz, 512 KB SRAM, 8 MB Flash, 2.4 GHz Wi-Fi).
- MEMS Inertial Sensor: InvenSense MPU6050 6-DoF IMU (tri-axial accelerometer +/-2g to +/-16g, tri-axial gyroscope +/-250 to +/-2000 deg/s, I2C digital interface).
- Digital Temperature Sensor: Maxim / Analog Devices DS18B20 digital thermal probe (TO-92 / stainless steel waterproof housing, -55 deg C to +125 deg C range, 1-Wire interface, 4.7 kOhm pull-up resistor).
- Electrical Current Transducer: Allegro MicroSystems ACS712-05B Hall-effect linear current sensor (galvanic isolation up to 2.1 kV RMS, +/-5A bidirectional range, 185 mV/A sensitivity, 5V supply).
- Energy Harvesting Transducer: Lead Zirconate Titanate (PZT) piezoelectric ceramic bender disk (27 mm diameter, brass substrate, resonant frequency ~4.6 kHz, capacitance ~22 nF).
- Experimental Machine: 12V DC brushed permanent-magnet electric motor (rated speed: 3000 RPM, rated current: 0.5A, stall current: 2.2A).
- DC Power Supply: Regulated variable benchtop DC power supply (0-30V, 0-5A) for motor excitation; 5V 2A USB power adapter for ESP32-S3 node.
- Signal Conditioning Components: 10 kOhm and 20 kOhm metal-film precision resistors (voltage divider), four 1N5819 Schottky barrier diodes (full-wave bridge rectifier), 10 uF 25V low-ESR electrolytic capacitor, and 1N4728A 3.3V 1W Zener diode."""
    },
    {
        "number": "4.8",
        "title": "Sensor Interfacing Design",
        "content": """Interfacing multimodal physical transducers to the ESP32-S3 microcontroller requires strict adherence to electrical specifications, bus timing constraints, and voltage level compatibility (Figure 4.6):

1. MPU6050 Inertial Measurement Unit (I2C Interfacing):
The MPU6050 operates from a 3.3V supply rail. Communication is established via the two-wire I2C serial bus:
- Serial Data (SDA): Connected to ESP32-S3 GPIO 8.
- Serial Clock (SCL): Connected to ESP32-S3 GPIO 9.
Both lines are pulled high to 3.3V via 4.7 kOhm pull-up resistors. The I2C hardware bus is initialized at 400 kHz (Fast Mode). The MPU6050 7-bit slave address is set to 0x68 (AD0 pin tied to GND).

2. DS18B20 Digital Temperature Sensor (1-Wire Interfacing):
The DS18B20 requires a single digital data line and ground return. It operates from the 3.3V rail:
- Data Pin (DQ): Connected to ESP32-S3 GPIO 4.
- A 4.7 kOhm pull-up resistor is placed between DQ and 3.3V to satisfy the open-drain 1-Wire bus timing specification. The sensor is configured in 12-bit resolution mode, providing a temperature resolution of 0.0625 deg C with a 750 ms conversion cycle.

3. ACS712-05B Current Sensor (Analog Signal Conditioning):
The ACS712 requires a 5V supply rail to bias its internal Hall-effect element and operational amplifier. In its quiescent state (zero current), the sensor outputs V_cc / 2 = 2.50 V. Under +/-5A current, its output swings from 1.575 V to 3.425 V (sensitivity S = 185 mV/A):
    V_out = 2.50 V + (I * 0.185 V/A)
Because the ESP32-S3 ADC maximum input voltage must not exceed 3.3V, directly connecting a 5V-powered sensor poses a risk of latch-up or ADC clipping. A precision passive resistive voltage divider is implemented:
    R1 = 10 kOhm, R2 = 20 kOhm
    Attenuation factor: alpha = R2 / (R1 + R2) = 20k / (10k + 20k) = 0.6667
The conditioned voltage fed to ESP32-S3 GPIO 1 (ADC1_CH0) becomes:
    V_ADC = V_out * 0.6667
At zero current, V_ADC = 2.50 V * 0.6667 = 1.667 V (perfectly centered within the 0 to 3.1 V linear ADC measurement range). At maximum +5A, V_out = 3.425 V, resulting in V_ADC = 2.283 V.

4. Piezoelectric Energy Harvesting Transducer (Rectification & Clamping):
The PZT piezoelectric disk generates an alternating current (AC) voltage under mechanical vibration strain. Connecting raw AC to a microcontroller ADC will cause negative voltage rail damage and erratic readings. A custom signal conditioning circuit is constructed:
- Full-Wave Bridge Rectifier: Four 1N5819 Schottky barrier diodes (forward voltage drop V_f ~ 0.25 V) rectify the AC waveform into pulsating DC.
- Reservoir Smoothing Capacitor: A 10 uF electrolytic capacitor smooths the pulsating DC into a steady voltage potential.
- Over-Voltage Protection Clamp: A 1N4728A 3.3V Zener diode is connected in parallel with the capacitor. If excessive mechanical shock induces voltage spikes exceeding 3.3V, the Zener diode breaks down into reverse conduction, safely shunting surge currents to ground and protecting ESP32-S3 GPIO 2 (ADC1_CH1)."""
    },
    {
        "number": "4.9",
        "title": "Communication Protocol Design",
        "content": """The communication design integrates two complementary networking protocols to ensure low-latency, deterministic telemetry transmission across all architectural boundaries (Figure 4.8):

1. Message Queuing Telemetry Transport (MQTT):
MQTT is utilized for edge-to-backend wireless telemetry over the local 2.4 GHz Wi-Fi network:
- Broker: Eclipse Mosquitto listening on TCP port 1883.
- Primary Telemetry Topic: industrial/mems/data
- Command & Control Topic: industrial/mems/config
- Quality of Service (QoS): Configured to QoS 0 for regular streaming (optimizing throughput) and QoS 1 for critical fault alert packets (guaranteeing at-least-once delivery with broker PUBACK).
- Payload Serialization: Compact JSON string format. An example telemetry payload is shown below:
{
  "node_id": "esp32s3_mems_01",
  "timestamp": 1732314560.125,
  "accel": {"x": 0.082, "y": -0.124, "z": 0.985},
  "gyro": {"x": 1.25, "y": -0.84, "z": 0.42},
  "temperature": 42.6,
  "current": 0.54,
  "piezo_voltage": 1.42,
  "vibration_rms": 1.85,
  "vibration_p2p": 0.48
}

2. Real-Time WebSockets (RFC 6455):
WebSockets are employed for full-duplex, low-latency communication between the FastAPI backend and browser clients:
- Endpoint: ws://localhost:8000/ws/sensors
- Handshake: Standard HTTP 101 Switching Protocols.
- Streaming Frequency: 5 Hz to 10 Hz pushed asynchronously by the backend ConnectionManager upon incoming MQTT packet arrival.
- Framing: Binary or UTF-8 JSON text frames. Eliminates HTTP polling overhead, delivering end-to-end sensor-to-dashboard latency under 50 milliseconds."""
    },
    {
        "number": "4.10",
        "title": "Database Schema Design",
        "content": """The relational database schema is implemented in SQLite 3 via SQLAlchemy ORM (Figure 4.7). The relational schema consists of four core tables:

1. machines Table:
- machine_id (VARCHAR(32), Primary Key): Unique alphanumeric machine identifier (e.g., "MTR-EXP-01").
- name (VARCHAR(64), NOT NULL): Descriptive asset name.
- model (VARCHAR(64)): Manufacturer model designation.
- rated_speed_rpm (INTEGER): Nominal operating speed in RPM (e.g., 3000).
- rated_current_a (FLOAT): Nominal full-load current in Amperes (e.g., 1.5).
- baseline_vibration_rms (FLOAT): Calibrated healthy baseline RMS velocity (e.g., 0.8 mm/s).
- status (VARCHAR(16), Default 'ONLINE'): Operational status ('ONLINE', 'OFFLINE', 'MAINTENANCE').
- created_at (TIMESTAMP): Record creation timestamp.

2. sensor_readings Table:
- id (INTEGER, Primary Key, Autoincrement): Unique record ID.
- machine_id (VARCHAR(32), Foreign Key -> machines.machine_id): Associated machine.
- timestamp (TIMESTAMP, Indexed): Sample acquisition timestamp.
- accel_x (FLOAT), accel_y (FLOAT), accel_z (FLOAT): Tri-axial acceleration in g.
- gyro_x (FLOAT), gyro_y (FLOAT), gyro_z (FLOAT): Tri-axial angular velocity in deg/s.
- temperature (FLOAT): Motor casing temperature in deg C.
- current (FLOAT): Motor load current in Amperes.
- piezo_voltage (FLOAT): Rectified piezoelectric harvesting voltage in Volts.
- vibration_rms (FLOAT): Computed RMS vibration velocity in mm/s.
- vibration_p2p (FLOAT): Peak-to-peak acceleration amplitude in g.
- health_score (INTEGER): Computed composite health index (0 to 100%).

3. fault_events Table:
- id (INTEGER, Primary Key, Autoincrement): Unique fault record ID.
- machine_id (VARCHAR(32), Foreign Key -> machines.machine_id): Associated machine.
- timestamp (TIMESTAMP, Indexed): Fault occurrence timestamp.
- severity (VARCHAR(16), NOT NULL): 'WARNING' or 'CRITICAL'.
- fault_type (VARCHAR(32), NOT NULL): 'VIBRATION_SEVERITY', 'OVERCURRENT', 'OVERHEAT', 'SENSOR_ERROR'.
- trigger_metric (VARCHAR(32)): Specific parameter triggering the alert.
- trigger_value (FLOAT): Recorded value during the fault event.
- threshold_value (FLOAT): Configured threshold limit that was breached.
- message (TEXT): Human-readable diagnostic message.
- acknowledged (BOOLEAN, Default FALSE): Operator acknowledgment flag.

4. energy_records Table:
- id (INTEGER, Primary Key, Autoincrement): Record ID.
- machine_id (VARCHAR(32), Foreign Key -> machines.machine_id): Associated machine.
- timestamp (TIMESTAMP, Indexed): Record timestamp.
- open_circuit_voltage (FLOAT): Measured peak open-circuit AC voltage.
- rectified_voltage (FLOAT): Measured smoothed DC capacitor voltage.
- storage_capacitance_uf (FLOAT): Nominal capacitance value (10.0 uF).
- energy_stored_uj (FLOAT): Calculated stored energy: E = 0.5 * C * V^2 in microjoules."""
    }
]

TABLE_4_1_DATA = {
    "title": "Table 4.1: ESP32-S3 Microcontroller Pin Assignment, Signal Conditioning, and Electrical Specifications",
    "headers": ["ESP32-S3 Pin", "Function / Role", "Connected Device", "Interface / Signal Type", "Voltage Level & Conditioning"],
    "rows": [
        ["GPIO 8", "I2C SDA (Data)", "MPU6050 IMU", "I2C Fast Mode (400 kHz)", "3.3V Logic (4.7 kOhm pull-up)"],
        ["GPIO 9", "I2C SCL (Clock)", "MPU6050 IMU", "I2C Fast Mode (400 kHz)", "3.3V Logic (4.7 kOhm pull-up)"],
        ["GPIO 4", "1-Wire DQ (Data)", "DS18B20 Temp Probe", "Dallas 1-Wire Digital", "3.3V Logic (4.7 kOhm pull-up)"],
        ["GPIO 1", "ADC1_CH0 (Analog)", "ACS712-05B Current", "Conditioned Analog Voltage", "0-3.3V (10k/20k divider from 5V)"],
        ["GPIO 2", "ADC1_CH1 (Analog)", "Piezo Transducer", "Conditioned DC Potential", "0-3.3V (Schottky bridge + 3.3V Zener)"],
        ["3V3 Pin", "System Power Out", "MPU6050, DS18B20", "Regulated DC Power Rail", "3.3V DC (+/-2% regulation, max 500 mA)"],
        ["5V / VBUS", "System Power In", "ACS712 Current Sensor", "Primary DC Power Rail", "5.0V DC from USB power source"],
        ["GND Pins", "Common Ground", "All Sensors & Motor PSU", "System Electrical Reference", "0V Common Ground Reference Plane"]
    ]
}
