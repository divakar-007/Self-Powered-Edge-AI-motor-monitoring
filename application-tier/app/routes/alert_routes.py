from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database.sqlite_database import get_db
from app.models.alert import Alert
from app.schemas.sensor_schema import AlertCreate, AlertResponse
from app.websocket.websocket_manager import websocket_manager

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

ACTION_SUGGESTIONS = {
    "VIBRATION": "Check motor base anchoring bolts, test for bearing race wear, and balance rotor.",
    "TEMPERATURE": "Ensure cooling fan airflow is unblocked, inspect thermal interface, and verify ambient limits.",
    "CURRENT": "Inspect mechanical drive for friction or binding, test winding insulation resistance.",
    "MULTI_FAULT": "Emergency safety stop recommended: compound failure poses severe mechanical and fire hazard.",
    "PIEZO_VOLTAGE": "Inspect piezo transducer bonding and check energy harvester rectifier circuit."
}

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    machine_id: Optional[str] = Query(None, description="Filter by machine ID"),
    severity: Optional[str] = Query(None, description="Filter by severity: WARNING or CRITICAL"),
    status: Optional[str] = Query(None, description="Filter by status: ACTIVE, ACKNOWLEDGED, RESOLVED"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Retrieves list of fault alerts with filtering options."""
    query = db.query(Alert)
    if machine_id:
        query = query.filter(Alert.machine_id == machine_id)
    if severity:
        query = query.filter(Alert.severity == severity.upper())
    if status:
        query = query.filter(Alert.status == status.upper())

    alerts = query.order_by(Alert.timestamp.desc()).limit(limit).all()

    results = []
    for a in alerts:
        results.append(AlertResponse(
            id=a.id,
            machine_id=a.machine_id,
            alert_type=a.alert_type,
            severity=a.severity,
            description=a.description,
            sensor_value=a.sensor_value,
            timestamp=a.timestamp,
            status=a.status,
            suggested_action=ACTION_SUGGESTIONS.get(a.alert_type, "Inspect motor and verify sensor connections.")
        ))
    return results

@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(alert_in: AlertCreate, db: Session = Depends(get_db)):
    """Manually creates an alert or records an edge-triggered hardware alert."""
    new_alert = Alert(
        machine_id=alert_in.machine_id,
        alert_type=alert_in.alert_type,
        severity=alert_in.severity,
        description=alert_in.description,
        sensor_value=alert_in.sensor_value,
        timestamp=alert_in.timestamp or datetime.utcnow(),
        status="ACTIVE"
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    # Broadcast via WebSocket
    alert_dict = {
        "id": new_alert.id,
        "machine_id": new_alert.machine_id,
        "alert_type": new_alert.alert_type,
        "severity": new_alert.severity,
        "description": new_alert.description,
        "sensor_value": new_alert.sensor_value,
        "timestamp": new_alert.timestamp.isoformat(),
        "status": new_alert.status,
        "suggested_action": ACTION_SUGGESTIONS.get(new_alert.alert_type, "Inspect sensor.")
    }
    await websocket_manager.broadcast_alert(alert_dict)

    return AlertResponse(
        id=new_alert.id,
        machine_id=new_alert.machine_id,
        alert_type=new_alert.alert_type,
        severity=new_alert.severity,
        description=new_alert.description,
        sensor_value=new_alert.sensor_value,
        timestamp=new_alert.timestamp,
        status=new_alert.status,
        suggested_action=ACTION_SUGGESTIONS.get(new_alert.alert_type)
    )

@router.put("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """Acknowledge an active alert by technician."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "ACKNOWLEDGED"
    db.commit()
    return {"status": "success", "message": f"Alert {alert_id} acknowledged"}

@router.put("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Mark an alert as resolved after maintenance."""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = "RESOLVED"
    db.commit()
    return {"status": "success", "message": f"Alert {alert_id} resolved"}
