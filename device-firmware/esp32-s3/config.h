#ifndef CONFIG_H
#define CONFIG_H

// ==========================================
// WiFi & Network Configuration
// ==========================================
#define WIFI_SSID           "YOUR_WIFI_SSID"
#define WIFI_PASSWORD       "YOUR_WIFI_PASSWORD"

// ==========================================
// MQTT Broker Configuration
// ==========================================
#define MQTT_BROKER_IP      "192.168.1.100" // IP address of computer running Mosquitto / Backend
#define MQTT_BROKER_PORT    1883
#define MQTT_CLIENT_ID      "ESP32S3_MOTOR_NODE_01"
#define MQTT_TOPIC_SENSORS  "mems/motor001/sensors"
#define MQTT_TOPIC_STATUS   "mems/motor001/status"
#define MQTT_TOPIC_ALERTS   "mems/motor001/alerts"

// ==========================================
// Device & Machine Identification
// ==========================================
#define DEVICE_ID           "ESP32_001"
#define MACHINE_ID          "MOTOR_001"
#define FIRMWARE_VERSION    "1.0.0-PROD"

// ==========================================
// Pin Assignments for ESP32-S3
// ==========================================
// MPU6050 (I2C)
#define PIN_I2C_SDA         8
#define PIN_I2C_SCL         9

// DS18B20 (OneWire)
#define PIN_ONEWIRE_TEMP    4   // Requires 4.7k ohm pull-up to 3.3V

// ACS712 Current Sensor (Analog Input)
// CAUTION: ACS712 outputs VCC/2 (2.5V) at 0A and up to 4.5V+ under load!
// MUST be scaled via a 10k/20k voltage divider to stay below 3.3V ADC max.
#define PIN_ADC_CURRENT     1   // GPIO 1 (ADC1_CH0)

// Piezoelectric Transducer (Analog Input)
// Transducer connected through full-wave Schottky bridge + 3.3V Zener diode clamp
#define PIN_ADC_PIEZO       2   // GPIO 2 (ADC1_CH1)

// Status LED
#define PIN_STATUS_LED      13

// ==========================================
// Sampling Rates & Sensor Calibration
// ==========================================
#define PUBLISH_INTERVAL_MS 1000  // 1 Hz periodic telemetry
#define ADC_MAX_VOLTAGE     3.3
#define ADC_RESOLUTION      4095.0

// ACS712-05B Parameters (5 Amp model: 185 mV/A sensitivity)
// With a 2:3 voltage divider (R1=10k, R2=20k), divider ratio = 20 / (10 + 20) = 0.667
#define ACS712_DIVIDER_RATIO 0.6667
#define ACS712_VCC           5.0
#define ACS712_SENSITIVITY   0.185 // 185 mV per Amp

#endif // CONFIG_H
