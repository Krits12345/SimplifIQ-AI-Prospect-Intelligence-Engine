"""
LangGraph Agent States
Defines state structures for the multi-agent workflow
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WorkflowState:
    """
    Central state object for the entire workflow
    Shared across all agents
    """
    # Lead information
    lead_id: int
    lead_name: str
    lead_email: str
    company_name: str
    website_url: str
    industry: Optional[str] = None
    
    # Research results
    company_description: str = ""
    about_page_content: str = ""
    website_content: str = ""
    meta_tags: Dict[str, str] = field(default_factory=dict)
    tech_stack: List[str] = field(default_factory=list)
    recent_news: List[Dict] = field(default_factory=list)
    
    # Analysis results
    strengths: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    # Competitor analysis
    competitors: List[str] = field(default_factory=list)
    competitor_data: Dict[str, Any] = field(default_factory=dict)
    
    # Website audit
    website_score: float = 0.0
    website_findings: List[Dict] = field(default_factory=list)
    
    # Confidence
    confidence_score: float = 0.0
    data_sources: List[str] = field(default_factory=list)
    
    # Report generation
    report_html: str = ""
    pdf_path: str = ""
    
    # Email
    email_content: str = ""
    
    # Workflow tracking
    steps_completed: List[str] = field(default_factory=list)
    errors: List[Dict] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_step(self, step: str):
        """Add completed step to tracking"""
        self.steps_completed.append(step)
    
    def add_error(self, step: str, error_msg: str):
        """Log an error"""
        self.errors.append({
            "step": step,
            "error": error_msg,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for database storage"""
        return {
            "lead_id": self.lead_id,
            "company_name": self.company_name,
            "industry": self.industry,
            "company_description": self.company_description,
            "tech_stack": self.tech_stack,
            "competitors": self.competitors,
            "competitor_data": self.competitor_data,
            "website_score": self.website_score,
            "confidence_score": self.confidence_score,
            "strengths": self.strengths,
            "opportunities": self.opportunities,
            "pain_points": self.pain_points,
            "recommendations": self.recommendations,
            "data_sources": self.data_sources,
        }
