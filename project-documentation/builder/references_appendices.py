# -*- coding: utf-8 -*-
"""
references_appendices.py - References, Appendices A1 to A8, and Technical Biography
"""

REFERENCES_LIST = [
    "[1] S. Li, L. Da Xu, and S. Zhao, \"The internet of things: A survey,\" Information Systems Frontiers, vol. 17, no. 2, pp. 243-259, Apr. 2015. DOI: 10.1007/s10796-014-9492-7.",
    "[2] G. A. Susto, A. Schirru, S. Pampuri, S. McLoone, and A. Beghi, \"Machine learning for predictive maintenance: A multiple classifier approach,\" IEEE Transactions on Industrial Informatics, vol. 11, no. 3, pp. 812-820, Jun. 2015. DOI: 10.1109/TII.2014.2349359.",
    "[3] A. Albarbar, S. Mekid, A. Starr, and R. Pietruszkiewicz, \"Suitability of MEMS accelerometers for condition monitoring: An experimental study,\" Sensors, vol. 8, no. 2, pp. 784-799, Feb. 2008. DOI: 10.3390/s8020784.",
    "[4] R. Sabato, C. Niezrecki, and G. Fortino, \"Wireless MEMS-based sensor networks for structural health monitoring: A review,\" IEEE Sensors Journal, vol. 17, no. 6, pp. 1599-1612, Mar. 2017. DOI: 10.1109/JSEN.2016.2647708.",
    "[5] S. Nandi, H. A. Toliyat, and X. Li, \"Condition monitoring and fault diagnosis of electrical machines—A review,\" IEEE Transactions on Energy Conversion, vol. 20, no. 4, pp. 719-729, Dec. 2005. DOI: 10.1109/TEC.2005.847954.",
    "[6] W. T. Thomson and M. Fenger, \"Current signature analysis to detect induction motor faults,\" IEEE Industry Applications Magazine, vol. 7, no. 4, pp. 26-34, Jul./Aug. 2001. DOI: 10.1109/2943.930988.",
    "[7] M. E. H. Benbouzid, \"A review of induction motors signature analysis as a medium for faults detection,\" IEEE Transactions on Industrial Electronics, vol. 47, no. 5, pp. 984-993, Oct. 2000. DOI: 10.1109/41.873206.",
    "[8] M. Blodt, M. Chabert, J. Regnier, and J. Faucher, \"Mechanical misalignment detection in induction machines by stator current signature analysis,\" IEEE Transactions on Industrial Electronics, vol. 55, no. 4, pp. 1793-1803, Apr. 2008. DOI: 10.1109/TIE.2008.917100.",
    "[9] S. Roundy and P. K. Wright, \"A piezoelectric vibration based generator for wireless electronics,\" Smart Materials and Structures, vol. 13, no. 5, pp. 1131-1142, Oct. 2004. DOI: 10.1088/0964-1726/13/5/018.",
    "[10] S. P. Beeby, M. J. Tudor, and N. M. White, \"Energy harvesting vibration sources for microsystems applications,\" Measurement Science and Technology, vol. 17, no. 12, pp. R175-R195, Nov. 2006. DOI: 10.1088/0957-0233/17/12/R01.",
    "[11] A. Erturk and D. J. Inman, Piezoelectric Energy Harvesting. Chichester, UK: John Wiley & Sons, 2011.",
    "[12] P. P. Ray, \"A review on TinyML: State-of-the-art and prospects,\" Journal of King Saud University - Computer and Information Sciences, vol. 34, no. 4, pp. 1595-1623, Apr. 2022. DOI: 10.1016/j.jksuci.2021.11.019.",
    "[13] P. Warden and D. Situnayake, TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers. Sebastopol, CA, USA: O'Reilly Media, 2019.",
    "[14] C. Banbury et al., \"Benchmarking TinyML systems: Challenges and direction,\" in Proc. IEEE Int. Conf. Acoust., Speech Signal Process. (ICASSP), Toronto, ON, Canada, Jun. 2021, pp. 8168-8172. DOI: 10.1109/ICASSP39728.2021.9413550.",
    "[15] V. C. Gungor and G. P. Hancke, \"Industrial wireless sensor networks: Challenges, design principles, and technical approaches,\" IEEE Transactions on Industrial Electronics, vol. 56, no. 10, pp. 4258-4265, Oct. 2009. DOI: 10.1109/TIE.2009.2015754.",
    "[16] U. Raza, P. Kulkarni, and M. Sooriyabandara, \"Low power wide area networks: An overview,\" IEEE Communications Surveys & Tutorials, vol. 19, no. 2, pp. 855-873, Secondquarter 2017. DOI: 10.1109/COMST.2017.2652320.",
    "[17] Mechanical Vibration — Evaluation of Machine Vibration by Measurements on Non-Rotating Parts — Part 3: Industrial Machines with Nominal Power Above 15 kW and Nominal Speeds Between 120 r/min and 15 000 r/min, ISO Standard 10816-3:2009, 2009.",
    "[18] InvenSense Inc., \"MPU-6000 and MPU-6050 Product Specification Revision 3.4,\" Document No. PS-MPU-6000A-00, Aug. 2013.",
    "[19] Maxim Integrated, \"DS18B20 Programmable Resolution 1-Wire Digital Thermometer,\" Datasheet Rev. 8, Mar. 2019.",
    "[20] Allegro MicroSystems LLC, \"ACS712: Fully Integrated, Hall-Effect-Based Linear Current Sensor IC with 2.1 kVRMS Voltage Isolation,\" Datasheet Rev. 15, Nov. 2017."
]

