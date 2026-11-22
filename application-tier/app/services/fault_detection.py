import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod
from app.config import settings

logger = logging.getLogger(__name__)

class ITinyMLDetector(ABC):
    """
    Interface for future TinyML model inference integration.
    Once an edge model is trained (e.g. Autoencoder for anomaly detection
    or 1D CNN on vibration accelerometer waveform), it implements this interface.
    """
    @abstractmethod
    def predict_anomaly(self, sensor_features: Dict[str, float]) -> Tuple[bool, float, str]:
        """
        Returns (is_anomaly, anomaly_score, detected_class)
        """
        pass

class TinyMLPlaceholderDetector(ITinyMLDetector):
    """
    Placeholder indicating architecture readiness for TinyML model deployment.
    Does not pretend to be a trained model.
    """
    def __init__(self):
        self.is_model_loaded = False
        self.model_version = "v0.0-uncalibrated-stub"

    def predict_anomaly(self, sensor_features: Dict[str, float]) -> Tuple[bool, float, str]:
        # Returns False since no weights/model file are currently deployed
        return (False, 0.0, "TINYML_NOT_YET_TRAINED")

class FaultStateTracker:
    """
    Tracks state of active faults to avoid repeating alerts on every 1-second sample,
    and detects when an abnormal condition has returned to normal (recovery detection).
    """
    def __init__(self):
        # Key: (machine_id, alert_type) -> {"severity": "WARNING"|"CRITICAL", "first_seen": datetime, "last_seen": datetime}
        self.active_faults: Dict[Tuple[str, str], Dict[str, Any]] = {}

    def should_emit_alert(self, machine_id: str, alert_type: str, severity: str) -> bool:
        key = (machine_id, alert_type)
        if key not in self.active_faults:
            # New fault detected!
            self.active_faults[key] = {
                "severity": severity,
                "first_seen": datetime.utcnow(),
                "last_seen": datetime.utcnow()
            }
            return True
        else:
            current = self.active_faults[key]
            # If severity escalated from WARNING to CRITICAL, emit alert!
            if current["severity"] == "WARNING" and severity == "CRITICAL":
                current["severity"] = "CRITICAL"
                current["last_seen"] = datetime.utcnow()
                return True
            # Otherwise, keep active without flooding duplicate alerts
            current["last_seen"] = datetime.utcnow()
            return False

    def check_recovery(self, machine_id: str, currently_triggered_types: List[str]) -> List[str]:
        """
        Checks which active faults for this machine are no longer present.
        Returns list of recovered alert types.
        """
        recovered = []
        keys_to_remove = []
        for (m_id, a_type), info in self.active_faults.items():
            if m_id == machine_id:
                if a_type not in currently_triggered_types:
                    recovered.append(a_type)
                    keys_to_remove.append((m_id, a_type))

        for k in keys_to_remove:
            del self.active_faults[k]

        return recovered

    def get_machine_overall_status(self, machine_id: str) -> str:
        severities = [info["severity"] for (m_id, _), info in self.active_faults.items() if m_id == machine_id]
        if "CRITICAL" in severities:
            return "CRITICAL"
        elif "WARNING" in severities:
            return "WARNING"
        return "NORMAL"

