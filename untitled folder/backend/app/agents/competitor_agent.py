"""
Competitor Agent — finds competitors via Tavily and analyzes top 3 with the LLM.

When OpenAI is unconfigured, competitor names from Tavily are still
populated but per-competitor analysis is skipped (the data is left empty
rather than fabricated).
"""

import logging

from app.agents.state import WorkflowState
from app.services.llm_service import LLMService
from app.utils.research import ResearchService

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = "You are an expert market analyst."

PROMPT_TEMPLATE = """\
Compare {company} with competitor {competitor} in the {industry} industry.

Return JSON only:
{{
    "positioning": "brief positioning",
    "strengths": ["..."],
    "weaknesses": ["..."],
    "market_focus": "target market description",
    "competitive_advantage": "key advantage"
}}
"""


class CompetitorAgent:
    def __init__(self):
        self.research = ResearchService()
        self.llm = LLMService()

    async def execute(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Competitor Agent started for: {state.company_name}")
        try:
            competitors = await self.research.search_competitors(
                state.company_name, state.industry
            )
            state.competitors = competitors

            if competitors:
                logger.info(f"Found {len(competitors)} competitors")
                state.data_sources.append("Competitor Analysis")

                if self.llm.enabled:
                    state.competitor_data = {
                        comp: self._analyze(state.company_name, comp, state.industry)
                        for comp in competitors[:3]
                    }
                else:
                    state.add_error(
                        "competitor_analysis",
                        "LLM unavailable; competitor names only, no analysis",
                    )

            state.add_step("competitor_analysis_complete")
            logger.info("Competitor Agent completed successfully")
        except Exception as e:
            logger.error(f"Competitor Agent error: {e}", exc_info=True)
            state.add_error("competitor_analysis", str(e))
        return state

    def _analyze(self, company: str, competitor: str, industry: str) -> dict:
        try:
            result = self.llm.chat_json(
                SYSTEM_PROMPT,
                PROMPT_TEMPLATE.format(
                    company=company,
                    competitor=competitor,
                    industry=industry or "tech",
                ),
                temperature=0.2,
                max_tokens=700,
            )
            return result or {}
        except Exception as e:
            logger.error(f"Failed to analyze competitor {competitor}: {e}")
            return {}
