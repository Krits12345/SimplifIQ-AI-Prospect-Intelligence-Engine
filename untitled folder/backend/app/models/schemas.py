"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime


# Lead Schemas
class LeadCreate(BaseModel):
    """Schema for creating a new lead"""
    name: str
    email: EmailStr
    company: str
    website: str
    industry: Optional[str] = None


class LeadResponse(BaseModel):
    """Schema for lead response"""
    id: int
    name: str
    email: str
    company: str
    website: str
    industry: Optional[str]
    created_at: datetime
    status: str = "processing"

    class Config:
        from_attributes = True


# Company Data Schemas
class CompanyDataResponse(BaseModel):
    """Schema for company research data"""
    company: str
    industry: Optional[str]
    description: Optional[str]
    tech_stack: Optional[list] = []
    competitors: Optional[list] = []
    website_score: Optional[int]
    confidence_score: Optional[float]
    strengths: Optional[list] = []
    opportunities: Optional[list] = []
    pain_points: Optional[list] = []
    
    class Config:
        from_attributes = True


# Report Schemas
class ReportResponse(BaseModel):
    """Schema for report response"""
    id: int
    lead_id: int
    pdf_path: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardMetrics(BaseModel):
    """Schema for dashboard metrics"""
    total_leads: int
    reports_generated: int
    emails_sent: int
    failures: int
    average_completion_time: float


class ActivityLog(BaseModel):
    """Schema for activity log"""
    event: str
    timestamp: datetime
    status: str
    lead_name: Optional[str]


class WorkflowStatus(BaseModel):
    """Real-time workflow status"""
    lead_id: int
    steps_completed: list
    current_step: str
    progress_percentage: int
    estimated_time_remaining: int
