"""
Agent model for Orange Sage
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class AgentStatus(str, enum.Enum):
    """Agent status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Agent(Base):
    """Agent model for AI agents"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), unique=True, nullable=False)  # UUID
    name = Column(String(255), nullable=False)
    task = Column(Text, nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.PENDING)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    parent_agent_id = Column(String(100), nullable=True)
    
    # Agent configuration
    agent_type = Column(String(100), nullable=False)  # OrangeSageAgent, etc.
    prompt_modules = Column(JSON, nullable=True)
    llm_config = Column(JSON, nullable=True)
    
    # Execution details
    iteration = Column(Integer, default=0)
    max_iterations = Column(Integer, default=200)
    sandbox_id = Column(String(100), nullable=True)
    
    # Timing
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Results
    final_result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    execution_summary = Column(JSON, nullable=True)
    
    # Relationships
    scan = relationship("Scan", back_populates="agents")
    
    def __repr__(self):
        return f"<Agent(id={self.id}, agent_id={self.agent_id}, name={self.name})>"
