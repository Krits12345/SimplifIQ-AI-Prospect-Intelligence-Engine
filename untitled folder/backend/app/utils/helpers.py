"""
Helper utilities for the application
"""

from typing import Optional
import re
import logging

logger = logging.getLogger(__name__)


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_website(url: str) -> bool:
    """Validate website URL format"""
    url_pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    return re.match(url_pattern, url) is not None


def normalize_url(url: str) -> str:
    """Normalize URL by ensuring it has http/https"""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    url = normalize_url(url)
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    return domain.replace("www.", "")


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def extract_technology_keywords(text: str) -> list:
    """Extract technology keywords from text"""
    tech_keywords = [
        "python", "javascript", "react", "vue", "angular", "nodejs",
        "fastapi", "django", "flask", "postgresql", "mongodb", "redis",
        "docker", "kubernetes", "aws", "azure", "gcp", "cloud",
        "machine learning", "ai", "blockchain", "api", "rest", "graphql"
    ]
    
    found_tech = []
    text_lower = text.lower()
    
    for tech in tech_keywords:
        if tech in text_lower:
            found_tech.append(tech)
    
    return list(set(found_tech))


def calculate_confidence_score(
    website_found: bool,
    news_found: int = 0,
    about_page_found: bool = False,
    company_info_available: bool = False,
    tech_stack_found: int = 0
) -> float:
    """
    Calculate confidence score based on available data
    
    Returns score between 0-100
    """
    score = 0
    
    if website_found:
        score += 20
    
    if about_page_found:
        score += 25
    
    if company_info_available:
        score += 30
    
    # News score (max 15 points)
    news_score = min(15, news_found * 3)
    score += news_score
    
    # Tech stack score (max 10 points)
    tech_score = min(10, tech_stack_found * 2)
    score += tech_score
    
    return min(100, score)
