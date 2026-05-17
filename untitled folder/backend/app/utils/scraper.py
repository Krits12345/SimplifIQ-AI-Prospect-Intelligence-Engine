"""
Web scraping utilities for extracting company information
"""

import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """Utility for scraping website content"""
    
    def __init__(self):
        self.timeout = 10
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def get_page_content(self, url: str) -> Optional[str]:
        """
        Fetch webpage content
        
        Args:
            url: Website URL to scrape
            
        Returns:
            HTML content or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self.headers, follow_redirects=True)
                response.raise_for_status()
                return response.text
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            return None
    
    def extract_meta_tags(self, html: str) -> Dict[str, str]:
        """
        Extract meta tags from HTML
        
        Returns:
            Dictionary with meta information
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            meta_data = {
                "title": "",
                "description": "",
                "keywords": "",
                "og_title": "",
                "og_description": "",
            }
            
            # Extract title
            if soup.title:
                meta_data["title"] = soup.title.string or ""
            
            # Extract meta tags
            for tag in soup.find_all("meta"):
                name = tag.get("name", "").lower()
                property_attr = tag.get("property", "").lower()
                content = tag.get("content", "")
                
                if name == "description":
                    meta_data["description"] = content
                elif name == "keywords":
                    meta_data["keywords"] = content
                elif property_attr == "og:title":
                    meta_data["og_title"] = content
                elif property_attr == "og:description":
                    meta_data["og_description"] = content
            
            return meta_data
        except Exception as e:
            logger.error(f"Failed to extract meta tags: {str(e)}")
            return {}
    
    def extract_text_content(self, html: str) -> str:
        """
        Extract main text content from HTML
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # Remove script and style tags
            for tag in soup(["script", "style"]):
                tag.decompose()
            
            text = soup.get_text(separator=" ")
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to 2000 chars
        except Exception as e:
            logger.error(f"Failed to extract text: {str(e)}")
            return ""
    
    def extract_social_links(self, html: str) -> Dict[str, str]:
        """
        Extract social media links from website
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            social_links = {}
            
            platforms = {
                "twitter": ["twitter.com", "x.com"],
                "linkedin": ["linkedin.com"],
                "github": ["github.com"],
                "facebook": ["facebook.com"],
                "instagram": ["instagram.com"],
            }
            
            for link in soup.find_all("a"):
                href = link.get("href", "").lower()
                for platform, domains in platforms.items():
                    if any(domain in href for domain in domains):
                        social_links[platform] = href
            
            return social_links
        except Exception as e:
            logger.error(f"Failed to extract social links: {str(e)}")
            return {}
    
    def check_https(self, url: str) -> bool:
        """Check if URL uses HTTPS"""
        return url.startswith("https://")
    
    def extract_broken_links(self, html: str, base_url: str) -> List[str]:
        """
        Identify potentially broken links
        Note: This is basic - real implementation would need to check each link
        """
        try:
            soup = BeautifulSoup(html, "html.parser")
            broken = []
            
            for link in soup.find_all("a"):
                href = link.get("href", "")
                # Simple heuristics for broken links
                if href in ["#", "", "javascript:void(0)"]:
                    broken.append(href)
            
            return broken
        except Exception as e:
            logger.error(f"Failed to extract links: {str(e)}")
            return []
