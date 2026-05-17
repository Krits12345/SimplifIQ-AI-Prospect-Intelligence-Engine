"""
Insight Agent - Generates AI-powered insights
Responsible for:
- Analyzing company strengths
- Identifying opportunities
- Finding pain points
- Generating recommendations
"""

import logging
from typing import List
import openai
from app.config import settings
from app.agents.state import WorkflowState

logger = logging.getLogger(__name__)

openai.api_key = settings.openai_api_key


class InsightAgent:
    """Generates AI insights about company"""
    
    def __init__(self):
        self.model_name = "gpt-3.5-turbo"
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Generate insights about company
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with insights
        """
        logger.info(f"Insight Agent started for: {state.company_name}")
        
        try:
            # Prepare context
            context = self._prepare_context(state)
            
            # Generate insights
            logger.info("Generating AI insights...")
            insights = await self._generate_insights(context)
            
            state.strengths = insights.get("strengths", [])
            state.opportunities = insights.get("opportunities", [])
            state.pain_points = insights.get("pain_points", [])
            state.recommendations = insights.get("recommendations", [])
            
            state.add_step("insight_complete")
            logger.info("Insight Agent completed successfully")
            
        except Exception as e:
            logger.error(f"Insight Agent error: {str(e)}")
            state.add_error("insights", str(e))
        
        return state
    
    def _prepare_context(self, state: WorkflowState) -> str:
        """Prepare context for AI analysis"""
        context = f"""
Company Name: {state.company_name}
Industry: {state.industry or "Unknown"}
Description: {state.company_description[:500]}
Website Content: {state.website_content[:500] if state.website_content else "Not available"}
About Page: {state.about_page_content[:500] if state.about_page_content else "Not available"}
Technologies: {", ".join(state.tech_stack)}
Recent News: {len(state.recent_news)} articles found
"""
        return context
    
    async def _generate_insights(self, context: str) -> dict:
        """Generate insights using Gemini API"""
        try:
            prompt = f"""
Based on this company information:

{context}

Please provide a JSON response with the following structure (no markdown, just JSON):
{{
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"],
    "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
    "recommendations": ["recommendation 1", "recommendation 2", "recommendation 3", "recommendation 4"]
}}

Focus on being specific and actionable. Each item should be 1-2 sentences max.
"""
            
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a senior business analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            result_text = response.choices[0].message.content
            
            # Parse response
            import json
            import re
            
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            
            return {
                "strengths": [],
                "opportunities": [],
                "pain_points": [],
                "recommendations": []
            }
        
        except Exception as e:
            logger.error(f"Failed to generate insights: {str(e)}")
            return {
                "strengths": [],
                "opportunities": [],
                "pain_points": [],
                "recommendations": []
            }
