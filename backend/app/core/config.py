"""
Configuration settings for Orange Sage Backend
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    APP_NAME: str = "Orange Sage API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8080"))
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]  # Allow all origins for Cloud Run
    ALLOWED_HOSTS: List[str] = ["*"]  # Allow all hosts for Cloud Run
    
    # Database
    DATABASE_URI: Optional[str] = (
        os.getenv("DATABASE_URL")
        or os.getenv("DATABASE_URI")
        or os.getenv("DATABSE_URI")  # legacy typo support
        or "sqlite:////app/orange_sage.db"
    )
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # LLM Configuration
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    DEFAULT_LLM_MODEL: str = "gpt-4o-mini"
    FALLBACK_LLM_MODEL: str = "gemini-2.0-flash-lite"
    
    # Agent Configuration
    MAX_AGENTS_PER_SCAN: int = 10
    AGENT_TIMEOUT_MINUTES: int = 30
    SANDBOX_TIMEOUT_MINUTES: int = 60
    
    # Docker/Sandbox
    DOCKER_NETWORK: str = "orange_sage_network"
    SANDBOX_IMAGE: str = "orange_sage/sandbox:latest"
    SANDBOX_MEMORY_LIMIT: str = "2g"
    SANDBOX_CPU_LIMIT: str = "1.0"
    
    # Storage
    UPLOAD_DIR: str = "./uploads"
    REPORTS_DIR: str = "./reports"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Monitoring
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env file


# Create settings instance
settings = Settings()



