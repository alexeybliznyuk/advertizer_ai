from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings.config import settings
import os

# Database URL
DATABASE_URL = f"postgresql://{settings.SENDER_DB_USER}:{settings.SENDER_DB_PASS}@{settings.SENDER_DB_HOST}:{settings.SENDER_DB_PORT}/{settings.SENDER_DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables"""
    from models import Base
    Base.metadata.create_all(bind=engine) 