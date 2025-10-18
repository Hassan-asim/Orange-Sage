"""
Scan model for Orange Sage
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ScanStatus(str, enum.Enum):
    """Scan status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Scan(Base):
    """Scan model for security assessments"""
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("targets.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Scan configuration
    scan_config = Column(JSON, nullable=True)
    agent_config = Column(JSON, nullable=True)
    
    # Timing
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Results
    summary = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="scans")
    target = relationship("Target", back_populates="scans")
    created_by_user = relationship("User", back_populates="scans")
    findings = relationship("Finding", back_populates="scan")
    agents = relationship("Agent", back_populates="scan")
    reports = relationship("Report", back_populates="scan")
    
    def __repr__(self):
        return f"<Scan(id={self.id}, name={self.name}, status={self.status})>"
