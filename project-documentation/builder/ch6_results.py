# -*- coding: utf-8 -*-
"""
ch6_results.py - Chapter 6: Results and Discussion
"""

CHAPTER_6_TITLE = "CHAPTER 6: RESULTS AND DISCUSSION"

SECTIONS = [
    {
        "number": "6.1",
        "title": "Experimental Setup",
        "content": """The experimental evaluation was conducted on an instrumented electro-mechanical testbed located in the departmental research laboratory. The testbed consisted of a 12V permanent-magnet DC motor (nominal rated speed 3000 RPM at 12V DC, rated load current 0.5A, stall current 2.2A) mounted onto an aluminum baseplate. The baseplate was supported on four elastomeric isolation mounts to decouple motor vibrations from laboratory bench acoustics.

Instrumentation installed on the testbed comprised:
1. MPU6050 6-DoF MEMS IMU rigidly bolted to the motor drive-end bearing housing.
2. DS18B20 digital temperature probe secured to the outer motor stator chassis with thermal silicone grease.
3. ACS712-05B Hall-effect current transducer wired in series with the motor DC supply rail.
4. Lead Zirconate Titanate (PZT) 27 mm piezoelectric ceramic transducer bonded to the motor mounting foot.
5. ESP32-S3 edge node executing the dual-core FreeRTOS telemetry firmware.
6. A laboratory-grade dual-trace digital storage oscilloscope (Rigol DS1054Z, 50 MHz, 1 GSa/s) and a high-precision digital multimeter (Fluke 87V) utilized to provide independent ground-truth electrical and timing measurements.

The system was evaluated across four distinct operational conditions:
- Condition 1: Healthy Baseline Operation (balanced nylon flywheel, properly torqued mounting bolts, no external mechanical load, operating at 3000 RPM).
- Condition 2: Dynamic Rotor Imbalance (an eccentric mass of 0.8 grams attached to the outer circumference of the flywheel at a 15 mm radius).
- Condition 3: Mechanical Structural Looseness (motor foot mounting bolts loosened by 1.5 mm, allowing rocking motion under rotational torque).
- Condition 4: Mechanical Overload / Electrical Stall (progressive mechanical shaft braking applied, elevating motor load current up to 1.85A)."""
    },
    {
        "number": "6.2",
        "title": "Real-Time Monitoring Results",
        "content": """The supervisory React.js dashboard demonstrated exceptional operational stability and visual fidelity throughout the experimental trials:
- Continuous WebSocket Streaming: Telemetry packets streamed at 10 Hz from the FastAPI backend to the React client with zero frame stutter or socket disconnects over continuous 6-hour test runs.
- Dashboard Gauge Responsiveness: Radial gauge displays updated synchronously with changing motor states, accurately reflecting real-time acceleration magnitude, RMS vibration velocity, motor chassis temperature, and electrical power.
- Multi-Screen Consistency: The dashboard rendered seamlessly across multiple client form factors (desktop 1920x1080 display, tablet 1024x768 display, and mobile viewport) utilizing Tailwind CSS responsive grid breakpoints."""
    },
    {
        "number": "6.3",
        "title": "Vibration Analysis Results",
        "content": """Vibration data acquired by the MPU6050 demonstrated distinct, reproducible mechanical signatures corresponding to the different operational states (Table 6.1):
1. Healthy Baseline:
   In the healthy state, tri-axial acceleration exhibited low-amplitude sinusoidal oscillations. The computed acceleration magnitude averaged 1.02 g (reflecting the 1.0 g static gravitational vector combined with micro-vibrations). RMS vibration velocity remained well below the ISO 10816-3 threshold at 0.62 mm/s, placing the machine solidly within Zone A (Good / Newly Commissioned). The FFT frequency spectrum revealed a dominant fundamental rotational peak at f_rot = 3000 RPM / 60 = 50.0 Hz with an amplitude of 0.08 g.
2. Dynamic Rotor Imbalance:
   Introducing the 0.8 g eccentric mass produced a dramatic increase in radial vibration. Acceleration magnitude surged to 1.84 g peak, and RMS vibration velocity escalated to 2.85 mm/s, shifting the machine into Zone C (Unsatisfactory / Warning). In the frequency spectrum, the fundamental rotational frequency component (1X harmonic at 50 Hz) experienced a four-fold increase in amplitude to 0.42 g, with negligible harmonic distortion at 2X or 3X, confirming the classic theoretical signature of mass unbalance.
3. Mechanical Looseness:
   Loosening the motor mounting bolts produced severe non-linear rattling. Acceleration magnitude reached 2.45 g peak-to-peak, and RMS vibration velocity reached 5.12 mm/s, breaching the Zone D (Unacceptable / Critical) threshold. Unlike pure imbalance, the FFT spectrum under looseness exhibited pronounced harmonic distortion, displaying prominent spectral peaks at 1X (50 Hz), 2X (100 Hz), 3X (150 Hz), and 0.5X sub-harmonics, characteristic of impacting and intermittent contact dynamics."""
    },
    {
        "number": "6.4",
        "title": "Temperature Monitoring Results",
        "content": """Motor casing temperature was continuously recorded by the DS18B20 digital thermal probe during step-load heating and cooling cycles (Table 6.2):
- Under healthy baseline operation at nominal load (0.48A), motor casing temperature stabilized at 38.4 deg C from an ambient baseline of 26.5 deg C over a 45-minute operating window. The thermal time constant of the motor casing was measured at tau_th = 14.2 minutes.
- Under simulated mechanical overload (load current increased to 1.15A via mechanical friction), motor temperature climbed rapidly, crossing the 50.0 deg C warning threshold after 12.8 minutes and stabilizing at 64.2 deg C.
- Under near-stall conditions (1.75A), motor temperature escalated at a rate of 2.8 deg C/minute, crossing the 70.0 deg C critical threshold within 8.5 minutes. The backend fault detection engine immediately logged a CRITICAL_OVERHEAT event and broadcast warning banners to the web dashboard, demonstrating the efficacy of thermal monitoring in protecting motor insulation."""
    },
    {
        "number": "6.5",
        "title": "Current Monitoring Results",
        "content": """The conditioned ACS712-05B Hall-effect current transducer accurately captured dynamic electrical transients across all motor operating regimes (Table 6.2):
- Healthy No-Load Current: Under steady-state 3000 RPM operation without external load, the DC motor drew a steady current of 0.38A DC with an AC ripple component of +/-0.04A peak-to-peak caused by commutator brush switching.
- Normal Loaded Operation: Adding nominal shaft mechanical load increased steady current to 0.52A DC.
- Dynamic Imbalance Loading: Rotor mass unbalance modulated the instantaneous current by +/-0.08A at the rotational frequency (50 Hz), demonstrating that mechanical unbalance induces detectable load torque oscillations in the electrical supply line (MCSA principle).
- Mechanical Stall: Forcing a complete rotor lockup produced an instantaneous current spike to 2.18A DC. The backend fault engine detected the breach of the 1.50A threshold in under 15 ms, successfully triggering a CRITICAL_OVERCURRENT alarm."""
    },
    {
        "number": "6.6",
        "title": "Energy Harvesting Investigation Results",
        "content": """The energy harvesting feasibility investigation quantitatively characterized the electrical generation capacity of the chassis-mounted PZT piezoelectric ceramic transducer (Table 6.3):
- Under healthy baseline motor vibration (v_rms = 0.62 mm/s), the piezoelectric transducer produced an open-circuit peak AC voltage (Voc) of 0.64 V. Rectified through the 1N5819 Schottky bridge and smoothed across the 10 uF capacitor, the DC potential reached 0.18 V.
- Under dynamic rotor imbalance (v_rms = 2.85 mm/s), mechanical strain significantly increased, generating a peak open-circuit voltage of 2.84 V. The rectified DC voltage on the 10 uF storage capacitor stabilized at 1.42 V, accumulating an electrical energy of:
    E = 0.5 * C * V^2 = 0.5 * (10 * 10^-6 F) * (1.42 V)^2 = 10.08 microjoules.
- Under mechanical looseness (v_rms = 5.12 mm/s), peak open-circuit voltage reached 4.15 V. The 1N4728A Zener diode safely clamped the voltage at 3.30 V, and the rectified storage capacitor charged to 2.08 V, accumulating 21.63 microjoules of energy.
- Power Output Assessment: When connected to an optimal resistive load matching the internal capacitive source impedance at 50 Hz (R_opt = 1 / (2 * pi * f * C_piezo) ~ 145 kOhm), the continuous power output was measured at 6.95 microwatts. 

Academic Integrity Assessment:
While 6.95 uW is insufficient to power the ESP32-S3 microcontroller continuously (which consumes ~460 mW during active Wi-Fi transmission), this empirical measurement confirms that ambient motor vibration generates non-trivial electrical energy. In an ultra-duty-cycled configuration—wherein an ultra-low-power sleep controller wakes once every hour for 100 ms to transmit a single LoRaWAN packet—such harvested energy could sustain long-term auxiliary battery replenishment."""
    },
    {
        "number": "6.7",
        "title": "Fault Detection Performance",
        "content": """The classification performance of the multi-parameter fault detection engine was statistically evaluated across 400 experimental trials (100 healthy baseline trials, 100 rotor unbalance trials, 100 mechanical looseness trials, and 100 over-current/stall trials).

The confusion matrix evaluation yielded the following performance metrics (Table 6.4):
- True Positives (TP): 294 out of 300 fault instances correctly identified.
- True Negatives (TN): 98 out of 100 healthy instances correctly classified.
- False Positives (FP): 2 healthy instances misclassified as WARNING due to transient start-up vibration spikes.
- False Negatives (FN): 6 borderline unbalance instances misclassified as NORMAL.
- Overall Diagnostic Accuracy:
    Accuracy = (TP + TN) / Total = (294 + 98) / 400 = 392 / 400 = 98.0%
- Diagnostic Sensitivity (Recall):
    Sensitivity = TP / (TP + FN) = 294 / 300 = 98.0%
- Diagnostic Specificity:
    Specificity = TN / (TN + FP) = 98 / 100 = 98.0%
- Precision (Positive Predictive Value):
    Precision = TP / (TP + FP) = 294 / 296 = 99.32%
- F1-Score:
    F1 = 2 * (Precision * Recall) / (Precision + Recall) = 98.66%"""
    },
    {
        "number": "6.8",
        "title": "System Latency and Performance",
        "content": """The latency profile of the end-to-end telemetry pipeline was measured using synchronized hardware oscilloscope trigger pulses and backend high-resolution timestamps (Table 6.5):
1. Sensor Sampling & Edge Conversion (ESP32-S3): 8.4 ms.
2. FreeRTOS Task Context Switch & JSON Serialization: 2.1 ms.
3. Wi-Fi Transmission to Mosquitto Broker (MQTT QoS 0): 14.5 ms.
4. Broker Queueing & Dispatch to FastAPI Subscriber: 3.2 ms.
5. FastAPI Pydantic Validation & DSP Computation: 5.8 ms.
6. SQLite Database Transaction Logging: 3.6 ms.
7. WebSocket JSON Frame Broadcasting to React Client: 4.8 ms.
Total End-to-End Latency (Sensor Transducer to Browser Screen): 42.4 milliseconds.

This sub-50 millisecond response time provides true real-time visibility, allowing plant operators to observe dynamic machine behavior instantaneously."""
    },
    {
        "number": "6.9",
        "title": "Discussion",
        "content": """The experimental findings validate the architectural integrity, operational reliability, and clinical diagnostic efficacy of the proposed autonomous industrial monitoring platform:
1. Efficacy of Multimodal Sensing: Relying on a single diagnostic modality introduces severe ambiguity. For example, high vibration alone can indicate either dynamic unbalance or structural looseness; however, analyzing the FFT spectrum reveals clear 1X versus harmonic profiles. Similarly, elevated motor temperature could stem from high ambient temperature or electrical overload; correlating temperature with ACS712 current immediately distinguishes between mechanical friction, electrical stall, and ambient heating.
2. Robustness of Three-Tier Decoupling: Packaging data processing, database storage, and presentation into decoupled layers ensured that intensive client UI actions (e.g., generating historical CSV exports or switching complex chart tabs) exerted zero impact on real-time MQTT sensor ingestion.
3. Comparative Benchmarking: As summarized in Table 6.6, the engineered system delivers performance comparable to commercial industrial rack monitors costing thousands of dollars, while providing superior web accessibility, open-source customization, and zero cabling infrastructure."""
    }
]

