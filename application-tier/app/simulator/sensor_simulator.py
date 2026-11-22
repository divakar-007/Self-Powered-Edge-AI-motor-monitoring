import asyncio
import logging
import math
import random
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import numpy as np

from app.config import settings
from app.services.sensor_service import sensor_service

logger = logging.getLogger(__name__)

class MotorSimulatorMode:
    NORMAL = "normal"
    HIGH_VIBRATION = "high_vibration"
    OVERHEATING = "overheating"
    HIGH_CURRENT = "high_current"
    MULTI_FAULT = "multi_fault"

class SensorSimulator:
    def __init__(self):
        self.is_running: bool = False
        self.mode: str = MotorSimulatorMode.NORMAL
        self.interval_seconds: float = settings.SIMULATOR_INTERVAL_SECONDS
        self._task: Optional[asyncio.Task] = None

        # State memory for smooth continuous dynamic evolution
        self.motor_temperature: float = 34.0
        self.time_step: float = 0.0

    def set_mode(self, new_mode: str) -> str:
        valid_modes = [
            MotorSimulatorMode.NORMAL,
            MotorSimulatorMode.HIGH_VIBRATION,
            MotorSimulatorMode.OVERHEATING,
            MotorSimulatorMode.HIGH_CURRENT,
            MotorSimulatorMode.MULTI_FAULT
        ]
        if new_mode in valid_modes:
            self.mode = new_mode
            logger.info(f"Sensor simulator mode set to: {new_mode}")
            return new_mode
        else:
            raise ValueError(f"Invalid mode: {new_mode}. Must be one of {valid_modes}")

    def generate_reading(self) -> Dict[str, Any]:
        """
        Generates realistic physics-correlated sensor measurements for a DC motor.
        """
        self.time_step += 0.2
        t = self.time_step

        # Default normal ranges
        base_vib = 1.0 + 0.3 * math.sin(t * 1.5) + random.uniform(-0.15, 0.15)
        target_temp = 38.0 + 2.0 * math.sin(t * 0.2)
        target_current = 0.55 + 0.08 * math.sin(t * 2.0) + random.uniform(-0.03, 0.03)

        # Apply specific anomaly behaviors based on current mode
        if self.mode == MotorSimulatorMode.HIGH_VIBRATION:
            # Mechanical imbalance & bearing defect harmonics
            base_vib = 4.8 + 1.6 * math.sin(t * 5.0) + 0.8 * math.sin(t * 12.0) + random.uniform(-0.3, 0.3)
            target_current += 0.25 # extra friction

        elif self.mode == MotorSimulatorMode.OVERHEATING:
            # Thermal runaway / cooling failure
            target_temp = 64.0 + 3.0 * math.sin(t * 0.5) + random.uniform(-0.5, 0.5)
            base_vib += 0.6 # slight thermal expansion vibration

        elif self.mode == MotorSimulatorMode.HIGH_CURRENT:
            # Mechanical overload / rotor binding / high mechanical torque
            target_current = 1.65 + 0.25 * math.sin(t * 3.0) + random.uniform(-0.05, 0.05)
            target_temp = 52.0 + 1.5 * math.sin(t * 0.3) # I^2 * R heating

        elif self.mode == MotorSimulatorMode.MULTI_FAULT:
            # Compound extreme failure mode
            base_vib = 5.8 + 2.0 * math.sin(t * 6.0) + random.uniform(-0.4, 0.4)
            target_temp = 68.0 + 2.5 * math.sin(t * 0.4)
            target_current = 1.85 + 0.3 * math.sin(t * 2.5)

        # Thermal inertia: temperature changes smoothly, not instantly
        self.motor_temperature += (target_temp - self.motor_temperature) * 0.08

        # 3-Axis Vibration (MPU6050)
        # Z axis typically captures perpendicular mounting vibration strongest
        vx = max(0.1, round(base_vib * 0.7 + random.uniform(-0.1, 0.1), 2))
        vy = max(0.1, round(base_vib * 0.6 + random.uniform(-0.1, 0.1), 2))
        vz = max(0.2, round(base_vib * 1.2 + random.uniform(-0.15, 0.15), 2))

        # Gyroscope (angular velocity)
        gyro_scale = 0.1 if self.mode == MotorSimulatorMode.NORMAL else 0.45
        gx = round(gyro_scale * math.cos(t * 1.8) + random.uniform(-0.02, 0.02), 3)
        gy = round(gyro_scale * math.sin(t * 1.8) + random.uniform(-0.02, 0.02), 3)
        gz = round(gyro_scale * 1.2 * math.cos(t * 2.5) + random.uniform(-0.03, 0.03), 3)

        # Temperature (DS18B20)
        temp_val = round(self.motor_temperature + random.uniform(-0.1, 0.1), 1)

        # Electrical Current (ACS712)
        current_val = round(max(0.1, target_current), 2)

        # Piezoelectric Harvester Transducer:
        # Generated open-circuit voltage correlates directly with vibration amplitude
        # V_piezo = k * a_vib + noise, capped at 5.0V zener protection
        piezo_v = round(min(4.8, max(0.3, 0.85 * base_vib + random.uniform(-0.1, 0.2))), 2)

        # High-frequency waveform samples (64 points) for live FFT visualization
        freq_fund = 50.0 if self.mode == MotorSimulatorMode.NORMAL else 120.0
        wave_t = np.linspace(0, 0.064, 64)
        synthetic_waveform = (
            base_vib * np.sin(2 * np.pi * freq_fund * wave_t) +
            (0.5 * base_vib) * np.sin(2 * np.pi * 2 * freq_fund * wave_t) +
            0.15 * np.random.randn(64)
        ).tolist()

        payload = {
            "device_id": settings.DEFAULT_DEVICE_ID,
            "machine_id": settings.DEFAULT_MACHINE_ID,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "simulation",
            "sensors": {
                "vibration_x": vx,
                "vibration_y": vy,
                "vibration_z": vz,
                "gyro_x": gx,
                "gyro_y": gy,
                "gyro_z": gz,
                "temperature": temp_val,
                "current": current_val,
                "piezo_voltage": piezo_v,
                "waveform_samples": synthetic_waveform
            }
        }
        return payload

    async def _run_loop(self):
        logger.info(f"Sensor simulator started. Interval: {self.interval_seconds}s. Mode: {self.mode}")
        while self.is_running:
            try:
                payload = self.generate_reading()
                await sensor_service.ingest_sensor_data(payload)
            except Exception as e:
                logger.error(f"Error in sensor simulator tick: {e}", exc_info=True)

            await asyncio.sleep(self.interval_seconds)

    def start(self, interval: Optional[float] = None) -> bool:
        if interval:
            self.interval_seconds = interval

        if not self.is_running:
            self.is_running = True
            self._task = asyncio.create_task(self._run_loop())
            logger.info("Sensor simulator task launched.")
            return True
        return False

    def stop(self) -> bool:
        if self.is_running:
            self.is_running = False
            if self._task and not self._task.done():
                self._task.cancel()
            logger.info("Sensor simulator stopped.")
            return True
        return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self.is_running,
            "mode": self.mode,
            "interval_seconds": self.interval_seconds,
            "source": "simulation",
            "total_readings": sensor_service.total_readings_processed
        }

sensor_simulator = SensorSimulator()
