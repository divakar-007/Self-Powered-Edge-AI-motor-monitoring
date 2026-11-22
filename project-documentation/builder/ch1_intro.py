# -*- coding: utf-8 -*-
"""
ch1_intro.py - Chapter 1: Introduction
"""

CHAPTER_1_TITLE = "CHAPTER 1: INTRODUCTION"

SECTIONS = [
    {
        "number": "1.1",
        "title": "Introduction",
        "content": """The rapid emergence of the fourth industrial revolution (Industry 4.0) has transformed conventional manufacturing facilities into highly connected, data-intensive cyber-physical ecosystems. At the core of contemporary industrial manufacturing plants, rotating machinery—specifically direct current (DC) motors, alternating current (AC) induction motors, centrifugal pumps, compressors, and gear transmissions—acts as the primary mechanical prime mover. The operational integrity, energy efficiency, and reliability of these electromechanical actuators dictate the continuous throughput of automated assembly lines, continuous processing refineries, and robotic workstations. 

However, rotating machines operate under relentless mechanical, electrical, thermal, and ambient stresses. Friction, shaft misalignment, mechanical imbalance, bearing raceway fatigue, rotor eccentricity, electrical winding degradation, and transient voltage surges induce gradual wear that, if left undetected, escalates into sudden, catastrophic equipment failure. Unscheduled downtime in heavy manufacturing facilities incurs severe economic ramifications, with industrial survey data indicating that equipment breakdown costs range from thousands to hundreds of thousands of dollars per hour, alongside hazardous safety conditions for plant personnel.

Consequently, modern plant management paradigms have systematically migrated away from reactive "run-to-failure" maintenance and static preventive "time-based" maintenance toward condition-based maintenance (CBM) and predictive maintenance (PdM). Condition-based maintenance leverages multimodal sensor transducers to continuously track physical parameters that signify mechanical health—predominantly structural vibration, surface temperature, and electrical load current. By analyzing deviations from normal operational baselines in real time, maintenance engineers can accurately identify early-stage anomalies, schedule corrective interventions prior to catastrophic breakdown, extend physical asset longevity, and optimize maintenance inventory logistics."""
    },
    {
        "number": "1.1.1",
        "title": "Overview of Industrial 4.0 & Predictive Maintenance",
        "content": """Traditional industrial maintenance strategies fall into three primary historical epochs:
1. Reactive Maintenance (Run-to-Failure): In this paradigm, machinery is operated continuously without intervention until functional failure occurs. While this strategy minimizes routine maintenance labor during healthy operation, the resulting breakdown is frequently catastrophic, leading to severe collateral damage across connected drive mechanisms, exorbitant emergency repair expenses, and extensive production stoppages.
2. Preventive Maintenance (Time-Based / Calendar-Based): In preventive maintenance, equipment is inspected, lubricated, or overhauled at predetermined operating hour intervals (e.g., every 500 operating hours or every 6 months), regardless of actual physical health. While this mitigates sudden catastrophic breakdowns, it introduces substantial operational inefficiencies: healthy components are prematurely discarded, maintenance labor is expended unnecessarily, and unexpected early-life failures (infant mortality) or rapid degradation events occurring between inspection cycles remain undetected.
3. Predictive Maintenance (PdM / Condition-Based Maintenance): Predictive maintenance combines continuous real-time telemetry, advanced physical modeling, and algorithmic anomaly detection to infer machine health dynamically. Sensor instrumentation permanently affixed to machine chassis continuously streams mechanical and thermal indicators to analytical engines. Maintenance actions are initiated solely when empirical physical indicators demonstrate degradation exceeding standardized severity thresholds (such as ISO 10816 standards for mechanical vibration).

The convergence of Micro-Electro-Mechanical Systems (MEMS), high-performance low-power system-on-chip (SoC) microcontrollers, edge artificial intelligence (TinyML), and scalable cloud-native web architectures has enabled the democratization of predictive maintenance. Where historical condition monitoring was economically restricted to multi-million-dollar turbine assets via costly proprietary diagnostic equipment, modern IoT architectures allow ubiquitous, node-level condition monitoring across distributed factory floors."""
    },
    {
        "number": "1.1.2",
        "title": "System Technologies",
        "content": """The proposed industrial monitoring architecture synthesizes multiple state-of-the-art hardware and software technologies into a cohesive, fault-tolerant monitoring fabric:
1. Micro-Electro-Mechanical Systems (MEMS) Transducers: MEMS sensors integrate micro-machined silicon mechanical elements with electronic signal processing circuitry onto monolithic silicon dies. In this project, the MPU6050 six-degree-of-freedom inertial measurement unit utilizes a micro-machined capacitive accelerometer array and vibratory MEMS rate gyroscopes to detect microscopic chassis oscillations and rotational dynamics at high operational bandwidths with minimal power dissipation.
2. High-Performance Dual-Core Edge Controller (ESP32-S3): The ESP32-S3 microcontroller features dual 32-bit Xtensa LX7 processor cores operating at up to 240 MHz, 512 KB internal SRAM, 8 MB external Flash, and integrated vector instructions specifically optimized for accelerating neural network matrix multiplications and digital signal processing (DSP) routines. It manages real-time sensor sampling, FreeRTOS multi-threading, local time-domain feature extraction, and encrypted wireless transmission.
3. Multimodal Physical Transduction: In addition to MEMS inertial sensing, the edge node employs a digital 1-Wire temperature sensor (DS18B20) for non-drifting thermal tracking, a galvanic Hall-effect sensor (ACS712) for motor current signature analysis (MCSA), and a lead zirconate titanate (PZT) piezoelectric transducer for kinetic vibration harvesting investigation.
4. Asynchronous Lightweight Messaging (MQTT): Telemetry transport utilizes the Message Queuing Telemetry Transport (MQTT) protocol over TCP/IP via an Eclipse Mosquitto message broker. MQTT's compact binary header, publish-subscribe decoupling, and configurable Quality of Service (QoS) ensure deterministic data delivery over bandwidth-constrained industrial wireless local area networks (WLAN).
5. Enterprise Three-Tier Software Architecture: The supervisory platform is structured into decoupled, production-grade layers:
   - Tier 1 (Presentation): A responsive single-page web application engineered with React.js 18, Vite, Tailwind CSS, and Chart.js, delivering real-time interactive canvas visualization, tabular fault diagnosis, and parametric configuration.
   - Tier 2 (Application): An asynchronous ASGI backend engineered with Python 3.11, FastAPI, Pydantic, and Uvicorn, managing asynchronous MQTT message ingestion, digital signal processing (FFT, peak-to-peak, and RMS extraction), threshold-based ISO 10816 fault classification, and real-time bidirectional WebSocket client broadcasting.
   - Tier 3 (Data): A robust dual-database persistence tier uniting SQLite for relational schema integrity, machine profiles, and fault event auditing with InfluxDB for optimized high-volume time-series telemetry storage."""
    },
    {
        "number": "1.2",
        "title": "Objectives",
        "content": """The primary and secondary engineering objectives of this project are defined as follows:

Primary Objectives:
1. Edge Sensing Node Development: Design, fabricate, and validate an intelligent multimodal hardware sensor node centered around the dual-core ESP32-S3 microcontroller to simultaneously capture mechanical vibration, angular velocity, winding surface temperature, and motor electrical current.
2. Signal Conditioning and Hardware Interfacing: Implement robust, noise-immune signal conditioning circuits to interface 5V analog sensors (ACS712) and AC piezoelectric transducers to the 3.3V ADC logic of the ESP32-S3, preventing electrical over-voltage damage and maximizing measurement resolution.
3. Real-Time Telemetry and Asynchronous Messaging: Develop an efficient FreeRTOS-based firmware pipeline executing on the ESP32-S3 to acquire sensor samples, construct structured JSON payloads, and stream telemetry over Wi-Fi using the MQTT protocol with minimal transmission jitter.
4. Three-Tier Architectural Implementation: Engineer a decoupled enterprise architecture separating presentation (React.js), application logic and digital signal processing (FastAPI), and persistent storage (SQLite and InfluxDB).
5. Automated Anomaly Detection: Implement deterministic multi-parameter thresholding based on the ISO 10816-3 mechanical vibration standard, electrical over-current limits, and thermal runaway thresholds to generate instant alerts.
6. Real-Time Web Dashboard: Construct a high-performance web dashboard displaying live streaming telemetry via WebSockets, historical trending charts, vibration FFT spectral analysis, and prescriptive maintenance recommendations.

Secondary / Exploratory Objectives:
1. Parasitic Energy Harvesting Feasibility: Experimentally evaluate the mechanical-to-electrical energy conversion efficiency of a chassis-mounted PZT piezoelectric transducer, measuring open-circuit voltage, rectified DC potential, and storage capacitor accumulation under motor operating vibrations.
2. Edge AI / TinyML Architectural Readiness: Architect an extensible software interface (ITinyMLDetector) in the application tier to support future on-device TensorFlow Lite / Edge Impulse neural network inference for automated vibration spectral classification.
3. Containerized Deployment: Package the supervisory backend, database engines, and message broker into modular Docker containers to guarantee reproducibility, horizontal scalability, and rapid industrial deployment."""
    },
    {
        "number": "1.3",
        "title": "Project Description",
        "content": """This project implements an end-to-end industrial condition monitoring system specifically tailored for rotating electromechanical machines such as direct current (DC) motors. The physical apparatus comprises a 12V DC experimental motor securely mounted on a structural testbed. A multimodal sensor cluster is physically coupled to the motor frame, comprising an MPU6050 6-DoF accelerometer/gyroscope positioned on the motor bearing housing, a DS18B20 digital thermal probe mechanically bonded to the motor casing, and an ACS712-05B Hall-effect current transducer wired in series with the motor DC power supply rail. In addition, a PZT piezoelectric ceramic transducer disk is affixed to the motor mounting bracket to measure structural acoustic and kinetic vibration potentials.

The central processing unit of the edge node is the ESP32-S3 microcontroller. The firmware executes two concurrent FreeRTOS tasks: Core 0 executes high-frequency synchronous sensor data acquisition, digital low-pass filtering, and ADC conversions; Core 1 handles network stack management, Wi-Fi connectivity monitoring, JSON serialization, and MQTT client publishing. Sensor data packets are published at regular intervals (100 ms to 1000 ms) to the MQTT topic "industrial/mems/data".

An Eclipse Mosquitto broker acts as the central messaging hub. The application tier, developed using Python FastAPI, subscribes to the broker topics asynchronously. Upon arrival of raw sensor packets, the backend DSP engine computes critical diagnostic metrics:
- Tri-axial acceleration vector magnitude: a_mag = sqrt(ax^2 + ay^2 + az^2)
- Root-Mean-Square (RMS) vibration velocity: v_rms = sqrt(1/N sum(v_i^2))
- Peak-to-peak acceleration amplitude: a_p2p = max(a) - min(a)
- Fast Fourier Transform (FFT) frequency spectrum for dominant vibration frequency identification.

The computed metrics are evaluated against ISO 10816-3 vibration severity thresholds (Class I/II industrial machines), current safety envelopes, and motor thermal limits. Anomalous conditions trigger immediate fault event records in the SQLite relational database and real-time push alerts to connected browser clients over persistent WebSocket channels (/ws/sensors). Operators interact with the system via a modern React.js dashboard that visualizes real-time sensor streams at 5 to 10 Hz refresh rates, historical time-series analytics, and diagnostic recommendations."""
    },
    {
        "number": "1.4",
        "title": "Scope of the Project",
        "content": """To maintain rigorous academic integrity, the project scope is clearly divided between implemented functional capabilities and planned future research extensions:

Implemented Scope:
1. Physical Edge Sensor Node: Fully functional hardware prototype using an ESP32-S3 microcontroller interfacing an MPU6050 (I2C), DS18B20 (1-Wire), ACS712 (conditioned analog ADC), and a PZT piezoelectric transducer.
2. Signal Conditioning Circuitry: Implemented resistor divider network for ACS712 voltage level translation (5V to 3.3V) and full-wave Schottky diode bridge rectifier with capacitor smoothing and Zener clamping for piezoelectric AC-to-DC conversion.
3. Dual-Core FreeRTOS Firmware: Robust C++ firmware developed under the Arduino-ESP32 framework, featuring task separation, brownout handling, automatic Wi-Fi reconnection, and MQTT client publishing.
4. Three-Tier Software Architecture: Complete, running software implementation encompassing a React 18 single-page application (Tier 1), a FastAPI ASGI backend with WebSocket streaming and DSP engine (Tier 2), and a hybrid persistence database layer uniting SQLite and InfluxDB (Tier 3).
5. Fault Detection and Classification: Multi-parameter rule-based diagnostic engine implementing ISO 10816-3 vibration severity standards, motor over-current thresholds, and winding temperature limits.
6. Energy Harvesting Investigation: Empirical measurement and mathematical modeling of piezoelectric open-circuit voltage, rectified capacitor charging curves, and harvestable electrical energy from motor chassis vibration.
7. Docker Containerization: Comprehensive Docker Compose configuration orchestrating backend services, InfluxDB time-series storage, and Mosquitto message broker.

Future Scope (Distinguished from Implemented Prototype):
1. Complete Autonomous Self-Powered Operation: The current experimental prototype relies on a regulated 5V USB power supply for operational stability. While piezoelectric harvesting was quantitatively characterized, powering the ESP32-S3 continuously from vibration alone requires ultra-low-power sub-mW microcontrollers, high-Q resonant energy harvesters, and specialized power management ICs (PMICs).
2. Embedded On-Device TinyML Inference: In the current prototype, DSP and rule-based fault detection execute within the application tier, accompanied by an architectural interface (ITinyMLDetector). Future work involves quantizing trained deep neural network models (e.g., 1D-CNN or Autoencoders) to INT8 and compiling them via ESP-NN to run directly on the ESP32-S3 dual-core vector units.
3. Long-Range Adaptive Radio (LoRaWAN): Transitioning from 2.4 GHz Wi-Fi to adaptive frequency-hopping LoRaWAN or 5G RedCap for multi-kilometer transmission range across harsh, metallically obstructed industrial environments."""
    },
    {
        "number": "1.5",
        "title": "Applications of the Project",
        "content": """The multimodal condition monitoring architecture engineered in this project is directly applicable across a wide spectrum of industrial sectors:
1. Automated Manufacturing and Assembly Lines: Continuous monitoring of conveyor drive motors, automated sorting actuators, and packaging machinery. Early detection of mechanical misalignment or bearing wear prevents unexpected production halts that delay supply chains.
2. Heating, Ventilation, and Air Conditioning (HVAC) Systems: Large commercial and industrial HVAC air handling units, chilled water circulation pumps, and cooling tower fans operate continuously in inaccessible building locations. Remote IoT vibration and thermal tracking eliminates the need for hazardous manual inspections.
3. Renewable Energy Systems (Wind Turbine Generators): Wind turbine nacelles house complex multi-stage gearboxes and high-capacity generators subject to extreme aerodynamic turbulence and mechanical fatigue. Deploying multimodal wireless sensor nodes enables structural health monitoring and predictive maintenance without costly offshore technician dispatch.
4. Mining, Petrochemical, and Chemical Processing: Slurry pumps, agitators, centrifuges, and compressors handling volatile chemicals require continuous bearing health tracking. The non-invasive clamp-on nature of the multimodal sensor node allows retrofitting onto legacy explosion-proof motor casings.
5. Electric Mobility and Rail Traction Systems: Traction motors in electric locomotives, urban metro rail, and commercial electric vehicles undergo continuous mechanical shock, thermal cycling, and variable torque loads. The integrated vibration and thermal telemetry provides onboard diagnostic health records for fleet depot maintenance."""
    }
]
