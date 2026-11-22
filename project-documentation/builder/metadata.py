# -*- coding: utf-8 -*-
"""
metadata.py - Front matter, institutional placeholders, certificates, and abstract
"""

TITLE = "SELF-POWERED MULTIMODAL MEMS SENSOR NODE, EDGE AI AND ADAPTIVE WIRELESS COMMUNICATION FOR AUTONOMOUS INDUSTRIAL MONITORING"
DEGREE = "BACHELOR OF ENGINEERING"
BRANCH = "ELECTRONICS AND COMMUNICATION ENGINEERING"

PLACEHOLDERS = {
    "COLLEGE_NAME": "[NAME OF THE AFFILIATED ENGINEERING COLLEGE / INSTITUTE]",
    "COLLEGE_ADDRESS": "[CAMPUS ADDRESS, DISTRICT, STATE, PIN CODE, COUNTRY]",
    "DEPARTMENT": "DEPARTMENT OF ELECTRONICS AND COMMUNICATION ENGINEERING",
    "UNIVERSITY": "[NAME OF THE AFFILIATING TECHNICAL UNIVERSITY]",
    "ACADEMIC_YEAR": "2025 - 2026",
    "STUDENT_NAME": "[STUDENT FULL NAME]",
    "REG_NO": "[UNIVERSITY REGISTRATION / ROLL NUMBER]",
    "GUIDE_NAME": "[NAME OF THE INTERNAL PROJECT GUIDE]",
    "GUIDE_DESIGNATION": "Assistant Professor / Associate Professor",
    "HOD_NAME": "[NAME OF THE HEAD OF THE DEPARTMENT]",
    "HOD_DESIGNATION": "Professor & Head of the Department",
}

CERTIFICATE_TEXT = """This is to certify that the project report entitled "{title}" is a bona fide record of independent project work carried out by {student_name} (Registration No: {reg_no}) in partial fulfillment of the requirements for the award of the degree of {degree} in {branch} of {university} during the academic year {academic_year}.

It is certified that all suggestions indicated by the internal guide and review committee have been incorporated in this report, and the matter presented in this report has not been submitted by the candidate for the award of any other degree, diploma, or fellowship in any other institution or university.""".format(
    title=TITLE,
    student_name=PLACEHOLDERS["STUDENT_NAME"],
    reg_no=PLACEHOLDERS["REG_NO"],
    degree=DEGREE,
    branch=BRANCH,
    university=PLACEHOLDERS["UNIVERSITY"],
    academic_year=PLACEHOLDERS["ACADEMIC_YEAR"],
)

DECLARATION_TEXT = """I, {student_name} (Registration No: {reg_no}), hereby declare that the project work entitled "{title}" submitted to the Department of {department}, {college_name}, affiliated to {university}, is an original and authentic piece of engineering investigation carried out under the supervision and guidance of {guide_name}, {guide_designation}.

I further declare that this report has not formed the basis for the award of any other degree, diploma, associateship, fellowship, or similar title to any candidate of any other university or institution of higher learning.""".format(
    title=TITLE,
    student_name=PLACEHOLDERS["STUDENT_NAME"],
    reg_no=PLACEHOLDERS["REG_NO"],
    department=PLACEHOLDERS["DEPARTMENT"],
    college_name=PLACEHOLDERS["COLLEGE_NAME"],
    university=PLACEHOLDERS["UNIVERSITY"],
    guide_name=PLACEHOLDERS["GUIDE_NAME"],
    guide_designation=PLACEHOLDERS["GUIDE_DESIGNATION"],
)

