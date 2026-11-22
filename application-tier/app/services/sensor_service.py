import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.config import settings
from app.database.sqlite_database import SessionLocal
from app.database.influx_database import influx_db
from app.models.machine import Machine, SensorConfiguration
from app.models.alert import Alert
from app.models.sensor_reading import SensorReading
from app.services.analytics_service import analytics_service
from app.services.fault_detection import fault_detector
from app.websocket.websocket_manager import websocket_manager

logger = logging.getLogger(__name__)

class SensorService:
    def __init__(self):
        self.latest_reading: Optional[Dict[str, Any]] = None
        self.latest_fft: Optional[Dict[str, Any]] = None
        self.total_readings_processed: int = 0

    def init_default_machine(self):
        """Initializes default machine in SQLite if not present."""
        db = SessionLocal()
        try:
            m = db.query(Machine).filter(Machine.id == settings.DEFAULT_MACHINE_ID).first()
            if not m:
                m = Machine(
                    id=settings.DEFAULT_MACHINE_ID,
                    machine_name="Industrial DC Motor - Line 1",
                    device_id=settings.DEFAULT_DEVICE_ID,
                    motor_type="12V Brushed DC Industrial Motor",
                    installation_date=datetime.utcnow(),
                    status="NORMAL"
                )
                db.add(m)
                db.commit()
                logger.info(f"Initialized default machine {settings.DEFAULT_MACHINE_ID} in SQLite.")

            # Seed default configurations if not present
            configs = [
                ("vibration", settings.THRESHOLD_VIB_WARNING, settings.THRESHOLD_VIB_CRITICAL),
                ("temperature", settings.THRESHOLD_TEMP_WARNING, settings.THRESHOLD_TEMP_CRITICAL),
                ("current", settings.THRESHOLD_CURRENT_WARNING, settings.THRESHOLD_CURRENT_CRITICAL),
                ("piezo_voltage", settings.THRESHOLD_PIEZO_WARNING, settings.THRESHOLD_PIEZO_CRITICAL)
            ]
            for s_name, w_th, c_th in configs:
                cfg = db.query(SensorConfiguration).filter(
                    SensorConfiguration.machine_id == settings.DEFAULT_MACHINE_ID,
                    SensorConfiguration.sensor_name == s_name
                ).first()
                if not cfg:
                    cfg = SensorConfiguration(
                        machine_id=settings.DEFAULT_MACHINE_ID,
                        sensor_name=s_name,
                        warning_threshold=w_th,
                        critical_threshold=c_th,
                        calibration_value=1.0
                    )
                    db.add(cfg)
            db.commit()
        except Exception as e:
            logger.error(f"Error seeding machine info: {e}")
            db.rollback()
        finally:
            db.close()

    async def ingest_sensor_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main pipeline for processing data from Simulator, MQTT, or HTTP.
        """
        device_id = payload.get("device_id", settings.DEFAULT_DEVICE_ID)
        machine_id = payload.get("machine_id", settings.DEFAULT_MACHINE_ID)
        source = payload.get("source", "simulation")
        ts = payload.get("timestamp")
        if isinstance(ts, str):
            try:
                timestamp = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            except Exception:
                timestamp = datetime.utcnow()
        elif isinstance(ts, datetime):
            timestamp = ts
        else:
            timestamp = datetime.utcnow()

        sensors = payload.get("sensors", {})
        vx = float(sensors.get("vibration_x", 0.0) or 0.0)
        vy = float(sensors.get("vibration_y", 0.0) or 0.0)
        vz = float(sensors.get("vibration_z", 0.0) or 0.0)

        # 1. Compute Vibration RMS
        vibration_rms = analytics_service.calculate_vibration_rms(vx, vy, vz)

        # 2. Compute FFT if waveform samples are available
        waveform = sensors.get("waveform_samples")
        if waveform:
            self.latest_fft = analytics_service.compute_fft(waveform)

        # 3. Fault Detection & State Evaluation
        eval_result = fault_detector.evaluate_readings(machine_id, sensors, vibration_rms)
        machine_status = eval_result["overall_status"]
        new_alerts = eval_result["new_alerts"]
        recovered_alerts = eval_result["recovered_alerts"]

        # 4. Database Persistence
        db: Session = SessionLocal()
        created_alerts_for_broadcast = []
        try:
            # Update machine status in SQLite
            db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
            if db_machine:
                db_machine.status = machine_status

            # Store any new alerts
            for alert_data in new_alerts:
                alert_obj = Alert(
                    machine_id=machine_id,
                    alert_type=alert_data["alert_type"],
                    severity=alert_data["severity"],
                    description=alert_data["description"],
                    sensor_value=alert_data.get("sensor_value"),
                    timestamp=timestamp,
                    status="ACTIVE"
                )
                db.add(alert_obj)
                db.commit()
                db.refresh(alert_obj)
                alert_payload = {
                    "id": alert_obj.id,
                    "machine_id": alert_obj.machine_id,
                    "alert_type": alert_obj.alert_type,
                    "severity": alert_obj.severity,
                    "description": alert_obj.description,
                    "sensor_value": alert_obj.sensor_value,
                    "timestamp": alert_obj.timestamp.isoformat(),
                    "status": alert_obj.status,
                    "suggested_action": alert_data.get("suggested_action")
                }
                created_alerts_for_broadcast.append(alert_payload)

            # Store reading into SQLite (serves as primary reliable store or InfluxDB backup)
            reading_record = SensorReading(
                device_id=device_id,
                machine_id=machine_id,
                timestamp=timestamp,
                source=source,
                vibration_x=vx,
                vibration_y=vy,
                vibration_z=vz,
                vibration_rms=vibration_rms,
                gyro_x=float(sensors.get("gyro_x") or 0.0),
                gyro_y=float(sensors.get("gyro_y") or 0.0),
                gyro_z=float(sensors.get("gyro_z") or 0.0),
                temperature=float(sensors.get("temperature") or 0.0),
                current=float(sensors.get("current") or 0.0),
                piezo_voltage=float(sensors.get("piezo_voltage") or 0.0)
            )
            db.add(reading_record)
            db.commit()
        except Exception as e:
            logger.error(f"Error persisting to SQLite: {e}")
            db.rollback()
        finally:
            db.close()

        # 5. Store to InfluxDB time-series (if available)
        influx_db.write_sensor_reading(
            device_id=device_id,
            machine_id=machine_id,
            timestamp=timestamp,
            sensors=sensors,
            vibration_rms=vibration_rms,
            source=source
        )

        # 6. Prepare combined response & cache
        reading_summary = {
            "device_id": device_id,
            "machine_id": machine_id,
            "timestamp": timestamp.isoformat(),
            "source": source,
            "vibration_x": vx,
            "vibration_y": vy,
            "vibration_z": vz,
            "vibration_rms": round(vibration_rms, 3),
            "gyro_x": float(sensors.get("gyro_x") or 0.0),
            "gyro_y": float(sensors.get("gyro_y") or 0.0),
            "gyro_z": float(sensors.get("gyro_z") or 0.0),
            "temperature": float(sensors.get("temperature") or 0.0),
            "current": float(sensors.get("current") or 0.0),
            "piezo_voltage": float(sensors.get("piezo_voltage") or 0.0),
            "machine_status": machine_status,
            "iso_zone": analytics_service.classify_iso_vibration_zone(vibration_rms)
        }

        self.latest_reading = reading_summary
        self.total_readings_processed += 1

        # 7. Broadcast via WebSockets
        await websocket_manager.broadcast_sensor_update(
            reading_summary,
            machine_status,
            created_alerts_for_broadcast
        )

        if recovered_alerts:
            await websocket_manager.broadcast_recovery(recovered_alerts, machine_id)

        return reading_summary

    def get_latest_reading(self) -> Optional[Dict[str, Any]]:
        if self.latest_reading:
            return self.latest_reading

        # Fallback to query SQLite
        db = SessionLocal()
        try:
            row = db.query(SensorReading).order_by(SensorReading.timestamp.desc()).first()
            if row:
                return {
                    "device_id": row.device_id,
                    "machine_id": row.machine_id,
                    "timestamp": row.timestamp.isoformat(),
                    "source": row.source,
                    "vibration_x": row.vibration_x,
                    "vibration_y": row.vibration_y,
                    "vibration_z": row.vibration_z,
                    "vibration_rms": row.vibration_rms,
                    "gyro_x": row.gyro_x,
                    "gyro_y": row.gyro_y,
                    "gyro_z": row.gyro_z,
                    "temperature": row.temperature,
                    "current": row.current,
                    "piezo_voltage": row.piezo_voltage,
                    "machine_status": "NORMAL"
                }
            return None
        finally:
            db.close()

    def get_history(self, machine_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves historical records from SQLite (or InfluxDB if available)."""
        db = SessionLocal()
        try:
            records = (
                db.query(SensorReading)
                .filter(SensorReading.machine_id == machine_id)
                .order_by(SensorReading.timestamp.desc())
                .limit(limit)
                .all()
            )
            results = []
            for r in reversed(records):
                results.append({
                    "id": r.id,
                    "device_id": r.device_id,
                    "machine_id": r.machine_id,
                    "timestamp": r.timestamp.isoformat(),
                    "source": r.source,
                    "vibration_x": r.vibration_x,
                    "vibration_y": r.vibration_y,
                    "vibration_z": r.vibration_z,
                    "vibration_rms": r.vibration_rms,
                    "gyro_x": r.gyro_x,
                    "gyro_y": r.gyro_y,
                    "gyro_z": r.gyro_z,
                    "temperature": r.temperature,
                    "current": r.current,
                    "piezo_voltage": r.piezo_voltage
                })
            return results
        finally:
            db.close()

sensor_service = SensorService()
