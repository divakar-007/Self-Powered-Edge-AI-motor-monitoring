import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "MEMS Industrial Monitoring System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    # SQLite
    SQLITE_DB_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data-tier",
        "sqlite",
        "mems_industrial.db"
    )

    # InfluxDB
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = "mems-industrial-secret-token-2026"
    INFLUXDB_ORG: str = "mems_org"
    INFLUXDB_BUCKET: str = "motor_telemetry"

    # MQTT
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_KEEP_ALIVE: int = 60
    MQTT_TOPIC_SENSORS: str = "mems/motor001/sensors"
    MQTT_TOPIC_STATUS: str = "mems/motor001/status"
    MQTT_TOPIC_ALERTS: str = "mems/motor001/alerts"

    # Machine Identifiers
    DEFAULT_MACHINE_ID: str = "MOTOR_001"
    DEFAULT_DEVICE_ID: str = "ESP32_001"

    # Default Thresholds
    THRESHOLD_TEMP_WARNING: float = 45.0
    THRESHOLD_TEMP_CRITICAL: float = 60.0
    THRESHOLD_VIB_WARNING: float = 3.0
    THRESHOLD_VIB_CRITICAL: float = 5.0
    THRESHOLD_CURRENT_WARNING: float = 1.0
    THRESHOLD_CURRENT_CRITICAL: float = 1.5
    THRESHOLD_PIEZO_WARNING: float = 3.8
    THRESHOLD_PIEZO_CRITICAL: float = 4.5

    # Simulator
    SIMULATOR_INTERVAL_SECONDS: float = 1.0
    SIMULATOR_AUTO_START: bool = True

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
