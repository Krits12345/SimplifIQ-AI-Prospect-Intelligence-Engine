"""
Research Agent - Gathers company information
Responsible for:
- Searching company information
- Scraping website
- Extracting about page
- Collecting recent news
"""

import logging
from typing import Dict, Any
import asyncio
from app.utils.scraper import WebScraper
from app.utils.research import ResearchService
from app.utils.helpers import extract_technology_keywords, extract_domain, normalize_url
from app.agents.state import WorkflowState

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Researches company and gathers basic information"""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.research = ResearchService()
    
    async def execute(self, state: WorkflowState) -> WorkflowState:
        """
        Main execution method for research agent
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated workflow state with research results
        """
        logger.info(f"Research Agent started for company: {state.company_name}")
        
        try:
            # Step 1: Search company information
            logger.info("Searching company information...")
            search_results = await self.research.search_company(state.company_name)
            
            if search_results.get("success"):
                state.company_description = search_results.get("answer", "")
                state.data_sources.append("Web Search")
                logger.info("Company search completed")
            else:
                logger.warning(f"Company search failed: {search_results.get('error')}")
            
            # Step 2: Scrape website
            logger.info(f"Scraping website: {state.website_url}")
            website_url = normalize_url(state.website_url)
            html_content = await self.scraper.get_page_content(website_url)
            
            if html_content:
                state.website_content = html_content
                state.data_sources.append("Website")
                
                # Extract meta tags
                meta_tags = self.scraper.extract_meta_tags(html_content)
                state.meta_tags = meta_tags
                
                # Extract technology stack
                text_content = self.scraper.extract_text_content(html_content)
                technologies = extract_technology_keywords(text_content + " " + html_content)
                state.tech_stack = technologies
                
                logger.info(f"Found {len(technologies)} technologies")
            else:
                logger.warning(f"Failed to scrape website")
            
            # Step 3: Scrape about page
            logger.info("Scraping about page...")
            domain = extract_domain(state.website_url)
            about_urls = [
                f"{website_url}/about",
                f"{website_url}/about-us",
                f"{website_url}/company",
            ]
            
            for about_url in about_urls:
                about_html = await self.scraper.get_page_content(about_url)
                if about_html:
                    state.about_page_content = self.scraper.extract_text_content(about_html)
                    state.data_sources.append("About Page")
                    logger.info("About page extracted")
                    break
            
            # Step 4: Search for recent news
            logger.info("Searching for recent news...")
            news_results = await self.research.search_news(state.company_name)
            state.recent_news = [
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", ""),
                }
                for result in news_results
            ]
            
            if state.recent_news:
                state.data_sources.append("News")
                logger.info(f"Found {len(state.recent_news)} news articles")
            
            state.add_step("research_complete")
            logger.info("Research Agent completed successfully")
            
        except Exception as e:
            logger.error(f"Research Agent error: {str(e)}")
            state.add_error("research", str(e))
        
        return state
