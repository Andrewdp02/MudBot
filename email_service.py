"""Email service for sending meme images via SMTP."""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import io
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending images via email."""
    
    def __init__(self):
        """Initialize email service with SMTP configuration."""
        if not all([Config.SMTP_SERVER, Config.SMTP_PORT, Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD]):
            raise ValueError("Email configuration is incomplete")
        
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = int(Config.SMTP_PORT)
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
        self.use_tls = Config.SMTP_USE_TLS.lower() == 'true' if Config.SMTP_USE_TLS else True
    
    def send_image(self, image_bytes: bytes, recipients: list = None) -> bool:
        """
        Send an image via email as an attachment.
        
        Args:
            image_bytes: Image data as bytes
            recipients: List of email addresses to send to (defaults to RECIPIENT_EMAIL from config)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            if recipients is None:
                # Parse RECIPIENT_EMAIL (can be comma-separated)
                if Config.RECIPIENT_EMAIL:
                    recipients = [email.strip() for email in Config.RECIPIENT_EMAIL.split(',')]
                else:
                    recipients = []
            
            # Ensure recipients is a list
            if isinstance(recipients, str):
                recipients = [email.strip() for email in recipients.split(',')]
            
            # Filter out empty strings
            recipients = [r for r in recipients if r and r.strip()]
            if not recipients:
                raise ValueError("No valid recipient email addresses provided")
            
            logger.info(f"Sending image to {', '.join(recipients)}")
            logger.info(f"Image size: {len(image_bytes)} bytes")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"The Daily Mud - {datetime.now().strftime('%B %d, %Y')}"
            
            # Add body text
            body = (
                "Here's your daily mud meme ☕\n\n"
                "You have been blessed by the MudBot"
            )
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach image
            image_part = MIMEBase('image', 'jpeg')
            image_part.set_payload(image_bytes)
            encoders.encode_base64(image_part)
            image_part.add_header(
                'Content-Disposition',
                f'attachment; filename=coffee_meme_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
            )
            msg.attach(image_part)
            
            # Send email
            logger.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    logger.debug("Starting TLS...")
                    server.starttls()
                
                logger.info("Logging in to email server...")
                server.login(self.email_address, self.email_password)
                
                logger.info("Sending email...")
                text = msg.as_string()
                server.sendmail(self.email_address, recipients, text)
            
            logger.info(f"Email sent successfully to {', '.join(recipients)}")
            return True
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error sending email: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise
