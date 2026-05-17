"""
SQLAlchemy database models
Defines all database tables and relationships
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Lead(Base):
    """Lead table - stores submitted lead information"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    company = Column(String(255), nullable=False)
    website = Column(String(500), nullable=False)
    industry = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(50), default="processing")  # processing, completed, failed
    
    # Relationships
    company_data = relationship("CompanyData", back_populates="lead", uselist=False)
    report = relationship("Report", back_populates="lead", uselist=False)
    logs = relationship("LogEntry", back_populates="lead")


class CompanyData(Base):
    """Company research data table - stores enriched company information"""
    __tablename__ = "company_data"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), unique=True, nullable=False)
    company = Column(String(255), nullable=False)
    industry = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    website_content = Column(Text, nullable=True)
    about_page = Column(Text, nullable=True)
    tech_stack = Column(JSON, default=[])  # List of technologies
    competitors = Column(JSON, default=[])  # List of competitor names
    competitor_data = Column(JSON, default={})  # Detailed competitor analysis
    recent_news = Column(JSON, default=[])  # Recent news about company
    website_score = Column(Float, nullable=True)  # 0-100
    confidence_score = Column(Float, nullable=True)  # 0-100
    strengths = Column(JSON, default=[])  # List of strengths
    opportunities = Column(JSON, default=[])  # List of opportunities
    pain_points = Column(JSON, default=[])  # List of pain points
    ai_recommendations = Column(JSON, default=[])  # AI generated recommendations
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="company_data")


class Report(Base):
    """Report table - stores generated PDF reports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), unique=True, nullable=False)
    pdf_path = Column(String(500), nullable=True)  # Local or S3 path
    google_drive_url = Column(String(500), nullable=True)  # Google Drive URL
    status = Column(String(50), default="pending")  # pending, generated, emailed, failed
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="report")


class LogEntry(Base):
    """Audit log table - tracks all workflow events"""
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    event = Column(String(255), nullable=False)  # validation_complete, research_started, etc
    status = Column(String(50))  # success, failure, info
    message = Column(Text, nullable=True)  # Detailed message
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    lead = relationship("Lead", back_populates="logs")