APPENDIX_A1 = {
    "title": "APPENDIX A1: COMPLETE ESP32-S3 FIRMWARE CODE",
    "content": """// ============================================================================
// PROJECT: SELF-POWERED MULTIMODAL MEMS SENSOR NODE FOR INDUSTRIAL MONITORING
// TARGET: ESP32-S3-WROOM-1 (Dual-Core Xtensa LX7 @ 240 MHz)
// FRAMEWORK: Arduino-ESP32 / FreeRTOS
// ============================================================================

#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "esp_adc_cal.h"

// Configuration Parameters
const char* WIFI_SSID     = "INDUSTRIAL_IOT_WLAN";
const char* WIFI_PASS     = "SecureFactoryPass2026";
const char* MQTT_BROKER   = "192.168.1.100";
const int   MQTT_PORT     = 1883;
const char* MQTT_TOPIC    = "industrial/mems/data";
const char* NODE_ID       = "esp32s3_mems_01";

// GPIO Pin Assignments
#define PIN_I2C_SDA       8
#define PIN_I2C_SCL       9
#define PIN_ONEWIRE_DQ    4
#define PIN_ADC_CURRENT   1   // ADC1_CH0 (ACS712 conditioned)
#define PIN_ADC_PIEZO     2   // ADC1_CH1 (Rectified Piezo)

// Global Sensor Objects
Adafruit_MPU6050 mpu;
OneWire oneWire(PIN_ONEWIRE_DQ);
DallasTemperature tempSensor(&oneWire);
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// Calibration Constants
const float CURRENT_ZERO_VOLTS = 1.667; // 2.50V * (20k / 30k)
const float CURRENT_SENSITIVITY = 0.1233; // 0.185 V/A * 0.6667
const float VOLTAGE_DIVIDER_RATIO = 0.6667;

// Telemetry Data Structure
struct TelemetryPacket {
    float ax, ay, az;
    float gx, gy, gz;
    float temp_c;
    float current_a;
    float piezo_v;
    uint32_t timestamp_ms;
};

QueueHandle_t telemetryQueue;

// Core 0 Task: Sensor Data Acquisition
void sensorTask(void *pvParameters) {
    TelemetryPacket packet;
    for(;;) {
        sensors_event_t a, g, temp;
        mpu.getEvent(&a, &g, &temp);
        
        packet.ax = a.acceleration.x / 9.80665; // Convert m/s^2 to g
        packet.ay = a.acceleration.y / 9.80665;
        packet.az = a.acceleration.z / 9.80665;
        packet.gx = g.gyro.x * 57.2957795;     // Convert rad/s to deg/s
        packet.gy = g.gyro.y * 57.2957795;
        packet.gz = g.gyro.z * 57.2957795;
        
        tempSensor.requestTemperatures();
        packet.temp_c = tempSensor.getTempCByIndex(0);
        
        // Multisampling ADC conversions
        uint32_t raw_current = 0, raw_piezo = 0;
        for (int i = 0; i < 16; i++) {
            raw_current += analogRead(PIN_ADC_CURRENT);
            raw_piezo   += analogRead(PIN_ADC_PIEZO);
        }
        float v_current_adc = ((raw_current / 16.0) / 4095.0) * 3.3;
        float v_piezo_adc   = ((raw_piezo / 16.0) / 4095.0) * 3.3;
        
        packet.current_a = (v_current_adc - CURRENT_ZERO_VOLTS) / CURRENT_SENSITIVITY;
        if (abs(packet.current_a) < 0.05) packet.current_a = 0.0; // Deadband
        packet.piezo_v   = v_piezo_adc;
        packet.timestamp_ms = millis();
        
        xQueueSend(telemetryQueue, &packet, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(100)); // 10 Hz sampling rate
    }
}

// Core 1 Task: Wireless Networking and MQTT Publishing
void networkTask(void *pvParameters) {
    TelemetryPacket packet;
    StaticJsonDocument<512> doc;
    char jsonBuffer[512];
    
    for(;;) {
        if (!mqttClient.connected()) {
            while (!mqttClient.connected()) {
                if (mqttClient.connect(NODE_ID)) {
                    Serial.println("[MQTT] Connected to Broker");
                } else {
                    vTaskDelay(pdMS_TO_TICKS(2000));
                }
            }
        }
        mqttClient.loop();
        
        if (xQueueReceive(telemetryQueue, &packet, pdMS_TO_TICKS(50)) == pdPASS) {
            doc.clear();
            doc["node_id"] = NODE_ID;
            doc["timestamp_ms"] = packet.timestamp_ms;
            
            JsonObject accel = doc.createNestedObject("accel");
            accel["x"] = packet.ax;
            accel["y"] = packet.ay;
            accel["z"] = packet.az;
            
            JsonObject gyro = doc.createNestedObject("gyro");
            gyro["x"] = packet.gx;
            gyro["y"] = packet.gy;
            gyro["z"] = packet.gz;
            
            doc["temperature"] = packet.temp_c;
            doc["current"]     = packet.current_a;
            doc["piezo_v"]     = packet.piezo_v;
            
            serializeJson(doc, jsonBuffer);
            mqttClient.publish(MQTT_TOPIC, jsonBuffer);
        }
    }
}

void setup() {
    Serial.begin(115200);
    Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, 400000);
    
    if (!mpu.begin(0x68, &Wire)) {
        Serial.println("[ERROR] MPU6050 not detected!");
        while(1) delay(100);
    }
    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);
    
    tempSensor.begin();
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db); // 0 to 3.3V range
    
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\\n[WIFI] Connected");
    
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    telemetryQueue = xQueueCreate(10, sizeof(TelemetryPacket));
    
    // Pin tasks to respective cores
    xTaskCreatePinnedToCore(sensorTask, "SensorTask", 4096, NULL, 2, NULL, 0);
    xTaskCreatePinnedToCore(networkTask, "NetworkTask", 4096, NULL, 1, NULL, 1);
}

void loop() {
    vTaskDelete(NULL); // FreeRTOS manages loop execution
}"""
}

