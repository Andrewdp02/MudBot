"""Twilio SMS/MMS integration for sending meme images."""
import logging
import io
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from config import Config
from image_hosting import ImageHostingService

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending images via Twilio SMS/MMS."""
    
    def __init__(self):
        """Initialize Twilio client."""
        if not all([Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_PHONE_NUMBER]):
            raise ValueError("Twilio configuration is incomplete")
        
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.from_number = Config.TWILIO_PHONE_NUMBER
    
    def send_image(self, image_bytes: bytes, recipient: str = None) -> bool:
        """
        Send an image via MMS using Twilio.
        
        This method automatically uploads the image to a hosting service (ImgBB by default)
        to get a publicly accessible URL, then sends it via Twilio MMS.
        
        Args:
            image_bytes: Image data as bytes
            recipient: Phone number to send to (defaults to RECIPIENT_PHONE_NUMBER from config)
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            recipient = recipient or Config.RECIPIENT_PHONE_NUMBER
            if not recipient:
                raise ValueError("No recipient phone number provided")
            
            logger.info(f"Sending image to {recipient}")
            logger.info(f"Image size: {len(image_bytes)} bytes")
            
            # Upload image to get a publicly accessible URL
            # Note: Twilio MMS requires images to be at a publicly accessible URL
            logger.info("Uploading image to hosting service...")
            image_url = ImageHostingService.upload_image(image_bytes)
            
            # Send MMS message with image URL
            return self.send_image_via_url(image_url, recipient)
            
        except Exception as e:
            logger.error(f"Error sending image: {e}")
            raise
    
    def send_image_via_url(self, image_url: str, recipient: str = None) -> bool:
        """
        Send an image via MMS using a publicly accessible URL.
        
        This is the recommended method for sending images via Twilio MMS.
        You'll need to upload your image to a hosting service first.
        
        Args:
            image_url: Publicly accessible URL of the image
            recipient: Phone number to send to (defaults to RECIPIENT_PHONE_NUMBER from config)
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            recipient = recipient or Config.RECIPIENT_PHONE_NUMBER
            if not recipient:
                raise ValueError("No recipient phone number provided")
            
            logger.info(f"Sending image from URL to {recipient}")
            
            message = self.client.messages.create(
                body="☕ Your daily coffee meme!",
                from_=self.from_number,
                to=recipient,
                media_url=[image_url]
            )
            
            logger.info(f"Message sent successfully. SID: {message.sid}")
            return True
            
        except TwilioException as e:
            logger.error(f"Twilio error sending message: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            raise
