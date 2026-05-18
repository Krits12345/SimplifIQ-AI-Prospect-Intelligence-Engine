"""
Database service for storing leads, reports, and logs
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.database import Lead, CompanyData, Report, LogEntry
from app.models.schemas import LeadCreate
from app.agents.state import WorkflowState

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations"""
    
    @staticmethod
    async def create_lead(db: Session, lead_data: LeadCreate) -> Lead:
        """Create new lead"""
        try:
            lead = Lead(
                name=lead_data.name,
                email=lead_data.email,
                company=lead_data.company,
                website=lead_data.website,
                industry=lead_data.industry,
                status="processing"
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)
            
            logger.info(f"Lead created: {lead.id}")
            return lead
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create lead: {str(e)}")
            raise
    
    @staticmethod
    async def save_company_data(db: Session, state: WorkflowState) -> CompanyData:
        """Save enriched company data"""
        try:
            company_data = CompanyData(
                lead_id=state.lead_id,
                company=state.company_name,
                industry=state.industry,
                description=state.company_description,
                website_content=state.website_content,
                about_page=state.about_page_content,
                tech_stack=state.tech_stack,
                competitors=state.competitors,
                competitor_data=state.competitor_data,
                recent_news=state.recent_news,
                website_score=state.website_score,
                confidence_score=state.confidence_score,
                strengths=state.strengths,
                opportunities=state.opportunities,
                pain_points=state.pain_points,
                ai_recommendations=state.recommendations
            )
            db.add(company_data)
            db.commit()
            
            logger.info(f"Company data saved for lead: {state.lead_id}")
            return company_data
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save company data: {str(e)}")
            raise
    
    @staticmethod
    async def save_report(db: Session, lead_id: int, pdf_path: str) -> Report:
        """Save or update report record"""
        try:
            report = db.query(Report).filter(Report.lead_id == lead_id).first()
            if report:
                report.pdf_path = pdf_path
                report.status = "generated"
                report.updated_at = datetime.utcnow()
            else:
                report = Report(
                    lead_id=lead_id,
                    pdf_path=pdf_path,
                    status="generated"
                )
                db.add(report)

            db.commit()
            db.refresh(report)
            logger.info(f"Report saved for lead: {lead_id}")
            return report
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save report: {str(e)}")
            raise
    
    @staticmethod
    def update_report_fields(db: Session, lead_id: int, **fields) -> bool:
        """Patch a Report row with the given fields. Returns True on success."""
        try:
            report = db.query(Report).filter(Report.lead_id == lead_id).first()
            if not report:
                return False
            for key, value in fields.items():
                setattr(report, key, value)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to update report fields for lead {lead_id}: {e}")
            return False

    @staticmethod
    async def log_event(
        db: Session,
        lead_id: int,
        event: str,
        status: str,
        message: str = None
    ) -> LogEntry:
        """Log workflow event"""
        try:
            log = LogEntry(
                lead_id=lead_id,
                event=event,
                status=status,
                message=message
            )
            db.add(log)
            db.commit()
            
            return log
        
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to log event: {str(e)}")
            raise
    
    @staticmethod
    def get_lead(db: Session, lead_id: int) -> Lead:
        """Get lead by ID"""
        return db.query(Lead).filter(Lead.id == lead_id).first()
    
    @staticmethod
    def get_company_data(db: Session, lead_id: int) -> CompanyData:
        """Get company data by lead ID"""
        return db.query(CompanyData).filter(CompanyData.lead_id == lead_id).first()
    
    @staticmethod
    def get_recent_leads(db: Session, limit: int = 10) -> list:
        """Get recent leads"""
        return db.query(Lead).order_by(Lead.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_dashboard_metrics(db: Session) -> dict:
        """Get dashboard metrics"""
        total_leads = db.query(Lead).count()
        reports_generated = db.query(Report).filter(Report.status == "generated").count()
        emails_sent = db.query(Report).filter(Report.email_sent == True).count()
        failures = db.query(LogEntry).filter(LogEntry.status == "failure").count()
        
        return {
            "total_leads": total_leads,
            "reports_generated": reports_generated,
            "emails_sent": emails_sent,
            "failures": failures,
            "average_completion_time": 0.0  # Would calculate from logs
        }
