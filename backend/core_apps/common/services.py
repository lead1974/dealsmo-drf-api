import os
import uuid
import shutil
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone

class MediaService:
    @staticmethod
    def save_image(image_file, article_id, is_featured=False):
        """
        Save image file and return its URL
        """
        # Generate unique filename
        ext = os.path.splitext(image_file.name)[1]
        filename = f"{uuid.uuid4()}{ext}"
        
        # Create path with article UUID for organization
        path = f"articles/{article_id}/{filename}"
        
        # Save file
        saved_path = default_storage.save(path, ContentFile(image_file.read()))
        
        # Generate URL
        url = f"{settings.MEDIA_URL}{saved_path}"
        
        return url

    @staticmethod
    def delete_image(url):
        """
        Delete image file from storage
        """
        if url.startswith(settings.MEDIA_URL):
            path = url.replace(settings.MEDIA_URL, '')
            if default_storage.exists(path):
                default_storage.delete(path)
    
    @staticmethod
    def delete_article_images(article_id):
        """
        Delete all images for an article
        """
        article_path = f"articles/{article_id}"
        if default_storage.exists(article_path):
            # List all files in the directory
            _, filenames = default_storage.listdir(article_path)
            
            # Delete each file
            for filename in filenames:
                file_path = f"{article_path}/{filename}"
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
            
            # Try to remove the directory (if empty)
            try:
                default_storage.delete(article_path)
            except:
                pass  # Directory might not be empty or might not be deletable 