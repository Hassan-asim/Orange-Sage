"""
Microservices Orchestrator for Orange Sage
Coordinates multiple security analysis microservices
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import aiohttp
import requests

logger = logging.getLogger(__name__)


class MicroservicesOrchestrator:
    """Orchestrates multiple security analysis microservices"""
    
    def __init__(self):
        self.services = {
            'vulnerability_scanner': {
                'url': 'http://localhost:8001',
                'description': 'Automated vulnerability scanning service',
                'capabilities': ['sql_injection', 'xss', 'csrf', 'path_traversal']
            },
            'network_analyzer': {
                'url': 'http://localhost:8002',
                'description': 'Network security analysis service',
                'capabilities': ['port_scanning', 'service_enumeration', 'ssl_analysis']
            },
            'code_analyzer': {
                'url': 'http://localhost:8003',
                'description': 'Static code analysis service',
                'capabilities': ['static_analysis', 'dependency_check', 'secrets_detection']
            },
            'compliance_checker': {
                'url': 'http://localhost:8004',
                'description': 'Compliance and standards checking service',
                'capabilities': ['owasp_top10', 'pci_dss', 'gdpr', 'iso27001']
            },
            'threat_intelligence': {
                'url': 'http://localhost:8005',
                'description': 'Threat intelligence and IOCs analysis',
                'capabilities': ['ioc_analysis', 'threat_hunting', 'malware_analysis']
            },
            'report_generator': {
                'url': 'http://localhost:8006',
                'description': 'Advanced report generation service',
                'capabilities': ['pdf_generation', 'html_reports', 'executive_summaries']
            }
        }
        self.active_tasks = {}
    
    async def start_comprehensive_analysis(
        self,
        target: str,
        analysis_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Start comprehensive security analysis using multiple microservices"""
        try:
            analysis_id = str(uuid.uuid4())
            logger.info(f"Starting comprehensive analysis {analysis_id} for target: {target}")
            
            # Initialize analysis session
            analysis_session = {
                'id': analysis_id,
                'target': target,
                'config': analysis_config,
                'started_at': datetime.now(),
                'services': {},
                'findings': [],
                'status': 'running'
            }
            
            # Start parallel analysis tasks
            tasks = []
            
            # Vulnerability scanning
            if analysis_config.get('enable_vulnerability_scanning', True):
                task = asyncio.create_task(
                    self._run_vulnerability_scanning(analysis_id, target, analysis_config)
                )
                tasks.append(task)
            
            # Network analysis
            if analysis_config.get('enable_network_analysis', True):
                task = asyncio.create_task(
                    self._run_network_analysis(analysis_id, target, analysis_config)
                )
                tasks.append(task)
            
            # Code analysis (if applicable)
            if analysis_config.get('enable_code_analysis', False):
                task = asyncio.create_task(
                    self._run_code_analysis(analysis_id, target, analysis_config)
                )
                tasks.append(task)
            
            # Compliance checking
            if analysis_config.get('enable_compliance_checking', True):
                task = asyncio.create_task(
                    self._run_compliance_checking(analysis_id, target, analysis_config)
                )
                tasks.append(task)
            
            # Threat intelligence
            if analysis_config.get('enable_threat_intelligence', True):
                task = asyncio.create_task(
                    self._run_threat_intelligence(analysis_id, target, analysis_config)
                )
                tasks.append(task)
            
            # Store active analysis
            self.active_tasks[analysis_id] = {
                'session': analysis_session,
                'tasks': tasks
            }
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            analysis_session['status'] = 'completed'
            analysis_session['completed_at'] = datetime.now()
            
            # Aggregate findings from all services
            all_findings = []
            for result in results:
                if isinstance(result, dict) and 'findings' in result:
                    all_findings.extend(result['findings'])
            
            analysis_session['findings'] = all_findings
            analysis_session['summary'] = self._generate_analysis_summary(all_findings)
            
            # Generate comprehensive report
            if analysis_config.get('generate_report', True):
                report_task = asyncio.create_task(
                    self._generate_comprehensive_report(analysis_id, analysis_session)
                )
                await report_task
            
            logger.info(f"Analysis {analysis_id} completed with {len(all_findings)} findings")
            
            return {
                'analysis_id': analysis_id,
                'status': 'completed',
                'findings': all_findings,
                'summary': analysis_session['summary'],
                'duration': (analysis_session['completed_at'] - analysis_session['started_at']).total_seconds()
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return {'error': str(e), 'status': 'failed'}
    
    async def _run_vulnerability_scanning(
        self,
        analysis_id: str,
        target: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run vulnerability scanning microservice"""
        try:
            service_url = self.services['vulnerability_scanner']['url']
            
            # Prepare scan request
            scan_request = {
                'analysis_id': analysis_id,
                'target': target,
                'scan_types': config.get('scan_types', ['web', 'api']),
                'depth': config.get('scan_depth', 'comprehensive'),
                'options': {
                    'enable_sql_injection': True,
                    'enable_xss': True,
                    'enable_csrf': True,
                    'enable_path_traversal': True,
                    'enable_command_injection': True,
                    'enable_authentication_bypass': True
                }
            }
            
            # Call vulnerability scanning service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{service_url}/scan",
                    json=scan_request,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Vulnerability scanning completed for {target}")
                        return result
                    else:
                        logger.error(f"Vulnerability scanning failed: {response.status}")
                        return {'error': f'Service returned status {response.status}'}
        
        except Exception as e:
            logger.error(f"Error in vulnerability scanning: {e}")
            return {'error': str(e)}
    
    async def _run_network_analysis(
        self,
        analysis_id: str,
        target: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run network analysis microservice"""
        try:
            service_url = self.services['network_analyzer']['url']
            
            # Prepare network analysis request
            network_request = {
                'analysis_id': analysis_id,
                'target': target,
                'analysis_types': config.get('network_analysis_types', ['port_scan', 'ssl_analysis', 'service_enumeration']),
                'options': {
                    'port_range': config.get('port_range', '1-65535'),
                    'scan_techniques': ['tcp_syn', 'tcp_connect', 'udp'],
                    'ssl_analysis': True,
                    'banner_grabbing': True
                }
            }
            
            # Call network analysis service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{service_url}/analyze",
                    json=network_request,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Network analysis completed for {target}")
                        return result
                    else:
                        logger.error(f"Network analysis failed: {response.status}")
                        return {'error': f'Service returned status {response.status}'}
        
        except Exception as e:
            logger.error(f"Error in network analysis: {e}")
            return {'error': str(e)}
    
    async def _run_code_analysis(
        self,
        analysis_id: str,
        target: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run code analysis microservice"""
        try:
            service_url = self.services['code_analyzer']['url']
            
            # Prepare code analysis request
            code_request = {
                'analysis_id': analysis_id,
                'target': target,
                'analysis_types': config.get('code_analysis_types', ['static_analysis', 'dependency_check']),
                'options': {
                    'languages': config.get('languages', ['python', 'javascript', 'java', 'php']),
                    'check_secrets': True,
                    'check_dependencies': True,
                    'check_hardcoded_credentials': True
                }
            }
            
            # Call code analysis service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{service_url}/analyze",
                    json=code_request,
                    timeout=aiohttp.ClientTimeout(total=900)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Code analysis completed for {target}")
                        return result
                    else:
                        logger.error(f"Code analysis failed: {response.status}")
                        return {'error': f'Service returned status {response.status}'}
        
        except Exception as e:
            logger.error(f"Error in code analysis: {e}")
            return {'error': str(e)}
    
    async def _run_compliance_checking(
        self,
        analysis_id: str,
        target: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run compliance checking microservice"""
        try:
            service_url = self.services['compliance_checker']['url']
            
            # Prepare compliance check request
            compliance_request = {
                'analysis_id': analysis_id,
                'target': target,
                'standards': config.get('compliance_standards', ['owasp_top10', 'pci_dss']),
                'options': {
                    'check_authentication': True,
                    'check_authorization': True,
                    'check_data_protection': True,
                    'check_encryption': True,
                    'check_logging': True
                }
            }
            
            # Call compliance checking service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{service_url}/check",
                    json=compliance_request,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Compliance checking completed for {target}")
                        return result
                    else:
                        logger.error(f"Compliance checking failed: {response.status}")
                        return {'error': f'Service returned status {response.status}'}
        
        except Exception as e:
            logger.error(f"Error in compliance checking: {e}")
            return {'error': str(e)}
    
    async def _run_threat_intelligence(
        self,
        analysis_id: str,
        target: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run threat intelligence microservice"""
        try:
            service_url = self.services['threat_intelligence']['url']
            
            # Prepare threat intelligence request
            ti_request = {
                'analysis_id': analysis_id,
                'target': target,
                'analysis_types': config.get('ti_analysis_types', ['ioc_analysis', 'threat_hunting']),
                'options': {
                    'check_known_malicious': True,
                    'check_suspicious_patterns': True,
                    'check_network_indicators': True,
                    'check_file_indicators': True
                }
            }
            
            # Call threat intelligence service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{service_url}/analyze",
                    json=ti_request,
                    timeout=aiohttp.ClientTimeout(total=600)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Threat intelligence analysis completed for {target}")
                        return result
                    else:
                        logger.error(f"Threat intelligence analysis failed: {response.status}")
                        return {'error': f'Service returned status {response.status}'}
        
        except Exception as e:
            logger.error(f"Error in threat intelligence analysis: {e}")
            return {'error': str(e)}
    
    async def _generate_comprehensive_report(
        self,
        analysis_id: str,
        analysis_session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive report using report generation microservice"""
        try:
            service_url = self.services['report_generator']['url']
            
            # Prepare report generation request
            report_request = {
                'analysis_id': analysis_id,
                'target': analysis_session['target'],
                'findings': analysis_session['findings'],
                'summary': analysis_session['summary'],
                'formats': ['pdf', 'html'],
                'options': {
                    'include_executive_summary': True,
                    'include_technical_details': True,
                    'include_recommendations': True,
                    'include_appendix': True,
                    'branding': {
                        'company_name': 'Orange Sage',
                        'logo_url': None,
                        'color_scheme': 'blue'
                    }
                }
            }
            
            # Call report generation service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{service_url}/generate",
                    json=report_request,
                    timeout=aiohttp.ClientTimeout(total=300)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Comprehensive report generated for analysis {analysis_id}")
                        return result
                    else:
                        logger.error(f"Report generation failed: {response.status}")
                        return {'error': f'Service returned status {response.status}'}
        
        except Exception as e:
            logger.error(f"Error in report generation: {e}")
            return {'error': str(e)}
    
    def _generate_analysis_summary(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate analysis summary from findings"""
        total_findings = len(findings)
        critical_count = len([f for f in findings if f.get('severity') == 'critical'])
        high_count = len([f for f in findings if f.get('severity') == 'high'])
        medium_count = len([f for f in findings if f.get('severity') == 'medium'])
        low_count = len([f for f in findings if f.get('severity') == 'low'])
        
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
        
        # Group findings by type
        findings_by_type = {}
        for finding in findings:
            finding_type = finding.get('type', 'unknown')
            if finding_type not in findings_by_type:
                findings_by_type[finding_type] = 0
            findings_by_type[finding_type] += 1
        
        return {
            'total_findings': total_findings,
            'critical_count': critical_count,
            'high_count': high_count,
            'medium_count': medium_count,
            'low_count': low_count,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'findings_by_type': findings_by_type,
            'top_vulnerabilities': self._get_top_vulnerabilities(findings)
        }
    
    def _get_top_vulnerabilities(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get top vulnerabilities by severity and impact"""
        # Sort findings by severity (critical first) and then by type
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_findings = sorted(
            findings,
            key=lambda x: (severity_order.get(x.get('severity', 'low'), 3), x.get('type', ''))
        )
        
        # Return top 10 most critical findings
        return sorted_findings[:10]
    
    async def get_analysis_status(self, analysis_id: str) -> Dict[str, Any]:
        """Get status of running analysis"""
        if analysis_id not in self.active_tasks:
            return {'error': 'Analysis not found'}
        
        task_info = self.active_tasks[analysis_id]
        session = task_info['session']
        
        # Check if tasks are still running
        running_tasks = [task for task in task_info['tasks'] if not task.done()]
        
        return {
            'analysis_id': analysis_id,
            'status': session['status'],
            'target': session['target'],
            'started_at': session['started_at'].isoformat(),
            'running_tasks': len(running_tasks),
            'total_tasks': len(task_info['tasks']),
            'findings_count': len(session.get('findings', [])),
            'summary': session.get('summary', {})
        }
    
    async def cancel_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Cancel running analysis"""
        if analysis_id not in self.active_tasks:
            return {'error': 'Analysis not found'}
        
        try:
            task_info = self.active_tasks[analysis_id]
            session = task_info['session']
            
            # Cancel all running tasks
            for task in task_info['tasks']:
                if not task.done():
                    task.cancel()
            
            # Update session status
            session['status'] = 'cancelled'
            session['cancelled_at'] = datetime.now()
            
            # Remove from active tasks
            del self.active_tasks[analysis_id]
            
            logger.info(f"Analysis {analysis_id} cancelled")
            
            return {
                'analysis_id': analysis_id,
                'status': 'cancelled',
                'message': 'Analysis cancelled successfully'
            }
            
        except Exception as e:
            logger.error(f"Error cancelling analysis {analysis_id}: {e}")
            return {'error': str(e)}
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get status of all microservices"""
        service_status = {}
        
        for service_name, service_info in self.services.items():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{service_info['url']}/health",
                        timeout=aiohttp.ClientTimeout(total=5)
                    ) as response:
                        if response.status == 200:
                            service_status[service_name] = {
                                'status': 'healthy',
                                'url': service_info['url'],
                                'description': service_info['description']
                            }
                        else:
                            service_status[service_name] = {
                                'status': 'unhealthy',
                                'url': service_info['url'],
                                'error': f'HTTP {response.status}'
                            }
            except Exception as e:
                service_status[service_name] = {
                    'status': 'unavailable',
                    'url': service_info['url'],
                    'error': str(e)
                }
        
        return service_status
    
    async def cleanup(self):
        """Cleanup resources and cancel all active tasks"""
        try:
            for analysis_id, task_info in self.active_tasks.items():
                # Cancel all tasks
                for task in task_info['tasks']:
                    if not task.done():
                        task.cancel()
                
                # Update session status
                task_info['session']['status'] = 'cancelled'
                task_info['session']['cancelled_at'] = datetime.now()
            
            # Clear active tasks
            self.active_tasks.clear()
            
            logger.info("Microservices orchestrator cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