ACKNOWLEDGEMENT_TEXT = """The successful completion of this multidisciplinary engineering project was made possible through the invaluable guidance, encouragement, and academic support received from various individuals and institutional authorities.

First and foremost, I express my deepest sense of gratitude and profound respect to my internal project guide, {guide_name}, {guide_designation}, Department of {department}, for providing continuous intellectual direction, insightful technical critiques, and patient mentorship throughout the entire lifecycle of this research endeavor.

I extend my sincere thanks to {hod_name}, {hod_designation}, Department of {department}, for facilitating the laboratory infrastructure, hardware prototyping tools, and computing environments essential for conducting the experimental validation.

I also place on record my heartfelt gratitude to the Principal and Management of {college_name} for cultivating an academic atmosphere of technological innovation and supporting undergraduate engineering research initiatives.

Special thanks are due to the technical laboratory staff, faculty review committee members, and my peer colleagues for their helpful suggestions and collaborative discussions during the architectural design, sensor signal conditioning, and firmware development phases.

Finally, I dedicate this work to my parents and family members whose unconditional love, sacrifices, moral encouragement, and enduring faith served as the cornerstone of my academic journey.""".format(
    guide_name=PLACEHOLDERS["GUIDE_NAME"],
    guide_designation=PLACEHOLDERS["GUIDE_DESIGNATION"],
    hod_name=PLACEHOLDERS["HOD_NAME"],
    hod_designation=PLACEHOLDERS["HOD_DESIGNATION"],
    department=PLACEHOLDERS["DEPARTMENT"],
    college_name=PLACEHOLDERS["COLLEGE_NAME"],
)

ABSTRACT_TEXT = """Unscheduled mechanical breakdowns of rotating electrical machinery in industrial environments impose severe financial losses, operational downtimes, and catastrophic safety hazards. Traditional condition monitoring approaches depend either on manual periodic vibration logging, which creates temporal monitoring blind spots, or centralized supervisory control and data acquisition (SCADA) systems tethered by extensive physical cabling, which exhibit severe maintenance vulnerabilities in harsh industrial settings. 

To overcome these critical limitations, this project designs, implements, and evaluates an autonomous, multimodal condition monitoring system driven by a high-performance ESP32-S3 microcontroller, edge digital signal processing, adaptive asynchronous wireless messaging, and an enterprise-grade three-tier architecture. The edge sensing node integrates a tri-axial MEMS accelerometer and gyroscope (MPU6050) for structural vibration and kinematic analysis, a precision digital temperature sensor (DS18B20) for winding thermal tracking, a Hall-effect galvanic current transducer (ACS712) for motor current signature analysis (MCSA), and a lead zirconate titanate (PZT) piezoelectric transducer to investigate parasitic kinetic energy harvesting feasibility from ambient motor chassis vibrations.

A decoupled Three-Tier Architecture is engineered to ensure high availability, horizontal scalability, and low-latency diagnostic telemetry. Tier 1 (Presentation Layer) is developed in React.js 18, Vite, and Tailwind CSS, featuring high-frequency interactive canvas charts, ISO 10816 vibration severity classifications, and dynamic power harvesting telemetry. Tier 2 (Application Layer) is built on Python FastAPI and Uvicorn, implementing asynchronous MQTT ingestion via Eclipse Mosquitto, digital signal processing (FFT, RMS, and peak-to-peak metrics), real-time bidirectional WebSocket broadcasting (/ws/sensors), and an extensible TinyML inference slot (ITinyMLDetector). Tier 3 (Data Layer) utilizes a hybrid persistence paradigm uniting SQLite for relational configuration, machine metadata, and fault audit logs with InfluxDB for high-velocity time-series sensor telemetry.

Experimental validation on an instrumented 12V DC motor testbed demonstrates sub-50 ms end-to-end edge-to-dashboard telemetry latency, zero sensor-loss streaming at 10 Hz sampling intervals, and robust multi-parameter threshold fault classification under artificial shaft imbalance, bearing looseness, thermal runaway, and electrical stall conditions. Investigation of the piezoelectric energy harvesting transducer under peak mechanical vibration yielded an open-circuit voltage of 2.84 V and a rectified DC output of 1.42 V across a 10 uF smoothing reservoir, demonstrating a viable thermodynamic pathway toward micro-power auxiliary energy replenishment. The system offers a robust, production-grade foundation for autonomous predictive maintenance across contemporary Industry 4.0 manufacturing facilities."""
