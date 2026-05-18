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


_TECH_KEYWORDS = [
    # Languages
    "Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "Ruby", "PHP",
    # Frontend frameworks
    "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt",
    # Backend frameworks
    "Node.js", "FastAPI", "Django", "Flask", "Rails", "Spring", "Express",
    # Datastores
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "DynamoDB",
    # Infra / cloud
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Cloudflare", "Vercel",
    # Concrete capabilities (not the generic "ai" / "api" / "cloud" noise)
    "GraphQL", "Kafka", "Snowflake", "Terraform", "Stripe", "Twilio",
    "OpenAI", "TensorFlow", "PyTorch", "LangChain",
]


def extract_technology_keywords(text: str) -> list:
    """Find concrete tech names in text using word-boundary matching.

    The previous implementation matched substrings against a list containing
    generic terms like "ai" and "api", which produced false positives on any
    page mentioning "main" or "available". This version uses a smaller, more
    specific list and a regex with word boundaries.
    """
    if not text:
        return []
    found = set()
    for keyword in _TECH_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.add(keyword)
    return sorted(found)


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
