"""
Scan endpoints for Orange Sage
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.models.scan import Scan, ScanStatus
from app.models.user import User
from app.schemas.scan import ScanCreate, ScanResponse, ScanStatusResponse
from app.services.agent_manager import AgentManager
from app.utils.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=ScanResponse)
async def create_scan(
    scan_data: ScanCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new security scan"""
    try:
        # Create scan record
        scan = Scan(
            name=scan_data.name,
            description=scan_data.description,
            project_id=scan_data.project_id,
            target_id=scan_data.target_id,
            created_by=current_user.id,
            scan_config=scan_data.scan_config,
            agent_config=scan_data.agent_config
        )
        
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        # Start scan in background
        agent_manager = AgentManager()
        background_tasks.add_task(
            agent_manager.start_scan,
            db,
            scan.id,
            scan_data.scan_config
        )
        
        return ScanResponse(
            id=scan.id,
            name=scan.name,
            description=scan.description,
            status=scan.status.value,
            project_id=scan.project_id,
            target_id=scan.target_id,
            created_by=scan.created_by,
            created_at=scan.created_at,
            started_at=scan.started_at,
            finished_at=scan.finished_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating scan: {str(e)}"
        )


@router.get("/{scan_id}", response_model=ScanStatusResponse)
async def get_scan_status(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get scan status and progress"""
    try:
        # Get scan
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        
        # Check if user has access to this scan
        if scan.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get agent manager and scan status
        agent_manager = AgentManager()
        status_info = await agent_manager.get_scan_status(scan_id, db)
        
        return ScanStatusResponse(
            scan_id=scan_id,
            name=scan.name,
            status=scan.status.value,
            target=scan.target.value if scan.target else None,
            agents_count=status_info.get("agents_count", 0),
            findings_count=status_info.get("findings_count", 0),
            started_at=scan.started_at,
            finished_at=scan.finished_at,
            summary=scan.summary,
            error=scan.error_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting scan status: {str(e)}"
        )


@router.get("/{scan_id}/agents")
async def get_scan_agents(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get agents for a scan"""
    try:
        # Get scan
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        
        # Check if user has access to this scan
        if scan.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get agents
        agent_manager = AgentManager()
        agents = await agent_manager.get_scan_agents(scan_id, db)
        
        return {"agents": agents}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting scan agents: {str(e)}"
        )


@router.post("/{scan_id}/cancel")
async def cancel_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a running scan"""
    try:
        # Get scan
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        
        # Check if user has access to this scan
        if scan.created_by != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Cancel scan
        agent_manager = AgentManager()
        result = await agent_manager.cancel_scan(scan_id, db)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error cancelling scan: {str(e)}"
        )


@router.get("/")
async def list_scans(
    project_id: int = None,
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List scans for the current user"""
    try:
        # Build query
        query = db.query(Scan).filter(Scan.created_by == current_user.id)
        
        if project_id:
            query = query.filter(Scan.project_id == project_id)
        
        if status:
            query = query.filter(Scan.status == ScanStatus(status))
        
        scans = query.order_by(Scan.created_at.desc()).all()
        
        return {
            "scans": [
                {
                    "id": scan.id,
                    "name": scan.name,
                    "status": scan.status.value,
                    "project_id": scan.project_id,
                    "target_id": scan.target_id,
                    "created_at": scan.created_at,
                    "started_at": scan.started_at,
                    "finished_at": scan.finished_at
                }
                for scan in scans
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing scans: {str(e)}"
        )
