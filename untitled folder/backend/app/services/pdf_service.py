"""
PDF generation service.

Primary engine: WeasyPrint (rich HTML/CSS rendering).
Fallback engine: ReportLab (pure-Python, no native deps) — guarantees the
workflow produces a PDF even when WeasyPrint's native libraries (Cairo, Pango,
GTK) are not installed on the host. Without this fallback, PDF generation
silently fails on fresh Windows machines and the rest of the workflow (email
delivery, Drive archive, Sheets update) skips.
"""

import logging
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Any

logger = logging.getLogger(__name__)

# Resolve once: <repo>/backend/reports — independent of process cwd.
_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_OUTPUT_DIR = _BACKEND_ROOT / "reports"


class PDFService:
    """Service for generating PDF reports with a graceful fallback."""

    def __init__(self):
        self.output_dir = _DEFAULT_OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf(
        self,
        html_content: str,
        company_name: str,
        lead_id: int,
        state: Optional[Any] = None,
    ) -> str:
        """
        Render the report to PDF.

        Tries WeasyPrint first (best fidelity to the styled HTML). If
        WeasyPrint is unavailable or throws at runtime, falls back to a
        ReportLab build that consumes either the workflow `state` directly
        or a text rendering of the HTML.

        Returns the absolute path to the generated PDF.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{lead_id}_{timestamp}.pdf"
        filepath = self.output_dir / filename

        if html_content:
            try:
                self._render_with_weasyprint(html_content, filepath)
                logger.info(f"PDF generated with WeasyPrint: {filepath}")
                return str(filepath)
            except Exception as e:
                logger.warning(
                    "WeasyPrint render failed (%s) — falling back to ReportLab", e
                )

        # Fallback path — always succeeds if reportlab is installed.
        self._render_with_reportlab(state, html_content, company_name, filepath)
        logger.info(f"PDF generated with ReportLab fallback: {filepath}")
        return str(filepath)

    def _render_with_weasyprint(self, html_content: str, filepath: Path) -> None:
        from weasyprint import HTML  # local import: optional dependency

        HTML(string=html_content).write_pdf(str(filepath))

    def _render_with_reportlab(
        self,
        state: Optional[Any],
        html_content: str,
        company_name: str,
        filepath: Path,
    ) -> None:
        """Build a structured PDF without native libs. Pure Python."""
        from reportlab.lib.pagesizes import LETTER
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            PageBreak,
        )

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=LETTER,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )

        base_styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "TitleStyle",
            parent=base_styles["Title"],
            fontSize=24,
            textColor=colors.HexColor("#0066cc"),
            spaceAfter=14,
        )
        h2 = ParagraphStyle(
            "H2",
            parent=base_styles["Heading2"],
            fontSize=15,
            textColor=colors.HexColor("#0066cc"),
            spaceBefore=12,
            spaceAfter=6,
        )
        body = ParagraphStyle(
            "Body",
            parent=base_styles["BodyText"],
            fontSize=10.5,
            leading=15,
            spaceAfter=6,
        )
        small = ParagraphStyle(
            "Small",
            parent=base_styles["BodyText"],
            fontSize=9,
            textColor=colors.grey,
        )

        def safe(value, default=""):
            return value if value not in (None, "", []) else default

        if state is not None:
            company = safe(getattr(state, "company_name", company_name), company_name)
            website = safe(getattr(state, "website_url", ""), "—")
            industry = safe(getattr(state, "industry", ""), "—")
            description = safe(
                getattr(state, "company_description", ""),
                "Company profile being analyzed.",
            )
            tech_stack = getattr(state, "tech_stack", []) or []
            strengths = getattr(state, "strengths", []) or []
            opportunities = getattr(state, "opportunities", []) or []
            pain_points = getattr(state, "pain_points", []) or []
            recommendations = getattr(state, "recommendations", []) or []
            competitors = getattr(state, "competitors", []) or []
            competitor_data = getattr(state, "competitor_data", {}) or {}
            recent_news = getattr(state, "recent_news", []) or []
            website_findings = getattr(state, "website_findings", []) or []
            website_score = float(getattr(state, "website_score", 0) or 0)
            confidence_score = float(getattr(state, "confidence_score", 0) or 0)
            data_sources = getattr(state, "data_sources", []) or []
            lead_name = safe(getattr(state, "lead_name", ""), "")
            lead_email = safe(getattr(state, "lead_email", ""), "")
        else:
            # Last-resort: derive plaintext from HTML, no structured data.
            company = company_name
            website = industry = "—"
            description = self._strip_html(html_content)[:1200] or "Report content unavailable."
            tech_stack = strengths = opportunities = pain_points = []
            recommendations = competitors = recent_news = website_findings = data_sources = []
            competitor_data = {}
            website_score = confidence_score = 0.0
            lead_name = lead_email = ""

        story = []
        story.append(Paragraph("SimplifIQ AI Prospect Intelligence", small))
        story.append(Paragraph(company, title_style))
        story.append(Paragraph("Company Intelligence Report", body))
        story.append(Spacer(1, 8))

        story.append(Paragraph("Executive Summary", h2))
        story.append(Paragraph(description, body))

        story.append(Paragraph("Key Metrics", h2))
        metric_data = [
            ["Website Health Score", f"{website_score:.0f} / 100"],
            ["Analysis Confidence", f"{confidence_score:.0f}%"],
            ["Industry", industry],
            ["Website", website],
            ["Technologies", ", ".join(tech_stack) if tech_stack else "Not identified"],
        ]
        metrics = Table(metric_data, hAlign="LEFT", colWidths=[2.2 * inch, 4.3 * inch])
        metrics.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f1f5f9")),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                ]
            )
        )
        story.append(metrics)

        def bullet_block(title: str, items: list, limit: int = 5):
            if not items:
                return
            story.append(Paragraph(title, h2))
            for item in items[:limit]:
                story.append(Paragraph(f"• {item}", body))

        bullet_block("Strengths", strengths)
        bullet_block("Growth Opportunities", opportunities)
        bullet_block("Pain Points", pain_points)

        if website_findings:
            story.append(Paragraph("Website Audit Findings", h2))
            for finding in website_findings[:6]:
                issue = finding.get("issue", "Finding")
                recommendation = finding.get("recommendation", "")
                story.append(Paragraph(f"<b>{issue}.</b> {recommendation}", body))

        if competitors:
            story.append(PageBreak())
            story.append(Paragraph("Competitive Intelligence", title_style))
            story.append(Paragraph("Identified Competitors", h2))
            for comp in competitors[:5]:
                positioning = (
                    competitor_data.get(comp, {}).get("positioning")
                    if isinstance(competitor_data, dict)
                    else None
                ) or "Competitive player in the market"
                story.append(Paragraph(f"<b>{comp}</b> — {positioning}", body))

        if recent_news:
            story.append(Paragraph("Recent News & Updates", h2))
            for news in recent_news[:3]:
                title_text = news.get("title", "News Article") if isinstance(news, dict) else str(news)
                snippet = news.get("snippet", "") if isinstance(news, dict) else ""
                story.append(Paragraph(f"<b>{title_text}</b>", body))
                if snippet:
                    story.append(Paragraph(snippet[:240], body))

        if recommendations:
            story.append(PageBreak())
            story.append(Paragraph("Strategic Recommendations", title_style))
            for i, rec in enumerate(recommendations[:6], 1):
                story.append(Paragraph(f"<b>Action {i}.</b> {rec}", body))

        story.append(Spacer(1, 12))
        if data_sources:
            story.append(Paragraph(f"Data Sources: {', '.join(data_sources)}", small))
        if lead_name or lead_email:
            story.append(Paragraph(f"Prepared for: {lead_name} • {lead_email}", small))
        story.append(
            Paragraph(
                f"Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} by SimplifIQ",
                small,
            )
        )

        doc.build(story)

    @staticmethod
    def _strip_html(html: str) -> str:
        if not html:
            return ""
        text = re.sub(r"<[^>]+>", " ", html)
        return re.sub(r"\s+", " ", text).strip()