APPENDIX_A2 = {
    "title": "APPENDIX A2: COMPLETE FASTAPI BACKEND CODE STRUCTURE",
    "content": """# Directory Tree: application-tier/
application-tier/
|-- app/
|   |-- __init__.py
|   |-- main.py                    # ASGI application & router mounts
|   |-- config.py                  # Environment settings & parameters
|   |-- api/
|   |   |-- __init__.py
|   |   |-- routes.py              # REST API endpoints (health, latest, history, export)
|   |-- core/
|   |   |-- __init__.py
|   |   |-- dsp_engine.py          # NumPy FFT, RMS velocity, Peak-to-Peak calculations
|   |   |-- fault_classifier.py    # ISO 10816-3 thresholds & diagnostic logic
|   |   |-- tinyml_interface.py    # Abstract ITinyMLDetector model contract
|   |-- db/
|   |   |-- __init__.py
|   |   |-- sqlite_database.py     # SQLite session & WAL engine
|   |   |-- models.py              # SQLAlchemy ORM declarations
|   |   |-- influx_client.py       # InfluxDB 2.0 time-series client
|   |-- services/
|   |   |-- __init__.py
|   |   |-- mqtt_service.py        # Paho MQTT subscriber client
|   |   |-- sensor_service.py      # Telemetry routing & persistence orchestration
|   |   |-- websocket_manager.py   # WebSocket broadcast connection pool
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml"""
}

