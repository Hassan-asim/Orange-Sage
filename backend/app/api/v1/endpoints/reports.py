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


@router.get("")
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reports for the current user"""
    try:
        reports = db.query(Report).order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
        
        # Return array directly for frontend compatibility
        return [
            {
                "id": report.id,
                "name": report.name,
                "format": report.format.value,
                "status": report.status.value,
                "scan_id": report.scan_id,
                "created_at": report.created_at.isoformat() if report.created_at else None,
                "generated_at": report.generated_at.isoformat() if report.generated_at else None,
                "download_url": report.download_url,
                "file_size": report.file_size
            }
            for report in reports
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching reports: {str(e)}"
        )


@router.post("/generate")
async def generate_report(
    scan_id: int,
    format: str = "html",
    include_charts: bool = True,
    include_pocs: bool = True,
    branding: str = "Orange Sage",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a detailed security assessment report for a scan"""
    try:
        from app.models.scan import Scan
        from app.models.finding import Finding
        from datetime import datetime
        
        # Get scan
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )
        
        # Get findings
        findings = db.query(Finding).filter(Finding.scan_id == scan_id).all()
        
        # Create report record
        report = Report(
            name=f"Security Assessment Report - {scan.name}",
            format=ReportFormat.HTML if format.lower() == "html" else ReportFormat.PDF,
            status=ReportStatus.COMPLETED,
            scan_id=scan_id,
            include_charts="true",
            include_pocs="true",
            branding=branding,
            generated_at=datetime.utcnow()
        )
        
        # Generate detailed HTML report
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Assessment Report - {scan.name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; 
               line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
        .header h1 {{ font-size: 32px; margin-bottom: 10px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .summary {{ padding: 30px; background: #f8f9fa; border-bottom: 3px solid #667eea; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }}
        .summary-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary-card h3 {{ font-size: 36px; margin-bottom: 5px; }}
        .summary-card p {{ color: #666; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }}
        .critical {{ color: #dc3545; }}
        .high {{ color: #fd7e14; }}
        .medium {{ color: #ffc107; }}
        .low {{ color: #28a745; }}
        .content {{ padding: 40px; }}
        .section {{ margin-bottom: 40px; }}
        .section h2 {{ color: #667eea; font-size: 24px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid #e9ecef; }}
        .finding {{ background: #f8f9fa; padding: 25px; margin-bottom: 20px; border-left: 4px solid #667eea; border-radius: 4px; }}
        .finding.critical {{ border-left-color: #dc3545; background: #fff5f5; }}
        .finding.high {{ border-left-color: #fd7e14; background: #fff8f0; }}
        .finding.medium {{ border-left-color: #ffc107; background: #fffbf0; }}
        .finding.low {{ border-left-color: #28a745; background: #f0fff4; }}
        .finding-header {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px; }}
        .finding-title {{ font-size: 20px; font-weight: 600; color: #2d3748; }}
        .severity-badge {{ padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; }}
        .severity-badge.critical {{ background: #dc3545; color: white; }}
        .severity-badge.high {{ background: #fd7e14; color: white; }}
        .severity-badge.medium {{ background: #ffc107; color: #000; }}
        .severity-badge.low {{ background: #28a745; color: white; }}
        .finding-meta {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 15px 0; 
                         padding: 15px; background: white; border-radius: 4px; }}
        .meta-item {{ }}
        .meta-label {{ font-weight: 600; color: #667eea; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .meta-value {{ color: #555; margin-top: 4px; font-family: 'Courier New', monospace; font-size: 13px; }}
        .finding-description {{ margin: 15px 0; line-height: 1.8; color: #4a5568; }}
        .remediation {{ background: #e3f2fd; padding: 15px; border-radius: 4px; margin-top: 15px; }}
        .remediation h4 {{ color: #1976d2; margin-bottom: 10px; font-size: 16px; }}
        .references {{ margin-top: 15px; }}
        .references h4 {{ color: #667eea; margin-bottom: 8px; font-size: 14px; }}
        .references ul {{ list-style: none; padding-left: 0; }}
        .references li {{ padding: 4px 0; color: #666; }}
        .references a {{ color: #667eea; text-decoration: none; }}
        .references a:hover {{ text-decoration: underline; }}
        .footer {{ background: #2d3748; color: white; padding: 20px 40px; text-align: center; font-size: 14px; }}
        .scan-info {{ background: #e3f2fd; padding: 20px; border-radius: 4px; margin-bottom: 20px; }}
        .scan-info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .info-item {{ }}
        .info-label {{ font-weight: 600; color: #1976d2; font-size: 12px; text-transform: uppercase; }}
        .info-value {{ color: #444; margin-top: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 Security Assessment Report</h1>
            <p>Generated by {branding} | {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary">
            <h2 style="color: #2d3748; margin-bottom: 10px;">Executive Summary</h2>
            <p>This report contains the results of a comprehensive security assessment performed on the target application.</p>
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>{len(findings)}</h3>
                    <p>Total Findings</p>
                </div>
                <div class="summary-card">
                    <h3 class="critical">{len([f for f in findings if f.severity.value == 'critical'])}</h3>
                    <p>Critical</p>
                </div>
                <div class="summary-card">
                    <h3 class="high">{len([f for f in findings if f.severity.value == 'high'])}</h3>
                    <p>High</p>
                </div>
                <div class="summary-card">
                    <h3 class="medium">{len([f for f in findings if f.severity.value == 'medium'])}</h3>
                    <p>Medium</p>
                </div>
                <div class="summary-card">
                    <h3 class="low">{len([f for f in findings if f.severity.value == 'low'])}</h3>
                    <p>Low</p>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📋 Scan Information</h2>
                <div class="scan-info">
                    <div class="scan-info-grid">
                        <div class="info-item">
                            <div class="info-label">Scan Name</div>
                            <div class="info-value">{scan.name}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Target</div>
                            <div class="info-value">{scan.target.value if scan.target else 'N/A'}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Scan Status</div>
                            <div class="info-value">{scan.status.value.upper()}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Started</div>
                            <div class="info-value">{scan.started_at.strftime('%Y-%m-%d %H:%M') if scan.started_at else 'N/A'}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Completed</div>
                            <div class="info-value">{scan.finished_at.strftime('%Y-%m-%d %H:%M') if scan.finished_at else 'N/A'}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔍 Detailed Findings</h2>
                <p style="margin-bottom: 20px; color: #666;">The following security issues were identified during the assessment. Each finding includes a detailed description, affected components, and remediation guidance.</p>
"""
        
        # Group findings by severity
        findings_by_severity = {
            'critical': [f for f in findings if f.severity.value == 'critical'],
            'high': [f for f in findings if f.severity.value == 'high'],
            'medium': [f for f in findings if f.severity.value == 'medium'],
            'low': [f for f in findings if f.severity.value == 'low']
        }
        
        # Add findings to report
        for severity, severity_findings in findings_by_severity.items():
            if severity_findings:
                for idx, finding in enumerate(severity_findings, 1):
                    html_content += f"""
                <div class="finding {severity}">
                    <div class="finding-header">
                        <div class="finding-title">#{idx}. {finding.title}</div>
                        <span class="severity-badge {severity}">{severity.upper()}</span>
                    </div>
                    
                    <div class="finding-meta">
                        <div class="meta-item">
                            <div class="meta-label">Type</div>
                            <div class="meta-value">{finding.vulnerability_type or 'N/A'}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Endpoint</div>
                            <div class="meta-value">{finding.endpoint or 'N/A'}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Parameter</div>
                            <div class="meta-value">{finding.parameter or 'N/A'}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Method</div>
                            <div class="meta-value">{finding.method or 'N/A'}</div>
                        </div>
                    </div>
                    
                    <div class="finding-description">
                        <strong>Description:</strong><br>
                        {finding.description or 'No description provided.'}
                    </div>
                    
                    <div class="remediation">
                        <h4>🛠️ Remediation</h4>
                        <p>{finding.remediation_text or 'Please consult with security experts for remediation guidance.'}</p>
                    </div>
                    
                    {f'''<div class="references">
                        <h4>📚 References</h4>
                        <ul>
                            {''.join([f'<li><strong>{k.upper()}:</strong> {v}</li>' for k, v in (finding.references or {}).items()])}
                        </ul>
                    </div>''' if finding.references else ''}
                </div>
"""
        
        html_content += """
            </div>
        </div>
        
        <div class="footer">
            <p>This report was generated automatically by Orange Sage Security Platform.</p>
            <p style="margin-top: 10px; font-size: 12px; opacity: 0.8;">© 2025 Orange Sage. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save report content
        import base64
        report.storage_key = f"report_{report.id}_{datetime.now().timestamp()}.html"
        report.download_url = f"/api/v1/reports/{report.id}/download"
        report.file_size = len(html_content.encode('utf-8'))
        report.report_metadata = {
            "html_content": base64.b64encode(html_content.encode('utf-8')).decode('utf-8'),
            "total_findings": len(findings),
            "findings_by_severity": {k: len(v) for k, v in findings_by_severity.items()}
        }
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return {
            "id": report.id,
            "name": report.name,
            "status": report.status.value,
            "format": report.format.value,
            "scan_id": scan_id,
            "download_url": report.download_url,
            "file_size": report.file_size,
            "generated_at": report.generated_at.isoformat() if report.generated_at else None,
            "preview": html_content[:500] + "..." if len(html_content) > 500 else html_content
        }
        
    except HTTPException:
        raise
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
    format: str = "html",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download a generated report as HTML or PDF (if available with WeasyPrint)"""
    try:
        import base64
        from app.models.scan import Scan

        # Get report
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )

        # Get HTML content from metadata
        if not report.report_metadata or 'html_content' not in report.report_metadata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report content not found"
            )

        # Decode HTML content
        html_content = base64.b64decode(report.report_metadata['html_content']).decode('utf-8')

        # Determine filename root
        scan = db.query(Scan).filter(Scan.id == report.scan_id).first()
        name_root = f"security_report_{scan.name if scan else report.id}".replace(" ", "_")

        if format.lower() == "pdf":
            # Try to render PDF with WeasyPrint
            try:
                import weasyprint
            except ImportError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="PDF export requires WeasyPrint. Please ask the server admin to install 'weasyprint'."
                )
            # Convert HTML to PDF
            pdf_bytes = weasyprint.HTML(string=html_content).write_pdf()
            pdf_filename = f"{name_root}.pdf"
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={pdf_filename}",
                    "Content-Length": str(len(pdf_bytes))
                }
            )

        # Default: Download HTML
        html_filename = f"{name_root}.html"
        return Response(
            content=html_content,
            media_type="text/html",
            headers={
                "Content-Disposition": f"attachment; filename={html_filename}",
                "Content-Length": str(len(html_content))
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error downloading report: {str(e)}"
        )
