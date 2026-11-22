from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database.sqlite_database import get_db
from app.schemas.sensor_schema import SensorDataPayload, SensorReadingResponse, SimulationControl
from app.services.sensor_service import sensor_service
from app.services.analytics_service import analytics_service
from app.simulator.sensor_simulator import sensor_simulator

router = APIRouter(prefix="/api", tags=["Sensors & Simulation"])

@router.get("/sensors/latest", response_model=Optional[dict])
async def get_latest_sensor_reading():
    """Returns the most recent sensor reading from the DC motor."""
    reading = sensor_service.get_latest_reading()
    if not reading:
        return {
            "message": "No sensor readings available yet. Start the simulator or publish hardware readings."
        }
    return reading

@router.get("/sensors/history", response_model=List[dict])
async def get_sensor_history(
    machine_id: str = Query("MOTOR_001", description="Machine identifier"),
    limit: int = Query(50, ge=1, le=500, description="Max number of historical records")
):
    """Retrieves chronological sensor history for trending and historical graphs."""
    return sensor_service.get_history(machine_id, limit)

@router.post("/sensors/data", status_code=status.HTTP_201_CREATED)
async def ingest_sensor_data(payload: SensorDataPayload):
    """
    Receives raw sensor readings from ESP32-S3 hardware via REST or external pipeline.
    Runs readings through validation, fault detection, and database storage.
    """
    try:
        data_dict = payload.model_dump()
        result = await sensor_service.ingest_sensor_data(data_dict)
        return {
            "status": "success",
            "message": "Sensor data ingested successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sensors/fft")
async def get_vibration_fft():
    """Returns frequency domain spectral bins and dominant frequency for vibration analysis."""
    if sensor_service.latest_fft:
        return sensor_service.latest_fft
    # Default synthetic spectrum if no waveform buffer is active
    return analytics_service.compute_fft([])

# --- Simulator Control Endpoints ---

@router.post("/simulation/start")
async def start_simulation(control: Optional[SimulationControl] = None):
    """Starts simulated multi-modal sensor generation loop."""
    interval = control.interval_seconds if control else 1.0
    if control and control.mode:
        sensor_simulator.set_mode(control.mode)
    started = sensor_simulator.start(interval)
    return {
        "status": "running" if (started or sensor_simulator.is_running) else "error",
        "message": "Sensor simulation started" if started else "Simulator was already running",
        "mode": sensor_simulator.mode,
        "interval_seconds": sensor_simulator.interval_seconds
    }

@router.post("/simulation/stop")
async def stop_simulation():
    """Stops the simulated sensor generation loop."""
    stopped = sensor_simulator.stop()
    return {
        "status": "stopped",
        "message": "Sensor simulation stopped" if stopped else "Simulator was not running"
    }

@router.get("/simulation/status")
async def get_simulation_status():
    """Returns the operational status of the sensor simulator."""
    return sensor_simulator.get_status()

@router.post("/simulation/mode")
async def set_simulation_mode(mode: str = Query(..., description="'normal', 'high_vibration', 'overheating', 'high_current', 'multi_fault'")):
    """Switches the simulator between normal operation and specific fault conditions."""
    try:
        active_mode = sensor_simulator.set_mode(mode)
        return {
            "status": "success",
            "active_mode": active_mode,
            "message": f"Simulation anomaly condition changed to {active_mode}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
