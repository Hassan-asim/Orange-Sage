"""
Comprehensive Scan Endpoints for Orange Sage
Integrates pentesting agents, microservices, and report generation
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.scan import Scan, ScanStatus
from app.models.project import Project
from app.models.target import Target
from app.models.finding import Finding
from app.models.agent import Agent, AgentStatus
from app.schemas.scan import ScanCreate, ScanResponse, ScanStatusResponse
from app.services.agent_manager import AgentManager
from app.services.microservices_orchestrator import MicroservicesOrchestrator
from app.services.advanced_report_generator import AdvancedReportGenerator
from app.agents.pentesting_agent import PentestingAgent
from app.utils.auth import get_current_user
from app.schemas.auth import UserResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
agent_manager = AgentManager()
microservices_orchestrator = MicroservicesOrchestrator()
report_generator = AdvancedReportGenerator()


@router.post("/projects/{project_id}/targets/{target_id}/comprehensive-scan", 
             response_model=ScanResponse, 
             status_code=status.HTTP_202_ACCEPTED)
async def start_comprehensive_scan(
    project_id: UUID,
    target_id: UUID,
    scan_config: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a comprehensive security scan with AI agents and microservices"""
    try:
        # Verify project and target ownership
        project = await db.get(Project, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Project not found or not owned by user"
            )

        target = await db.get(Target, target_id)
        if not target or target.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Target not found or not part of project"
            )

        # Create scan record
        scan = Scan(
            project_id=project_id,
            target_id=target_id,
            name=f"Comprehensive Security Scan - {target.value}",
            scan_type="comprehensive",
            status=ScanStatus.PENDING,
            created_by=current_user.id,
            config=scan_config
        )
        db.add(scan)
        await db.commit()
        await db.refresh(scan)

        # Start comprehensive scan in background
        background_tasks.add_task(
            _execute_comprehensive_scan,
            scan.id,
            target.value,
            scan_config,
            db
        )

        logger.info(f"Started comprehensive scan {scan.id} for target {target.value}")

        return ScanResponse(
            id=scan.id,
            project_id=scan.project_id,
            target_id=scan.target_id,
            name=scan.name,
            status=scan.status,
            created_at=scan.created_at,
            created_by=scan.created_by
        )

    except Exception as e:
        logger.error(f"Error starting comprehensive scan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start scan: {str(e)}"
        )


async def _execute_comprehensive_scan(
    scan_id: UUID,
    target: str,
    scan_config: Dict[str, Any],
    db: AsyncSession
):
    """Execute comprehensive security scan"""
    try:
        # Update scan status
        scan = await db.get(Scan, scan_id)
        if not scan:
            logger.error(f"Scan {scan_id} not found")
            return

        scan.status = ScanStatus.RUNNING
        scan.started_at = datetime.now()
        await db.commit()

        logger.info(f"Starting comprehensive scan {scan_id} for target: {target}")

        # Phase 1: AI Agent Pentesting
        logger.info("Phase 1: AI Agent Pentesting")
        pentesting_results = await _run_ai_pentesting(scan_id, target, scan_config, db)

        # Phase 2: Microservices Analysis
        logger.info("Phase 2: Microservices Analysis")
        microservices_results = await _run_microservices_analysis(scan_id, target, scan_config, db)

        # Phase 3: Advanced Analysis
        logger.info("Phase 3: Advanced Analysis")
        advanced_results = await _run_advanced_analysis(scan_id, target, scan_config, db)

        # Phase 4: Report Generation
        logger.info("Phase 4: Report Generation")
        report_results = await _generate_comprehensive_report(
            scan_id, target, scan_config, db
        )

        # Update scan completion
        scan.status = ScanStatus.COMPLETED
        scan.finished_at = datetime.now()
        scan.summary = {
            'phases_completed': 4,
            'ai_agent_results': pentesting_results,
            'microservices_results': microservices_results,
            'advanced_results': advanced_results,
            'report_generated': report_results is not None
        }
        await db.commit()

        logger.info(f"Comprehensive scan {scan_id} completed successfully")

    except Exception as e:
        logger.error(f"Error in comprehensive scan {scan_id}: {e}")
        # Update scan status to failed
        scan = await db.get(Scan, scan_id)
        if scan:
            scan.status = ScanStatus.FAILED
            scan.error_message = str(e)
            scan.finished_at = datetime.now()
            await db.commit()


