"""
Main workflow orchestrator using LangGraph
Coordinates all agents in the proper sequence
"""

import logging
import asyncio
from typing import Dict, Any
from app.agents.state import WorkflowState
from app.agents.research_agent import ResearchAgent
from app.agents.insight_agent import InsightAgent
from app.agents.competitor_agent import CompetitorAgent
from app.agents.audit_agent import AuditAgent
from app.agents.report_agent import ReportAgent
from app.agents.email_agent import EmailAgent
from app.services.pdf_service import PDFService
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class LeadWorkflow:
    """Main workflow orchestrator for lead processing"""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.insight_agent = InsightAgent()
        self.competitor_agent = CompetitorAgent()
        self.audit_agent = AuditAgent()
        self.report_agent = ReportAgent()
        self.email_agent = EmailAgent()
        self.pdf_service = PDFService()
        self.email_service = EmailService()
    
    async def execute_workflow(self, state: WorkflowState) -> WorkflowState:
        """
        Execute complete workflow for a lead
        
        Sequential execution of all agents
        
        Args:
            state: Initial workflow state
            
        Returns:
            Final state with all results
        """
        logger.info(f"Starting workflow for lead: {state.lead_id}")
        
        try:
            # Step 1: Research
            logger.info("Step 1: Research Agent")
            state = await self.research_agent.execute(state)
            
            # Step 2: Insights
            logger.info("Step 2: Insight Agent")
            state = await self.insight_agent.execute(state)
            
            # Step 3: Competitor Analysis
            logger.info("Step 3: Competitor Agent")
            state = await self.competitor_agent.execute(state)
            
            # Step 4: Website Audit
            logger.info("Step 4: Audit Agent")
            state = await self.audit_agent.execute(state)
            
            # Step 5: Report Generation
            logger.info("Step 5: Report Agent")
            state = await self.report_agent.execute(state)
            
            # Step 6: PDF Generation
            logger.info("Step 6: PDF Generation")
            try:
                pdf_path = self.pdf_service.generate_pdf(
                    state.report_html,
                    state.company_name,
                    state.lead_id
                )
                state.pdf_path = pdf_path
                state.add_step("pdf_generated")
            except Exception as e:
                logger.error(f"PDF generation failed: {str(e)}")
                state.add_error("pdf_generation", str(e))
            
            # Step 7: Email Generation
            logger.info("Step 7: Email Agent")
            state = await self.email_agent.execute(state)
            
            # Step 8: Send Email
            logger.info("Step 8: Sending Email")
            try:
                email_sent = await self.email_service.send_report_email(
                    to_email=state.lead_email,
                    to_name=state.lead_name,
                    company_name=state.company_name,
                    email_content=state.email_content,
                    pdf_path=state.pdf_path
                )
                
                if email_sent:
                    state.add_step("email_sent")
                else:
                    state.add_error("email_sending", "Failed to send email")
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                state.add_error("email_sending", str(e))
            
            state.add_step("workflow_completed")
            logger.info(f"Workflow completed successfully for lead: {state.lead_id}")
            
        except Exception as e:
            logger.error(f"Workflow failed: {str(e)}")
            state.add_error("workflow", str(e))
        
        return state
    
    async def get_workflow_status(self, lead_id: int) -> Dict[str, Any]:
        """
        Get current workflow status (placeholder for real implementation)
        """
        return {
            "lead_id": lead_id,
            "status": "processing",
            "current_step": "Researching company...",
            "progress_percentage": 45
        }
