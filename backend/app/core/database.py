"""
Database configuration for Orange Sage
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URI,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URI else {},
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    echo=False           # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables"""
    # Import all models to ensure they are registered
    from app.models.user import User
    from app.models.project import Project
    from app.models.target import Target
    from app.models.scan import Scan
    from app.models.finding import Finding
    from app.models.agent import Agent
    from app.models.report import Report
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
