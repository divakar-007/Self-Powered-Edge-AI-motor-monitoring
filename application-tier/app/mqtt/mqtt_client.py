import asyncio
import logging
import threading
import time
from typing import Optional, Dict, Any
import paho.mqtt.client as mqtt

from app.config import settings
from app.mqtt.mqtt_handler import MQTTHandler

logger = logging.getLogger(__name__)

class MQTTClientManager:
    def __init__(self):
        self.client: Optional[mqtt.Client] = None
        self.is_connected: bool = False
        self.last_error: Optional[str] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    def start(self, event_loop: asyncio.AbstractEventLoop):
        self.loop = event_loop
        self._thread = threading.Thread(target=self._run_mqtt_loop, daemon=True)
        self._thread.start()

    def _run_mqtt_loop(self):
        logger.info(f"Initiating MQTT Client connection to {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}...")
        try:
            # Use MQTT v5 or v3.1.1
            client_id = f"mems-backend-{int(time.time())}"
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=client_id
            )

            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message

            try:
                self.client.connect(
                    host=settings.MQTT_BROKER_HOST,
                    port=settings.MQTT_BROKER_PORT,
                    keepalive=settings.MQTT_KEEP_ALIVE
                )
                self.client.loop_forever()
            except Exception as e:
                self.is_connected = False
                self.last_error = str(e)
                logger.warning(
                    f"MQTT broker not reachable at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT} ({e}). "
                    "Backend will continue in standalone simulation mode. To enable physical hardware MQTT, start Mosquitto broker."
                )
        except Exception as e:
            self.is_connected = False
            self.last_error = str(e)
            logger.warning(f"MQTT initialization exception: {e}")

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.is_connected = True
            self.last_error = None
            logger.info("Successfully connected to Mosquitto MQTT Broker!")

            # Subscribe to sensor, status and alert topics
            topics = [
                (settings.MQTT_TOPIC_SENSORS, 0),
                (settings.MQTT_TOPIC_STATUS, 0),
                (settings.MQTT_TOPIC_ALERTS, 0)
            ]
            client.subscribe(topics)
            logger.info(f"Subscribed to MQTT topics: {[t[0] for t in topics]}")
        else:
            self.is_connected = False
            self.last_error = f"MQTT connection failed with code {rc}"
            logger.warning(self.last_error)

    def _on_disconnect(self, client, userdata, flags, rc, properties=None):
        self.is_connected = False
        logger.warning(f"Disconnected from MQTT Broker (rc={rc}). Will attempt reconnection.")

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            payload_str = msg.payload.decode("utf-8")
        except UnicodeDecodeError:
            logger.error("Failed to decode MQTT message payload as UTF-8")
            return

        if self.loop and self.loop.is_running():
            if topic == settings.MQTT_TOPIC_SENSORS:
                MQTTHandler.handle_sensor_message(topic, payload_str, self.loop)
            elif topic == settings.MQTT_TOPIC_STATUS:
                MQTTHandler.handle_status_message(topic, payload_str)
            elif topic == settings.MQTT_TOPIC_ALERTS:
                MQTTHandler.handle_alert_message(topic, payload_str)

    def publish_command(self, topic: str, message: str) -> bool:
        if self.is_connected and self.client:
            self.client.publish(topic, message)
            return True
        return False

    def get_status(self) -> Dict[str, Any]:
        return {
            "connected": self.is_connected,
            "broker_host": settings.MQTT_BROKER_HOST,
            "broker_port": settings.MQTT_BROKER_PORT,
            "topics": [
                settings.MQTT_TOPIC_SENSORS,
                settings.MQTT_TOPIC_STATUS,
                settings.MQTT_TOPIC_ALERTS
            ],
            "error": self.last_error
        }

mqtt_manager = MQTTClientManager()