async def _run_ai_pentesting(
    scan_id: UUID,
    target: str,
    scan_config: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Run AI-powered pentesting"""
    try:
        # Create pentesting agent
        agent_id = str(uuid.uuid4())
        pentesting_agent = PentestingAgent(
            agent_id=agent_id,
            target=target,
            config=scan_config
        )

        # Execute pentesting
        results = await pentesting_agent.execute_pentest()

        # Store findings in database
        if results.get('findings'):
            for finding_data in results['findings']:
                finding = Finding(
                    scan_id=scan_id,
                    title=finding_data.get('title', 'Security Finding'),
                    description=finding_data.get('description', ''),
                    severity=finding_data.get('severity', 'medium'),
                    finding_type=finding_data.get('type', 'unknown'),
                    endpoint=finding_data.get('endpoint', ''),
                    parameter=finding_data.get('parameter', ''),
                    payload=finding_data.get('payload', ''),
                    remediation=finding_data.get('remediation', ''),
                    references=finding_data.get('references', {}),
                    created_by_agent=agent_id
                )
                db.add(finding)

        await db.commit()

        logger.info(f"AI pentesting completed for scan {scan_id}")
        return results

    except Exception as e:
        logger.error(f"Error in AI pentesting: {e}")
        return {'error': str(e)}


async def _run_microservices_analysis(
    scan_id: UUID,
    target: str,
    scan_config: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Run microservices-based analysis"""
    try:
        # Configure microservices analysis
        analysis_config = {
            'enable_vulnerability_scanning': scan_config.get('enable_vulnerability_scanning', True),
            'enable_network_analysis': scan_config.get('enable_network_analysis', True),
            'enable_code_analysis': scan_config.get('enable_code_analysis', False),
            'enable_compliance_checking': scan_config.get('enable_compliance_checking', True),
            'enable_threat_intelligence': scan_config.get('enable_threat_intelligence', True),
            'scan_types': scan_config.get('scan_types', ['web', 'api']),
            'scan_depth': scan_config.get('scan_depth', 'comprehensive')
        }

        # Start microservices analysis
        results = await microservices_orchestrator.start_comprehensive_analysis(
            target=target,
            analysis_config=analysis_config
        )

        # Store additional findings from microservices
        if results.get('findings'):
            for finding_data in results['findings']:
                finding = Finding(
                    scan_id=scan_id,
                    title=finding_data.get('title', 'Microservices Finding'),
                    description=finding_data.get('description', ''),
                    severity=finding_data.get('severity', 'medium'),
                    finding_type=finding_data.get('type', 'microservices'),
                    endpoint=finding_data.get('endpoint', ''),
                    parameter=finding_data.get('parameter', ''),
                    payload=finding_data.get('payload', ''),
                    remediation=finding_data.get('remediation', ''),
                    references=finding_data.get('references', {}),
                    created_by_agent='microservices'
                )
                db.add(finding)

        await db.commit()

        logger.info(f"Microservices analysis completed for scan {scan_id}")
        return results

    except Exception as e:
        logger.error(f"Error in microservices analysis: {e}")
        return {'error': str(e)}


async def _run_advanced_analysis(
    scan_id: UUID,
    target: str,
    scan_config: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Run advanced analysis techniques"""
    try:
        # Get existing findings for correlation
        stmt = select(Finding).where(Finding.scan_id == scan_id)
        existing_findings = (await db.execute(stmt)).scalars().all()

        # Perform correlation analysis
        correlation_results = await _correlate_findings(existing_findings)

        # Perform risk assessment
        risk_assessment = await _assess_risk_level(existing_findings)

        # Generate recommendations
        recommendations = await _generate_security_recommendations(existing_findings)

        logger.info(f"Advanced analysis completed for scan {scan_id}")
        return {
            'correlation_analysis': correlation_results,
            'risk_assessment': risk_assessment,
            'recommendations': recommendations
        }

    except Exception as e:
        logger.error(f"Error in advanced analysis: {e}")
        return {'error': str(e)}


async def _correlate_findings(findings: List[Finding]) -> Dict[str, Any]:
    """Correlate findings to identify attack chains and patterns"""
    try:
        # Group findings by type and severity
        findings_by_type = {}
        findings_by_severity = {}
        
        for finding in findings:
            finding_type = finding.finding_type
            severity = finding.severity
            
            if finding_type not in findings_by_type:
                findings_by_type[finding_type] = []
            findings_by_type[finding_type].append(finding)
            
            if severity not in findings_by_severity:
                findings_by_severity[severity] = []
            findings_by_severity[severity].append(finding)

        # Identify potential attack chains
        attack_chains = []
        
        # SQL Injection -> Data Exfiltration
        sql_injection = [f for f in findings if f.finding_type == 'sql_injection']
        data_exposure = [f for f in findings if 'data' in f.title.lower() or 'information' in f.title.lower()]
        
        if sql_injection and data_exposure:
            attack_chains.append({
                'chain': 'SQL Injection -> Data Exfiltration',
                'findings': sql_injection + data_exposure,
                'risk_level': 'high'
            })

        # XSS -> Session Hijacking
        xss_findings = [f for f in findings if f.finding_type == 'xss']
        session_findings = [f for f in findings if 'session' in f.title.lower()]
        
        if xss_findings and session_findings:
            attack_chains.append({
                'chain': 'XSS -> Session Hijacking',
                'findings': xss_findings + session_findings,
                'risk_level': 'high'
            })

        return {
            'findings_by_type': {k: len(v) for k, v in findings_by_type.items()},
            'findings_by_severity': {k: len(v) for k, v in findings_by_severity.items()},
            'attack_chains': attack_chains,
            'correlation_score': len(attack_chains) * 10
        }

    except Exception as e:
        logger.error(f"Error in correlation analysis: {e}")
        return {'error': str(e)}


async def _assess_risk_level(findings: List[Finding]) -> Dict[str, Any]:
    """Assess overall risk level based on findings"""
    try:
        # Calculate risk metrics
        total_findings = len(findings)
        critical_count = len([f for f in findings if f.severity == 'critical'])
        high_count = len([f for f in findings if f.severity == 'high'])
        medium_count = len([f for f in findings if f.severity == 'medium'])
        low_count = len([f for f in findings if f.severity == 'low'])

        # Calculate risk score
        risk_score = (critical_count * 10 + high_count * 7 + medium_count * 4 + low_count * 1)
        risk_score = min(risk_score, 100)

        # Determine risk level
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Identify high-risk combinations
        high_risk_combinations = []
        
        if critical_count > 0 and high_count > 2:
            high_risk_combinations.append("Multiple critical and high severity findings")
        
        if total_findings > 20:
            high_risk_combinations.append("High volume of security findings")

        return {
            'total_findings': total_findings,
            'critical_count': critical_count,
            'high_count': high_count,
            'medium_count': medium_count,
            'low_count': low_count,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'high_risk_combinations': high_risk_combinations
        }

    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        return {'error': str(e)}


async def _generate_security_recommendations(findings: List[Finding]) -> List[str]:
    """Generate security recommendations based on findings"""
    try:
        recommendations = []

        # Analyze findings and generate specific recommendations
        critical_findings = [f for f in findings if f.severity == 'critical']
        if critical_findings:
            recommendations.append("Immediately address all critical severity findings as they pose the highest risk.")

        sql_injection = [f for f in findings if f.finding_type == 'sql_injection']
        if sql_injection:
            recommendations.append("Implement parameterized queries and input validation to prevent SQL injection attacks.")

        xss_findings = [f for f in findings if f.finding_type == 'xss']
        if xss_findings:
            recommendations.append("Implement proper input validation and output encoding to prevent XSS attacks.")

        # General recommendations
        recommendations.extend([
            "Conduct regular security assessments and penetration testing.",
            "Implement a Web Application Firewall (WAF) for additional protection.",
            "Establish security awareness training for development teams.",
            "Implement a secure development lifecycle (SDL) process.",
            "Regularly update and patch all software components.",
            "Implement comprehensive logging and monitoring for security events."
        ])

        return recommendations

    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return ["Error generating recommendations"]


async def _generate_comprehensive_report(
    scan_id: UUID,
    target: str,
    scan_config: Dict[str, Any],
    db: AsyncSession
) -> Dict[str, Any]:
    """Generate comprehensive security report"""
    try:
        # Get scan data
        scan = await db.get(Scan, scan_id)
        if not scan:
            return {'error': 'Scan not found'}

        # Get all findings
        stmt = select(Finding).where(Finding.scan_id == scan_id)
        findings = (await db.execute(stmt)).scalars().all()

        # Convert findings to dict format
        findings_data = []
        for finding in findings:
            findings_data.append({
                'title': finding.title,
                'description': finding.description,
                'severity': finding.severity,
                'type': finding.finding_type,
                'endpoint': finding.endpoint,
                'parameter': finding.parameter,
                'payload': finding.payload,
                'remediation': finding.remediation,
                'references': finding.references
            })

        # Prepare scan data
        scan_data = {
            'id': str(scan.id),
            'name': scan.name,
            'scan_type': scan.scan_type,
            'status': scan.status.value,
            'created_at': scan.created_at.isoformat() if scan.created_at else None,
            'started_at': scan.started_at.isoformat() if scan.started_at else None,
            'finished_at': scan.finished_at.isoformat() if scan.finished_at else None,
            'summary': scan.summary
        }

        # Prepare target info
        target_info = {
            'url': target,
            'hostname': target.split('://')[-1].split('/')[0] if '://' in target else target
        }

        # Generate PDF report
        pdf_bytes = await report_generator.generate_comprehensive_report(
            scan_data=scan_data,
            findings=findings_data,
            target_info=target_info,
            branding={
                'company_name': 'Orange Sage',
                'logo_url': None,
                'color_scheme': 'blue'
            }
        )

        # Generate HTML report
        html_content = await report_generator.generate_html_report(
            scan_data=scan_data,
            findings=findings_data,
            target_info=target_info,
            branding={
                'company_name': 'Orange Sage',
                'logo_url': None,
                'color_scheme': 'blue'
            }
        )

        logger.info(f"Comprehensive report generated for scan {scan_id}")
        return {
            'pdf_report': base64.b64encode(pdf_bytes).decode('utf-8'),
            'html_report': html_content,
            'findings_count': len(findings_data)
        }

    except Exception as e:
        logger.error(f"Error generating comprehensive report: {e}")
        return {'error': str(e)}


@router.get("/scans/{scan_id}/comprehensive-status", response_model=ScanStatusResponse)
async def get_comprehensive_scan_status(
    scan_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive scan status and progress"""
    try:
        # Get scan
        scan = await db.get(Scan, scan_id)
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )

        # Verify ownership
        project = await db.get(Project, scan.project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this scan"
            )

        # Get findings count
        stmt = select(Finding).where(Finding.scan_id == scan_id)
        findings = (await db.execute(stmt)).scalars().all()
        findings_count = len(findings)

        # Get agents count
        stmt = select(Agent).where(Agent.scan_id == scan_id)
        agents = (await db.execute(stmt)).scalars().all()
        agents_count = len(agents)

        # Calculate progress
        progress = 0
        if scan.status == ScanStatus.COMPLETED:
            progress = 100
        elif scan.status == ScanStatus.RUNNING:
            # Estimate progress based on findings and time
            if scan.started_at:
                elapsed = (datetime.now() - scan.started_at).total_seconds()
                progress = min(int(elapsed / 60 * 10), 90)  # Rough estimate
            else:
                progress = 10

        return ScanStatusResponse(
            id=scan.id,
            project_id=scan.project_id,
            target_id=scan.target_id,
            name=scan.name,
            status=scan.status,
            progress=progress,
            started_at=scan.started_at,
            finished_at=scan.finished_at,
            findings_count=findings_count,
            agents_count=agents_count,
            summary=scan.summary,
            error=scan.error_message
        )

    except Exception as e:
        logger.error(f"Error getting scan status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get scan status: {str(e)}"
        )


@router.get("/scans/{scan_id}/comprehensive-report")
async def download_comprehensive_report(
    scan_id: UUID,
    format: str = "pdf",
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download comprehensive security report"""
    try:
        # Get scan
        scan = await db.get(Scan, scan_id)
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Scan not found"
            )

        # Verify ownership
        project = await db.get(Project, scan.project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this scan"
            )

        # Get findings
        stmt = select(Finding).where(Finding.scan_id == scan_id)
        findings = (await db.execute(stmt)).scalars().all()

        # Convert findings to dict format
        findings_data = []
        for finding in findings:
            findings_data.append({
                'title': finding.title,
                'description': finding.description,
                'severity': finding.severity,
                'type': finding.finding_type,
                'endpoint': finding.endpoint,
                'parameter': finding.parameter,
                'payload': finding.payload,
                'remediation': finding.remediation,
                'references': finding.references
            })

        # Prepare data
        scan_data = {
            'id': str(scan.id),
            'name': scan.name,
            'scan_type': scan.scan_type,
            'status': scan.status.value,
            'created_at': scan.created_at.isoformat() if scan.created_at else None,
            'started_at': scan.started_at.isoformat() if scan.started_at else None,
            'finished_at': scan.finished_at.isoformat() if scan.finished_at else None,
            'summary': scan.summary
        }

        target_info = {
            'url': scan.target.value if scan.target else 'Unknown',
            'hostname': 'Unknown'
        }

        if format.lower() == "pdf":
            # Generate PDF report
            pdf_bytes = await report_generator.generate_comprehensive_report(
                scan_data=scan_data,
                findings=findings_data,
                target_info=target_info
            )
            
            return {
                'content': base64.b64encode(pdf_bytes).decode('utf-8'),
                'content_type': 'application/pdf',
                'filename': f"orange_sage_report_{scan_id}.pdf"
            }
        
        elif format.lower() == "html":
            # Generate HTML report
            html_content = await report_generator.generate_html_report(
                scan_data=scan_data,
                findings=findings_data,
                target_info=target_info
            )
            
            return {
                'content': html_content,
                'content_type': 'text/html',
                'filename': f"orange_sage_report_{scan_id}.html"
            }
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid format. Supported formats: pdf, html"
            )

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )
