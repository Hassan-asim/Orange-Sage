"""
Report endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.core.database import get_db
from app.models.report import Report, ReportFormat, ReportStatus
from app.models.user import User
from app.services.report_generator import ReportGenerator
from app.utils.auth import get_current_user

router = APIRouter()


@router.post("/generate")
async def generate_report(
    scan_id: int,
    format: str = "pdf",
    include_charts: bool = True,
    include_pocs: bool = True,
    branding: str = "Orange Sage",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a report for a scan"""
    try:
        # Validate format
        try:
            report_format = ReportFormat(format)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid format. Must be one of: {', '.join([f.value for f in ReportFormat])}"
            )
        
        # Generate report
        report_generator = ReportGenerator()
        options = {
            "include_charts": include_charts,
            "include_pocs": include_pocs,
            "branding": branding
        }
        
        result = await report_generator.generate_report(
            db, scan_id, report_format, options
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )


@router.get("/{report_id}/status")
async def get_report_status(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get report generation status"""
    try:
        report_generator = ReportGenerator()
        status_info = await report_generator.get_report_status(report_id, db)
        
        return status_info
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting report status: {str(e)}"
        )


@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a generated report"""
    try:
        report_generator = ReportGenerator()
        file_path = await report_generator.download_report(report_id, db)
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report file not found"
            )
        
        # Get file info
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        
        # Determine content type
        if file_path.endswith('.pdf'):
            media_type = "application/pdf"
        elif file_path.endswith('.docx'):
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        elif file_path.endswith('.html'):
            media_type = "text/html"
        else:
            media_type = "application/octet-stream"
        
        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(file_size)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading report: {str(e)}"
        )
