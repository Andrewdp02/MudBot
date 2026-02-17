"""OpenAI API integration for generating coffee memes."""
import base64
import logging
import requests
from openai import OpenAI
from config import Config

logger = logging.getLogger(__name__)

# gpt-image-1 returns base64 only (url is always null); DALL-E returns url or b64
GPT_IMAGE_MODELS = ("gpt-image-1", "gpt-image-1-mini")


class OpenAIService:
    """Service for interacting with OpenAI API to generate meme text and images."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in configuration")
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    def generate_meme_text(self) -> str:
        """
        Generate a short, funny coffee meme caption using the chat API.
        The text is designed to be overlaid on a meme image.
        
        Returns:
            str: The meme caption (one or two lines, no quotes)
        """
        try:
            logger.info("Generating meme text...")
            response = self.client.chat.completions.create(
                model=Config.TEXT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You write short, funny captions for coffee memes. "
                            "Reply with ONLY the caption text—no quotes, no explanation, no prefix. "
                            "Keep it to one or two short lines, relatable and suitable for a meme image."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Write a {Config.MEME_STYLE} coffee meme caption.",
                    },
                ],
                max_tokens=100,
            )
            text = (response.choices[0].message.content or "").strip().strip('"\'')
            logger.info(f"Meme text: {text!r}")
            return text
        except Exception as e:
            logger.error(f"Error generating meme text: {e}")
            raise
    
    def generate_meme_image(self, meme_text: str) -> bytes:
        """
        Generate a coffee meme image that displays the given text using DALL-E.
        The image prompt instructs the model to render the exact text clearly.
        
        Args:
            meme_text: The caption to display on the image (from generate_meme_text).
        
        Returns:
            bytes: The generated image as bytes
        """
        try:
            logger.info("Generating coffee meme image with caption...")
            
            # Prompt tells DALL-E exactly what text to show so it renders it clearly
            image_prompt = (
                "Create a funny, relatable coffee meme image. "
                "The image MUST display this exact text clearly and legibly, in large readable text: "
                f'"{meme_text}". '
                "Style: realistic, like something you would see on Facebook or Instagram. "
                "Make the text the main focus of the meme."
            )
            
            image_model = Config.OPENAI_MODEL
            is_gpt_image = image_model.lower() in GPT_IMAGE_MODELS

            # Model-specific sizes and quality (gpt-image-1 uses different options)
            if is_gpt_image:
                size = Config.IMAGE_SIZE
                if size not in ["1024x1024", "1536x1024", "1024x1536", "auto"]:
                    size = "1024x1024"
                quality = Config.IMAGE_QUALITY
                if quality not in ("high", "medium", "low", "auto"):
                    quality = "high" if quality == "hd" else "medium"
            else:
                size = Config.IMAGE_SIZE
                if size not in ["1024x1024", "1792x1024", "1024x1792"]:
                    size = "1024x1024"
                    logger.warning(f"Invalid image size, using default: {size}")
                quality = Config.IMAGE_QUALITY

            kwargs = {
                "model": image_model,
                "prompt": image_prompt,
                "size": size,
                "quality": quality,
                "n": 1,
            }

            # Generate image
            response = self.client.images.generate(**kwargs)

            # gpt-image-1 returns base64 only (url is null); DALL-E returns url
            item = response.data[0]
            if getattr(item, "b64_json", None):
                image_bytes = base64.b64decode(item.b64_json)
                logger.info(f"Image generated (base64), size: {len(image_bytes)} bytes")
            elif getattr(item, "url", None):
                image_url = item.url
                logger.info(f"Image generated at: {image_url}")
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                image_bytes = image_response.content
                logger.info(f"Downloaded image, size: {len(image_bytes)} bytes")
            else:
                raise ValueError("Image response had no b64_json or url")
            
            return image_bytes
            
        except Exception as e:
            logger.error(f"Error generating meme image: {e}")
            raise
