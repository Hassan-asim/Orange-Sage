"""
Finding endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.finding import Finding, SeverityLevel, FindingStatus
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/")
async def list_findings(
    scan_id: int = None,
    severity: str = None,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List findings"""
    query = db.query(Finding)
    
    if scan_id:
        query = query.filter(Finding.scan_id == scan_id)
    
    if severity:
        query = query.filter(Finding.severity == SeverityLevel(severity))
    
    if status:
        query = query.filter(Finding.status == FindingStatus(status))
    
    findings = query.order_by(Finding.created_at.desc()).all()
    
    # Return array directly for frontend compatibility
    return [
        {
            "id": finding.id,
            "title": finding.title,
            "description": finding.description,
            "severity": finding.severity.value,
            "status": finding.status.value,
            "vulnerability_type": finding.vulnerability_type,
            "endpoint": finding.endpoint,
            "parameter": finding.parameter,
            "method": finding.method,
            "created_at": finding.created_at.isoformat() if finding.created_at else None,
            "created_by_agent": finding.created_by_agent,
            "scan_id": finding.scan_id
        }
        for finding in findings
    ]


@router.get("/{finding_id}")
async def get_finding(
    finding_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific finding"""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Finding not found"
        )
    
    return {
        "id": finding.id,
        "title": finding.title,
        "description": finding.description,
        "severity": finding.severity.value,
        "status": finding.status.value,
        "vulnerability_type": finding.vulnerability_type,
        "endpoint": finding.endpoint,
        "parameter": finding.parameter,
        "method": finding.method,
        "request_sample": finding.request_sample,
        "response_sample": finding.response_sample,
        "poc_artifact_key": finding.poc_artifact_key,
        "remediation_text": finding.remediation_text,
        "references": finding.references,
        "created_at": finding.created_at,
        "created_by_agent": finding.created_by_agent
    }
