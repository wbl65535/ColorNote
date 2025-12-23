import os
import uuid
from typing import List, Optional
from datetime import datetime

class VercelBlobService:
    """Service for handling image uploads to Vercel Blob Storage"""

    def __init__(self):
        self.token = os.getenv('BLOB_READ_WRITE_TOKEN')
        if not self.token:
            raise ValueError("BLOB_READ_WRITE_TOKEN environment variable is required")

    def upload_image(self, file_data: bytes, filename: str, note_id: int) -> str:
        """
        Upload image to Vercel Blob and return the URL

        Args:
            file_data: Raw image file bytes
            filename: Original filename
            note_id: Associated note ID

        Returns:
            str: Public URL of uploaded image
        """
        try:
            # Import here to avoid import errors if not installed
            from vercel_blob import put

            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = self._get_file_extension(filename)
            unique_filename = f"notes/{note_id}/{timestamp}_{uuid.uuid4().hex[:8]}.{file_extension}"

            # Upload to Vercel Blob
            blob = put(unique_filename, file_data, {
                'access': 'public',
                'token': self.token
            })

            return blob.url

        except ImportError:
            raise ImportError("vercel-blob package is required for image uploads")
        except Exception as e:
            raise Exception(f"Failed to upload image: {str(e)}")

    def delete_image(self, image_url: str) -> bool:
        """
        Delete image from Vercel Blob

        Args:
            image_url: Full URL of image to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            # Import here to avoid import errors if not installed
            from vercel_blob import delete

            # Extract filename from URL
            # URL format: https://[project].vercel-storage.com/notes/[note_id]/[filename]
            filename = self._extract_filename_from_url(image_url)
            if not filename:
                return False

            # Delete from Vercel Blob
            delete(filename, {'token': self.token})
            return True

        except ImportError:
            raise ImportError("vercel-blob package is required for image deletion")
        except Exception as e:
            raise Exception(f"Failed to delete image: {str(e)}")

    def validate_image_file(self, file_data: bytes, filename: str) -> tuple[bool, str]:
        """
        Validate image file before upload

        Args:
            file_data: Raw file bytes
            filename: Original filename

        Returns:
            tuple: (is_valid, error_message)
        """
        # Check file size (5MB limit)
        max_size = 5 * 1024 * 1024  # 5MB
        if len(file_data) > max_size:
            return False, "图片大小不能超过 5MB"

        # Check file extension
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        file_extension = self._get_file_extension(filename).lower()

        if file_extension not in allowed_extensions:
            return False, f"不支持的文件格式。允许的格式: {', '.join(allowed_extensions)}"

        # Basic file header validation
        if not self._is_valid_image_header(file_data):
            return False, "文件不是有效的图片格式"

        return True, ""

    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        if '.' not in filename:
            return ''
        return filename.rsplit('.', 1)[1].lower()

    def _extract_filename_from_url(self, url: str) -> Optional[str]:
        """Extract filename from Vercel Blob URL"""
        try:
            # URL format: https://[project].vercel-storage.com/notes/[note_id]/[filename]
            parts = url.split('/')
            if len(parts) >= 4 and 'vercel-storage.com' in url:
                # Find the index of 'notes' and take everything after it
                notes_index = -1
                for i, part in enumerate(parts):
                    if part == 'notes':
                        notes_index = i
                        break

                if notes_index >= 0:
                    return '/'.join(parts[notes_index:])
        except:
            pass
        return None

    def _is_valid_image_header(self, file_data: bytes) -> bool:
        """Check if file has valid image header"""
        if len(file_data) < 4:
            return False

        # Check common image file signatures
        headers = {
            b'\xff\xd8\xff': 'jpg',      # JPEG
            b'\x89PNG\r\n\x1a\n': 'png', # PNG
            b'GIF87a': 'gif',             # GIF87a
            b'GIF89a': 'gif',             # GIF89a
            b'RIFF': 'webp'               # WebP (starts with RIFF)
        }

        file_start = file_data[:8]  # Check first 8 bytes

        for header, _ in headers.items():
            if file_start.startswith(header):
                return True

        return False

# Global service instance
blob_service = VercelBlobService()

def upload_note_images(images: List[bytes], filenames: List[str], note_id: int) -> List[str]:
    """
    Upload multiple images for a note

    Args:
        images: List of image file bytes
        filenames: List of original filenames
        note_id: Note ID to associate images with

    Returns:
        List[str]: List of uploaded image URLs
    """
    uploaded_urls = []

    for image_data, filename in zip(images, filenames):
        # Validate image
        is_valid, error = blob_service.validate_image_file(image_data, filename)
        if not is_valid:
            raise ValueError(f"Image validation failed for {filename}: {error}")

        # Upload image
        url = blob_service.upload_image(image_data, filename, note_id)
        uploaded_urls.append(url)

    return uploaded_urls

def delete_note_images(image_urls: List[str]) -> bool:
    """
    Delete all images associated with a note

    Args:
        image_urls: List of image URLs to delete

    Returns:
        bool: True if all deletions successful
    """
    success = True

    for url in image_urls:
        try:
            blob_service.delete_image(url)
        except Exception as e:
            print(f"Failed to delete image {url}: {e}")
            success = False

    return success