APPENDIX_A3 = {
    "title": "APPENDIX A3: REACT FRONTEND CODE STRUCTURE",
    "content": """# Directory Tree: presentation-tier/
presentation-tier/
|-- public/
|   |-- vite.svg
|-- src/
|   |-- assets/
|   |-- components/
|   |   |-- Navbar.jsx             # Top status banner & connection pills
|   |   |-- Sidebar.jsx            # Multi-view navigation bar
|   |   |-- MetricCard.jsx         # KPI metric widgets with sparklines
|   |   |-- RadialGauge.jsx        # Animated SVG health and RMS gauges
|   |   |-- ChartContainer.jsx     # Reusable Chart.js canvas wrapper
|   |-- hooks/
|   |   |-- useWebSocket.js        # Persistent WS hook with auto-reconnection
|   |-- pages/
|   |   |-- Dashboard.jsx          # Executive KPI summary & alert highlights
|   |   |-- LiveMonitoring.jsx     # High-frequency waveforms & FFT spectrum
|   |   |-- FaultDetection.jsx     # ISO 10816-3 severity matrix & recommendations
|   |   |-- EnergyMonitoring.jsx   # Kinetic harvesting analytics (Voc, Vcap, P_harv)
|   |   |-- History.jsx            # Tabular logs, date filters & CSV export
|   |   |-- Settings.jsx           # Network endpoints & alarm threshold tuning
|   |-- services/
|   |   |-- apiService.js          # REST client wrapper (Axios / Fetch)
|   |-- App.jsx                    # Root router and layout shell
|   |-- main.jsx                   # React 18 DOM mount point
|   |-- index.css                  # Tailwind CSS utility imports
|-- package.json
|-- vite.config.js
|-- tailwind.config.js"""
}

APPENDIX_A4 = {
    "title": "APPENDIX A4: DATABASE SCHEMA AND SQL DDL SCRIPTS",
    "content": """-- ============================================================================
-- SQL DDL SCHEMA SPECIFICATION FOR INDUSTRIAL CONDITION MONITORING (SQLite 3)
-- ============================================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS machines (
    machine_id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    model VARCHAR(64),
    rated_speed_rpm INTEGER DEFAULT 3000,
    rated_current_a REAL DEFAULT 0.50,
    baseline_vibration_rms REAL DEFAULT 0.71,
    status VARCHAR(16) DEFAULT 'ONLINE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id VARCHAR(32) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    accel_x REAL NOT NULL,
    accel_y REAL NOT NULL,
    accel_z REAL NOT NULL,
    gyro_x REAL NOT NULL,
    gyro_y REAL NOT NULL,
    gyro_z REAL NOT NULL,
    temperature REAL NOT NULL,
    current REAL NOT NULL,
    piezo_voltage REAL NOT NULL,
    vibration_rms REAL NOT NULL,
    vibration_p2p REAL NOT NULL,
    health_score INTEGER NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sensor_time ON sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_sensor_machine ON sensor_readings(machine_id);

CREATE TABLE IF NOT EXISTS fault_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id VARCHAR(32) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    severity VARCHAR(16) NOT NULL,
    fault_type VARCHAR(32) NOT NULL,
    trigger_metric VARCHAR(32) NOT NULL,
    trigger_value REAL NOT NULL,
    threshold_value REAL NOT NULL,
    message TEXT NOT NULL,
    acknowledged BOOLEAN DEFAULT 0,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_fault_time ON fault_events(timestamp);

CREATE TABLE IF NOT EXISTS energy_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id VARCHAR(32) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    open_circuit_voltage REAL NOT NULL,
    rectified_voltage REAL NOT NULL,
    storage_capacitance_uf REAL DEFAULT 10.0,
    energy_stored_uj REAL NOT NULL,
    FOREIGN KEY (machine_id) REFERENCES machines(machine_id) ON DELETE CASCADE
);"""
}