class FaultDetectionService:
    def __init__(self):
        self.state_tracker = FaultStateTracker()
        self.tinyml_engine = TinyMLPlaceholderDetector()
        # In-memory threshold cache, synchronized with SQLite
        self.thresholds: Dict[str, Dict[str, float]] = {
            "vibration": {
                "warning": settings.THRESHOLD_VIB_WARNING,
                "critical": settings.THRESHOLD_VIB_CRITICAL
            },
            "temperature": {
                "warning": settings.THRESHOLD_TEMP_WARNING,
                "critical": settings.THRESHOLD_TEMP_CRITICAL
            },
            "current": {
                "warning": settings.THRESHOLD_CURRENT_WARNING,
                "critical": settings.THRESHOLD_CURRENT_CRITICAL
            },
            "piezo_voltage": {
                "warning": settings.THRESHOLD_PIEZO_WARNING,
                "critical": settings.THRESHOLD_PIEZO_CRITICAL
            }
        }

    def update_thresholds(self, sensor_name: str, warning: float, critical: float):
        if sensor_name in self.thresholds:
            self.thresholds[sensor_name]["warning"] = warning
            self.thresholds[sensor_name]["critical"] = critical
            logger.info(f"Updated thresholds for {sensor_name}: warning={warning}, critical={critical}")

    def get_thresholds(self) -> Dict[str, Dict[str, float]]:
        return self.thresholds

    def evaluate_readings(
        self,
        machine_id: str,
        sensors: Dict[str, Any],
        vibration_rms: float
    ) -> Dict[str, Any]:
        """
        Evaluates incoming sensor metrics against calibrated industrial safety thresholds.
        Returns newly triggered alerts, recovered alerts, and overall machine status.
        """
        new_alerts: List[Dict[str, Any]] = []
        active_triggered_types: List[str] = []

        temp = sensors.get("temperature")
        current = sensors.get("current")
        piezo = sensors.get("piezo_voltage")

        # 1. Vibration Check
        vib_th = self.thresholds["vibration"]
        if vibration_rms >= vib_th["critical"]:
            active_triggered_types.append("VIBRATION")
            if self.state_tracker.should_emit_alert(machine_id, "VIBRATION", "CRITICAL"):
                new_alerts.append({
                    "machine_id": machine_id,
                    "alert_type": "VIBRATION",
                    "severity": "CRITICAL",
                    "description": f"Critical vibration RMS {vibration_rms:.2f} m/s² exceeds limit ({vib_th['critical']} m/s²). Risk of catastrophic mechanical failure or severe bearing damage.",
                    "sensor_value": round(vibration_rms, 2),
                    "suggested_action": "Immediately reduce motor RPM or halt operation. Inspect motor mountings, shaft alignment, and bearing lubrication."
                })
        elif vibration_rms >= vib_th["warning"]:
            active_triggered_types.append("VIBRATION")
            if self.state_tracker.should_emit_alert(machine_id, "VIBRATION", "WARNING"):
                new_alerts.append({
                    "machine_id": machine_id,
                    "alert_type": "VIBRATION",
                    "severity": "WARNING",
                    "description": f"Elevated vibration RMS {vibration_rms:.2f} m/s² exceeds warning limit ({vib_th['warning']} m/s²). Mechanical unbalance or rotor looseness detected.",
                    "sensor_value": round(vibration_rms, 2),
                    "suggested_action": "Schedule preventative inspection of mechanical couplings and check for eccentric rotor load."
                })

        # 2. Temperature Check
        if temp is not None:
            temp_th = self.thresholds["temperature"]
            if temp >= temp_th["critical"]:
                active_triggered_types.append("TEMPERATURE")
                if self.state_tracker.should_emit_alert(machine_id, "TEMPERATURE", "CRITICAL"):
                    new_alerts.append({
                        "machine_id": machine_id,
                        "alert_type": "TEMPERATURE",
                        "severity": "CRITICAL",
                        "description": f"Thermal runaway: Motor temperature {temp:.1f} °C breached critical safety limit ({temp_th['critical']} °C).",
                        "sensor_value": round(temp, 1),
                        "suggested_action": "Shut down DC drive immediately to prevent winding insulation breakdown and magnet demagnetization. Inspect ventilation duct."
                    })
            elif temp >= temp_th["warning"]:
                active_triggered_types.append("TEMPERATURE")
                if self.state_tracker.should_emit_alert(machine_id, "TEMPERATURE", "WARNING"):
                    new_alerts.append({
                        "machine_id": machine_id,
                        "alert_type": "TEMPERATURE",
                        "severity": "WARNING",
                        "description": f"Elevated thermal dissipation: Motor temperature {temp:.1f} °C exceeds warning threshold ({temp_th['warning']} °C).",
                        "sensor_value": round(temp, 1),
                        "suggested_action": "Check ambient temperature, motor cooling airflow, and verify thermal paste on DS18B20 probe."
                    })

        # 3. Electrical Current Check
        if current is not None:
            cur_th = self.thresholds["current"]
            if current >= cur_th["critical"]:
                active_triggered_types.append("CURRENT")
                if self.state_tracker.should_emit_alert(machine_id, "CURRENT", "CRITICAL"):
                    new_alerts.append({
                        "machine_id": machine_id,
                        "alert_type": "CURRENT",
                        "severity": "CRITICAL",
                        "description": f"Severe overcurrent {current:.2f} A exceeds limit ({cur_th['critical']} A). Motor stall or internal short circuit suspected.",
                        "sensor_value": round(current, 2),
                        "suggested_action": "Trip DC motor circuit breaker. Inspect drive gearbox for mechanical jam and measure armature resistance."
                    })
            elif current >= cur_th["warning"]:
                active_triggered_types.append("CURRENT")
                if self.state_tracker.should_emit_alert(machine_id, "CURRENT", "WARNING"):
                    new_alerts.append({
                        "machine_id": machine_id,
                        "alert_type": "CURRENT",
                        "severity": "WARNING",
                        "description": f"High current consumption {current:.2f} A exceeds threshold ({cur_th['warning']} A). Mechanical drag or excessive load detected.",
                        "sensor_value": round(current, 2),
                        "suggested_action": "Verify mechanical load torque and check belt or gear tension."
                    })

        # 4. Multi-Condition Abnormal Interaction
        if len(active_triggered_types) >= 2:
            multi_key = "MULTI_FAULT"
            active_triggered_types.append(multi_key)
            if self.state_tracker.should_emit_alert(machine_id, multi_key, "CRITICAL"):
                new_alerts.append({
                    "machine_id": machine_id,
                    "alert_type": multi_key,
                    "severity": "CRITICAL",
                    "description": f"Compound multi-modal anomaly detected across {', '.join(set(active_triggered_types))}. Severe compounded electro-mechanical degradation.",
                    "sensor_value": float(len(active_triggered_types)),
                    "suggested_action": "Emergency maintenance intervention required. Lockout/tagout equipment before physical disassembly."
                })

        # 5. Recovery Detection
        recovered_alerts = self.state_tracker.check_recovery(machine_id, active_triggered_types)

        overall_status = self.state_tracker.get_machine_overall_status(machine_id)

        return {
            "overall_status": overall_status,
            "new_alerts": new_alerts,
            "recovered_alerts": recovered_alerts,
            "active_fault_count": len(self.state_tracker.active_faults)
        }

fault_detector = FaultDetectionService()
