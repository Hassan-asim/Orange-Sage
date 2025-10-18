"""
Agent Manager Service for Orange Sage
Handles AI agent orchestration and execution
"""

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.scan import Scan, ScanStatus
from app.models.agent import Agent, AgentStatus
from app.models.finding import Finding, SeverityLevel
from app.services.llm_service import LLMService
from app.services.sandbox_service import SandboxService
from app.utils.agent_factory import AgentFactory

logger = logging.getLogger(__name__)


class AgentManager:
    """Manages AI agents for security assessments"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.sandbox_service = SandboxService()
        self.agent_factory = AgentFactory()
        self.active_agents: Dict[str, Any] = {}
        self.active_scans: Dict[str, Any] = {}
    
    async def start_scan(self, db: Session, scan_id: int, scan_config: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new security scan with AI agents"""
        try:
            # Get scan from database
            scan = db.query(Scan).filter(Scan.id == scan_id).first()
            if not scan:
                raise ValueError(f"Scan {scan_id} not found")
            
            # Update scan status
            scan.status = ScanStatus.RUNNING
            scan.started_at = datetime.utcnow()
            db.commit()
            
            # Store scan info
            self.active_scans[str(scan_id)] = {
                "scan_id": scan_id,
                "scan": scan,
                "agents": {},
                "findings": [],
                "status": "running"
            }
            
            # Create root agent
            root_agent = await self._create_root_agent(scan, scan_config)
            
            # Start agent execution
            asyncio.create_task(self._execute_agent(root_agent, db))
            
            logger.info(f"Started scan {scan_id} with root agent {root_agent.agent_id}")
            
            return {
                "scan_id": scan_id,
                "status": "started",
                "root_agent_id": root_agent.agent_id,
                "message": "Scan started successfully"
            }
            
        except Exception as e:
            logger.error(f"Error starting scan {scan_id}: {e}")
            # Update scan status to failed
            if scan:
                scan.status = ScanStatus.FAILED
                scan.error_message = str(e)
                db.commit()
            raise
    
    async def _create_root_agent(self, scan: Scan, scan_config: Dict[str, Any]) -> Agent:
        """Create root agent for scan"""
        agent_id = str(uuid.uuid4())
        
        # Create agent record
        agent = Agent(
            agent_id=agent_id,
            name="Orange Sage Root Agent",
            task=f"Perform comprehensive security assessment of {scan.target.value}",
            status=AgentStatus.PENDING,
            scan_id=scan.id,
            agent_type="OrangeSageAgent",
            prompt_modules=["root_agent"],
            llm_config={
                "model_name": settings.DEFAULT_LLM_MODEL,
                "temperature": 0.7,
                "max_tokens": 4000
            }
        )
        
        return agent
    
    async def _execute_agent(self, agent: Agent, db: Session):
        """Execute an agent"""
        try:
            # Update agent status
            agent.status = AgentStatus.RUNNING
            agent.started_at = datetime.utcnow()
            db.commit()
            
            # Create sandbox for agent
            sandbox_info = await self.sandbox_service.create_sandbox(agent.agent_id)
            agent.sandbox_id = sandbox_info["workspace_id"]
            db.commit()
            
            # Initialize agent instance
            agent_instance = self.agent_factory.create_agent(
                agent_type=agent.agent_type,
                config={
                    "agent_id": agent.agent_id,
                    "task": agent.task,
                    "sandbox_info": sandbox_info,
                    "llm_config": agent.llm_config
                }
            )
            
            # Store active agent
            self.active_agents[agent.agent_id] = {
                "agent": agent,
                "instance": agent_instance,
                "db": db
            }
            
            # Execute agent
            result = await agent_instance.execute()
            
            # Process results
            await self._process_agent_results(agent, result, db)
            
            # Update agent status
            agent.status = AgentStatus.COMPLETED
            agent.finished_at = datetime.utcnow()
            agent.final_result = result
            db.commit()
            
            logger.info(f"Agent {agent.agent_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Error executing agent {agent.agent_id}: {e}")
            agent.status = AgentStatus.FAILED
            agent.error_message = str(e)
            agent.finished_at = datetime.utcnow()
            db.commit()
            
        finally:
            # Cleanup
            if agent.agent_id in self.active_agents:
                del self.active_agents[agent.agent_id]
            
            # Cleanup sandbox
            if agent.sandbox_id:
                await self.sandbox_service.destroy_sandbox(agent.sandbox_id)
    
    async def _process_agent_results(self, agent: Agent, result: Dict[str, Any], db: Session):
        """Process agent execution results"""
        try:
            # Extract findings from result
            findings = result.get("findings", [])
            
            for finding_data in findings:
                finding = Finding(
                    title=finding_data.get("title", "Security Finding"),
                    description=finding_data.get("description", ""),
                    severity=SeverityLevel(finding_data.get("severity", "medium")),
                    scan_id=agent.scan_id,
                    vulnerability_type=finding_data.get("type", ""),
                    endpoint=finding_data.get("endpoint", ""),
                    parameter=finding_data.get("parameter", ""),
                    method=finding_data.get("method", ""),
                    request_sample=finding_data.get("request_sample", ""),
                    response_sample=finding_data.get("response_sample", ""),
                    poc_artifact_key=finding_data.get("poc_artifact_key", ""),
                    remediation_text=finding_data.get("remediation", ""),
                    references=finding_data.get("references", {}),
                    created_by_agent=agent.agent_id
                )
                
                db.add(finding)
            
            db.commit()
            
            # Update scan summary
            scan = db.query(Scan).filter(Scan.id == agent.scan_id).first()
            if scan:
                scan.summary = {
                    "total_findings": len(findings),
                    "critical_count": len([f for f in findings if f.get("severity") == "critical"]),
                    "high_count": len([f for f in findings if f.get("severity") == "high"]),
                    "medium_count": len([f for f in findings if f.get("severity") == "medium"]),
                    "low_count": len([f for f in findings if f.get("severity") == "low"]),
                    "agents_completed": 1
                }
                db.commit()
            
        except Exception as e:
            logger.error(f"Error processing agent results: {e}")
    
    async def get_scan_status(self, scan_id: int, db: Session) -> Dict[str, Any]:
        """Get scan status and progress"""
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return {"error": "Scan not found"}
        
        # Get agents for this scan
        agents = db.query(Agent).filter(Agent.scan_id == scan_id).all()
        
        # Get findings count
        findings_count = db.query(Finding).filter(Finding.scan_id == scan_id).count()
        
        return {
            "scan_id": scan_id,
            "status": scan.status.value,
            "name": scan.name,
            "target": scan.target.value if scan.target else None,
            "agents_count": len(agents),
            "findings_count": findings_count,
            "started_at": scan.started_at.isoformat() if scan.started_at else None,
            "finished_at": scan.finished_at.isoformat() if scan.finished_at else None,
            "summary": scan.summary,
            "error": scan.error_message
        }
    
    async def get_scan_agents(self, scan_id: int, db: Session) -> List[Dict[str, Any]]:
        """Get agents for a scan"""
        agents = db.query(Agent).filter(Agent.scan_id == scan_id).all()
        
        return [
            {
                "id": agent.agent_id,
                "name": agent.name,
                "status": agent.status.value,
                "task": agent.task,
                "iteration": agent.iteration,
                "max_iterations": agent.max_iterations,
                "started_at": agent.started_at.isoformat() if agent.started_at else None,
                "finished_at": agent.finished_at.isoformat() if agent.finished_at else None,
                "error": agent.error_message
            }
            for agent in agents
        ]
    
    async def cancel_scan(self, scan_id: int, db: Session) -> Dict[str, Any]:
        """Cancel a running scan"""
        try:
            # Update scan status
            scan = db.query(Scan).filter(Scan.id == scan_id).first()
            if not scan:
                return {"error": "Scan not found"}
            
            scan.status = ScanStatus.CANCELLED
            scan.finished_at = datetime.utcnow()
            db.commit()
            
            # Cancel active agents
            agents = db.query(Agent).filter(
                Agent.scan_id == scan_id,
                Agent.status == AgentStatus.RUNNING
            ).all()
            
            for agent in agents:
                agent.status = AgentStatus.CANCELLED
                agent.finished_at = datetime.utcnow()
                
                # Cancel active agent instance
                if agent.agent_id in self.active_agents:
                    try:
                        await self.active_agents[agent.agent_id]["instance"].cancel()
                    except Exception as e:
                        logger.error(f"Error cancelling agent {agent.agent_id}: {e}")
            
            db.commit()
            
            return {
                "scan_id": scan_id,
                "status": "cancelled",
                "message": "Scan cancelled successfully"
            }
            
        except Exception as e:
            logger.error(f"Error cancelling scan {scan_id}: {e}")
            return {"error": str(e)}
    
    async def cleanup(self):
        """Cleanup resources"""
        try:
            # Cancel all active agents
            for agent_id, agent_info in self.active_agents.items():
                try:
                    await agent_info["instance"].cancel()
                except Exception as e:
                    logger.error(f"Error cancelling agent {agent_id}: {e}")
            
            # Cleanup sandboxes
            await self.sandbox_service.cleanup_all()
            
            logger.info("Agent manager cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
