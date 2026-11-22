/**
 * @file esp32_s3_mems_node.ino
 * @brief Self-Powered Multimodal MEMS Sensor Node Firmware for ESP32-S3
 * @details Collects MPU6050 (Vibration/Motion), DS18B20 (Temperature),
 *          ACS712 (Current), and Piezoelectric Transducer (Voltage) readings,
 *          formats to JSON and publishes via MQTT to the Application Tier backend.
 *
 * Required Libraries:
 * - PubSubClient (by Nick O'Leary)
 * - ArduinoJson (by Benoit Blanchon, v6 or v7)
 * - Adafruit MPU6050 & Adafruit BusIO
 * - OneWire (by Paul Stoffregen)
 * - DallasTemperature (by Miles Burton)
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

#include "config.h"

// Hardware instances
WiFiClient espClient;
PubSubClient mqttClient(espClient);
Adafruit_MPU6050 mpu;
OneWire oneWire(PIN_ONEWIRE_TEMP);
DallasTemperature tempSensor(&oneWire);

// Timing variables
unsigned long lastPublishTime = 0;
unsigned long lastReconnectAttempt = 0;

// Sensor calibration offsets
float acs712_zero_voltage = 2.50; // Calibrated 0A voltage at 5V rail

// Function Prototypes
void setupWiFi();
void reconnectMQTT();
void readAndPublishSensors();
float readACS712Current();
float readPiezoVoltage();

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println(F("\n=============================================="));
  Serial.println(F("  MEMS Industrial Sensor Node - ESP32-S3"));
  Serial.println(F("  Multimodal Vibration, Temp, Current & Piezo"));
  Serial.println(F("=============================================="));

  pinMode(PIN_STATUS_LED, OUTPUT);
  pinMode(PIN_ADC_CURRENT, INPUT);
  pinMode(PIN_ADC_PIEZO, INPUT);

  // Set ADC attenuation to 11dB (allows up to ~3.1-3.3V measurement range)
  analogSetAttenuation(ADC_11db);

  // Initialize I2C for MPU6050
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL, 400000); // Fast mode 400kHz
  if (!mpu.begin(0x68, &Wire)) {
    Serial.println(F("[-] Warning: MPU6050 sensor not found on I2C bus!"));
  } else {
    Serial.println(F("[+] MPU6050 initialized successfully."));
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);
  }

  // Initialize DS18B20 OneWire Temperature
  tempSensor.begin();
  Serial.println(F("[+] DS18B20 temperature sensor bus initialized."));

  // Connect to WiFi
  setupWiFi();

  // Configure MQTT
  mqttClient.setServer(MQTT_BROKER_IP, MQTT_BROKER_PORT);
  mqttClient.setBufferSize(1024); // Expand buffer for JSON payload
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    setupWiFi();
  }

  if (!mqttClient.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > 5000) {
      lastReconnectAttempt = now;
      reconnectMQTT();
    }
  } else {
    mqttClient.loop();
  }

  // Periodic Telemetry Publishing
  unsigned long currentMillis = millis();
  if (currentMillis - lastPublishTime >= PUBLISH_INTERVAL_MS) {
    lastPublishTime = currentMillis;
    readAndPublishSensors();
  }
}

void setupWiFi() {
  Serial.print(F("[*] Connecting to WiFi SSID: "));
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(F("."));
    digitalWrite(PIN_STATUS_LED, !digitalRead(PIN_STATUS_LED));
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(F("\n[+] WiFi Connected!"));
    Serial.print(F("[+] IP Address: "));
    Serial.println(WiFi.localIP());
    digitalWrite(PIN_STATUS_LED, HIGH);
  } else {
    Serial.println(F("\n[-] WiFi Connection Timeout. Node will continue and retry."));
  }
}

void reconnectMQTT() {
  Serial.print(F("[*] Connecting to MQTT Broker: "));
  Serial.print(MQTT_BROKER_IP);
  Serial.print(F(":"));
  Serial.println(MQTT_BROKER_PORT);

  if (mqttClient.connect(MQTT_CLIENT_ID)) {
    Serial.println(F("[+] Connected to Mosquitto MQTT Broker!"));
    
    // Publish online status
    StaticJsonDocument<256> statusDoc;
    statusDoc["device_id"] = DEVICE_ID;
    statusDoc["machine_id"] = MACHINE_ID;
    statusDoc["status"] = "ONLINE";
    statusDoc["firmware"] = FIRMWARE_VERSION;
    statusDoc["ip"] = WiFi.localIP().toString();

    char statusBuffer[256];
    serializeJson(statusDoc, statusBuffer);
    mqttClient.publish(MQTT_TOPIC_STATUS, statusBuffer, true);
  } else {
    Serial.print(F("[-] MQTT connection failed, rc="));
    Serial.println(mqttClient.state());
  }
}

void readAndPublishSensors() {
  // 1. Read MPU6050
  sensors_event_t a, g, temp_mpu;
  float ax = 0.0, ay = 0.0, az = 0.0;
  float gx = 0.0, gy = 0.0, gz = 0.0;

  if (mpu.getEvent(&a, &g, &temp_mpu)) {
    ax = a.acceleration.x;
    ay = a.acceleration.y;
    az = a.acceleration.z;
    gx = g.gyro.x;
    gy = g.gyro.y;
    gz = g.gyro.z;
  }

  // 2. Read DS18B20 Temperature
  tempSensor.requestTemperatures();
  float motorTemp = tempSensor.getTempCByIndex(0);
  if (motorTemp == DEVICE_DISCONNECTED_C || motorTemp < -50.0) {
    motorTemp = 0.0; // Mark disconnected
  }

  // 3. Read Conditioned ACS712 Current
  float currentAmps = readACS712Current();

  // 4. Read Piezoelectric Transducer Voltage
  float piezoVolts = readPiezoVoltage();

  // 5. Serialize to JSON matching backend schema
  StaticJsonDocument<768> doc;
  doc["device_id"] = DEVICE_ID;
  doc["machine_id"] = MACHINE_ID;
  doc["source"] = "hardware"; // Explicitly identifies physical hardware telemetry

  JsonObject sensors = doc.createNestedObject("sensors");
  sensors["vibration_x"] = round(ax * 100.0) / 100.0;
  sensors["vibration_y"] = round(ay * 100.0) / 100.0;
  sensors["vibration_z"] = round(az * 100.0) / 100.0;
  sensors["gyro_x"] = round(gx * 1000.0) / 1000.0;
  sensors["gyro_y"] = round(gy * 1000.0) / 1000.0;
  sensors["gyro_z"] = round(gz * 1000.0) / 1000.0;
  sensors["temperature"] = round(motorTemp * 10.0) / 10.0;
  sensors["current"] = round(currentAmps * 100.0) / 100.0;
  sensors["piezo_voltage"] = round(piezoVolts * 100.0) / 100.0;

  char jsonBuffer[768];
  size_t len = serializeJson(doc, jsonBuffer);

  // Publish to MQTT
  if (mqttClient.connected()) {
    bool published = mqttClient.publish(MQTT_TOPIC_SENSORS, jsonBuffer);
    if (!published) {
      Serial.println(F("[-] Failed to publish MQTT telemetry packet."));
    }
  }

  // Print diagnostic log
  Serial.print(F("[TELEMETRY] Vib_Z: "));
  Serial.print(az, 2);
  Serial.print(F(" m/s2 | Temp: "));
  Serial.print(motorTemp, 1);
  Serial.print(F(" C | Current: "));
  Serial.print(currentAmps, 2);
  Serial.print(F(" A | Piezo: "));
  Serial.print(piezoVolts, 2);
  Serial.println(F(" V"));
}

float readACS712Current() {
  // Read and average 32 ADC samples to filter switching noise
  long sum = 0;
  for (int i = 0; i < 32; i++) {
    sum += analogRead(PIN_ADC_CURRENT);
    delayMicroseconds(50);
  }
  float avgRaw = (float)sum / 32.0;

  // Convert ESP32 ADC reading to voltage at ADC pin
  float vPin = (avgRaw / ADC_RESOLUTION) * ADC_MAX_VOLTAGE;

  // Compensate for 20k / (10k + 20k) voltage divider
  float vSensorOut = vPin / ACS712_DIVIDER_RATIO;

  // Convert voltage offset to current: I = (V_out - V_zero) / Sensitivity
  float current = (vSensorOut - acs712_zero_voltage) / ACS712_SENSITIVITY;

  return abs(current);
}

float readPiezoVoltage() {
  // Read rectified and clamped piezoelectric transducer voltage
  long sum = 0;
  for (int i = 0; i < 16; i++) {
    sum += analogRead(PIN_ADC_PIEZO);
    delayMicroseconds(50);
  }
  float avgRaw = (float)sum / 16.0;
  float voltage = (avgRaw / ADC_RESOLUTION) * ADC_MAX_VOLTAGE;
  return voltage;
}
