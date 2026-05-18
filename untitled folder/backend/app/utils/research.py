"""
Research service using Tavily API for company intelligence
"""

import httpx
import logging
from typing import Dict, List, Optional
from app.config import settings
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


class ResearchService:
    """Service for researching companies using Tavily API and web search"""

    def __init__(self):
        self.tavily_api_key = settings.tavily_api_key
        self.tavily_url = "https://api.tavily.com/search"
        self.llm = LLMService()
    
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
                answer = data.get("answer", "")
                results = data.get("results", [])

                # Prefer the LLM if configured — much higher precision than
                # the punctuation-splitting heuristic. Fall back to the
                # heuristic so the agent still works without an LLM key.
                competitors = self._extract_competitors_llm(company_name, answer, results)
                if not competitors:
                    competitors = self._extract_competitors_heuristic(answer)
                return competitors
        except Exception as e:
            logger.error(f"Competitor search failed: {str(e)}")
            return []

    def _extract_competitors_llm(
        self, company_name: str, answer: str, results: List[Dict]
    ) -> List[str]:
        """Ask the LLM to pull clean competitor names out of search results."""
        if not self.llm.enabled:
            return []
        snippets = "\n".join(
            f"- {r.get('title', '')}: {r.get('content', '')[:240]}"
            for r in results[:6]
        )
        user_prompt = (
            f"Identify direct competitors of {company_name} from the search material below.\n\n"
            f"Answer summary: {answer}\n\n"
            f"Top search results:\n{snippets}\n\n"
            'Return JSON only: {"competitors": ["Name 1", "Name 2", ...]}.\n'
            "Rules: real company names only (no descriptions, no the/an, no 'etc.'). "
            "Exclude the target company itself. Max 5 entries. "
            'If no competitors are clearly identified, return {"competitors": []}.'
        )
        parsed = self.llm.chat_json(
            "You extract competitor company names from search results. Be precise; do not invent names.",
            user_prompt,
            temperature=0.0,
            max_tokens=200,
        )
        if not parsed:
            return []
        raw = parsed.get("competitors") or []
        cleaned = []
        for name in raw:
            if not isinstance(name, str):
                continue
            name = name.strip().strip(".,;")
            if not name or name.lower() == company_name.lower():
                continue
            if name not in cleaned:
                cleaned.append(name)
        return cleaned[:5]

    @staticmethod
    def _extract_competitors_heuristic(text: str) -> List[str]:
        """Last-resort extraction when no LLM is available."""
        competitors = []
        for sentence in (text or "").split("."):
            if "competitor" in sentence.lower() or "alternative" in sentence.lower():
                for word in sentence.split(","):
                    word = word.strip()
                    if len(word) > 3 and word[0].isupper():
                        competitors.append(word)
        seen = []
        for name in competitors:
            if name not in seen:
                seen.append(name)
        return seen[:5]
