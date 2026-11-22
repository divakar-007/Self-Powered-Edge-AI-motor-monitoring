from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.sqlite_database import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(String(50), primary_key=True, index=True) # e.g. "MOTOR_001"
    machine_name = Column(String(100), nullable=False)
    device_id = Column(String(50), nullable=False, index=True) # e.g. "ESP32_001"
    motor_type = Column(String(100), default="DC Brushless Industrial Motor")
    installation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="NORMAL") # NORMAL, WARNING, CRITICAL, OFFLINE

    configurations = relationship("SensorConfiguration", back_populates="machine", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="machine", cascade="all, delete-orphan")

class SensorConfiguration(Base):
    __tablename__ = "sensor_configurations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(String(50), ForeignKey("machines.id"), nullable=False)
    sensor_name = Column(String(50), nullable=False) # vibration, temperature, current, piezo_voltage
    warning_threshold = Column(Float, nullable=False)
    critical_threshold = Column(Float, nullable=False)
    calibration_value = Column(Float, default=1.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    machine = relationship("Machine", back_populates="configurations")
