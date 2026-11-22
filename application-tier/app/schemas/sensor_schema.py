from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SensorMetrics(BaseModel):
    vibration_x: Optional[float] = Field(None, description="Acceleration X in m/s²")
    vibration_y: Optional[float] = Field(None, description="Acceleration Y in m/s²")
    vibration_z: Optional[float] = Field(None, description="Acceleration Z in m/s²")
    gyro_x: Optional[float] = Field(None, description="Angular velocity X in rad/s")
    gyro_y: Optional[float] = Field(None, description="Angular velocity Y in rad/s")
    gyro_z: Optional[float] = Field(None, description="Angular velocity Z in rad/s")
    temperature: Optional[float] = Field(None, description="Motor surface temperature in °C")
    current: Optional[float] = Field(None, description="Electrical current draw in Amperes")
    piezo_voltage: Optional[float] = Field(None, description="Harvested piezoelectric open-circuit voltage in Volts")
    # Additional optional waveform buffer for live FFT display
    waveform_samples: Optional[List[float]] = Field(None, description="High-frequency acceleration waveform window for FFT")

class SensorDataPayload(BaseModel):
    device_id: str = Field(..., example="ESP32_001")
    machine_id: str = Field(..., example="MOTOR_001")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = Field("simulation", example="simulation", description="'simulation' or 'hardware'")
    sensors: SensorMetrics

class SensorReadingResponse(BaseModel):
    id: Optional[int] = None
    device_id: str
    machine_id: str
    timestamp: datetime
    source: str
    vibration_x: Optional[float] = None
    vibration_y: Optional[float] = None
    vibration_z: Optional[float] = None
    vibration_rms: Optional[float] = None
    gyro_x: Optional[float] = None
    gyro_y: Optional[float] = None
    gyro_z: Optional[float] = None
    temperature: Optional[float] = None
    current: Optional[float] = None
    piezo_voltage: Optional[float] = None
    machine_status: Optional[str] = "NORMAL"

class MachineBase(BaseModel):
    id: str
    machine_name: str
    device_id: str
    motor_type: Optional[str] = "DC Brushless Industrial Motor"
    status: Optional[str] = "NORMAL"

class MachineCreate(MachineBase):
    pass

class MachineResponse(MachineBase):
    installation_date: datetime
    active_alerts_count: Optional[int] = 0

    class Config:
        from_attributes = True

class SensorThresholdConfig(BaseModel):
    sensor_name: str
    warning_threshold: float
    critical_threshold: float
    calibration_value: Optional[float] = 1.0

class AlertCreate(BaseModel):
    machine_id: str
    alert_type: str
    severity: str
    description: str
    sensor_value: Optional[float] = None
    timestamp: Optional[datetime] = None

class AlertResponse(BaseModel):
    id: int
    machine_id: str
    alert_type: str
    severity: str
    description: str
    sensor_value: Optional[float] = None
    timestamp: datetime
    status: str
    suggested_action: Optional[str] = None

    class Config:
        from_attributes = True

class SimulationControl(BaseModel):
    action: str = Field(..., example="start", description="'start', 'stop', or 'set_mode'")
    mode: Optional[str] = Field(None, example="normal", description="'normal', 'high_vibration', 'overheating', 'high_current', 'multi_fault'")
    interval_seconds: Optional[float] = Field(1.0, ge=0.2, le=10.0)

class AnalyticsSummary(BaseModel):
    machine_id: str
    health_score: float # 0 - 100%
    overall_status: str # NORMAL, WARNING, CRITICAL
    mean_vibration_rms: float
    max_vibration_rms: float
    mean_temperature: float
    max_temperature: float
    mean_current: float
    peak_current: float
    mean_piezo_voltage: float
    estimated_energy_harvested_uj: float # Microjoules
    total_alerts_24h: int
    active_warnings: int
    active_criticals: int
    data_source: str
    influxdb_available: bool

class VibrationAnalytics(BaseModel):
    machine_id: str
    rms: float
    peak_to_peak: float
    crest_factor: float
    dominant_frequency_hz: float
    spectrum_frequencies: List[float]
    spectrum_amplitudes: List[float]
    iso_vibration_severity_zone: str # Zone A (Good), Zone B (Acceptable), Zone C (Unsatisfactory), Zone D (Unacceptable)
