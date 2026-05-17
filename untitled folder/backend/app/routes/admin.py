"""
Admin dashboard and analytics routes
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.database_service import DatabaseService
from app.models.schemas import DashboardMetrics, ActivityLog

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get dashboard metrics"""
    try:
        metrics = DatabaseService.get_dashboard_metrics(db)
        
        return {
            "metrics": metrics,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Failed to get dashboard: {str(e)}")
        return {"error": str(e)}


@router.get("/recent-activity")
async def get_recent_activity(limit: int = 20, db: Session = Depends(get_db)):
    """Get recent activity feed"""
    try:
        leads = DatabaseService.get_recent_leads(db, limit)
        
        activities = []
        for lead in leads:
            activities.append({
                "lead_id": lead.id,
                "name": lead.name,
                "company": lead.company,
                "status": lead.status,
                "created_at": lead.created_at.isoformat()
            })
        
        return {"activities": activities}
    
    except Exception as e:
        logger.error(f"Failed to get activity: {str(e)}")
        return {"error": str(e)}


@router.get("/leads-summary")
async def get_leads_summary(db: Session = Depends(get_db)):
    """Get summary statistics"""
    try:
        from sqlalchemy import func
        from app.models.database import Lead
        
        total = db.query(Lead).count()
        processing = db.query(Lead).filter(Lead.status == "processing").count()
        completed = db.query(Lead).filter(Lead.status == "completed").count()
        failed = db.query(Lead).filter(Lead.status == "failed").count()
        
        return {
            "total": total,
            "processing": processing,
            "completed": completed,
            "failed": failed,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }
    
    except Exception as e:
        logger.error(f"Failed to get summary: {str(e)}")
        return {"error": str(e)}
