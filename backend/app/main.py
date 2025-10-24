"""
Orange Sage Backend API
A comprehensive cybersecurity assessment platform with AI agents
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.core.config import settings
from app.core.database import init_db
from app.core.logging_config import setup_logging
from app.api.v1.api import api_router
from app.services.agent_manager import AgentManager
from app.services.report_generator import ReportGenerator

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global services
agent_manager: AgentManager = None
report_generator: ReportGenerator = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting Orange Sage Backend API")
    
    # Initialize database
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"⚠️  Database initialization failed: {e}")
        logger.info("⚠️  Continuing without database (in-memory mode)")
    
    # Initialize services
    global agent_manager, report_generator
    try:
        agent_manager = AgentManager()
        logger.info("✅ Agent Manager initialized")
    except Exception as e:
        logger.warning(f"⚠️  Agent Manager initialization failed (Docker not available): {e}")
        agent_manager = None
    
    try:
        report_generator = ReportGenerator()
        logger.info("✅ Report Generator initialized")
    except Exception as e:
        logger.warning(f"⚠️  Report Generator initialization failed: {e}")
        report_generator = None
    
    logger.info("✅ Services initialized")
    logger.info("🌐 Orange Sage Backend API ready")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Orange Sage Backend API")
    if agent_manager:
        try:
            await agent_manager.cleanup()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    logger.info("✅ Cleanup completed")


# Create FastAPI application
app = FastAPI(
    title="Orange Sage API",
    description="AI-powered cybersecurity assessment platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    redirect_slashes=False  # Disable automatic trailing slash redirects
)

# Add middleware - CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Cloud Run
    allow_credentials=False,  # Must be False when using wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# TrustedHostMiddleware - only add if not using wildcard
if settings.ALLOWED_HOSTS != ["*"]:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Orange Sage API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Orange Sage Backend API",
        "version": "1.0.0"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
