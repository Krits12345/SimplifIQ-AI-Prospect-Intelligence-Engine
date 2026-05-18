"""
Report retrieval and download routes.

Returns only data the workflow actually computed. If the run is still in
progress (or the AI step failed and left fields empty), the endpoint emits
HTTP 202 / 404 / partial responses rather than fabricating placeholder
competitors or generic insights.
"""

import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.agents.email_agent import EmailAgent
from app.agents.state import WorkflowState
from app.database import get_db
from app.models.database import Report
from app.services.database_service import DatabaseService
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/reports", tags=["reports"])
email_service = EmailService()
email_agent = EmailAgent()


@router.get("/{lead_id}")
async def get_report(lead_id: int, response: Response, db: Session = Depends(get_db)):
    """
    Return the report payload assembled from real workflow output.

    202 if the workflow is still running or hasn't started enrichment yet.
    """
    lead = DatabaseService.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    company_data = DatabaseService.get_company_data(db, lead_id)
    if not company_data:
        response.status_code = status.HTTP_202_ACCEPTED
        return {
            "lead_id": lead_id,
            "status": "processing",
            "message": "Report is still being generated. Try again shortly.",
        }

    report = db.query(Report).filter(Report.lead_id == lead_id).first()
    generated_date = company_data.updated_at or lead.created_at

    # Compose only from fields the workflow actually populated. Empty lists
    # remain empty; the frontend renders them as "no data surfaced" rather
    # than receiving fabricated values.
    competitor_intelligence = {
        "competitors": company_data.competitors or [],
        "competitor_details": company_data.competitor_data or {},
        "positioning_notes": _positioning_notes(company_data.competitor_data or {}),
    }

    website_audit = {
        "website_score": company_data.website_score,
        "has_website_content": bool(company_data.website_content),
    }

    research_confidence = {
        "confidence_score": company_data.confidence_score,
        "sources": _data_sources(company_data),
        "limitations": _limitations(company_data),
    }

    return {
        "lead_id": lead_id,
        "company_name": company_data.company,
        "website": lead.website,
        "industry": company_data.industry,
        "generated_date": generated_date.isoformat(),
        "status": (report.status if report else "processing"),
        "executive_summary": company_data.description or None,
        "company_intelligence": {
            "overview": company_data.description or None,
            "industry": company_data.industry,
            "tech_stack": company_data.tech_stack or [],
            "strengths": company_data.strengths or [],
            "opportunities": company_data.opportunities or [],
            "pain_points": company_data.pain_points or [],
        },
        "website_audit": website_audit,
        "competitor_intelligence": competitor_intelligence,
        "research_confidence": research_confidence,
        "strategic_recommendations": company_data.ai_recommendations or [],
        "report_metadata": {
            "sources_analyzed": len(_data_sources(company_data)),
            "insights_generated": _count_insights(company_data),
            "confidence_score": company_data.confidence_score,
            "pdf_available": bool(report and report.pdf_path),
            "drive_url": report.google_drive_url if report else None,
            "email_sent": bool(report and report.email_sent),
        },
    }


@router.post("/{lead_id}/send")
async def send_report(lead_id: int, db: Session = Depends(get_db)):
    """
    Resend the personalized intelligence email.

    Regenerates the email body from the persisted research so the content
    matches the original (or improves on it if the LLM was unavailable the
    first time) — rather than sending a hardcoded generic note.
    """
    lead = DatabaseService.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    report = db.query(Report).filter(Report.lead_id == lead_id).first()
    if not report or not report.pdf_path:
        raise HTTPException(status_code=404, detail="Report PDF not found")

    state = _rebuild_state_for_email(db, lead, report)
    state = await email_agent.execute(state)

    email_sent = await email_service.send_report_email(
        to_email=lead.email,
        to_name=lead.name,
        company_name=lead.company,
        email_content=state.email_content,
        pdf_path=report.pdf_path,
    )

    if email_sent:
        report.email_sent = True
        report.status = "emailed"
        report.email_sent_at = datetime.utcnow()
        db.commit()
        return {"status": "sent", "message": f"Report email sent to {lead.email}"}

    # SendGrid disabled or send failed — surface honestly, do not pretend.
    return {
        "status": "queued",
        "message": (
            f"Email not delivered (SendGrid not configured or returned an error). "
            f"Report PDF is available for download for {lead.email}."
        ),
    }


@router.get("/{lead_id}/download")
async def download_report(lead_id: int, db: Session = Depends(get_db)):
    """Download the generated PDF."""
    report = db.query(Report).filter(Report.lead_id == lead_id).first()
    if not report or not report.pdf_path:
        raise HTTPException(status_code=404, detail="Report PDF not found")

    pdf_path = Path(report.pdf_path)
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"report_{lead_id}.pdf",
    )


# ---------- helpers ----------

def _positioning_notes(competitor_data: dict) -> list:
    """Surface positioning strings the LLM actually returned, in order."""
    notes = []
    for name, data in competitor_data.items():
        positioning = (data or {}).get("positioning")
        if positioning:
            notes.append(f"{name}: {positioning}")
    return notes


def _data_sources(company_data) -> list:
    sources = []
    if company_data.website_content:
        sources.append("Company website")
    if company_data.about_page:
        sources.append("About page")
    if company_data.competitors:
        sources.append("Competitor research")
    if company_data.recent_news:
        sources.append("Recent news & press")
    return sources


def _limitations(company_data) -> list:
    limitations = []
    if not company_data.website_content:
        limitations.append("Website content could not be retrieved.")
    if not company_data.competitors:
        limitations.append("No competitors were identified from public sources.")
    if not company_data.ai_recommendations:
        limitations.append("AI recommendations are unavailable (LLM not configured).")
    return limitations


def _count_insights(company_data) -> int:
    return sum(
        len(getattr(company_data, attr, []) or [])
        for attr in ("strengths", "opportunities", "pain_points", "ai_recommendations")
    )


def _rebuild_state_for_email(db, lead, report) -> WorkflowState:
    """Reconstruct enough WorkflowState for the EmailAgent."""
    company_data = DatabaseService.get_company_data(db, lead.id) or None
    state = WorkflowState(
        lead_id=lead.id,
        lead_name=lead.name,
        lead_email=lead.email,
        company_name=lead.company,
        website_url=lead.website,
        industry=(company_data.industry if company_data else lead.industry),
    )
    if company_data:
        state.company_description = company_data.description or ""
        state.tech_stack = company_data.tech_stack or []
        state.strengths = company_data.strengths or []
        state.opportunities = company_data.opportunities or []
        state.pain_points = company_data.pain_points or []
        state.recommendations = company_data.ai_recommendations or []
        state.competitors = company_data.competitors or []
        state.competitor_data = company_data.competitor_data or {}
        state.website_score = company_data.website_score or 0.0
        state.confidence_score = company_data.confidence_score or 0.0
    state.pdf_path = report.pdf_path
    return state
