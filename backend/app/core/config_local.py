"""
Local configuration for Orange Sage (without Docker)
"""

import os
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator

class LocalSettings(BaseSettings):
    PROJECT_NAME: str = "Orange Sage"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-super-secret-key-for-local-development"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database - Using SQLite for local development
    DATABASE_URL: str = "sqlite:///./orange_sage.db"
    ASYNC_DATABASE_URL: str = "sqlite+aiosqlite:///./orange_sage.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, List):
            return v
        raise ValueError("BACKEND_CORS_ORIGINS must be a string or list of strings")

    # LLM - Use your API keys here
    OPENAI_API_KEY: str = "sk-your-openai-key-here"
    GEMINI_API_KEY: str = "AIzaSyC-your-gemini-key-here"
    LLM_MODEL: str = "gpt-4o"

    # Local file storage (no S3/MinIO needed)
    UPLOAD_DIR: str = "./uploads"
    REPORTS_DIR: str = "./reports"
    
    # Create directories if they don't exist
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.REPORTS_DIR, exist_ok=True)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = LocalSettings()