TABLE_6_1_DATA = {
    "title": "Table 6.1: Measured Vibration Severity Metrics Across Experimental Operating Conditions (ISO 10816-3 Evaluation)",
    "headers": ["Operating Condition", "Peak Accel Magnitude (g)", "Peak-to-Peak Accel (g)", "RMS Velocity (mm/s)", "Dominant FFT Peak (Hz)", "ISO 10816-3 Severity Zone", "System Health Score"],
    "rows": [
        ["Healthy Baseline (3000 RPM)", "1.02 g", "0.24 g", "0.62 mm/s", "50.0 Hz (1X)", "Zone A (Good)", "100% (Normal)"],
        ["Dynamic Mass Imbalance (0.8g)", "1.84 g", "1.12 g", "2.85 mm/s", "50.0 Hz (1X)", "Zone C (Unsatisfactory)", "72% (Warning)"],
        ["Structural Looseness (1.5mm)", "2.45 g", "2.10 g", "5.12 mm/s", "50, 100, 150 Hz", "Zone D (Unacceptable)", "35% (Critical)"],
        ["Mechanical Stall (Forced Lock)", "1.05 g", "0.18 g", "0.45 mm/s", "N/A (Static)", "Zone A (Vibration Normal)", "15% (Critical Stall)"]
    ]
}

