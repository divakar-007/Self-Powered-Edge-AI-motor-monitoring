import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Ensure sqlite directory exists
if not os.path.isabs(settings.SQLITE_DB_PATH):
    # Base on application-tier directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    resolved_path = os.path.abspath(os.path.join(base_dir, settings.SQLITE_DB_PATH))
else:
    resolved_path = settings.SQLITE_DB_PATH

db_dir = os.path.dirname(resolved_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{resolved_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_sqlite_db():
    from app.models import machine, alert, sensor_reading
    Base.metadata.create_all(bind=engine)
    from app.services.sensor_service import sensor_service
    sensor_service.init_default_machine()
