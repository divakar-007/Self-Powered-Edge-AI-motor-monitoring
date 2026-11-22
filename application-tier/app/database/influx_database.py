import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.config import settings

logger = logging.getLogger(__name__)

class InfluxDBManager:
    def __init__(self):
        self.client = None
        self.write_api = None
        self.query_api = None
        self.is_connected = False
        self.last_error = None
        self._init_client()

    def _init_client(self):
        try:
            from influxdb_client import InfluxDBClient
            from influxdb_client.client.write_api import SYNCHRONOUS

            self.client = InfluxDBClient(
                url=settings.INFLUXDB_URL,
                token=settings.INFLUXDB_TOKEN,
                org=settings.INFLUXDB_ORG,
                timeout=3000
            )
            # Verify connectivity via health check
            health = self.client.health()
            if health.status == "pass":
                self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
                self.query_api = self.client.query_api()
                self.is_connected = True
                self.last_error = None
                logger.info(f"Connected to InfluxDB at {settings.INFLUXDB_URL}")
            else:
                self.is_connected = False
                self.last_error = f"InfluxDB health status: {health.status}"
                logger.warning(f"InfluxDB health check failed: {health.status}. Falling back to SQLite.")
        except Exception as e:
            self.is_connected = False
            self.last_error = str(e)
            logger.warning(f"InfluxDB is unavailable at {settings.INFLUXDB_URL} ({e}). Running in SQLite-only mode.")

    def write_sensor_reading(
        self,
        device_id: str,
        machine_id: str,
        timestamp: datetime,
        sensors: Dict[str, Any],
        vibration_rms: float,
        source: str = "simulation"
    ) -> bool:
        if not self.is_connected or not self.write_api:
            return False

        try:
            from influxdb_client import Point

            point = (
                Point("motor_sensor_data")
                .tag("device_id", device_id)
                .tag("machine_id", machine_id)
                .tag("source", source)
                .time(timestamp)
            )

            # Numerical fields
            numeric_fields = [
                "vibration_x", "vibration_y", "vibration_z",
                "gyro_x", "gyro_y", "gyro_z",
                "temperature", "current", "piezo_voltage"
            ]

            for field in numeric_fields:
                val = sensors.get(field)
                if val is not None:
                    point.field(field, float(val))

            point.field("vibration_rms", float(vibration_rms))

            self.write_api.write(bucket=settings.INFLUXDB_BUCKET, org=settings.INFLUXDB_ORG, record=point)
            return True
        except Exception as e:
            logger.error(f"Failed to write to InfluxDB: {e}")
            self.is_connected = False
            self.last_error = str(e)
            return False

    def query_history(self, machine_id: str, start_time: str = "-1h") -> List[Dict[str, Any]]:
        if not self.is_connected or not self.query_api:
            return []

        query = f'''
        from(bucket: "{settings.INFLUXDB_BUCKET}")
          |> range(start: {start_time})
          |> filter(fn: (r) => r["_measurement"] == "motor_sensor_data")
          |> filter(fn: (r) => r["machine_id"] == "{machine_id}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> sort(columns: ["_time"], desc: false)
        '''
        try:
            tables = self.query_api.query(query, org=settings.INFLUXDB_ORG)
            results = []
            for table in tables:
                for record in table.records:
                    results.append(record.values)
            return results
        except Exception as e:
            logger.error(f"Error querying InfluxDB: {e}")
            return []

    def get_status(self) -> Dict[str, Any]:
        return {
            "connected": self.is_connected,
            "url": settings.INFLUXDB_URL,
            "org": settings.INFLUXDB_ORG,
            "bucket": settings.INFLUXDB_BUCKET,
            "error": self.last_error
        }

influx_db = InfluxDBManager()
