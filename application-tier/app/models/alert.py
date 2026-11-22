from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.sqlite_database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    machine_id = Column(String(50), ForeignKey("machines.id"), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False) # VIBRATION, TEMPERATURE, CURRENT, PIEZO_VOLTAGE, MULTI_FAULT
    severity = Column(String(20), nullable=False) # WARNING, CRITICAL
    description = Column(String(255), nullable=False)
    sensor_value = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20), default="ACTIVE") # ACTIVE, ACKNOWLEDGED, RESOLVED

    machine = relationship("Machine", back_populates="alerts")
