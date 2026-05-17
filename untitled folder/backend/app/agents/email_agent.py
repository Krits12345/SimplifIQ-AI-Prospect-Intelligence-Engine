"""
Email Agent - Generates personalized outreach emails
Responsible for:
- Creating personalized email content
- Crafting compelling subject lines
"""

import logging
from app.agents.state import WorkflowState
import openai
from app.config import settings
import re

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key


class EmailAgent:
    """Generates personalized outreach emails"""
    
    def __init__(self):
        self.model_name = "gpt-3.5-turbo"
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Generate personalized email
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with email content
        """
        logger.info(f"Email Agent started for: {state.lead_email}")
        
        try:
            # Generate email content
            email_content = await self._generate_email(state)
            state.email_content = email_content
            
            state.add_step("email_generated")
            logger.info("Email Agent completed successfully")
            
        except Exception as e:
            logger.error(f"Email Agent error: {str(e)}")
            state.add_error("email", str(e))
        
        return state
    
    async def _generate_email(self, state: WorkflowState) -> str:
        """Generate personalized email content"""
        try:
            prompt = f"""
Generate a professional, personalized business email for:

Name: {state.lead_name}
Company: {state.company_name}
Industry: {state.industry or 'Tech'}

Key Findings from our analysis:
- Strengths: {', '.join(state.strengths[:2])}
- Opportunities: {', '.join(state.opportunities[:2])}
- Website Health Score: {state.website_score:.0f}/100
- Confidence Score: {state.confidence_score:.0f}%

Create an email that:
1. Opens with a specific insight from the analysis
2. References their company's strengths
3. Highlights key opportunities
4. Includes a call-to-action for a consultation
5. Is professional but personable
6. Is 3-4 paragraphs max
7. Ends with a warm signature

Format:
Subject: [subject line]

[Email body]

Best regards,
SimplifIQ AI Prospect Intelligence Team
"""
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert business development writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=600
            )
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Failed to generate email: {str(e)}")
            # Return fallback email
            return f"""
Subject: Your {state.company_name} Company Intelligence Report

Hi {state.lead_name},

We recently completed a comprehensive AI-powered analysis of {state.company_name} and wanted to share our findings.

Our research identified several significant growth opportunities and strategic recommendations specific to your business. We've prepared a detailed report that includes competitive intelligence, website health analysis, and actionable recommendations.

We'd love to schedule a brief consultation to discuss how these insights can help accelerate your company's growth.

Best regards,
SimplifIQ AI Prospect Intelligence Team
"""
