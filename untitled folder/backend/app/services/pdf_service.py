"""
PDF generation service using WeasyPrint
Converts HTML reports to PDF
"""

import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class PDFService:
    """Service for generating PDF reports"""
    
    def __init__(self):
        self.output_dir = Path("reports")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_pdf(self, html_content: str, company_name: str, lead_id: int) -> str:
        """
        Generate PDF from HTML content
        
        Args:
            html_content: HTML report content
            company_name: Company name
            lead_id: Lead ID
            
        Returns:
            Path to generated PDF
        """
        try:
            from weasyprint import HTML
        except ImportError as e:
            logger.error("WeasyPrint is not installed or missing native dependencies.")
            raise ImportError(
                "WeasyPrint import failed. Install WeasyPrint and its native dependencies "
                "following https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation"
            ) from e

        try:
            # Create filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{lead_id}_{timestamp}.pdf"
            filepath = self.output_dir / filename
            
            logger.info(f"Generating PDF: {filepath}")
            
            document = HTML(string=html_content)
            document.write_pdf(str(filepath))
            
            logger.info(f"PDF generated successfully: {filepath}")
            
            return str(filepath)
        except Exception as e:
            logger.error(f"Failed to generate PDF: {str(e)}")
            raise
