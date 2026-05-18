"""
Lead submission and management routes
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.models.schemas import LeadCreate, LeadResponse
from app.database import get_db
from app.services.database_service import DatabaseService
from app.workflows.lead_workflow import LeadWorkflow
from app.agents.state import WorkflowState
from app.services.email_service import EmailService
from app.services.sheets_service import SheetsService
from app.utils.helpers import validate_email, validate_website

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/leads", tags=["leads"])

workflow = LeadWorkflow()
email_service = EmailService()
sheets_service = SheetsService()


@router.post("/submit", response_model=LeadResponse)
async def submit_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Submit a lead for analysis
    
    This endpoint:
    1. Validates input
    2. Creates lead record
    3. Sends welcome email
    4. Triggers background workflow
    """
    try:
        # Validation
        if not validate_email(lead_data.email):
            raise HTTPException(status_code=400, detail="Invalid email format")
        
        if not validate_website(lead_data.website):
            raise HTTPException(status_code=400, detail="Invalid website URL")
        
        if not lead_data.name or not lead_data.company:
            raise HTTPException(status_code=400, detail="Name and company are required")
        
        # Log validation step
        logger.info(f"Validating lead: {lead_data.email}")
        
        # Create lead in database
        lead = await DatabaseService.create_lead(db, lead_data)
        
        # Log
        await DatabaseService.log_event(
            db,
            lead.id,
            "lead_captured",
            "success",
            f"Lead created: {lead_data.email}"
        )
        
        # Send welcome email
        await email_service.send_welcome_email(lead_data.email, lead_data.name)

        # Bonus: append to Google Sheets leads tracker (no-op if not configured)
        try:
            sheets_service.append_lead(lead)
        except Exception as sheet_err:
            logger.error(f"Sheets append failed for lead {lead.id}: {sheet_err}")

        # Trigger background workflow
        if background_tasks:
            background_tasks.add_task(
                run_workflow_background,
                lead.id,
                lead_data
            )
        
        logger.info(f"Lead submitted successfully: {lead.id}")
        
        return LeadResponse(
            id=lead.id,
            name=lead.name,
            email=lead.email,
            company=lead.company,
            website=lead.website,
            industry=lead.industry,
            created_at=lead.created_at,
            status="processing"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to submit lead: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit lead")


@router.get("/status/{lead_id}")
async def get_lead_status(lead_id: int, db: Session = Depends(get_db)):
    """Get current status of lead processing"""
    try:
        lead = DatabaseService.get_lead(db, lead_id)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Get workflow status
        workflow_status = await workflow.get_workflow_status(lead_id)
        
        return {
            "lead_id": lead_id,
            "email": lead.email,
            "company": lead.company,
            "status": lead.status,
            "created_at": lead.created_at,
            "workflow": workflow_status
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get lead status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get status")


@router.get("/{lead_id}")
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get lead details"""
    try:
        lead = DatabaseService.get_lead(db, lead_id)
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        company_data = DatabaseService.get_company_data(db, lead_id)
        
        return {
            "lead": LeadResponse(
                id=lead.id,
                name=lead.name,
                email=lead.email,
                company=lead.company,
                website=lead.website,
                industry=lead.industry,
                created_at=lead.created_at,
                status=lead.status
            ),
            "company_data": company_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get lead: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get lead")


async def run_workflow_background(lead_id: int, lead_data: LeadCreate):
    """
    Run the complete workflow in background
    """
    try:
        logger.info(f"Starting background workflow for lead: {lead_id}")
        
        # Create initial state
        state = WorkflowState(
            lead_id=lead_id,
            lead_name=lead_data.name,
            lead_email=lead_data.email,
            company_name=lead_data.company,
            website_url=lead_data.website,
            industry=lead_data.industry
        )
        
        # Execute workflow
        final_state = await workflow.execute_workflow(state)
        
        logger.info(f"Workflow completed for lead: {lead_id}")
        
    except Exception as e:
        logger.error(f"Background workflow failed: {str(e)}")