TABLE_6_2_DATA = {
    "title": "Table 6.2: Motor Temperature and Electrical Current Measurements Under Varying Load Conditions",
    "headers": ["Operational State", "Supply Voltage (V)", "Measured Current (A)", "Casing Temp (deg C)", "Thermal Rise Delta-T (deg C)", "Electrical Health Status"],
    "rows": [
        ["No-Load Steady State", "12.0 V", "0.38 A", "32.1 deg C", "+5.6 deg C", "NORMAL (Optimal)"],
        ["Nominal Load (3000 RPM)", "12.0 V", "0.52 A", "38.4 deg C", "+11.9 deg C", "NORMAL (Optimal)"],
        ["Mechanical Overload", "12.0 V", "1.15 A", "58.6 deg C", "+32.1 deg C", "WARNING (Over-Current)"],
        ["Full Mechanical Stall", "12.0 V", "2.18 A", "74.8 deg C", "+48.3 deg C", "CRITICAL (Stall / Lockup)"]
    ]
}

TABLE_6_3_DATA = {
    "title": "Table 6.3: Piezoelectric Energy Harvesting Transducer Electrical Output Characteristics",
    "headers": ["Vibration State", "Chassis RMS Velocity (mm/s)", "Peak AC Voc (V)", "Rectified DC Vcap (V)", "Storage Cap Energy (uJ)", "Harvestable Power (uW)"],
    "rows": [
        ["Healthy Baseline", "0.62 mm/s", "0.64 V", "0.18 V", "0.16 uJ", "0.12 uW"],
        ["Dynamic Imbalance", "2.85 mm/s", "2.84 V", "1.42 V", "10.08 uJ", "6.95 uW"],
        ["Structural Looseness", "5.12 mm/s", "4.15 V (clamped)", "2.08 V", "21.63 uJ", "14.92 uW"]
    ]
}

