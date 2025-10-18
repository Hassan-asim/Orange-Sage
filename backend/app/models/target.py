"""
Target model for Orange Sage
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class Target(Base):
    """Target model for security assessment"""
    __tablename__ = "targets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # url, repository, upload
    value = Column(Text, nullable=False)  # URL, repo path, or file path
    description = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    config = Column(JSON, nullable=True)  # Additional configuration
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="targets")
    scans = relationship("Scan", back_populates="target")
    
    def __repr__(self):
        return f"<Target(id={self.id}, name={self.name}, type={self.type})>"
