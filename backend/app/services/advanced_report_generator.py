"""
Advanced Report Generator for Orange Sage
Generates comprehensive PDF reports with detailed analysis
"""

import asyncio
import base64
import io
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# PDF generation libraries
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

# HTML to PDF conversion
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    # WeasyPrint requires GTK+ libraries which are not available by default on Windows
    # The application will work fine without it, using ReportLab for PDF generation instead
    WEASYPRINT_AVAILABLE = False
    weasyprint = None
    # Only log at debug level to avoid alarming users
    logger_temp = logging.getLogger(__name__)
    logger_temp.debug(f"WeasyPrint not available: {e}")

from jinja2 import Template

logger = logging.getLogger(__name__)


class AdvancedReportGenerator:
    """Advanced report generator with comprehensive analysis"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2E86AB')
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.HexColor('#A23B72')
        ))
        
        # Finding title style
        self.styles.add(ParagraphStyle(
            name='FindingTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#F18F01')
        ))
        
        # Critical severity style
        self.styles.add(ParagraphStyle(
            name='CriticalSeverity',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#D32F2F'),
            backColor=colors.HexColor('#FFEBEE')
        ))
        
        # High severity style
        self.styles.add(ParagraphStyle(
            name='HighSeverity',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#F57C00'),
            backColor=colors.HexColor('#FFF3E0')
        ))
        
        # Medium severity style
        self.styles.add(ParagraphStyle(
            name='MediumSeverity',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#FBC02D'),
            backColor=colors.HexColor('#FFFDE7')
        ))
        
        # Low severity style
        self.styles.add(ParagraphStyle(
            name='LowSeverity',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#388E3C'),
            backColor=colors.HexColor('#E8F5E8')
        ))
    
    async def generate_comprehensive_report(
        self,
        scan_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        target_info: Dict[str, Any],
        branding: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """Generate comprehensive PDF report"""
        try:
            # Create PDF document
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build report content
            story = []
            
            # Cover page
            story.extend(self._create_cover_page(scan_data, target_info, branding))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self._create_executive_summary(scan_data, findings))
            story.append(PageBreak())
            
            # Methodology
            story.extend(self._create_methodology_section())
            story.append(PageBreak())
            
            # Detailed findings
            story.extend(self._create_findings_section(findings))
            story.append(PageBreak())
            
            # Risk assessment
            story.extend(self._create_risk_assessment_section(findings))
            story.append(PageBreak())
            
            # Recommendations
            story.extend(self._create_recommendations_section(findings))
            story.append(PageBreak())
            
            # Technical details
            story.extend(self._create_technical_details_section(scan_data, findings))
            story.append(PageBreak())
            
            # Appendix
            story.extend(self._create_appendix_section(scan_data, findings))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            logger.info(f"Generated comprehensive report with {len(findings)} findings")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise
    
    def _create_cover_page(
        self,
        scan_data: Dict[str, Any],
        target_info: Dict[str, Any],
        branding: Optional[Dict[str, Any]] = None
    ) -> List:
        """Create cover page"""
        story = []
        
        # Title
        story.append(Paragraph("Orange Sage Security Assessment Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Target information
        story.append(Paragraph("Target Information", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        target_table_data = [
            ['Target:', target_info.get('url', target_info.get('hostname', 'N/A'))],
            ['Scan Date:', scan_data.get('created_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))],
            ['Scan ID:', scan_data.get('id', 'N/A')],
            ['Scan Type:', scan_data.get('scan_type', 'Comprehensive Security Assessment')],
            ['Status:', scan_data.get('status', 'Completed')]
        ]
        
        target_table = Table(target_table_data, colWidths=[2*inch, 4*inch])
        target_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(target_table)
        story.append(Spacer(1, 30))
        
        # Confidentiality notice
        story.append(Paragraph(
            "CONFIDENTIAL - This report contains sensitive security information and should be handled with appropriate care.",
            self.styles['Normal']
        ))
        
        return story
    
    def _create_executive_summary(
        self,
        scan_data: Dict[str, Any],
        findings: List[Dict[str, Any]]
    ) -> List:
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Calculate statistics
        total_findings = len(findings)
        critical_count = len([f for f in findings if f.get('severity') == 'critical'])
        high_count = len([f for f in findings if f.get('severity') == 'high'])
        medium_count = len([f for f in findings if f.get('severity') == 'medium'])
        low_count = len([f for f in findings if f.get('severity') == 'low'])
        
        # Risk score calculation
        risk_score = (critical_count * 10 + high_count * 7 + medium_count * 4 + low_count * 1)
        risk_score = min(risk_score, 100)
        
        # Summary text
        summary_text = f"""
        This security assessment was conducted on {scan_data.get('target', 'the target system')} 
        using Orange Sage's AI-powered penetration testing capabilities. The assessment identified 
        {total_findings} security findings across various categories.
        
        <b>Key Statistics:</b><br/>
        • Total Findings: {total_findings}<br/>
        • Critical: {critical_count}<br/>
        • High: {high_count}<br/>
        • Medium: {medium_count}<br/>
        • Low: {low_count}<br/>
        • Overall Risk Score: {risk_score}/100
        """
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Risk level
        if risk_score >= 80:
            risk_level = "CRITICAL"
            risk_color = colors.HexColor('#D32F2F')
        elif risk_score >= 60:
            risk_level = "HIGH"
            risk_color = colors.HexColor('#F57C00')
        elif risk_score >= 40:
            risk_level = "MEDIUM"
            risk_color = colors.HexColor('#FBC02D')
        else:
            risk_level = "LOW"
            risk_color = colors.HexColor('#388E3C')
        
        story.append(Paragraph(f"<b>Overall Risk Level: {risk_level}</b>", 
                              ParagraphStyle('RiskLevel', parent=self.styles['Normal'], 
                                           fontSize=14, textColor=risk_color)))
        
        return story
    
    def _create_methodology_section(self) -> List:
        """Create methodology section"""
        story = []
        
        story.append(Paragraph("Assessment Methodology", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        methodology_text = """
        This security assessment was conducted using Orange Sage's AI-powered penetration testing framework, 
        which combines automated vulnerability scanning with intelligent analysis and manual verification techniques.
        
        <b>Phase 1: Reconnaissance</b><br/>
        • Information gathering and target enumeration<br/>
        • Technology fingerprinting and service identification<br/>
        • Network and application mapping<br/>
        
        <b>Phase 2: Vulnerability Scanning</b><br/>
        • Automated vulnerability detection using multiple techniques<br/>
        • Custom payload injection and testing<br/>
        • Configuration analysis and security header assessment<br/>
        
        <b>Phase 3: Exploitation Testing</b><br/>
        • Manual verification of identified vulnerabilities<br/>
        • Proof-of-concept exploitation where safe and appropriate<br/>
        • Impact assessment and risk evaluation<br/>
        
        <b>Phase 4: Analysis and Reporting</b><br/>
        • Comprehensive analysis of findings<br/>
        • Risk scoring and prioritization<br/>
        • Detailed remediation recommendations<br/>
        """
        
        story.append(Paragraph(methodology_text, self.styles['Normal']))
        
        return story
    
    def _create_findings_section(self, findings: List[Dict[str, Any]]) -> List:
        """Create detailed findings section"""
        story = []
        
        story.append(Paragraph("Detailed Findings", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        if not findings:
            story.append(Paragraph("No security findings were identified during this assessment.", 
                                  self.styles['Normal']))
            return story
        
        # Group findings by severity
        findings_by_severity = {
            'critical': [f for f in findings if f.get('severity') == 'critical'],
            'high': [f for f in findings if f.get('severity') == 'high'],
            'medium': [f for f in findings if f.get('severity') == 'medium'],
            'low': [f for f in findings if f.get('severity') == 'low']
        }
        
        for severity in ['critical', 'high', 'medium', 'low']:
            severity_findings = findings_by_severity[severity]
            if not severity_findings:
                continue
            
            # Severity header
            severity_title = f"{severity.upper()} SEVERITY FINDINGS ({len(severity_findings)})"
            story.append(Paragraph(severity_title, self.styles['SectionHeader']))
            story.append(Spacer(1, 12))
            
            # Individual findings
            for i, finding in enumerate(severity_findings, 1):
                story.extend(self._create_finding_detail(finding, i))
                story.append(Spacer(1, 20))
        
        return story
    
    def _create_finding_detail(self, finding: Dict[str, Any], finding_number: int) -> List:
        """Create detailed finding information"""
        story = []
        
        # Finding title
        title = f"Finding {finding_number}: {finding.get('title', 'Security Finding')}"
        story.append(Paragraph(title, self.styles['FindingTitle']))
        story.append(Spacer(1, 8))
        
        # Finding details table
        details_data = [
            ['Severity:', finding.get('severity', 'Unknown').upper()],
            ['Type:', finding.get('type', 'Unknown')],
            ['Endpoint:', finding.get('endpoint', 'N/A')],
            ['Parameter:', finding.get('parameter', 'N/A')],
            ['Payload:', finding.get('payload', 'N/A')]
        ]
        
        details_table = Table(details_data, colWidths=[1.5*inch, 4.5*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 12))
        
        # Description
        story.append(Paragraph("<b>Description:</b>", self.styles['Normal']))
        story.append(Paragraph(finding.get('description', 'No description available.'), 
                              self.styles['Normal']))
        story.append(Spacer(1, 8))
        
        # Remediation
        if finding.get('remediation'):
            story.append(Paragraph("<b>Remediation:</b>", self.styles['Normal']))
            story.append(Paragraph(finding['remediation'], self.styles['Normal']))
            story.append(Spacer(1, 8))
        
        # References
        if finding.get('references'):
            story.append(Paragraph("<b>References:</b>", self.styles['Normal']))
            refs = finding['references']
            ref_text = ""
            for ref_type, ref_url in refs.items():
                ref_text += f"• {ref_type.upper()}: {ref_url}<br/>"
            story.append(Paragraph(ref_text, self.styles['Normal']))
        
        return story
    
    def _create_risk_assessment_section(self, findings: List[Dict[str, Any]]) -> List:
        """Create risk assessment section"""
        story = []
        
        story.append(Paragraph("Risk Assessment", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Calculate risk metrics
        total_findings = len(findings)
        critical_count = len([f for f in findings if f.get('severity') == 'critical'])
        high_count = len([f for f in findings if f.get('severity') == 'high'])
        medium_count = len([f for f in findings if f.get('severity') == 'medium'])
        low_count = len([f for f in findings if f.get('severity') == 'low'])
        
        # Risk score
        risk_score = (critical_count * 10 + high_count * 7 + medium_count * 4 + low_count * 1)
        risk_score = min(risk_score, 100)
        
        # Risk assessment text
        risk_text = f"""
        <b>Risk Metrics:</b><br/>
        • Total Security Findings: {total_findings}<br/>
        • Critical Severity: {critical_count} findings<br/>
        • High Severity: {high_count} findings<br/>
        • Medium Severity: {medium_count} findings<br/>
        • Low Severity: {low_count} findings<br/>
        • Calculated Risk Score: {risk_score}/100<br/><br/>
        
        <b>Risk Level Interpretation:</b><br/>
        """
        
        if risk_score >= 80:
            risk_text += "• <b>CRITICAL RISK</b> - Immediate action required to address security vulnerabilities<br/>"
        elif risk_score >= 60:
            risk_text += "• <b>HIGH RISK</b> - Prompt remediation recommended<br/>"
        elif risk_score >= 40:
            risk_text += "• <b>MEDIUM RISK</b> - Address findings within reasonable timeframe<br/>"
        else:
            risk_text += "• <b>LOW RISK</b> - Monitor and address as part of regular maintenance<br/>"
        
        story.append(Paragraph(risk_text, self.styles['Normal']))
        
        return story
    
    def _create_recommendations_section(self, findings: List[Dict[str, Any]]) -> List:
        """Create recommendations section"""
        story = []
        
        story.append(Paragraph("Security Recommendations", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Generate recommendations based on findings
        recommendations = self._generate_recommendations(findings)
        
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", self.styles['Normal']))
            story.append(Spacer(1, 8))
        
        return story
    
    def _create_technical_details_section(
        self,
        scan_data: Dict[str, Any],
        findings: List[Dict[str, Any]]
    ) -> List:
        """Create technical details section"""
        story = []
        
        story.append(Paragraph("Technical Details", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Scan configuration
        story.append(Paragraph("<b>Scan Configuration:</b>", self.styles['Normal']))
        story.append(Spacer(1, 8))
        
        config_data = [
            ['Scan ID:', scan_data.get('id', 'N/A')],
            ['Scan Type:', scan_data.get('scan_type', 'Comprehensive Security Assessment')],
            ['Start Time:', scan_data.get('started_at', 'N/A')],
            ['End Time:', scan_data.get('finished_at', 'N/A')],
            ['Duration:', scan_data.get('duration', 'N/A')],
            ['Agent Count:', scan_data.get('agent_count', 'N/A')]
        ]
        
        config_table = Table(config_data, colWidths=[2*inch, 4*inch])
        config_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(config_table)
        story.append(Spacer(1, 20))
        
        # Tools and techniques used
        story.append(Paragraph("<b>Tools and Techniques Used:</b>", self.styles['Normal']))
        story.append(Spacer(1, 8))
        
        tools_text = """
        • Orange Sage AI Pentesting Agent<br/>
        • Custom Python Security Scripts<br/>
        • HTTP Request/Response Analysis<br/>
        • SQL Injection Payload Testing<br/>
        • Cross-Site Scripting (XSS) Testing<br/>
        • Command Injection Testing<br/>
        • Path Traversal Testing<br/>
        • SSL/TLS Configuration Analysis<br/>
        • Security Header Assessment<br/>
        • Session Management Testing<br/>
        """
        
        story.append(Paragraph(tools_text, self.styles['Normal']))
        
        return story
    
    def _create_appendix_section(
        self,
        scan_data: Dict[str, Any],
        findings: List[Dict[str, Any]]
    ) -> List:
        """Create appendix section"""
        story = []
        
        story.append(Paragraph("Appendix", self.styles['SectionHeader']))
        story.append(Spacer(1, 12))
        
        # Raw findings data
        story.append(Paragraph("<b>Raw Findings Data:</b>", self.styles['Normal']))
        story.append(Spacer(1, 8))
        
        # Create a table with all findings
        if findings:
            findings_data = [['Title', 'Severity', 'Type', 'Endpoint']]
            for finding in findings:
                findings_data.append([
                    finding.get('title', 'N/A')[:50] + '...' if len(finding.get('title', '')) > 50 else finding.get('title', 'N/A'),
                    finding.get('severity', 'N/A'),
                    finding.get('type', 'N/A'),
                    finding.get('endpoint', 'N/A')[:30] + '...' if len(finding.get('endpoint', '')) > 30 else finding.get('endpoint', 'N/A')
                ])
            
            findings_table = Table(findings_data, colWidths=[2*inch, 1*inch, 1.5*inch, 2*inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(findings_table)
        
        return story
    
    def _generate_recommendations(self, findings: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        # Analyze findings and generate specific recommendations
        critical_findings = [f for f in findings if f.get('severity') == 'critical']
        if critical_findings:
            recommendations.append("Immediately address all critical severity findings as they pose the highest risk to the organization.")
        
        sql_injection = [f for f in findings if f.get('type') == 'sql_injection']
        if sql_injection:
            recommendations.append("Implement parameterized queries and prepared statements to prevent SQL injection attacks.")
        
        xss_findings = [f for f in findings if f.get('type') == 'xss']
        if xss_findings:
            recommendations.append("Implement proper input validation and output encoding to prevent Cross-Site Scripting (XSS) attacks.")
        
        command_injection = [f for f in findings if f.get('type') == 'command_injection']
        if command_injection:
            recommendations.append("Avoid executing user input as system commands and implement proper input sanitization.")
        
        path_traversal = [f for f in findings if f.get('type') == 'path_traversal']
        if path_traversal:
            recommendations.append("Implement proper file path validation and access controls to prevent directory traversal attacks.")
        
        missing_headers = [f for f in findings if 'security headers' in f.get('title', '').lower()]
        if missing_headers:
            recommendations.append("Implement comprehensive security headers including Content-Security-Policy, X-Frame-Options, and others.")
        
        ssl_issues = [f for f in findings if f.get('type') == 'ssl_tls']
        if ssl_issues:
            recommendations.append("Review and strengthen SSL/TLS configuration, including cipher suites and certificate management.")
        
        session_issues = [f for f in findings if f.get('type') == 'session_management']
        if session_issues:
            recommendations.append("Implement secure session management practices including secure cookies and session timeout.")
        
        # General recommendations
        recommendations.extend([
            "Conduct regular security assessments and penetration testing.",
            "Implement a Web Application Firewall (WAF) to provide additional protection.",
            "Establish a security awareness training program for development teams.",
            "Implement a secure development lifecycle (SDL) process.",
            "Regularly update and patch all software components.",
            "Implement comprehensive logging and monitoring for security events."
        ])
        
        return recommendations
    
    async def generate_html_report(
        self,
        scan_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        target_info: Dict[str, Any],
        branding: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate HTML report"""
        try:
            # HTML template
            html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Orange Sage Security Assessment Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    .header { text-align: center; color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 20px; }
                    .section { margin: 30px 0; }
                    .finding { border: 1px solid #ddd; margin: 15px 0; padding: 15px; border-radius: 5px; }
                    .critical { border-left: 5px solid #D32F2F; background-color: #FFEBEE; }
                    .high { border-left: 5px solid #F57C00; background-color: #FFF3E0; }
                    .medium { border-left: 5px solid #FBC02D; background-color: #FFFDE7; }
                    .low { border-left: 5px solid #388E3C; background-color: #E8F5E8; }
                    .stats { display: flex; justify-content: space-around; margin: 20px 0; }
                    .stat-box { text-align: center; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
                    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Orange Sage Security Assessment Report</h1>
                    <h2>{{ target_info.url or target_info.hostname }}</h2>
                    <p>Generated on: {{ scan_data.created_at or 'N/A' }}</p>
                </div>
                
                <div class="section">
                    <h2>Executive Summary</h2>
                    <div class="stats">
                        <div class="stat-box">
                            <h3>{{ findings|length }}</h3>
                            <p>Total Findings</p>
                        </div>
                        <div class="stat-box">
                            <h3>{{ findings|selectattr('severity', 'equalto', 'critical')|list|length }}</h3>
                            <p>Critical</p>
                        </div>
                        <div class="stat-box">
                            <h3>{{ findings|selectattr('severity', 'equalto', 'high')|list|length }}</h3>
                            <p>High</p>
                        </div>
                        <div class="stat-box">
                            <h3>{{ findings|selectattr('severity', 'equalto', 'medium')|list|length }}</h3>
                            <p>Medium</p>
                        </div>
                        <div class="stat-box">
                            <h3>{{ findings|selectattr('severity', 'equalto', 'low')|list|length }}</h3>
                            <p>Low</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Detailed Findings</h2>
                    {% for finding in findings %}
                    <div class="finding {{ finding.severity }}">
                        <h3>{{ finding.title }}</h3>
                        <p><strong>Severity:</strong> {{ finding.severity|upper }}</p>
                        <p><strong>Type:</strong> {{ finding.type }}</p>
                        <p><strong>Endpoint:</strong> {{ finding.endpoint }}</p>
                        <p><strong>Description:</strong> {{ finding.description }}</p>
                        {% if finding.remediation %}
                        <p><strong>Remediation:</strong> {{ finding.remediation }}</p>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                
                <div class="section">
                    <h2>Recommendations</h2>
                    <ul>
                        {% for rec in recommendations %}
                        <li>{{ rec }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </body>
            </html>
            """
            
            # Generate recommendations
            recommendations = self._generate_recommendations(findings)
            
            # Render template
            template = Template(html_template)
            html_content = template.render(
                scan_data=scan_data,
                findings=findings,
                target_info=target_info,
                recommendations=recommendations
            )
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            raise
