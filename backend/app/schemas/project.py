# backend/app/schemas/project.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    """Project creation schema"""
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    """Project update schema (partial)"""
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    """Project response schema"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True