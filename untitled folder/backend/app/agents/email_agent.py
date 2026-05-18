"""
Email Agent — drafts a personalized outreach email referencing the report.

If the LLM is unavailable we fall back to a clearly-templated body that
references real data from the workflow state (company, strengths, scores).
We never invent specifics that weren't observed.
"""

import logging

from app.agents.state import WorkflowState
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = "You are an expert business development writer."

PROMPT_TEMPLATE = """\
Write a professional, personalized outreach email.

Recipient name: {lead_name}
Company: {company_name}
Industry: {industry}

Real findings from our research (use these — do not invent any others):
- Strengths: {strengths}
- Opportunities: {opportunities}
- Website Health Score: {website_score:.0f}/100
- Confidence Score: {confidence_score:.0f}%

Requirements:
1. Open with a specific insight grounded in the findings above.
2. Reference real strengths the analysis surfaced.
3. Highlight one or two opportunities.
4. Close with a call-to-action for a 20-minute consultation.
5. Professional but personable, 3–4 short paragraphs.

Format exactly:
Subject: <subject line>

<email body>

Best regards,
SimplifIQ AI Prospect Intelligence Team
"""


class EmailAgent:
    def __init__(self):
        self.llm = LLMService()

    async def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Email Agent started for: {state.lead_email}")
        try:
            content = self._llm_email(state) or self._fallback_email(state)
            state.email_content = content
            state.add_step("email_generated")
        except Exception as e:
            logger.error(f"Email Agent error: {e}", exc_info=True)
            state.add_error("email", str(e))
            state.email_content = self._fallback_email(state)
        return state

    def _llm_email(self, state: WorkflowState) -> str:
        if not self.llm.enabled:
            return ""
        prompt = PROMPT_TEMPLATE.format(
            lead_name=state.lead_name,
            company_name=state.company_name,
            industry=state.industry or "Tech",
            strengths=", ".join(state.strengths[:2]) or "(none surfaced)",
            opportunities=", ".join(state.opportunities[:2]) or "(none surfaced)",
            website_score=state.website_score or 0.0,
            confidence_score=state.confidence_score or 0.0,
        )
        return self.llm.chat(
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=600,
        ) or ""

    @staticmethod
    def _fallback_email(state: WorkflowState) -> str:
        strengths_line = (
            f"We highlighted strengths including {', '.join(state.strengths[:2])}."
            if state.strengths
            else ""
        )
        opps_line = (
            f"We also flagged opportunities such as {', '.join(state.opportunities[:2])}."
            if state.opportunities
            else ""
        )
        return (
            f"Subject: Your {state.company_name} Intelligence Report\n\n"
            f"Hi {state.lead_name},\n\n"
            f"We've finished a research pass on {state.company_name} and put the findings into the attached PDF. "
            f"{strengths_line} {opps_line}\n\n"
            "Happy to walk you through the recommendations on a short call.\n\n"
            "Best regards,\n"
            "SimplifIQ AI Prospect Intelligence Team\n"
        )
