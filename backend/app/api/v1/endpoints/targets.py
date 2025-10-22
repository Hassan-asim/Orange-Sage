"""
Target endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.target import Target
from app.models.project import Project
from app.models.user import User
from app.utils.auth import get_current_user
from app.schemas.target import TargetCreate, TargetUpdate, TargetResponse

router = APIRouter()


@router.post("/", response_model=TargetResponse)
async def create_target(
    data: TargetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new target"""
    try:
        # Verify project exists and user has access
        project = db.query(Project).filter(Project.id == data.project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this project"
            )

        target = Target(
            name=data.name,
            type=data.type,
            value=data.value,
            description=data.description,
            project_id=data.project_id,
            config=data.config
        )
        db.add(target)
        db.commit()
        db.refresh(target)
        return target
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating target: {str(e)}"
        )


@router.get("/")
async def list_targets(
    project_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List targets"""
    query = db.query(Target)
    
    if project_id:
        query = query.filter(Target.project_id == project_id)
    
    targets = query.all()
    
    return {
        "targets": [
            {
                "id": target.id,
                "name": target.name,
                "type": target.type,
                "value": target.value,
                "description": target.description,
                "project_id": target.project_id,
                "created_at": target.created_at
            }
            for target in targets
        ]
    }


@router.get("/{target_id}", response_model=TargetResponse)
async def get_target(
    target_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific target"""
    target = db.query(Target).filter(Target.id == target_id).first()
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Target not found"
        )
    # Ownership check through project relationship
    project = db.query(Project).filter(Project.id == target.project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return target


@router.put("/{target_id}", response_model=TargetResponse)
async def update_target(
    target_id: int,
    data: TargetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a target (partial)"""
    target = db.query(Target).filter(Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")
    project = db.query(Project).filter(Project.id == target.project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        if data.name is not None:
            target.name = data.name
        if data.type is not None:
            target.type = data.type
        if data.value is not None:
            target.value = data.value
        if data.description is not None:
            target.description = data.description
        if data.config is not None:
            target.config = data.config
        db.commit()
        db.refresh(target)
        return target
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating target: {str(e)}")


@router.delete("/{target_id}")
async def delete_target(
    target_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a target if no scans exist for it"""
    target = db.query(Target).filter(Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found")
    project = db.query(Project).filter(Project.id == target.project_id).first()
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    try:
        from app.models.scan import Scan
        scans_count = db.query(Scan).filter(Scan.target_id == target_id).count()
        if scans_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete target with {scans_count} associated scans"
            )
        db.delete(target)
        db.commit()
        return {"status": "deleted", "target_id": target_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting target: {str(e)}")
