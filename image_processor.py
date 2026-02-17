"""Image processing utilities for SMS compatibility."""
import logging
import io
from PIL import Image
from config import Config

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Service for processing images to meet SMS/MMS requirements."""
    
    MAX_SIZE_MB = Config.MAX_IMAGE_SIZE_MB
    MAX_SIZE_BYTES = int(MAX_SIZE_MB * 1024 * 1024)
    
    # Common MMS size limits by carrier (use the most restrictive)
    MAX_DIMENSION = 1600  # Maximum width or height in pixels
    
    @classmethod
    def process_for_sms(cls, image_bytes: bytes) -> bytes:
        """
        Process image to ensure it meets SMS/MMS requirements.
        
        Args:
            image_bytes: Original image as bytes
            
        Returns:
            bytes: Processed image as bytes
        """
        try:
            logger.info(f"Processing image for SMS. Original size: {len(image_bytes)} bytes")
            
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            original_format = image.format
            
            # Convert RGBA to RGB if necessary (for JPEG compatibility)
            if image.mode in ('RGBA', 'LA', 'P'):
                logger.info(f"Converting image from {image.mode} to RGB")
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                rgb_image.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = rgb_image
            
            # Resize if dimensions are too large
            width, height = image.size
            if width > cls.MAX_DIMENSION or height > cls.MAX_DIMENSION:
                logger.info(f"Resizing image from {width}x{height} to fit {cls.MAX_DIMENSION}px limit")
                image.thumbnail((cls.MAX_DIMENSION, cls.MAX_DIMENSION), Image.Resampling.LANCZOS)
            
            # Compress to meet size requirements
            output = io.BytesIO()
            quality = 95
            
            # Try to save as JPEG (more efficient for photos/memes)
            image_format = 'JPEG'
            if original_format == 'PNG' and image.mode == 'RGB':
                # Convert PNG to JPEG for better compression
                image_format = 'JPEG'
            
            while True:
                output.seek(0)
                output.truncate(0)
                
                image.save(output, format=image_format, quality=quality, optimize=True)
                size = len(output.getvalue())
                
                if size <= cls.MAX_SIZE_BYTES or quality <= 50:
                    break
                
                quality -= 5
                logger.debug(f"Image too large ({size} bytes), reducing quality to {quality}")
            
            processed_bytes = output.getvalue()
            logger.info(f"Processed image size: {len(processed_bytes)} bytes (quality: {quality})")
            
            if len(processed_bytes) > cls.MAX_SIZE_BYTES:
                logger.warning(
                    f"Image size ({len(processed_bytes)} bytes) still exceeds limit "
                    f"({cls.MAX_SIZE_BYTES} bytes) after processing. "
                    f"Some carriers may reject this message."
                )
            
            return processed_bytes
            
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise
