from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.sqlite_database import get_db
from app.models.machine import Machine, SensorConfiguration
from app.models.alert import Alert
from app.schemas.sensor_schema import MachineCreate, MachineResponse, SensorThresholdConfig
from app.services.fault_detection import fault_detector

router = APIRouter(prefix="/api/machines", tags=["Machines"])

@router.get("", response_model=List[MachineResponse])
def get_machines(db: Session = Depends(get_db)):
    """Retrieves all registered industrial machines."""
    machines = db.query(Machine).all()
    results = []
    for m in machines:
        alert_count = db.query(Alert).filter(Alert.machine_id == m.id, Alert.status == "ACTIVE").count()
        results.append(MachineResponse(
            id=m.id,
            machine_name=m.machine_name,
            device_id=m.device_id,
            motor_type=m.motor_type,
            status=m.status,
            installation_date=m.installation_date,
            active_alerts_count=alert_count
        ))
    return results

@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: str, db: Session = Depends(get_db)):
    """Retrieves details of an individual machine by ID."""
    m = db.query(Machine).filter(Machine.id == machine_id).first()
    if not m:
        raise HTTPException(status_code=404, detail=f"Machine {machine_id} not found")

    alert_count = db.query(Alert).filter(Alert.machine_id == m.id, Alert.status == "ACTIVE").count()
    return MachineResponse(
        id=m.id,
        machine_name=m.machine_name,
        device_id=m.device_id,
        motor_type=m.motor_type,
        status=m.status,
        installation_date=m.installation_date,
        active_alerts_count=alert_count
    )

@router.get("/{machine_id}/thresholds")
def get_machine_thresholds(machine_id: str, db: Session = Depends(get_db)):
    """Retrieves warning and critical sensor thresholds for a given machine."""
    configs = db.query(SensorConfiguration).filter(SensorConfiguration.machine_id == machine_id).all()
    if not configs:
        # Return currently active engine thresholds
        return fault_detector.get_thresholds()

    result = {}
    for c in configs:
        result[c.sensor_name] = {
            "warning": c.warning_threshold,
            "critical": c.critical_threshold,
            "calibration_value": c.calibration_value
        }
    return result

@router.put("/{machine_id}/thresholds")
def update_machine_thresholds(machine_id: str, thresholds: Dict[str, Dict[str, float]], db: Session = Depends(get_db)):
    """Updates fault detection thresholds in SQLite and updates the live detection service."""
    for sensor_name, vals in thresholds.items():
        warning = vals.get("warning")
        critical = vals.get("critical")
        if warning is not None and critical is not None:
            # Update live engine
            fault_detector.update_thresholds(sensor_name, float(warning), float(critical))

            # Persist to database
            cfg = db.query(SensorConfiguration).filter(
                SensorConfiguration.machine_id == machine_id,
                SensorConfiguration.sensor_name == sensor_name
            ).first()
            if cfg:
                cfg.warning_threshold = float(warning)
                cfg.critical_threshold = float(critical)
            else:
                cfg = SensorConfiguration(
                    machine_id=machine_id,
                    sensor_name=sensor_name,
                    warning_threshold=float(warning),
                    critical_threshold=float(critical)
                )
                db.add(cfg)
    db.commit()
    return {
        "status": "success",
        "message": "Thresholds successfully updated and applied",
        "thresholds": fault_detector.get_thresholds()
    }
