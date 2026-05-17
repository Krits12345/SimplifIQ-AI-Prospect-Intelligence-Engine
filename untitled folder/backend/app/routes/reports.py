"""
Report retrieval and download routes
"""

import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.database_service import DatabaseService
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/{lead_id}")
async def get_report(lead_id: int, db: Session = Depends(get_db)):
    """Get report for a lead"""
    try:
        lead = DatabaseService.get_lead(db, lead_id)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        company_data = DatabaseService.get_company_data(db, lead_id)
        
        if not company_data:
            raise HTTPException(status_code=404, detail="Report not available yet")
        
        return {
            "lead_id": lead_id,
            "company": company_data.company,
            "industry": company_data.industry,
            "description": company_data.description,
            "strengths": company_data.strengths,
            "opportunities": company_data.opportunities,
            "pain_points": company_data.pain_points,
            "recommendations": company_data.ai_recommendations,
            "competitors": company_data.competitors,
            "website_score": company_data.website_score,
            "confidence_score": company_data.confidence_score,
            "data_sources": company_data.updated_at
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get report")


@router.get("/{lead_id}/download")
async def download_report(lead_id: int, db: Session = Depends(get_db)):
    """Download PDF report"""
    try:
        from app.models.database import Report
        
        report = db.query(Report).filter(Report.lead_id == lead_id).first()
        
        if not report or not report.pdf_path:
            raise HTTPException(status_code=404, detail="Report PDF not found")
        
        pdf_path = Path(report.pdf_path)
        
        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Report file not found")
        
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"report_{lead_id}.pdf"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to download report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to download report")
