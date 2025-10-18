"""
Scan schemas
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class ScanCreate(BaseModel):
    """Scan creation schema"""
    name: str
    description: Optional[str] = None
    project_id: int
    target_id: int
    scan_config: Optional[Dict[str, Any]] = None
    agent_config: Optional[Dict[str, Any]] = None


class ScanResponse(BaseModel):
    """Scan response schema"""
    id: int
    name: str
    description: Optional[str]
    status: str
    project_id: int
    target_id: int
    created_by: int
    created_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ScanStatusResponse(BaseModel):
    """Scan status response schema"""
    scan_id: int
    name: str
    status: str
    target: Optional[str]
    agents_count: int
    findings_count: int
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    summary: Optional[Dict[str, Any]]
    error: Optional[str]
