"""
Finding model for Orange Sage
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class SeverityLevel(str, enum.Enum):
    """Severity level enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, enum.Enum):
    """Finding status enumeration"""
    OPEN = "open"
    TRIAGED = "triaged"
    FALSE_POSITIVE = "false_positive"
    RESOLVED = "resolved"


class Finding(Base):
    """Finding model for security vulnerabilities"""
    __tablename__ = "findings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(SeverityLevel), nullable=False)
    status = Column(Enum(FindingStatus), default=FindingStatus.OPEN)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    
    # Technical details
    vulnerability_type = Column(String(100), nullable=True)  # SQLi, XSS, etc.
    endpoint = Column(String(500), nullable=True)
    parameter = Column(String(255), nullable=True)
    method = Column(String(10), nullable=True)  # GET, POST, etc.
    
    # Evidence
    request_sample = Column(Text, nullable=True)
    response_sample = Column(Text, nullable=True)
    poc_artifact_key = Column(String(500), nullable=True)  # S3 key for PoC
    
    # Remediation
    remediation_text = Column(Text, nullable=True)
    references = Column(JSON, nullable=True)  # CWE, OWASP links
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by_agent = Column(String(100), nullable=True)
    
    # Relationships
    scan = relationship("Scan", back_populates="findings")
    comments = relationship("FindingComment", back_populates="finding")
    
    def __repr__(self):
        return f"<Finding(id={self.id}, title={self.title}, severity={self.severity})>"
