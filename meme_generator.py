"""Main script for generating and sending daily coffee memes."""
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from config import Config
from openai_service import OpenAIService
from image_processor import ImageProcessor
from email_service import EmailService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('meme_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to generate and send coffee meme."""
    try:
        logger.info("=" * 60)
        logger.info("Starting coffee meme generation")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)
        
        # Validate configuration
        logger.info("Validating configuration...")
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Initialize services
        logger.info("Initializing services...")
        openai_service = OpenAIService()
        email_service = EmailService()
        logger.info("Services initialized successfully")
        
        # Step 1a: Generate meme text
        logger.info("Step 1a: Generating meme text...")
        meme_text = openai_service.generate_meme_text()
        logger.info(f"Meme text: {meme_text!r}")
        
        # Step 1b: Generate meme image with that text
        logger.info("Step 1b: Generating coffee meme image with caption...")
        image_bytes = openai_service.generate_meme_image(meme_text)
        logger.info(f"Image generated: {len(image_bytes)} bytes")
        
        # Step 2: Process image for email (optional, but helps with size)
        logger.info("Step 2: Processing image for email...")
        processed_image = ImageProcessor.process_for_sms(image_bytes)  # Reuse same processor
        logger.info(f"Image processed: {len(processed_image)} bytes")
        
        # Step 3: Save image to local directory
        logger.info("Step 3: Saving image to local directory...")
        memes_dir = Path("coffee memes")
        memes_dir.mkdir(exist_ok=True)
        
        # Create timestamped filename: coffee_meme_YYYY-MM-DD_HH-MM-SS.jpg
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"coffee_meme_{timestamp}.jpg"
        filepath = memes_dir / filename
        
        # Save the processed image
        with open(filepath, 'wb') as f:
            f.write(processed_image)
        logger.info(f"Image saved to: {filepath}")
        
        # Step 4: Send image via email
        logger.info("Step 4: Sending image via email...")
        # Parse recipient emails (support comma-separated list)
        recipient_emails = [email.strip() for email in Config.RECIPIENT_EMAIL.split(',')] if Config.RECIPIENT_EMAIL else []
        success = email_service.send_image(processed_image, recipients=recipient_emails)
        
        if success:
            logger.info("=" * 60)
            logger.info("SUCCESS: Coffee meme sent successfully via email!")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Failed to send meme")
            return 1
            
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
