from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class Note(db.Model):
    """Note model representing user notes in the ColorNote application"""

    __tablename__ = 'notes'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Note content fields
    title = Column(String(30), nullable=False)
    content = Column(Text, nullable=False)
    color = Column(String(7), nullable=False, default='#FFE57F')

    # Image storage (URLs stored as JSON array)
    image_urls = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        """String representation of the Note object"""
        return f'<Note {self.id}: {self.title}>'

    def to_dict(self):
        """Convert Note object to dictionary for API responses"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'color': self.color,
            'image_urls': self.image_urls or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def validate_title(title):
        """Validate title field"""
        if not title or not isinstance(title, str):
            return False, "Title is required and must be a string"

        title = title.strip()
        if len(title) == 0:
            return False, "Title cannot be empty"

        if len(title) > 30:
            return False, "Title cannot exceed 30 characters"

        return True, title

    @staticmethod
    def validate_content(content):
        """Validate content field"""
        if not content or not isinstance(content, str):
            return False, "Content is required and must be a string"

        content = content.strip()
        if len(content) == 0:
            return False, "Content cannot be empty"

        if len(content) > 500:
            return False, "Content cannot exceed 500 characters"

        return True, content

    @staticmethod
    def validate_color(color):
        """Validate color field (HEX format)"""
        if not color or not isinstance(color, str):
            return False, "Color is required and must be a string"

        import re
        if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
            return False, "Color must be in HEX format (#RRGGBB)"

        return True, color

    @staticmethod
    def validate_image_urls(image_urls):
        """Validate image_urls field"""
        if image_urls is None:
            return True, []

        if not isinstance(image_urls, list):
            return False, "Image URLs must be a list"

        if len(image_urls) > 3:
            return False, "Cannot have more than 3 images per note"

        # Validate each URL format
        import re
        url_pattern = re.compile(r'^https://[^\s/$.?#].[^\s]*$')

        for url in image_urls:
            if not isinstance(url, str):
                return False, "All image URLs must be strings"
            if not url_pattern.match(url):
                return False, "Invalid URL format for image"

        return True, image_urls

    def validate(self):
        """Validate the entire Note object"""
        errors = []

        # Validate title
        title_valid, title_result = self.validate_title(self.title)
        if not title_valid:
            errors.append(f"Title: {title_result}")
        else:
            self.title = title_result

        # Validate content
        content_valid, content_result = self.validate_content(self.content)
        if not content_valid:
            errors.append(f"Content: {content_result}")
        else:
            self.content = content_result

        # Validate color
        color_valid, color_result = self.validate_color(self.color)
        if not color_valid:
            errors.append(f"Color: {color_result}")
        else:
            self.color = color_result

        # Validate image URLs
        images_valid, images_result = self.validate_image_urls(self.image_urls)
        if not images_valid:
            errors.append(f"Images: {images_result}")
        else:
            self.image_urls = images_result

        return len(errors) == 0, errors
