"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.llm_service import LLMService
from app.services.sandbox_service import SandboxService

router = APIRouter()


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "Orange Sage API",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with service status"""
    try:
        # Check database
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Check LLM services
    llm_service = LLMService()
    llm_status = await llm_service.test_connection()
    
    # Check sandbox service
    sandbox_service = SandboxService()
    sandbox_status = "healthy" if sandbox_service.docker_client else "unhealthy"
    
    return {
        "status": "healthy",
        "service": "Orange Sage API",
        "version": "1.0.0",
        "components": {
            "database": db_status,
            "llm_services": llm_status,
            "sandbox_service": sandbox_status
        }
    }
