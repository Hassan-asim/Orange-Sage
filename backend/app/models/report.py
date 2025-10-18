"""
Report model for Orange Sage
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class ReportFormat(str, enum.Enum):
    """Report format enumeration"""
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"


class ReportStatus(str, enum.Enum):
    """Report status enumeration"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(Base):
    """Report model for generated reports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    format = Column(Enum(ReportFormat), nullable=False)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    
    # Report configuration
    include_charts = Column(String(10), default="true")
    include_pocs = Column(String(10), default="true")
    branding = Column(String(100), nullable=True)
    custom_template = Column(String(255), nullable=True)
    
    # File storage
    storage_key = Column(String(500), nullable=True)  # S3 key
    file_size = Column(Integer, nullable=True)
    download_url = Column(String(1000), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Timing
    generated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Metadata
    generation_error = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    scan = relationship("Scan", back_populates="reports")
    
    def __repr__(self):
        return f"<Report(id={self.id}, name={self.name}, format={self.format})>"
