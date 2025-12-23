from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, Note

class NoteRepository:
    """Data access layer for Note entities"""

    @staticmethod
    def get_all() -> List[Note]:
        """Get all notes ordered by creation date (newest first)"""
        try:
            return Note.query.order_by(Note.created_at.desc()).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve notes: {str(e)}")

    @staticmethod
    def get_by_id(note_id: int) -> Optional[Note]:
        """Get a note by its ID"""
        try:
            return Note.query.get(note_id)
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve note {note_id}: {str(e)}")

    @staticmethod
    def create(title: str, content: str, color: str = '#FFE57F', image_urls: List[str] = None) -> Note:
        """Create a new note"""
        try:
            # Create new note instance
            note = Note(
                title=title,
                content=content,
                color=color,
                image_urls=image_urls or []
            )

            # Validate the note
            is_valid, errors = note.validate()
            if not is_valid:
                raise ValueError(f"Validation failed: {', '.join(errors)}")

            # Save to database
            db.session.add(note)
            db.session.commit()

            return note

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to create note: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def update(note_id: int, title: str = None, content: str = None, color: str = None, image_urls: List[str] = None) -> Optional[Note]:
        """Update an existing note"""
        try:
            note = Note.query.get(note_id)
            if not note:
                return None

            # Update fields if provided
            if title is not None:
                note.title = title
            if content is not None:
                note.content = content
            if color is not None:
                note.color = color
            if image_urls is not None:
                note.image_urls = image_urls

            # Validate the updated note
            is_valid, errors = note.validate()
            if not is_valid:
                raise ValueError(f"Validation failed: {', '.join(errors)}")

            # Save changes
            db.session.commit()

            return note

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to update note {note_id}: {str(e)}")
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete(note_id: int) -> bool:
        """Delete a note by its ID"""
        try:
            note = Note.query.get(note_id)
            if not note:
                return False

            db.session.delete(note)
            db.session.commit()

            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to delete note {note_id}: {str(e)}")

    @staticmethod
    def exists(note_id: int) -> bool:
        """Check if a note exists"""
        try:
            return Note.query.get(note_id) is not None
        except SQLAlchemyError:
            return False

    @staticmethod
    def count() -> int:
        """Get total count of notes"""
        try:
            return Note.query.count()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to count notes: {str(e)}")

    @staticmethod
    def get_recent(limit: int = 10) -> List[Note]:
        """Get most recent notes"""
        try:
            return Note.query.order_by(Note.created_at.desc()).limit(limit).all()
        except SQLAlchemyError as e:
            raise Exception(f"Failed to retrieve recent notes: {str(e)}")
