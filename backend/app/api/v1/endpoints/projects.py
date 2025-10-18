"""
Project endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.project import Project
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter()


@router.get("/")
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List projects for the current user"""
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    
    return {
        "projects": [
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at
            }
            for project in projects
        ]
    }


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }
