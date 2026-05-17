"""
Research service using Tavily API for company intelligence
"""

import httpx
import logging
from typing import Dict, List, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class ResearchService:
    """Service for researching companies using Tavily API and web search"""
    
    def __init__(self):
        self.tavily_api_key = settings.tavily_api_key
        self.tavily_url = "https://api.tavily.com/search"
    
    async def search_company(self, company_name: str) -> Dict:
        """
        Search for company information using Tavily API
        
        Args:
            company_name: Name of company to research
            
        Returns:
            Research results with news, info, competitors
        """
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                payload = {
                    "api_key": self.tavily_api_key,
                    "query": f"{company_name} company information",
                    "include_answer": True,
                    "max_results": 10
                }
                
                response = await client.post(self.tavily_url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                return {
                    "success": True,
                    "results": data.get("results", []),
                    "answer": data.get("answer", ""),
                    "query": company_name
                }
        except Exception as e:
            logger.error(f"Tavily search failed for {company_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    async def search_news(self, company_name: str) -> List[Dict]:
        """
        Search for recent news about company
        """
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                payload = {
                    "api_key": self.tavily_api_key,
                    "query": f"{company_name} news recent updates",
                    "include_answer": False,
                    "max_results": 5,
                    "topic": "news"
                }
                
                response = await client.post(self.tavily_url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                return data.get("results", [])
        except Exception as e:
            logger.error(f"News search failed: {str(e)}")
            return []
    
    async def search_competitors(self, company_name: str, industry: Optional[str]) -> List[str]:
        """
        Identify competitors of the company
        """
        try:
            query = f"{company_name} competitors"
            if industry:
                query += f" in {industry}"
            
            async with httpx.AsyncClient(timeout=15) as client:
                payload = {
                    "api_key": self.tavily_api_key,
                    "query": query,
                    "include_answer": True,
                    "max_results": 8
                }
                
                response = await client.post(self.tavily_url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                # Extract competitor names from answer
                answer = data.get("answer", "")
                competitors = self._extract_competitors(answer)
                
                return competitors
        except Exception as e:
            logger.error(f"Competitor search failed: {str(e)}")
            return []
    
    def _extract_competitors(self, text: str) -> List[str]:
        """
        Extract competitor names from text
        Simple heuristic-based extraction
        """
        competitors = []
        # This is simplified - in production, use NER model
        sentences = text.split(".")
        for sentence in sentences:
            if "competitor" in sentence.lower() or "alternative" in sentence.lower():
                words = sentence.split(",")
                for word in words:
                    word = word.strip()
                    if len(word) > 3 and word[0].isupper():
                        competitors.append(word)
        
        return list(set(competitors))[:5]  # Return top 5 unique
