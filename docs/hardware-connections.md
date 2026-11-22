# Hardware Connections, Conditioning & Electrical Safety Guide

**Target Microcontroller:** ESP32-S3 (Dual-Core Xtensa LX7 @ 240MHz, 3.3V Logic)  
**Target Motor:** 12V Brushed Industrial DC Motor  
**Primary Power Source:** USB-C 5V @ 1.5A to ESP32-S3 Dev Board  
**Motor Power Source:** Regulated Bench DC Power Supply (12V, 2A)

---

## 1. Safety Rules & Precautions

> [!CAUTION]
> 1. **DO NOT CONNECT MAINS VOLTAGE (110V/230V AC)** during prototype testing! Use isolated DC bench power for motor tests.
> 2. **DO NOT CONNECT ACS712 DIRECTLY TO ESP32 ADC**: The ACS712 runs on 5V VCC and outputs up to 4.5V+. Direct connection will fry the ESP32-S3 ADC pin. You must use a voltage divider.
> 3. **DO NOT CONNECT UNCONDITIONED PIEZO TRANSDUCERS**: Piezo discs generate high-voltage spikes (10V-30V transient) upon shock. Use the clamp and rectifier circuit shown below.
> 4. **COMMON GROUND**: Connect GND of the ESP32-S3, DC motor power supply, and sensor breakout boards together to ensure a shared 0V reference.

---

## 2. Master Wiring Table

| Component | Sensor Pin | ESP32-S3 Pin | Voltage Level | Signal Conditioning Circuitry |
| :--- | :--- | :--- | :--- | :--- |
| **MPU6050** | VCC | 3V3 | 3.3V DC | Powered from ESP32 3.3V rail |
| | GND | GND | 0V | Common Ground |
| | SDA | GPIO 8 | 3.3V I2C | 4.7 kΩ pull-up to 3.3V |
| | SCL | GPIO 9 | 3.3V I2C | 4.7 kΩ pull-up to 3.3V |
| **DS18B20** | VDD | 3V3 | 3.3V DC | Powered from 3.3V rail |
| | GND | GND | 0V | Common Ground |
| | DATA | GPIO 4 | 3.3V OneWire | **Requires 4.7 kΩ pull-up resistor between DATA and 3V3** |
| **ACS712** | VCC | 5V (VBUS) | 5.0V DC | Powered from USB 5V rail |
| | GND | GND | 0V | Common Ground |
| | OUT | GPIO 1 (ADC1_0) | **Conditioned** | **Voltage divider: $R_1=10\,\text{k}\Omega$, $R_2=20\,\text{k}\Omega$ to GND** |
| | IP+ / IP- | Motor Series | DC Load (12V) | In series with Motor (+) positive lead |
| **Piezo Transducer** | Terminals | GPIO 2 (ADC1_1) | **Conditioned** | **Schottky Bridge + $10\,\mu\text{F}$ cap + 3.3V Zener diode clamp** |

---

## 3. Signal Conditioning Circuits

### A. ACS712 Current Sensor 5V-to-3.3V Conditioning
The ACS712 operates at 5.0V and outputs $V_{out} = 2.50\,\text{V} + (I \times \text{Sensitivity})$.  
At 2.5A, $V_{out} \approx 2.96\,\text{V}$. At peak or reverse transients, $V_{out}$ can reach 4.5V+.  
To keep the maximum output safely below the ESP32 ADC limit ($3.3\,\text{V}$), use a precise 2:3 resistive voltage divider:

```
ACS712 OUT (0 - 5V)
        |
      [10kΩ] (R1)
        |
        +-----> Connect to ESP32-S3 GPIO 1 (ADC1_CH0)
        |
      [20kΩ] (R2)
        |
       GND
```

**Transfer Function:**
$$V_{ADC} = V_{OUT} \times \frac{R_2}{R_1 + R_2} = V_{OUT} \times \frac{20}{10 + 20} = 0.667 \times V_{OUT}$$
When $V_{OUT} = 5.0\,\text{V}$, $V_{ADC} = 3.33\,\text{V}$. Safe for the ESP32-S3.

---

### B. Piezoelectric Harvester Protection & Clamping Circuit
Piezoelectric transducers produce AC spikes that must be rectified and bounded:

```
  Piezo Disc (+) ────+
                     │
              [1N5819 Bridge]
              (4x Schottky)
                     │
  Piezo Disc (-) ────+
                     │
                     +────┬────────┬────────┬───────> Connect to ESP32-S3 GPIO 2
                          │ +      │        │
                       [10µF]    [100kΩ]  [3.3V Zener]
                       (Filter)  (Load)   (1N4728A Clamp)
                          │        │        │
                     ─────┴────────┴────────┴───────> Common GND
```

- **Schottky Bridge (1N5819)**: Low forward voltage drop ($V_f \approx 0.2\,\text{V}$) ensures minimal scavenging loss during AC-to-DC conversion.
- **Smoothing Capacitor ($10\,\mu\text{F}$, 25V)**: Filters vibration pulses into a measurable DC voltage level.
- **Bleed Load ($100\,\text{k}\Omega$)**: Represents an electrical load resistance to evaluate instantaneous power.
- **3.3V Zener Diode (1N4728A)**: Clamps any extreme mechanical shock spikes safely to 3.3V.

---

## 4. Future Autonomous Energy Harvesting Subsystem Design

```
+--------------------+      +--------------------+      +--------------------+
| Piezo Scavenger    | ---> | LTC3588-1 /        | ---> | Supercapacitor     | ---> ESP32-S3
| Micro-Generator    |      | Nanopower Harvester|      | Bank (0.1F - 1.0F) |      Deep-Sleep
+--------------------+      +--------------------+      +--------------------+      Duty Cycle
```

For true energy autonomy in future revisions:
1. Replace discrete diodes with an integrated **LTC3588-1** Piezoelectric Energy Harvesting Power Supply IC with internal low-loss bridge rectifier and high-efficiency buck converter.
2. Store harvested energy in a **5.5V, 0.47F supercapacitor**.
3. Operate the ESP32-S3 in deep sleep (drawing $< 10\,\mu\text{A}$), waking up every 60 seconds to sample sensors and burst-publish via ESP-NOW / MQTT.