APPENDIX_A5 = {
    "title": "APPENDIX A5: HARDWARE PIN ASSIGNMENT AND CONNECTION MAPPING",
    "content": """| Microcontroller Pin | Signal Name | Connected Hardware | Function Description | Electrical Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **GPIO 8** | I2C_SDA | MPU6050 SDA | Serial Data Line | I2C Fast Mode (400 kHz, 3.3V) |
| **GPIO 9** | I2C_SCL | MPU6050 SCL | Serial Clock Line | I2C Fast Mode (400 kHz, 3.3V) |
| **GPIO 4** | ONEWIRE_DQ | DS18B20 Data | Digital Thermal Data | Dallas 1-Wire (4.7k pull-up to 3.3V) |
| **GPIO 1** | ADC1_CH0 | ACS712 Conditioned | Motor Current In | Conditioned Analog (0 - 3.3V) |
| **GPIO 2** | ADC1_CH1 | Piezo Conditioned | Harvested DC Potential | Rectified Analog (0 - 3.3V clamped) |
| **3V3 Pin** | 3.3V OUT | Sensors VDD | System 3.3V Power Rail | Regulated 3.3V DC (+/-2%) |
| **5V / VBUS** | 5.0V IN | ACS712 VCC | Main Supply Rail | 5.0V DC from USB power supply |
| **GND** | GROUND | System Ground Plane | Common Reference Plane | 0V Common Ground Reference |"""
}

APPENDIX_A6 = {
    "title": "APPENDIX A6: SENSOR SIGNAL CONDITIONING CIRCUITS",
    "content": """1. ACS712 Current Sensor Voltage Divider Circuit:
The ACS712 sensor requires a 5V supply rail and outputs 2.50V at zero current. To match the 3.3V ADC of the ESP32-S3, a passive resistive divider is used:
   V_sensor (0-5V) ---> [ R1 = 10 kOhm ] ---> Node V_ADC ---> [ R2 = 20 kOhm ] ---> GND
   Divider attenuation factor: alpha = 20k / (10k + 20k) = 0.6667
   At zero current: V_ADC = 2.50V * 0.6667 = 1.667V.
   At +5A current: V_ADC = 3.425V * 0.6667 = 2.283V.

2. Piezoelectric Harvester Full-Wave Bridge Rectifier & Over-Voltage Clamp:
The PZT bender generates an AC voltage during chassis vibration:
   PZT Lead (+) ---> [ AC Terminal 1: Full-Wave 1N5819 Schottky Bridge ]
   PZT Lead (-) ---> [ AC Terminal 2: Full-Wave 1N5819 Schottky Bridge ]
   Rectifier (+) ---> [ Node V_DC ] ---> [ Reservoir Cap: 10 uF, 25V ] ---> GND
   Rectifier (+) ---> [ Cathode: 1N4728A 3.3V 1W Zener Diode ] ---> Anode to GND
   Node V_DC connected directly to ESP32-S3 GPIO 2 (ADC1_CH1)."""
}

