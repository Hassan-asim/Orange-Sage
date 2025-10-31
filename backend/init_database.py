#!/usr/bin/env python3
"""
Database initialization script for Orange Sage
Creates all necessary tables in PostgreSQL database
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.config import settings
from app.core.database import Base, engine
from app.models.user import User
from app.models.project import Project
from app.models.target import Target
from app.models.scan import Scan
from app.models.finding import Finding
from app.models.agent import Agent
from app.models.report import Report

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        logger.info("🔄 Creating database tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ All tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False

def verify_tables():
    """Verify that tables were created"""
    try:
        with engine.connect() as connection:
            # Check if users table exists
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'users'
                );
            """))
            
            if result.scalar():
                logger.info("✅ Users table exists")
            else:
                logger.error("❌ Users table not found")
                return False
            
            # List all tables
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tables = [row[0] for row in result]
            logger.info(f"📋 Created tables: {', '.join(tables)}")
            
        return True
    except Exception as e:
        logger.error(f"❌ Failed to verify tables: {e}")
        return False

def main():
    """Main initialization function"""
    logger.info("🚀 Starting database initialization...")
    
    # Check if DATABASE_URL is set
    if not settings.DATABASE_URI:
        logger.error("❌ DATABASE_URL environment variable not set")
        logger.info("💡 Please set DATABASE_URL in your environment or .env file")
        logger.info("💡 Example: DATABASE_URL=postgresql+psycopg2://user:password@host:port/database")
        sys.exit(1)
    
    logger.info(f"🔗 Using database: {settings.DATABASE_URI}")
    
    # Test connection
    if not test_database_connection():
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        sys.exit(1)
    
    # Verify tables
    if not verify_tables():
        sys.exit(1)
    
    logger.info("🎉 Database initialization completed successfully!")
    logger.info("💡 You can now start your application and register users")

if __name__ == "__main__":
    main()
