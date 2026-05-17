"""
Email service using SendGrid for sending personalized emails
"""

import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment
import base64
from pathlib import Path
from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SendGrid"""
    
    def __init__(self):
        self.sg = SendGridAPIClient(settings.sendgrid_api_key)
        self.from_email = settings.from_email
    
    async def send_report_email(
        self,
        to_email: str,
        to_name: str,
        company_name: str,
        email_content: str,
        pdf_path: Optional[str] = None
    ) -> bool:
        """
        Send personalized report email with PDF attachment
        
        Args:
            to_email: Recipient email
            to_name: Recipient name
            company_name: Company name
            email_content: Email body content
            pdf_path: Path to PDF attachment
            
        Returns:
            True if sent successfully
        """
        try:
            # Extract subject and body
            lines = email_content.strip().split('\n')
            subject = "Company Intelligence Report"
            body = email_content
            
            if lines and lines[0].startswith("Subject:"):
                subject = lines[0].replace("Subject:", "").strip()
                body = '\n'.join(lines[1:]).strip()
            
            message = Mail(
                from_email=self.from_email,
                to_emails=(to_email, to_name),
                subject=subject,
                plain_text_content=body
            )
            
            # Attach PDF if provided
            if pdf_path and Path(pdf_path).exists():
                with open(pdf_path, 'rb') as attachment:
                    pdf_data = base64.b64encode(attachment.read()).decode()
                
                pdf_attachment = Attachment(
                    file_content=pdf_data,
                    file_name=Path(pdf_path).name,
                    file_type="application/pdf"
                )
                message.attachment = pdf_attachment
                
                logger.info(f"PDF attached: {pdf_path}")
            
            # Send email
            response = self.sg.send(message)
            
            logger.info(f"Email sent to {to_email}: Status {response.status_code}")
            
            return response.status_code == 202
        
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    async def send_welcome_email(self, to_email: str, to_name: str) -> bool:
        """Send welcome email when lead is captured"""
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=(to_email, to_name),
                subject="Thank you for submitting your lead - Analysis in progress",
                plain_text_content=f"""
Hi {to_name},

Thank you for submitting your company for analysis. We're currently processing your request and will send you a comprehensive intelligence report shortly.

You'll receive:
✓ Complete company research and analysis
✓ Website health assessment
✓ Competitor intelligence
✓ Personalized growth recommendations
✓ Strategic next steps

Thank you for choosing SimplifIQ AI Prospect Intelligence.

Best regards,
SimplifIQ Team
"""
            )
            
            response = self.sg.send(message)
            logger.info(f"Welcome email sent to {to_email}")
            return response.status_code == 202
        
        except Exception as e:
            logger.error(f"Failed to send welcome email: {str(e)}")
            return False
