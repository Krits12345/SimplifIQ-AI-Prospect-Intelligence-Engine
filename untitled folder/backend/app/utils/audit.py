"""
Website health audit analysis
Generates scores and insights about website quality
"""

import httpx
from typing import Dict, List
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class WebsiteAudit:
    """Analyzes website health and generates audit score"""
    
    async def audit_website(self, url: str, html_content: str, meta_data: Dict) -> Dict:
        """
        Perform complete website audit
        
        Returns audit results including score and findings
        """
        findings = []
        score = 100
        
        # Check HTTPS
        if not url.startswith("https://"):
            findings.append({
                "category": "Security",
                "issue": "Website does not use HTTPS",
                "severity": "high",
                "recommendation": "Migrate to HTTPS for better security and SEO"
            })
            score -= 15
        else:
            findings.append({
                "category": "Security",
                "issue": "HTTPS enabled",
                "status": "good"
            })
        
        # Check meta description
        if not meta_data.get("description"):
            findings.append({
                "category": "SEO",
                "issue": "Missing meta description",
                "severity": "medium",
                "recommendation": "Add compelling meta descriptions to all pages"
            })
            score -= 10
        else:
            findings.append({
                "category": "SEO",
                "issue": "Meta description present",
                "status": "good"
            })
        
        # Check title tag
        if not meta_data.get("title"):
            findings.append({
                "category": "SEO",
                "issue": "Missing page title",
                "severity": "high",
                "recommendation": "Add descriptive title tags"
            })
            score -= 10
        else:
            findings.append({
                "category": "SEO",
                "issue": "Page title present",
                "status": "good"
            })
        
        # Check for mobile responsiveness indicators
        if "viewport" in html_content.lower():
            findings.append({
                "category": "Mobile",
                "issue": "Mobile responsive",
                "status": "good"
            })
        else:
            findings.append({
                "category": "Mobile",
                "issue": "No viewport meta tag detected",
                "severity": "medium",
                "recommendation": "Add mobile viewport meta tag"
            })
            score -= 10
        
        # Check page size
        page_size_kb = len(html_content) / 1024
        if page_size_kb > 3000:
            findings.append({
                "category": "Performance",
                "issue": f"Large page size: {page_size_kb:.0f}KB",
                "severity": "low",
                "recommendation": "Optimize assets and reduce page size"
            })
            score -= 5
        else:
            findings.append({
                "category": "Performance",
                "issue": "Reasonable page size",
                "status": "good"
            })
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        return {
            "score": score,
            "findings": findings,
            "summary": self._generate_summary(score)
        }
    
    def _generate_summary(self, score: int) -> str:
        """Generate human-readable summary based on score"""
        if score >= 85:
            return "Excellent website quality and SEO optimization"
        elif score >= 70:
            return "Good website health with room for improvement"
        elif score >= 50:
            return "Moderate website health - multiple issues to address"
        else:
            return "Poor website health - significant improvements needed"
