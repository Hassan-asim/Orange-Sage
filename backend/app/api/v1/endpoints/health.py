"""
Health check endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.llm_service import LLMService
from app.services.sandbox_service import SandboxService
from sqlalchemy import text
import os
from app.core.config import settings

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
        # Check database (SQLAlchemy 2.x compatible)
        db.execute(text("SELECT 1"))
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


@router.post("/chat")
async def chat_with_gemini(
    data: dict,
    current_user = Depends(get_current_user)
):
    """Chat with Gemini but restrict to Orange Sage / cybersecurity questions."""
    try:
        message = data.get("message", "").strip()
        if not message:
            raise HTTPException(status_code=400, detail="Message is required.")
        import google.generativeai as genai
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=503, detail="Gemini API key not configured.")
        genai.configure(api_key=api_key)
        SYSTEM_PROMPT = (
            "You are Orange Sage's AI assistant. Only answer questions about this app or cybersecurity. "
            "For other inquiries, respond: 'Sorry, I can only answer questions about Orange Sage and cybersecurity.'"
        )
        model_name = settings.FALLBACK_LLM_MODEL if hasattr(settings, "FALLBACK_LLM_MODEL") else "gemini-pro"
        chat = genai.GenerativeModel(model_name).start_chat([{"role": "user", "parts": [SYSTEM_PROMPT]}, {"role": "user", "parts": [message]}])
        gemini_reply = chat.last.text.strip() if hasattr(chat.last, 'text') else chat.last if chat.last else "No reply."
        return {"reply": gemini_reply}
    except HTTPException:
        raise
    except Exception as e:
        return {"error": str(e)}
