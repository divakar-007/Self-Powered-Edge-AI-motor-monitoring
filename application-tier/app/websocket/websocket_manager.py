import logging
import json
from typing import List, Dict, Any
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast_json(self, data: Dict[str, Any]):
        """Broadcasts JSON data payload to all connected clients."""
        if not self.active_connections:
            return

        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.warning(f"Error broadcasting to client: {e}. Marking connection for removal.")
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead)

    async def broadcast_sensor_update(self, sensor_reading: Dict[str, Any], machine_status: str, alerts: List[Dict[str, Any]] = None):
        payload = {
            "type": "SENSOR_UPDATE",
            "data": sensor_reading,
            "machine_status": machine_status,
            "alerts": alerts or []
        }
        await self.broadcast_json(payload)

    async def broadcast_alert(self, alert: Dict[str, Any]):
        payload = {
            "type": "NEW_ALERT",
            "alert": alert
        }
        await self.broadcast_json(payload)

    async def broadcast_recovery(self, recovered_types: List[str], machine_id: str):
        payload = {
            "type": "ALERT_RECOVERY",
            "machine_id": machine_id,
            "recovered_types": recovered_types
        }
        await self.broadcast_json(payload)

websocket_manager = WebSocketManager()
