"""
Local Orange Sage Backend (without Docker dependencies)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.core.config_local import settings
from app.core.database_local import init_db, get_db
from app.core.logging_config import setup_logging
from app.api.v1.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    init_db()  # Initialize SQLite database
    print("🚀 Orange Sage Backend started successfully!")
    print(f"📊 API Documentation: http://localhost:8000/api/v1/docs")
    print(f"🌐 CORS Origins: {settings.BACKEND_CORS_ORIGINS}")
    yield
    # Shutdown
    print("👋 Orange Sage Backend shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Cybersecurity Assessment Platform",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Orange Sage API",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "sqlite",
        "message": "Orange Sage is running locally"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_local:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
