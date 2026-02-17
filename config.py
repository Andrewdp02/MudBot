"""Configuration management for Coffee Meme Generator."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for API keys and settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Email Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER")  # e.g., smtp.gmail.com, smtp-mail.outlook.com
    SMTP_PORT = os.getenv("SMTP_PORT", "587")  # Default: 587 (TLS), 465 for SSL
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true")  # true for TLS, false for SSL
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")  # Your email address
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Your email password or app password
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")  # Recipient email address(es), comma-separated for multiple
    
    # Image Generation Parameters
    # Pricing for various models: https://developers.openai.com/api/docs/pricing/
    TEXT_MODEL = os.getenv("TEXT_MODEL", "gpt-4.1-mini")  # gpt-4.1-mini, gpt-4.1, etc.
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-image-1")  # dall-e-3, dall-e-2, etc.
    IMAGE_SIZE = os.getenv("IMAGE_SIZE", "1024x1024")  # Default: 1024x1024
    IMAGE_QUALITY = os.getenv("IMAGE_QUALITY", "low")  # standard or hd
    MAX_IMAGE_SIZE_MB = float(os.getenv("MAX_IMAGE_SIZE_MB", "5.0"))  # Email attachment size limit (typically 25MB, but 5MB is safer)
    
    # Meme Generation Parameters
    MEME_STYLE = os.getenv("MEME_STYLE", "funny")  # funny, motivational, relatable, etc.
    
    # Image Hosting (no longer needed for email, but kept for potential future use)
    # ImgBB is the default (works without API key, no registration issues)
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")  # Optional: not needed for email
    # Imgur is a fallback option (requires Client ID, registration currently broken)
    IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID", "")  # Optional: not needed for email
    
    @classmethod
    def validate(cls):
        """Validate that all required configuration values are set."""
        required_vars = [
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
            ("SMTP_SERVER", cls.SMTP_SERVER),
            ("EMAIL_ADDRESS", cls.EMAIL_ADDRESS),
            ("EMAIL_PASSWORD", cls.EMAIL_PASSWORD),
            ("RECIPIENT_EMAIL", cls.RECIPIENT_EMAIL),
        ]
        
        missing = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing.append(var_name)
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please set these in your .env file. See .env.example for reference."
            )
        
        return True
