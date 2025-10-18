"""
Target endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.target import Target
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter()


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


@router.get("/{target_id}")
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
    
    return {
        "id": target.id,
        "name": target.name,
        "type": target.type,
        "value": target.value,
        "description": target.description,
        "project_id": target.project_id,
        "config": target.config,
        "created_at": target.created_at
    }
