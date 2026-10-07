from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=Session, autoflush=False, autocommit=False)


def get_db():
    """FastAPI dependency that gives one transaction scope per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
