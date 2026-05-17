"""
Competitor Agent - Identifies and analyzes competitors
Responsible for:
- Finding competitors
- Comparing positioning
- Analyzing competitor strengths
"""

import logging
from app.utils.research import ResearchService
from app.agents.state import WorkflowState
import openai
from app.config import settings
import json
import re

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key


class CompetitorAgent:
    """Identifies and analyzes competitors"""
    
    def __init__(self):
        self.research = ResearchService()
        self.model_name = "gpt-3.5-turbo"
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Find and analyze competitors
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with competitor analysis
        """
        logger.info(f"Competitor Agent started for: {state.company_name}")
        
        try:
            # Step 1: Search for competitors
            logger.info("Searching for competitors...")
            competitors = await self.research.search_competitors(
                state.company_name,
                state.industry
            )
            state.competitors = competitors
            
            if competitors:
                logger.info(f"Found {len(competitors)} competitors")
                state.data_sources.append("Competitor Analysis")
                
                # Step 2: Analyze each competitor
                competitor_data = {}
                for competitor in competitors[:3]:  # Analyze top 3
                    logger.info(f"Analyzing competitor: {competitor}")
                    analysis = await self._analyze_competitor(
                        state.company_name,
                        competitor,
                        state.industry
                    )
                    competitor_data[competitor] = analysis
                
                state.competitor_data = competitor_data
            
            state.add_step("competitor_analysis_complete")
            logger.info("Competitor Agent completed successfully")
            
        except Exception as e:
            logger.error(f"Competitor Agent error: {str(e)}")
            state.add_error("competitor_analysis", str(e))
        
        return state
    
    async def _analyze_competitor(
        self,
        company: str,
        competitor: str,
        industry: str
    ) -> dict:
        """
        Analyze a specific competitor
        """
        try:
            prompt = f"""
Compare {company} with competitor {competitor} in the {industry or 'tech'} industry.

Provide a JSON response:
{{
    "positioning": "brief positioning",
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "market_focus": "target market description",
    "competitive_advantage": "key advantage"
}}
"""
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert market analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=700
            )
            
            result_text = response.choices[0].message.content
            
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {
                "positioning": "",
                "strengths": [],
                "weaknesses": [],
                "market_focus": ""
            }
        
        except Exception as e:
            logger.error(f"Failed to analyze competitor {competitor}: {str(e)}")
            return {}
