"""
Target schemas
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class TargetCreate(BaseModel):
    """Target creation schema"""
    name: str
    type: str  # url, repository, upload
    value: str  # URL, repo path, or file path
    description: Optional[str] = None
    project_id: int
    config: Optional[Dict[str, Any]] = None


class TargetUpdate(BaseModel):
    """Target update schema (partial)"""
    name: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None


class TargetResponse(BaseModel):
    """Target response schema"""
    id: int
    name: str
    type: str
    value: str
    description: Optional[str]
    project_id: int
    config: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