APPENDIX_A7 = {
    "title": "APPENDIX A7: ISO 10816-3 VIBRATION SEVERITY STANDARD TABLE",
    "content": """The International Organization for Standardization (ISO) 10816-3 standard governs the evaluation of machine vibration severity by measurements on non-rotating parts for industrial machines:

| Machine Class | Vibration Velocity RMS (mm/s) | Severity Zone Classification | Operational Evaluation & Prescriptive Maintenance Recommendation |
| :--- | :--- | :--- | :--- |
| **Class I / II** | **v_rms < 0.71 mm/s** | **Zone A** (Good) | Newly commissioned or refurbished machine. Unrestricted continuous operation. |
| **Class I / II** | **0.71 <= v_rms < 1.80 mm/s** | **Zone B** (Acceptable) | Normal continuous industrial operation without operational restrictions. |
| **Class I / II** | **1.80 <= v_rms < 4.50 mm/s** | **Zone C** (Unsatisfactory) | Machine exhibits incipient mechanical defect (unbalance, misalignment). Schedule inspection. |
| **Class I / II** | **v_rms >= 4.50 mm/s** | **Zone D** (Unacceptable) | Severe mechanical vibration. High risk of catastrophic failure. Immediate shutdown required. |"""
}

APPENDIX_A8 = {
    "title": "APPENDIX A8: DOCKER COMPOSE DEPLOYMENT CONFIGURATION",
    "content": """version: '3.8'

services:
  mems-broker:
    image: eclipse-mosquitto:2.0-alpine
    container_name: mems-broker
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto-data:/mosquitto/data
    networks:
      - mems-net

  mems-backend:
    build:
      context: ./application-tier
      dockerfile: Dockerfile
    container_name: mems-backend
    restart: unless-stopped
    environment:
      - MQTT_BROKER_HOST=mems-broker
      - MQTT_BROKER_PORT=1883
      - INFLUXDB_URL=http://mems-influxdb:8086
      - INFLUXDB_TOKEN=my-super-secret-auth-token
      - INFLUXDB_ORG=mems_org
      - INFLUXDB_BUCKET=mems_telemetry
    ports:
      - "8000:8000"
    volumes:
      - ./data-tier/sqlite:/app/data
    depends_on:
      - mems-broker
    networks:
      - mems-net

  mems-frontend:
    build:
      context: ./presentation-tier
      dockerfile: Dockerfile
    container_name: mems-frontend
    restart: unless-stopped
    ports:
      - "5173:80"
    depends_on:
      - mems-backend
    networks:
      - mems-net

  mems-influxdb:
    image: influxdb:2.7-alpine
    container_name: mems-influxdb
    restart: unless-stopped
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=adminpassword123
      - DOCKER_INFLUXDB_INIT_ORG=mems_org
      - DOCKER_INFLUXDB_INIT_BUCKET=mems_telemetry
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token
    ports:
      - "8086:8086"
    volumes:
      - influxdb-storage:/var/lib/influxdb2
    networks:
      - mems-net

networks:
  mems-net:
    driver: bridge

volumes:
  mosquitto-data:
  influxdb-storage:"""
}

TECHNICAL_BIOGRAPHY = """# TECHNICAL BIOGRAPHY

**[STUDENT FULL NAME]** is a final-year Bachelor of Engineering candidate in the Department of Electronics and Communication Engineering at [NAME OF THE AFFILIATED ENGINEERING COLLEGE / INSTITUTE], affiliated with [NAME OF THE AFFILIATING TECHNICAL UNIVERSITY]. 

His academic specializations and engineering research interests include Embedded Systems Design, Micro-Electro-Mechanical Systems (MEMS) Instrumentation, Digital Signal Processing, Industrial Internet of Things (IIoT), and Edge Artificial Intelligence (TinyML). 

Throughout his undergraduate engineering tenure, he has engineered diverse cyber-physical systems, authored technical implementations in C++, Python, and modern JavaScript, and conducted empirical investigations into kinetic energy harvesting and fault diagnostics in electromechanical systems. Following graduation, he intends to pursue advanced industrial research and professional engineering leadership in intelligent cyber-physical systems, autonomous robotics, and predictive maintenance infrastructure."""
