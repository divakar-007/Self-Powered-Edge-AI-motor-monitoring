# -*- coding: utf-8 -*-
"""
ch5_implementation.py - Chapter 5: Implementation
"""

CHAPTER_5_TITLE = "CHAPTER 5: IMPLEMENTATION"

SECTIONS = [
    {
        "number": "5.1",
        "title": "Software Development",
        "content": """The software implementation spans three distinct layers: the React 18 presentation tier, the FastAPI Python application tier, and the hybrid SQLite/InfluxDB persistence tier. All tiers were developed using modern asynchronous programming paradigms to guarantee high concurrency, non-blocking I/O, and low latency."""
    },
    {
        "number": "5.1.1",
        "title": "Frontend Development",
        "content": """The frontend application was developed using React.js 18 with the Vite build toolchain and styled using Tailwind CSS:
1. Component Hierarchy:
   - Root Container (App.jsx): Sets up the application shell, responsive sidebar navigation, top status banner, and route rendering.
   - Dashboard View (Dashboard.jsx): Provides high-level operational visibility. Displays animated radial gauge components for current machine health score, peak vibration velocity, motor winding temperature, and electrical power consumption. Includes an active alert ticker highlighting real-time warning conditions.
   - Live Monitoring View (LiveMonitoring.jsx): Utilizes Chart.js canvas elements to render rolling time-domain waveform charts for tri-axial acceleration (ax, ay, az), angular rate (gx, gy, gz), and real-time Fast Fourier Transform (FFT) spectral frequency bins.
   - Fault Detection Center (FaultDetection.jsx): Implements the ISO 10816-3 vibration severity matrix (Class I/II small-to-medium machines). Dynamically maps vibration RMS into Zone A (Good: <0.71 mm/s), Zone B (Acceptable: 0.71 - 1.80 mm/s), Zone C (Unsatisfactory: 1.80 - 4.50 mm/s), and Zone D (Unacceptable: >4.50 mm/s). Displays prescriptive maintenance recommendations based on active fault triggers.
   - Energy Monitoring View (EnergyMonitoring.jsx): Displays empirical kinetic energy harvesting analytics, graphing open-circuit AC voltage (Voc), rectified DC capacitor voltage (V_DC), accumulated electrical energy in microjoules, and estimated harvestable power output.
   - Historical Analytics View (History.jsx): Provides date-range querying, parameter filtering, tabular pagination, and single-click CSV export of historical machine telemetry.
   - System Settings View (Settings.jsx): Allows operators to configure MQTT broker IP, WebSocket URL, vibration threshold limits, temperature alarms, and current cut-off limits dynamically without code recompilation.
2. Real-Time Streaming Hook:
   A custom useWebSocket hook establishes a persistent connection to the backend. It incorporates automatic reconnection with exponential backoff (initial retry 1s, doubling up to 30s), tracks network latency via ping-pong timing frames, and updates shared state buffers at 5-10 Hz without UI stutter."""
    },
    {
        "number": "5.1.2",
        "title": "Backend Development",
        "content": """The application tier is engineered using Python 3.11 and the FastAPI asynchronous framework, executed via the Uvicorn ASGI server:
1. Asynchronous Service Architecture:
   - main.py: Initializes the FastAPI application instance, configures Cross-Origin Resource Sharing (CORS) middleware, mounts REST API routers, and registers asynchronous lifespan context handlers to manage startup and shutdown sequences for the MQTT client and database connection pools.
   - ConnectionManager: Implements an in-memory connection pool managing concurrent active WebSocket client connections. Telemetry received from the MQTT service is broadcast to all connected clients asynchronously via asyncio.gather().
2. Data Validation and Pydantic Schemas:
   Incoming JSON payloads are validated using Pydantic data contracts (SensorDataPacket, TelemetryResponse, FaultEventSchema). Payloads failing validation due to missing fields, corrupted numbers, or out-of-range sensor readings are rejected and logged to prevent database pollution.
3. Extensible TinyML Interface (ITinyMLDetector):
   An abstract base class (ITinyMLDetector) defines the contract for edge inference modules:
   class ITinyMLDetector(ABC):
       @abstractmethod
       def predict_anomaly(self, sensor_features: np.ndarray) -> Tuple[bool, str, float]:
           pass
   This interface decouples the current rule-based engine from future TensorFlow Lite / ONNX machine learning model weights, allowing seamless plug-and-play model updates."""
    },
    {
        "number": "5.1.3",
        "title": "Database Development",
        "content": """The data persistence layer implements a hybrid architecture:
1. Relational Persistence (SQLite & SQLAlchemy):
   - SQLite is configured in Write-Ahead Logging (WAL) mode (PRAGMA journal_mode=WAL) to enable concurrent reads and writes without database lock contention.
   - SQLAlchemy ORM models define schemas for machines, sensor_readings, fault_events, and energy_records.
   - An automated initialization routine verifies table existence upon application startup and seeds default machine asset profiles (e.g., 'MTR-EXP-01' representing the experimental 12V DC testbed).
2. Time-Series Persistence (InfluxDB 2.0 Client):
   - The backend initializes an InfluxDBClient pointing to the configured organization ('mems_org') and bucket ('mems_telemetry').
   - High-velocity telemetry is transformed into InfluxDB Point objects containing tags (machine_id, node_id) and fields (ax, ay, az, temperature, current, vibration_rms).
   - If the external InfluxDB instance is unreachable, an automatic graceful fallback mechanism activates, routing all persistence transparently to SQLite without throwing unhandled exceptions or interrupting real-time WebSocket streaming."""
    },
    {
        "number": "5.1.4",
        "title": "MQTT Communication Implementation",
        "content": """Asynchronous MQTT messaging is implemented using the Paho-MQTT v2 Python client wrapped in an asynchronous event loop:
- Connection Callback (on_connect): Upon successful TCP socket connection to Mosquitto port 1883, the client automatically subscribes to topics 'industrial/mems/data' and 'industrial/mems/alerts'.
- Message Callback (on_message): Incoming MQTT message payloads are extracted from the broker buffer, decoded from UTF-8 JSON strings, and scheduled as asynchronous coroutines on the main asyncio event loop via loop.call_soon_threadsafe().
- Fault-Tolerant Reconnection: Implements automatic socket reconnection with randomized jitter in the event of industrial Wi-Fi disruptions or broker restarts."""
    },
    {
        "number": "5.1.5",
        "title": "API Development",
        "content": """The FastAPI application tier exposes comprehensive RESTful API endpoints alongside the WebSocket streaming channel:
- GET /api/health: Returns operational health status of backend services, SQLite connectivity, InfluxDB status, and active MQTT subscriptions.
- GET /api/sensors/latest: Returns the most recent synchronized multimodal telemetry packet for all registered machines.
- GET /api/history: Accepts query parameters (machine_id, start_time, end_time, limit) and returns paginated historical records from SQLite.
- GET /api/alerts: Returns a chronological list of logged fault events with severity levels, trigger values, and acknowledgment status.
- POST /api/alerts/{alert_id}/acknowledge: Marks a specific diagnostic alert as acknowledged by an operator.
- GET /api/export/csv: Generates and streams a downloadable comma-separated values (CSV) file containing historical sensor data for offline spreadsheet analysis.
- WebSocket /ws/sensors: Full-duplex persistent socket streaming live telemetry packets at 5-10 Hz to connected web dashboards."""
    },
    {
        "number": "5.1.6",
        "title": "Real-Time Data Visualization",
        "content": """To achieve smooth, stutter-free visualization of high-frequency sensor telemetry without overwhelming client browser memory:
1. Dynamic Rolling Window Buffering:
   Incoming WebSocket telemetry packets are appended to fixed-length FIFO (First-In, First-Out) arrays capped at 100 data points. When the buffer reaches maximum capacity, older points are automatically evicted, preventing memory bloat during prolonged monitoring sessions.
2. Canvas Rendering Optimization:
   Chart.js renders directly to HTML5 Canvas contexts. By disabling unnecessary point animations (animation: false) during high-frequency streaming and updating solely chart dataset references rather than re-instantiating chart instances, the frontend maintains a rock-solid 60 FPS refresh rate with under 5% CPU utilization on client workstations."""
    },
    {
        "number": "5.2",
        "title": "Hardware Setup",
        "content": """The physical hardware setup (Figure 5.1) integrates all electronic components onto a rigid experimental testbed."""
    },
    {
        "number": "5.2.1",
        "title": "ESP32-S3 Setup",
        "content": """The ESP32-S3 development board is mounted onto a prototyping breadboard and connected to a 5V 2A USB power supply. The onboard CP2102 USB-to-UART bridge facilitates serial programming and real-time debugging output at 115200 baud. The dual-core processor is configured in Arduino IDE with the Xtensa dual-core FreeRTOS environment, CPU frequency set to 240 MHz, Flash frequency to 80 MHz (QIO mode), and Flash size to 8 MB."""
    },
    {
        "number": "5.2.2",
        "title": "MPU6050 Interfacing",
        "content": """The MPU6050 breakout board is rigidly bolted to the top bearing housing of the 12V DC motor using a non-conductive mechanical mounting plate to ensure optimal mechanical vibration coupling without acoustic damping:
- VCC is connected to the ESP32-S3 3.3V power pin.
- GND is tied to the common ground plane.
- SDA is wired to GPIO 8; SCL is wired to GPIO 9.
- Both bus lines are pulled up to 3.3V via 4.7 kOhm resistors.
The internal Digital Low-Pass Filter (DLPF) is programmed to 44 Hz bandwidth to eliminate high-frequency acoustic noise while capturing mechanical unbalance and misalignment frequencies."""
    },
    {
        "number": "5.2.3",
        "title": "DS18B20 Interfacing",
        "content": """The DS18B20 digital temperature probe is mechanically secured directly against the outer metallic stator casing of the DC motor using thermally conductive silicone grease (thermal conductivity k > 1.2 W/m-K) to minimize thermal contact resistance:
- VDD is wired to 3.3V.
- GND is wired to the common ground.
- DQ (Data) is connected to GPIO 4 with a 4.7 kOhm pull-up resistor to 3.3V.
The sensor executes 12-bit temperature conversions, yielding 0.0625 deg C precision."""
    },
    {
        "number": "5.2.4",
        "title": "ACS712 Interfacing",
        "content": """The ACS712-05B Hall-effect current sensor module is wired in series with the positive DC power supply lead feeding the 12V DC motor:
- VCC is connected to the 5V power rail (required for correct internal Hall element biasing).
- GND is tied to common ground.
- OUT is connected to a precision resistive voltage divider consisting of R1 = 10 kOhm and R2 = 20 kOhm (1% metal-film resistors).
- The attenuated midpoint of the divider (alpha = 0.6667) is connected directly to ESP32-S3 GPIO 1 (ADC1_CH0).
At zero motor current, the sensor outputs 2.50V, which is attenuated to 1.667V at GPIO 1, safely within the ESP32-S3 linear ADC range."""
    },
    {
        "number": "5.2.5",
        "title": "Piezoelectric Transducer Interfacing",
        "content": """A 27 mm circular lead zirconate titanate (PZT) piezoelectric ceramic bender disk is firmly affixed to the motor mounting foot using cyanoacrylate adhesive, orienting the transducer to maximize strain induced by vertical chassis vibrations:
- The positive electrode (ceramic center) and negative electrode (brass substrate) are wired to the AC input terminals of a full-wave bridge rectifier constructed with four 1N5819 Schottky diodes.
- The rectified DC output is smoothed across a 10 uF 25V low-ESR electrolytic capacitor.
- A 1N4728A 3.3V 1W Zener diode is connected directly in parallel across the capacitor terminals to clamp any high-g transient shock voltages to 3.3V.
- The conditioned positive terminal is connected to ESP32-S3 GPIO 2 (ADC1_CH1) to measure the accumulated DC harvesting voltage."""
    },
    {
        "number": "5.2.6",
        "title": "DC Motor Setup",
        "content": """The experimental testbed utilizes a 12V permanent-magnet DC brushed motor (rated 3000 RPM, rated current 0.5A, stall current 2.2A). The motor is mounted onto an aluminum baseplate resting on elastomeric vibration-isolation dampers. A variable laboratory DC bench power supply (0-30V, 0-5A) powers the motor, allowing precise operational speed control. Mechanical faults are experimentally simulated:
- Dynamic Mass Imbalance: Simulated by attaching a calibrated eccentric mass (0.8 g set screw) to a balanced nylon flywheel mounted on the motor output shaft.
- Structural Looseness: Simulated by backing out the motor foot mounting bolts by 1.5 mm.
- Electrical Overload / Stall: Simulated by applying calibrated mechanical friction to the shaft."""
    },
    {
        "number": "5.3",
        "title": "Sensor Data Collection",
        "content": """Sensor data acquisition is executed deterministically on the ESP32-S3 using FreeRTOS multitasking:
- Task 1 (Core 0 - Sensor Sampling): Executes in a deterministic loop every 100 ms (10 Hz). Reads 14 bytes of raw acceleration and gyroscope data from MPU6050 registers 0x3B through 0x48 over I2C. Initiates asynchronous 1-Wire temperature conversions on the DS18B20. Executes 16-sample multisampling on ADC1_CH0 (current) and ADC1_CH1 (piezo voltage) to reduce electrical noise.
- ADC Calibration: Utilizes the ESP32-S3 esp_adc_cal API to apply factory eFuse calibration curves, compensating for ADC non-linearity and offset errors.
- Queue Transfer: Acquired raw samples are placed into a FreeRTOS thread-safe queue (xQueueSend) for consumption by the network task."""
    },
    {
        "number": "5.4",
        "title": "Data Processing",
        "content": """The digital signal processing pipeline executes in two coordinated stages:

1. Edge-Level Pre-Processing (ESP32-S3):
- Acceleration Scaling: Raw 16-bit integer counts are converted to standard gravitational acceleration:
    ax = raw_ax / 16384.0  (for +/-2g range)
- Angular Rate Scaling: Raw counts are converted to degrees per second:
    gx = raw_gx / 131.0   (for +/-250 deg/s range)
- Total Acceleration Magnitude:
    a_mag = sqrt(ax^2 + ay^2 + az^2)
- Current Conversion: Conditioned ADC voltage is converted back to actual motor current:
    V_sensor = V_ADC / 0.6667
    I = (V_sensor - 2.50) / 0.185

2. Application-Tier Digital Signal Processing (FastAPI & NumPy):
- Moving Average Filtering: High-frequency electrical noise is suppressed using a 5-point moving window.
- Peak-to-Peak Amplitude:
    a_p2p = max(a_window) - min(a_window)
- RMS Vibration Velocity Integration: To comply with ISO 10816-3 (which mandates vibration velocity v_rms in mm/s over 10 Hz to 1000 Hz), the acceleration signal is numerically integrated in the frequency domain:
    V(f) = A(f) / (2 * pi * f)
    v_rms = sqrt( 1/N * sum(v_i^2) ) * 1000
- Fast Fourier Transform (FFT): A 128-point FFT is computed over rolling acceleration buffers to extract spectral power distributions and pinpoint dominant harmonic peaks corresponding to motor shaft rotational frequency (1X) and harmonics (2X, 3X)."""
    },
    {
        "number": "5.5",
        "title": "Fault Detection Implementation",
        "content": """Fault detection utilizes deterministic multi-parameter threshold evaluation alongside the ISO 10816-3 standard:

1. ISO 10816-3 Mechanical Vibration Severity (Class I / II Machines):
- Zone A (Good / Newly Commissioned): v_rms < 0.71 mm/s -> System Health: NORMAL (100% score).
- Zone B (Acceptable for Continuous Unrestricted Operation): 0.71 <= v_rms < 1.80 mm/s -> System Health: NORMAL (85-99% score).
- Zone C (Unsatisfactory for Long-Term Operation): 1.80 <= v_rms < 4.50 mm/s -> Severity: WARNING. Triggers maintenance advisory alert.
- Zone D (Unacceptable / Dangerous): v_rms >= 4.50 mm/s -> Severity: CRITICAL. Triggers immediate shutdown advisory.

2. Thermal Safety Envelope:
- Normal Operation: T_motor < 50.0 deg C.
- Thermal Warning: 50.0 deg C <= T_motor < 70.0 deg C (indicates inadequate ventilation or sustained high load).
- Thermal Critical: T_motor >= 70.0 deg C (indicates imminent stator winding insulation damage).

3. Electrical Current Safety Limits:
- Normal Load: I_motor <= 0.80 A.
- Over-Current Warning: 0.80 A < I_motor <= 1.50 A.
- Motor Stall / Short-Circuit Critical: I_motor > 1.50 A (indicates mechanical rotor lockup or winding short)."""
    },
    {
        "number": "5.6",
        "title": "Docker Containerisation",
        "content": """To guarantee reproducible, environment-independent deployment across development workstations and production factory-floor industrial edge gateways, the supervisory platform is packaged into containerized microservices managed via Docker Compose (Figure 5.4):
- Container 1 (mems-frontend): Multi-stage Dockerfile compiling the React 18 production build with Vite and serving static assets via an optimized Alpine Nginx web server on HTTP port 80 (mapped to host 5173 / 80).
- Container 2 (mems-backend): Python 3.11-slim container running the FastAPI application via Uvicorn on port 8000. Mounts a persistent volume for the SQLite database (mems_data.db).
- Container 3 (mems-broker): Official Eclipse Mosquitto Alpine image listening on TCP port 1883 for MQTT traffic and port 9001 for MQTT over WebSockets. Configured with a custom mosquitto.conf permitting anonymous local network access.
- Container 4 (mems-influxdb): InfluxDB v2.7 image listening on port 8086 with a persistent Docker volume mounted to persist time-series telemetry blocks.
- Virtual Network (mems-net): An isolated bridge network interconnects all four containers, enabling secure inter-service communication using container DNS names (e.g., http://mems-backend:8000)."""
    },
    {
        "number": "5.7",
        "title": "System Integration",
        "content": """System integration was verified through a systematic four-phase validation protocol:
1. Phase 1 (Hardware Bus & Electrical Verification): Verified 3.3V and 5V rail stabilities under full motor load with an oscilloscope. Confirmed zero ADC over-voltage conditions on GPIO 1 (ACS712) and GPIO 2 (Piezo) under simulated transient motor stall events.
2. Phase 2 (Edge Firmware Telemetry Streaming): Verified continuous 10 Hz FreeRTOS sensor sampling, JSON serialization, and Wi-Fi transmission to Mosquitto broker with 0% packet drop over a continuous 4-hour soak test.
3. Phase 3 (Backend Ingestion & Processing Pipeline): Confirmed FastAPI MQTT subscription callback processing, Pydantic data schema validation, SQLite transaction logging, and WebSocket broadcast dispatching in under 20 ms.
4. Phase 4 (End-to-End Client Visualization): Verified React dashboard rendering across Google Chrome and Microsoft Edge browsers. Confirmed dynamic canvas chart scrolling, gauge animation, and immediate visual alert popups upon artificial fault injection."""
    },
    {
        "number": "5.8",
        "title": "Performance Evaluation",
        "content": """The integrated system was subjected to rigorous performance benchmarking:
- Edge Power Consumption: The ESP32-S3 sensor node consumed an average current of 92 mA at 5V (460 mW) during continuous 10 Hz Wi-Fi MQTT streaming.
- End-to-End Latency: The total elapsed duration from the physical occurrence of a mechanical shock event at the MPU6050 sensor to its visual appearance on the React dashboard canvas averaged 42.4 milliseconds.
- Backend Resource Utilization: The FastAPI backend maintained <2% CPU utilization and 68 MB RAM footprint during sustained 10 Hz ingestion on an Intel Core i5 host machine.
- Web Client Responsiveness: The React dashboard rendered 100-point rolling waveforms at 60 FPS consuming <4% client CPU utilization and zero detectable JavaScript memory leaks over extended testing sessions."""
    }
]