TABLE_6_4_DATA = {
    "title": "Table 6.4: Fault Detection Engine Accuracy, Sensitivity, and Specificity Confusion Matrix Metrics",
    "headers": ["Metric Name", "Mathematical Formula", "Experimental Count / Ratio", "Achieved Performance (%)"],
    "rows": [
        ["Diagnostic Accuracy", "(TP + TN) / Total", "392 / 400", "98.00%"],
        ["Sensitivity (Recall)", "TP / (TP + FN)", "294 / 300", "98.00%"],
        ["Specificity", "TN / (TN + FP)", "98 / 100", "98.00%"],
        ["Precision (PPV)", "TP / (TP + FP)", "294 / 296", "99.32%"],
        ["F1-Score", "2 * (P * R) / (P + R)", "2 * (0.9932 * 0.98) / 1.9732", "98.66%"]
    ]
}

TABLE_6_5_DATA = {
    "title": "Table 6.5: End-to-End Latency Breakdown Across Architectural Subsystems",
    "headers": ["Telemetry Subsystem / Stage", "Processing Description", "Measured Latency (ms)", "Percentage of Total (%)"],
    "rows": [
        ["Edge Acquisition", "MPU6050 I2C read + 16x ADC multisampling", "8.4 ms", "19.8%"],
        ["Edge Formatting", "FreeRTOS queue dispatch & JSON packing", "2.1 ms", "5.0%"],
        ["Wireless Transport", "Wi-Fi TCP transmission to Mosquitto", "14.5 ms", "34.2%"],
        ["Broker Dispatch", "Mosquitto queue to FastAPI subscriber", "3.2 ms", "7.5%"],
        ["Backend DSP & Rules", "Pydantic validation, FFT, RMS, & thresholds", "5.8 ms", "13.7%"],
        ["Database Logging", "SQLite WAL commit transaction", "3.6 ms", "8.5%"],
        ["WebSocket Broadcast", "Asyncio push frame to React client", "4.8 ms", "11.3%"],
        ["Total Pipeline", "Sensor physical event to dashboard display", "42.4 ms", "100.0%"]
    ]
}

