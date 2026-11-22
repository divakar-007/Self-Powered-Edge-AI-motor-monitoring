# -*- coding: utf-8 -*-
"""
ch3_methodology.py - Chapter 3: Problem Definition and Methodology
"""

CHAPTER_3_TITLE = "CHAPTER 3: PROBLEM DEFINITION AND METHODOLOGY"

SECTIONS = [
    {
        "number": "3.1",
        "title": "Problem Definition",
        "content": """Industrial manufacturing facilities, process plants, and automated assembly operations rely extensively on rotating machinery—primarily electric motors, centrifugal pumps, industrial fans, and gearboxes—as fundamental prime movers. The mechanical and electrical reliability of these electro-mechanical actuators directly determines plant operational throughput, product quality, and workplace safety.

Under normal industrial operations, these machines are subjected to severe operational stresses including dynamic mechanical vibration, cyclic thermal expansion, electrical harmonic distortion, and environmental particulate contamination. Over time, these operational stresses inevitably induce progressive mechanical degradation, such as:
1. Dynamic shaft unbalance resulting from uneven mass distribution.
2. Angular or parallel shaft misalignment across flexible couplings.
3. Bearing raceway micro-spalling, ball element fatigue, and lubricant breakdown.
4. Stator winding insulation thermal degradation leading to inter-turn short circuits.
5. Rotor bar fractures and electrical over-current stall conditions.

Without continuous, automated diagnostic monitoring, these progressive defects escalate into catastrophic sudden failures. The problem addressed by this engineering project is the lack of an autonomous, low-cost, multimodal condition monitoring system that can simultaneously capture high-bandwidth vibration, temperature, current, and energy harvesting metrics, process them at the edge, transmit telemetry reliably over wireless industrial channels, and present real-time actionable diagnostic guidance to plant engineers through an enterprise-grade supervisory architecture."""
    },
    {
        "number": "3.2",
        "title": "Existing System",
        "content": """In contemporary industrial facilities, condition monitoring is predominantly executed via two divergent paradigms:

1. Manual Route-Based Periodic Vibration Data Logging:
In this conventional approach, certified maintenance technicians carry portable, handheld vibration meters and infrared thermal guns through the factory floor on a scheduled periodic basis (e.g., once every two weeks or once a month). The technician manually presses a handheld accelerometer probe against designated motor bearing test points, records peak vibration amplitudes in a handheld logger, and manually logs values into a maintenance spreadsheet. 

2. Centralized Hardwired SCADA Systems:
In critical infrastructure installations (such as power generation turbines or high-capacity petrochemical compressors), permanent monitoring is accomplished via legacy Supervisory Control and Data Acquisition (SCADA) systems. Heavy industrial-grade piezoelectric accelerometers (typically 100 mV/g ICP/IEPE sensors) and resistance temperature detectors (Pt100 RTDs) are hardwired via shielded, armored twisted-pair cabling directly to centralized Programmable Logic Controller (PLC) input racks and rack-mounted monitoring modules (e.g., Bentley Nevada 3500 series)."""
    },
    {
        "number": "3.3",
        "title": "Limitations of the Existing System",
        "content": """Both existing paradigms exhibit severe technical, operational, and financial limitations:

Limitations of Route-Based Manual Monitoring:
- Temporal Monitoring Blind Spots: Inspections occur at discrete, widely spaced intervals. Incipient mechanical faults—such as sudden lubricant starvation, bearing cage fracture, or foreign object obstruction—can develop, escalate, and cause catastrophic machine breakdown entirely between inspection intervals.
- High Recurring Labor Cost: Deploying skilled vibration analysts across hundreds of distributed factory assets requires substantial continuous labor expenditures.
- Measurement Inconsistency and Operator Error: Handheld probe readings are highly sensitive to probe contact angle, applied hand pressure, and exact probe placement on the motor housing, leading to poor repeatability and false trend alarms.
- Hazardous Exposure: Manual inspection requires personnel to place handheld instruments directly onto operating, high-voltage rotating machinery in noisy, hot, and chemically hazardous environments.

Limitations of Hardwired SCADA Systems:
- Prohibitive Installation Cost: Running armored instrumentation cabling through industrial conduits, cable trays, and explosion-proof penetrations frequently costs between $100 and $300 per linear meter. In sprawling industrial complexes, installation costs often exceed sensor hardware costs by a factor of ten.
- Cable Fragility and Maintenance Overhead: Physical cables running through factory floors are highly susceptible to mechanical severing by forklifts, thermal degradation from adjacent steam pipes, and electromagnetic interference (EMI) induced by large variable-frequency drives (VFDs).
- Lack of Scalability: Adding a new monitoring point requires running additional physical copper lines back to the centralized PLC cabinet, consuming finite analog input channels.
- Proprietary Lock-In and High Capital Expenditure: Enterprise rack systems require expensive proprietary software licenses and specialized hardware modules, making broad deployment across auxiliary balance-of-plant motors economically unfeasible."""
    },
    {
        "number": "3.4",
        "title": "Proposed System",
        "content": """To decisively overcome the limitations of both manual inspection routes and expensive hardwired SCADA systems, this project proposes an intelligent, multimodal, edge-computed, three-tier condition monitoring architecture.

The proposed system deploys an autonomous, compact hardware sensor node permanently attached to the monitored motor chassis. The node incorporates:
1. MPU6050 6-DoF MEMS Inertial Measurement Unit: Directly measures high-frequency structural vibration along three orthogonal axes (X, Y, Z) and angular velocity to detect mechanical imbalance, misalignment, and structural looseness.
2. DS18B20 Digital Temperature Sensor: Mechanically coupled to the motor stator casing to continuously track thermal escalation with 0.0625 deg C digital resolution, eliminating analog noise interference.
3. ACS712-05B Hall-Effect Current Sensor: Conditioned to interface with the microcontroller ADC, capturing instantaneous motor current signatures to detect electrical overloads, phase anomalies, and mechanical stall events.
4. Piezoelectric Energy Harvesting Transducer: Affixed to the motor mounting foot to investigate the conversion of parasitic chassis mechanical vibration into harvestable electrical potential.
5. ESP32-S3 Microcontroller Edge Core: Executes high-speed sampling, FreeRTOS dual-core multitasking, local digital filtering, JSON serialization, and wireless MQTT transmission.
6. Decoupled Three-Tier Supervisory Architecture: Telemetry is ingested by an asynchronous FastAPI backend (Tier 2), persisted into a hybrid SQLite / InfluxDB database layer (Tier 3), and rendered dynamically through an interactive React.js single-page application (Tier 1) delivering real-time charts, ISO 10816-3 diagnostics, and prescriptive maintenance alerts."""
    },
    {
        "number": "3.5",
        "title": "Advantages of the Proposed System",
        "content": """The proposed architecture offers several distinct technical and operational advantages over existing solutions:
1. Continuous 24/7 Unattended Telemetry: Eliminates temporal blind spots by continuously acquiring and evaluating sensor data at frequencies up to 10 Hz, catching rapid degradation events in real time.
2. Low-Cost and Readily Scalable: Built using commercial-off-the-shelf (COTS) MEMS sensors and open-source software frameworks, reducing per-node capital expenditure by over 90% compared to proprietary industrial rack systems.
3. Zero-Cable Wireless Topology: Sensor nodes communicate over Wi-Fi via lightweight MQTT messaging, completely eliminating costly physical conduit runs and fragile industrial wiring.
4. Multimodal Cross-Parameter Correlation: Correlating vibration, casing temperature, and motor current simultaneously enables high-accuracy diagnostic discrimination between mechanical defects (high vibration, normal current) and electrical overload/stalls (extreme current, thermal rise).
5. Standardized ISO 10816 Diagnostic Compliance: Automated mathematical computation of RMS vibration velocity and real-time classification against internationally accepted vibration severity guidelines removes subjective human interpretation.
6. Energy Harvesting Investigation: Provides experimental data and theoretical models on kinetic energy recovery, establishing the blueprint for fully self-powered perpetual sensor nodes.
7. Modular Three-Tier Enterprise Design: Decoupled presentation, application, and database tiers ensure horizontal scalability, containerized Docker deployment, and high operational uptime."""
    },
    {
        "number": "3.6",
        "title": "Methodology",
        "content": """The project was executed through a rigorous six-stage engineering methodology:

Stage 1: System Requirements and Mathematical Modeling
Define functional requirements, operational envelopes (voltage, current, vibration limits), and mathematical relationships governing mechanical vibration RMS velocity (ISO 10816), Hall-effect current transduction, and piezoelectric electromechanical charge generation.

Stage 2: Hardware Interfacing and Signal Conditioning Design
Design and fabricate custom signal conditioning circuits: a resistive voltage divider for the ACS712 5V-to-3.3V analog level translation, and a full-wave Schottky bridge rectifier (1N5819) with reservoir smoothing capacitor (10 uF) and 3.3V Zener diode (1N4728A) over-voltage clamp for the piezoelectric transducer.

Stage 3: Embedded Firmware Development (ESP32-S3)
Develop modular C++ firmware under the Arduino-ESP32 platform utilizing FreeRTOS dual-core execution. Task 1 (pinned to Core 0) executes I2C MPU6050 acquisition, 1-Wire DS18B20 temperature reads, and calibrated ADC conversions. Task 2 (pinned to Core 1) manages network connectivity, JSON serialization, and asynchronous MQTT publishing to the Eclipse Mosquitto broker.

Stage 4: Application Tier and Digital Signal Processing (FastAPI)
Develop an asynchronous Python ASGI backend using FastAPI and Uvicorn. Implement an asynchronous MQTT subscriber client (paho-mqtt), a digital signal processing pipeline (NumPy FFT, peak-to-peak, and RMS integration), multi-parameter threshold evaluation, and a bidirectional WebSocket broadcaster (/ws/sensors) to distribute telemetry with sub-50 ms latency.

Stage 5: Data Tier Persistence and Storage Architecture
Configure a hybrid persistence layer: SQLite via SQLAlchemy ORM for relational machine configurations, alert history, and audit logging; InfluxDB time-series engine for high-volume high-resolution sensor metrics storage.

Stage 6: Frontend Development and System Integration (React.js)
Build a responsive single-page web dashboard using React 18, Vite, and Tailwind CSS. Implement interactive Chart.js canvas visualizations across six specialized views: Executive Dashboard, Live Monitoring, ISO Fault Diagnostics, Energy Harvesting Analytics, Historical Analytics, and System Settings. Validate the entire integrated stack on an instrumented 12V DC motor testbed."""
    },
    {
        "number": "3.7",
        "title": "System Architecture",
        "content": """The overall system architecture bridges the physical machine environment with enterprise web supervisory monitoring through five interconnected subsystems:

1. Physical Testbed and Multimodal Sensor Cluster: The 12V DC experimental motor mounted on an isolated aluminum baseplate, equipped with the MPU6050 IMU, DS18B20 thermal sensor, ACS712 current transducer, and PZT piezoelectric harvester.
2. Edge Processing Controller (ESP32-S3): Dual-core Xtensa LX7 SoC performing hardware interfacing, synchronous sensor sampling, digital filtering, and Wi-Fi transmission.
3. Industrial Message Broker (Eclipse Mosquitto): Lightweight MQTT messaging hub managing asynchronous publish-subscribe message routing over standard TCP/IP port 1883.
4. Application Processing Tier (FastAPI Backend): High-performance Python ASGI application executing DSP spectral feature extraction, rule-based ISO fault classification, database persistence, and WebSocket broadcasting.
5. Supervisory Web Presentation Tier (React.js Dashboard): Browser-based operator interface delivering real-time streaming charts, tabular diagnostic notifications, historical data queries, and system configuration controls."""
    },
    {
        "number": "3.8",
        "title": "Working Principle",
        "content": """The end-to-end working principle of the proposed system encompasses a seven-stage continuous data telemetry and diagnostic pipeline:

Stage 1: Sensor Data Collection
The MPU6050 acquires tri-axial acceleration (ax, ay, az in g-force) and tri-axial angular velocity (gx, gy, gz in deg/s) via the I2C bus at 400 kHz clock frequency. The DS18B20 acquires motor chassis temperature in degrees Celsius via the Dallas 1-Wire digital bus. The ACS712 outputs an analog voltage proportional to the motor DC supply current, which is conditioned and sampled by the ESP32-S3 12-bit ADC. The piezoelectric transducer generates an AC voltage proportional to chassis vibration strain, which is rectified, filtered, and sampled by a secondary ADC channel.

Stage 2: ESP32-S3 On-Chip Processing and Packetization
The ESP32-S3 Core 0 applies calibrated scale factors to convert raw register counts into standard engineering units. The firmware computes the total acceleration magnitude vector:
    a_mag = sqrt(ax^2 + ay^2 + az^2)
Sensor readings are packed into a compact, standardized JSON payload string containing node ID, timestamp, and all physical sensor measurements.

Stage 3: MQTT Asynchronous Wireless Communication
The ESP32-S3 Core 1 publishes the serialized JSON packet over local 2.4 GHz Wi-Fi to the MQTT topic "industrial/mems/data" with Quality of Service QoS 0/1. The Eclipse Mosquitto broker validates the packet and instantly dispatches it to all subscribed application services.

Stage 4: FastAPI Backend Ingestion and DSP Pipeline
The FastAPI backend maintains a persistent asynchronous MQTT client. Upon packet arrival:
- The JSON payload is validated against strict Pydantic data schemas.
- The DSP engine computes peak-to-peak acceleration and performs numerical integration to derive Root-Mean-Square (RMS) vibration velocity in mm/s.
- Fast Fourier Transform (FFT) algorithms compute the frequency spectrum to identify dominant vibration harmonics.

Stage 5: Database Persistence
The backend persists the validated telemetry:
- Tabular records containing machine status, fault state, and alert logs are written to SQLite relational tables (sensor_readings, fault_events).
- Simultaneously, metric points are written to InfluxDB buckets for long-term time-series trending.

Stage 6: Real-Time WebSocket Broadcasting
The FastAPI WebSocket ConnectionManager immediately pushes the enriched telemetry packet across active WebSocket channels (/ws/sensors) to all connected web clients in under 10 milliseconds.

Stage 7: Frontend Visualization and Prescriptive Maintenance
The React.js single-page application receives the WebSocket stream, pushes new data points into dynamic rolling Chart.js buffers, updates animated gauge displays, and evaluates current metrics against ISO 10816-3 thresholds. If vibration or temperature exceeds safe limits, the dashboard flashes visual warnings, logs the fault event, and displays prescriptive corrective maintenance actions for plant operators."""
    }
]
