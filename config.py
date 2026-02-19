"""Configuration management for Coffee Meme Generator."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for API keys and settings."""
    
    # AI Provider: "openai" or "grok"
    AI_PROVIDER = (os.getenv("AI_PROVIDER", "openai") or "openai").strip().lower()
    if AI_PROVIDER not in ("openai", "grok"):
        AI_PROVIDER = "openai"
    
    # OpenAI Configuration (used when AI_PROVIDER=openai)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Grok / xAI Configuration (used when AI_PROVIDER=grok)
    XAI_API_KEY = os.getenv("XAI_API_KEY")
    GROK_TEXT_MODEL = os.getenv("GROK_TEXT_MODEL", "grok-2-latest")  # e.g. grok-2-latest, grok-3-mini
    GROK_IMAGE_MODEL = os.getenv("GROK_IMAGE_MODEL", "grok-imagine-image")
    GROK_ASPECT_RATIO = os.getenv("GROK_ASPECT_RATIO", "1:1")  # 1:1, 16:9, 9:16, 4:3, 3:4, etc.
    GROK_RESOLUTION = os.getenv("GROK_RESOLUTION", "1k")  # 1k or 2k
    
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
            ("SMTP_SERVER", cls.SMTP_SERVER),
            ("EMAIL_ADDRESS", cls.EMAIL_ADDRESS),
            ("EMAIL_PASSWORD", cls.EMAIL_PASSWORD),
            ("RECIPIENT_EMAIL", cls.RECIPIENT_EMAIL),
        ]
        if cls.AI_PROVIDER == "openai":
            required_vars.insert(0, ("OPENAI_API_KEY", cls.OPENAI_API_KEY))
        else:
            required_vars.insert(0, ("XAI_API_KEY", cls.XAI_API_KEY))
        
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