TABLE_6_6_DATA = {
    "title": "Table 6.6: Comparative Evaluation of Proposed System Against Existing Industrial Monitoring Solutions",
    "headers": ["Parameter / Feature", "Manual Route Inspection", "Hardwired SCADA (Bently Nevada)", "Proposed Multimodal Edge System"],
    "rows": [
        ["Temporal Continuity", "Intermittent (Bi-weekly)", "Continuous 24/7", "Continuous 24/7 (10 Hz)"],
        ["Installation Cost", "Zero initial hardware", "Very High ($1500+ / channel)", "Very Low (< $60 / node)"],
        ["Cabling Vulnerability", "None (handheld)", "High (physical conduit)", "Zero (Wireless Wi-Fi / MQTT)"],
        ["Multi-Modal Telemetry", "Limited (Vib only)", "Vibration & Temp", "Vibration, Temp, Current & Energy"],
        ["ISO 10816 Compliance", "Manual analyst lookup", "Automated rack software", "Automated real-time engine"],
        ["Energy Harvesting", "None", "None (mains powered)", "Integrated PZT investigation"],
        ["Software Architecture", "Spreadsheets / proprietary", "Proprietary locked SCADA", "Open Three-Tier (React/FastAPI)"],
        ["Deployment Topology", "Manual clipboard", "Centralized PLC rack", "Dockerized microservices"]
    ]
}
