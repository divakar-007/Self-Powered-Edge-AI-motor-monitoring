# ESP32-S3 Edge Firmware – Multimodal MEMS Sensor Node

This directory contains the production-ready C++ firmware for the **ESP32-S3** microcontroller edge node.

---

## 1. Features
- **Multimodal Sensor Sampling**:
  - **MPU6050** via hardware I2C (`Wire` bus at 400kHz) for 3-axis vibration acceleration & angular rate.
  - **DS18B20** via OneWire protocol with high-resolution digital temperature acquisition.
  - **ACS712** current sensor via calibrated ADC sampling with 32x oversampling and hardware voltage divider compensation.
  - **Piezoelectric Transducer** conditioned via full-wave Schottky bridge rectifier and 3.3V Zener over-voltage clamping.
- **Adaptive MQTT Telemetry**:
  - Automatically reconnects on network or broker interruption.
  - Publishes serialized JSON payloads to `mems/motor001/sensors`.
  - Publishes device heartbeat and status to `mems/motor001/status`.
  - Flags all physical hardware readings explicitly with `"source": "hardware"`.

---

## 2. Hardware Pinout Reference (ESP32-S3)

| Component | Signal | ESP32-S3 Pin | Voltage Level | Notes / Conditioning Required |
|-----------|--------|--------------|---------------|-------------------------------|
| **MPU6050** | VCC | 3.3V | 3.3V | Connect to ESP32 3V3 rail |
| | GND | GND | 0V | Common Ground |
| | SDA | GPIO 8 | 3.3V | Internal/External 4.7k pull-up |
| | SCL | GPIO 9 | 3.3V | Internal/External 4.7k pull-up |
| **DS18B20** | VDD | 3.3V | 3.3V | Connect to 3.3V rail |
| | GND | GND | 0V | Common Ground |
| | DATA | GPIO 4 | 3.3V | **Requires 4.7kΩ pull-up to 3.3V** |
| **ACS712** | VCC | 5.0V (VBUS) | 5.0V | Powers internal Hall IC |
| | GND | GND | 0V | Common Ground |
| | OUT | GPIO 1 (ADC1_0)| **Conditioned** | **CRITICAL: 10k/20k voltage divider to protect 3.3V ADC!** |
| **Piezo Transducer**| + / - | GPIO 2 (ADC1_1)| **Conditioned** | **CRITICAL: Schottky bridge + 3.3V Zener diode clamp!** |

---

## 3. Important Electrical & Safety Guidelines

> [!CAUTION]
> **Voltage Divider Protection for ACS712:**
> The ACS712 operates at 5.0V. At 0A, its quiescent output is ~2.5V ($V_{CC}/2$), and under current surges it can reach 4.5V+!
> Directly wiring ACS712 `OUT` to the ESP32-S3 ADC pin will damage the microcontroller.
> **You MUST connect a voltage divider**:
> $$R_1 = 10\,\text{k}\Omega,\quad R_2 = 20\,\text{k}\Omega$$
> Connect $R_1$ between ACS712 `OUT` and ESP32 GPIO 1. Connect $R_2$ between GPIO 1 and GND.

> [!CAUTION]
> **Piezoelectric Transducer Spike Protection:**
> Piezoelectric elements generate high-voltage transient spikes when struck or vibrated violently.
> Do NOT connect the bare piezo disc directly to an ADC pin.
> Use a full-wave bridge rectifier (4x 1N5819 Schottky diodes), a $10\,\mu\text{F}$ capacitor, and a **3.3V Zener diode (1N4728A)** across the positive and negative terminals to clamp voltage strictly below 3.3V.

> [!NOTE]
> **Power Supply:**
> The prototype is powered via the ESP32-S3 USB-C cable (5V, 1A). Do not attempt to run the ESP32 solely off the piezoelectric transducer in this prototype phase.

---

## 4. How to Compile & Flash

### Prerequisites
1. Download and install **Arduino IDE 2.x** (or VS Code with PlatformIO).
2. Install **ESP32 Board Package** (`esp32` by Espressif Systems v2.0.14+).
3. Select Board: **ESP32-S3 Dev Module**.
4. In Arduino Library Manager, install:
   - `PubSubClient` by Nick O'Leary
   - `ArduinoJson` by Benoit Blanchon (v6 or v7)
   - `Adafruit MPU6050` & `Adafruit Unified Sensor`
   - `OneWire` by Paul Stoffregen
   - `DallasTemperature` by Miles Burton

### Flashing Steps
1. Open `esp32_s3_mems_node.ino` in Arduino IDE.
2. Edit `config.h`: Set `WIFI_SSID`, `WIFI_PASSWORD`, and `MQTT_BROKER_IP`.
3. Connect ESP32-S3 via USB-C.
4. Select the matching COM port.
5. Click **Upload**.
6. Open the Serial Monitor at **115200 baud** to verify telemetry packets.
