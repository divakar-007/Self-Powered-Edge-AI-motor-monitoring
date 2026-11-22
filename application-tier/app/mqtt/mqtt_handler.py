import asyncio
import json
import logging
from typing import Dict, Any
from app.services.sensor_service import sensor_service

logger = logging.getLogger(__name__)

class MQTTHandler:
    @staticmethod
    def handle_sensor_message(topic: str, payload_str: str, loop: asyncio.AbstractEventLoop):
        try:
            payload = json.loads(payload_str)
            logger.info(f"Received MQTT sensor message on [{topic}] from {payload.get('device_id', 'unknown')}")

            # Schedule asynchronous ingestion inside the running event loop
            asyncio.run_coroutine_threadsafe(
                sensor_service.ingest_sensor_data(payload),
                loop
            )
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON payload on MQTT topic {topic}: {e}")
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}", exc_info=True)

    @staticmethod
    def handle_status_message(topic: str, payload_str: str):
        logger.info(f"MQTT Device Status [{topic}]: {payload_str}")

    @staticmethod
    def handle_alert_message(topic: str, payload_str: str):
        logger.warning(f"MQTT Device Hardware Alert [{topic}]: {payload_str}")
