import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database.sqlite_database import init_sqlite_db
from app.routes.sensor_routes import router as sensor_router
from app.routes.machine_routes import router as machine_router
from app.routes.alert_routes import router as alert_router
from app.routes.analytics_routes import router as analytics_router
from app.websocket.websocket_manager import websocket_manager
from app.mqtt.mqtt_client import mqtt_manager
from app.simulator.sensor_simulator import sensor_simulator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("mems-industrial-backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    logger.info(f"=== Starting {settings.APP_NAME} ===")
    
    # 1. Initialize SQLite Database Tables
    try:
        init_sqlite_db()
        logger.info("SQLite database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize SQLite: {e}")

    # 2. Start MQTT Client (runs in daemon thread, reconnects automatically)
    loop = asyncio.get_running_loop()
    try:
        mqtt_manager.start(loop)
    except Exception as e:
        logger.warning(f"Could not start MQTT manager: {e}")

    # 3. Start Sensor Simulator if configured
    if settings.SIMULATOR_AUTO_START:
        sensor_simulator.start(settings.SIMULATOR_INTERVAL_SECONDS)
        logger.info("Sensor simulator auto-started in background.")

    yield

    # Shutdown sequence
    logger.info("Shutting down application...")
    sensor_simulator.stop()
    if mqtt_manager.client:
        mqtt_manager.client.disconnect()
    logger.info("Shutdown complete.")

app = FastAPI(
    title="MEMS Industrial Monitoring System API",
    description="Application Tier REST API and Real-Time WebSocket server for DC Motor Multi-Modal Health Monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow development frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(sensor_router)
app.include_router(machine_router)
app.include_router(alert_router)
app.include_router(analytics_router)

# WebSocket Endpoint
@app.websocket("/ws/sensors")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Keep connection open and accept ping/pong or client commands
            data = await websocket.receive_text()
            # Echo or process client command if needed
            logger.debug(f"Received WS text from client: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.warning(f"WebSocket client error: {e}")
        websocket_manager.disconnect(websocket)

@app.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "tier": "Application Tier (Backend)",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/api/health",
        "websocket": "/ws/sensors"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
