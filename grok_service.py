"""Grok / xAI API integration for generating coffee memes.

Uses only the Grok image model (grok-imagine-image) to create the meme in one step.
No separate text model. See: https://docs.x.ai/developers/model-capabilities/images/generation
"""
import logging
import requests
import xai_sdk
from config import Config

logger = logging.getLogger(__name__)


class GrokService:
    """Service for generating coffee memes using only the Grok image model."""

    def __init__(self):
        """Initialize xAI client for image generation."""
        if not Config.XAI_API_KEY:
            raise ValueError("XAI_API_KEY is not set in configuration (required when AI_PROVIDER=grok)")
        self.client = xai_sdk.Client(api_key=Config.XAI_API_KEY)

    def generate_meme_image(self) -> bytes:
        """
        Generate a coffee meme image using the Grok image model (grok-imagine-image).
        One prompt only; no separate text model.
        """
        try:
            logger.info("Generating coffee meme image (Grok)...")

            prompt = (
                f"Create a funny, relatable coffee meme. "
                f"Style: {Config.MEME_STYLE}, like something you would see on Facebook or Twitter. "
                "The image should be a complete meme with visible text/caption."
            )

            response = self.client.image.sample(
                prompt=prompt,
                model=Config.GROK_IMAGE_MODEL,
                aspect_ratio=Config.GROK_ASPECT_RATIO,
                resolution=Config.GROK_RESOLUTION,
            )

            if getattr(response, "image", None):
                logger.info(f"Image generated (Grok), size: {len(response.image)} bytes")
                return response.image
            if getattr(response, "url", None):
                logger.info(f"Image generated at: {response.url}")
                image_response = requests.get(response.url)
                image_response.raise_for_status()
                image_bytes = image_response.content
                logger.info(f"Downloaded image, size: {len(image_bytes)} bytes")
                return image_bytes
            raise ValueError("Grok image response had no image or url")
        except Exception as e:
            logger.error(f"Error generating meme image (Grok): {e}")
            raise
