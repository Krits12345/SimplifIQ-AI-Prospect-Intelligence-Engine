"""
Audit Agent - Performs website health audit
Responsible for:
- Analyzing website quality
- Generating audit score
- Finding SEO and performance issues
"""

import logging
from app.utils.audit import WebsiteAudit
from app.agents.state import WorkflowState
from app.utils.helpers import calculate_confidence_score

logger = logging.getLogger(__name__)


class AuditAgent:
    """Performs website health audit"""
    
    def __init__(self):
        self.audit = WebsiteAudit()
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Audit website health
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with audit results
        """
        logger.info(f"Audit Agent started for: {state.website_url}")
        
        try:
            # Perform audit
            audit_results = await self.audit.audit_website(
                state.website_url,
                state.website_content,
                state.meta_tags
            )
            
            state.website_score = audit_results.get("score", 0)
            state.website_findings = audit_results.get("findings", [])
            
            logger.info(f"Website audit score: {state.website_score}")
            
            # Calculate confidence score
            confidence = calculate_confidence_score(
                website_found=bool(state.website_content),
                news_found=len(state.recent_news),
                about_page_found=bool(state.about_page_content),
                company_info_available=bool(state.company_description),
                tech_stack_found=len(state.tech_stack)
            )
            state.confidence_score = confidence
            
            logger.info(f"Confidence score: {confidence}%")
            
            state.add_step("audit_complete")
            logger.info("Audit Agent completed successfully")
            
        except Exception as e:
            logger.error(f"Audit Agent error: {str(e)}")
            state.add_error("audit", str(e))
        
        return state
