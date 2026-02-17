"""Image hosting service for making images publicly accessible for Twilio MMS."""
import logging
import base64
import requests
from config import Config

logger = logging.getLogger(__name__)


class ImageHostingService:
    """Service for uploading images to a hosting service for public access."""
    
    @staticmethod
    def upload_to_imgbb(image_bytes: bytes, api_key: str = None) -> str:
        """
        Upload image to ImgBB and return the public URL.
        
        ImgBB offers free image hosting with an optional API key for higher limits.
        Works without API key for basic usage.
        
        Args:
            image_bytes: Image data as bytes
            api_key: ImgBB API key (optional, but recommended for higher rate limits)
                    Get one at: https://api.imgbb.com/ (free, no registration issues)
            
        Returns:
            str: Public URL of the uploaded image
        """
        try:
            logger.info("Uploading image to ImgBB...")
            
            # Encode image to base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Prepare data
            data = {'image': image_b64}
            
            # Add API key if provided (for higher rate limits)
            api_key = api_key or Config.IMGBB_API_KEY
            if api_key:
                data['key'] = api_key
                logger.debug("Using ImgBB API key for higher rate limits")
            else:
                logger.info("Using ImgBB without API key (basic mode)")
            
            # Upload to ImgBB
            response = requests.post(
                'https://api.imgbb.com/1/upload',
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get('success'):
                image_url = result['data']['url']
                logger.info(f"Image uploaded successfully to ImgBB: {image_url}")
                return image_url
            else:
                error_msg = result.get('error', {}).get('message', 'Unknown error')
                raise Exception(f"ImgBB API error: {error_msg}")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_data = e.response.json() if e.response.content else {}
                error_msg = error_data.get('error', {}).get('message', 'Bad request')
                logger.error(f"ImgBB API returned 400 Bad Request: {error_msg}")
            elif e.response.status_code == 429:
                logger.error("ImgBB API rate limit exceeded. Consider getting a free API key at https://api.imgbb.com/")
            logger.error(f"HTTP error uploading to ImgBB: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error uploading to ImgBB: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error uploading image to ImgBB: {e}")
            raise
    
    @staticmethod
    def upload_to_imgur(image_bytes: bytes, client_id: str = None) -> str:
        """
        Upload image to Imgur and return the public URL.
        
        Note: Imgur's API requires a Client ID for authentication.
        Get one at: https://api.imgur.com/oauth2/addclient
        
        Args:
            image_bytes: Image data as bytes
            client_id: Imgur client ID (required)
                      Get one at: https://api.imgur.com/oauth2/addclient
            
        Returns:
            str: Public URL of the uploaded image
            
        Raises:
            ValueError: If no Client ID is provided
        """
        # Check for Client ID
        actual_client_id = client_id or Config.IMGUR_CLIENT_ID
        if not actual_client_id:
            error_msg = (
                "Imgur Client ID is required for image hosting. "
                "Twilio MMS requires images to be hosted at a publicly accessible URL. "
                "Please set IMGUR_CLIENT_ID in your .env file. "
                "Get a free Client ID at: https://api.imgur.com/oauth2/addclient"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info("Uploading image to Imgur...")
            
            # Encode image to base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Prepare headers with Client ID
            headers = {'Authorization': f'Client-ID {actual_client_id}'}
            
            # Upload to Imgur
            response = requests.post(
                'https://api.imgur.com/3/image',
                headers=headers,
                data={'image': image_b64}
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('success'):
                image_url = data['data']['link']
                logger.info(f"Image uploaded successfully: {image_url}")
                return image_url
            else:
                error_msg = data.get('data', {}).get('error', 'Unknown error')
                raise Exception(f"Imgur API error: {error_msg}")
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                logger.error("Imgur API returned 403 Forbidden. Check that your Client ID is correct.")
            elif e.response.status_code == 401:
                logger.error("Imgur API returned 401 Unauthorized. Check that your Client ID is valid.")
            logger.error(f"HTTP error uploading to Imgur: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error uploading to Imgur: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error uploading image: {e}")
            raise
    
    @staticmethod
    def upload_to_imgur_anonymous(image_bytes: bytes) -> str:
        """
        Upload image to Imgur using the Client ID from config.
        
        Note: This still requires a Client ID (from Config.IMGUR_CLIENT_ID).
        Imgur's API does not support truly anonymous uploads.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            str: Public URL of the uploaded image
        """
        return ImageHostingService.upload_to_imgur(image_bytes, client_id=None)
    
    @staticmethod
    def upload_image(image_bytes: bytes) -> str:
        """
        Upload image using the configured hosting service.
        
        Tries ImgBB first (default, no registration issues), falls back to Imgur if configured.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            str: Public URL of the uploaded image
        """
        # Try ImgBB first (works without API key, no registration issues)
        try:
            return ImageHostingService.upload_to_imgbb(image_bytes)
        except Exception as e:
            logger.warning(f"ImgBB upload failed: {e}")
            
            # Fallback to Imgur if configured
            if Config.IMGUR_CLIENT_ID:
                logger.info("Falling back to Imgur...")
                try:
                    return ImageHostingService.upload_to_imgur(image_bytes)
                except Exception as imgur_error:
                    logger.error(f"Imgur upload also failed: {imgur_error}")
                    raise Exception(
                        f"Both image hosting services failed. ImgBB error: {e}. "
                        f"Imgur error: {imgur_error}. Please check your configuration."
                    )
            else:
                raise Exception(
                    f"ImgBB upload failed and no Imgur Client ID configured. "
                    f"Error: {e}. Consider getting a free ImgBB API key at https://api.imgbb.com/"
                )