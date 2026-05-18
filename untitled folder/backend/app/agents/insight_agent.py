"""
Insight Agent — strengths, opportunities, pain points, recommendations.

Uses the shared LLMService. If OpenAI is unconfigured, the agent records
the limitation on state and leaves the fields empty — downstream consumers
must NOT substitute placeholders.
"""

import logging

from app.agents.state import WorkflowState
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = "You are a senior business analyst."

PROMPT_TEMPLATE = """\
Based on this company information:

{context}

Return JSON only (no markdown), matching this exact schema:
{{
    "strengths": ["..."],
    "opportunities": ["..."],
    "pain_points": ["..."],
    "recommendations": ["..."]
}}

Each list should have 3-4 items. Each item is 1-2 sentences, specific and actionable.
"""


class InsightAgent:
    def __init__(self):
        self.llm = LLMService()

    async def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Insight Agent started for: {state.company_name}")

        if not self.llm.enabled:
            state.add_error("insights", "LLM unavailable; insights not generated")
            return state

        try:
            result = self.llm.chat_json(
                SYSTEM_PROMPT,
                PROMPT_TEMPLATE.format(context=self._prepare_context(state)),
                temperature=0.2,
                max_tokens=800,
            )
            if not result:
                state.add_error("insights", "LLM returned no parsable JSON")
                return state

            state.strengths = result.get("strengths", []) or []
            state.opportunities = result.get("opportunities", []) or []
            state.pain_points = result.get("pain_points", []) or []
            state.recommendations = result.get("recommendations", []) or []
            state.add_step("insight_complete")
            logger.info("Insight Agent completed successfully")
        except Exception as e:
            logger.error(f"Insight Agent error: {e}", exc_info=True)
            state.add_error("insights", str(e))
        return state

    @staticmethod
    def _prepare_context(state: WorkflowState) -> str:
        return (
            f"Company Name: {state.company_name}\n"
            f"Industry: {state.industry or 'Unknown'}\n"
            f"Description: {(state.company_description or '')[:500]}\n"
            f"Website Content: {(state.website_content or 'Not available')[:500]}\n"
            f"About Page: {(state.about_page_content or 'Not available')[:500]}\n"
            f"Technologies: {', '.join(state.tech_stack)}\n"
            f"Recent News: {len(state.recent_news)} articles found"
        )
