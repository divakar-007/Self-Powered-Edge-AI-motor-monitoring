from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database.sqlite_database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    device_id = Column(String(50), nullable=False, index=True)
    machine_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    source = Column(String(20), default="simulation") # simulation or hardware

    vibration_x = Column(Float, nullable=True)
    vibration_y = Column(Float, nullable=True)
    vibration_z = Column(Float, nullable=True)
    vibration_rms = Column(Float, nullable=True)
    gyro_x = Column(Float, nullable=True)
    gyro_y = Column(Float, nullable=True)
    gyro_z = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
    piezo_voltage = Column(Float, nullable=True)
