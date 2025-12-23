from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.repositories import NoteRepository
from app.services import upload_note_images, delete_note_images
import traceback

api_bp = Blueprint('api', __name__)

# Color options for notes
AVAILABLE_COLORS = [
    {'value': '#FFE57F', 'name': 'Yellow'},
    {'value': '#FFB3BA', 'name': 'Pink'},
    {'value': '#BAE1FF', 'name': 'Blue'},
    {'value': '#BAFFC9', 'name': 'Green'},
    {'value': '#E0BBE4', 'name': 'Purple'},
    {'value': '#FFDAC1', 'name': 'Orange'}
]

@api_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes ordered by creation date (newest first)"""
    try:
        notes = NoteRepository.get_all()
        notes_data = [note.to_dict() for note in notes]
        return jsonify({'notes': notes_data})
    except Exception as e:
        print(f"Error getting notes: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to retrieve notes'}), 500

@api_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note with optional image uploads"""
    try:
        # Handle form data
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        color = request.form.get('color', '#FFE57F')

        # Validate required fields
        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400

        # Validate color
        if color not in [c['value'] for c in AVAILABLE_COLORS]:
            color = '#FFE57F'  # Default to yellow

        # Handle image uploads
        image_urls = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            if len(files) > 3:
                return jsonify({'error': 'Maximum 3 images allowed per note'}), 400

            # Filter out empty files and process uploads
            valid_files = []
            filenames = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    valid_files.append(file.read())
                    filenames.append(filename)

            # Upload images if any valid files
            if valid_files:
                try:
                    image_urls = upload_note_images(valid_files, filenames, 0)  # note_id will be set after creation
                except Exception as e:
                    print(f"Image upload failed: {e}")
                    return jsonify({'error': 'Failed to upload images'}), 500

        # Create the note
        note = NoteRepository.create(
            title=title,
            content=content,
            color=color,
            image_urls=image_urls
        )

        # If we uploaded images with temporary note_id=0, we need to update the URLs
        # For simplicity in this implementation, we'll handle this in the service layer
        # In a real app, you might want to create the note first, then upload images

        return jsonify(note.to_dict()), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error creating note: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to create note'}), 500

@api_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a single note by ID"""
    try:
        note = NoteRepository.get_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        return jsonify(note.to_dict())
    except Exception as e:
        print(f"Error getting note {note_id}: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to retrieve note'}), 500

@api_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update an existing note with optional image management"""
    try:
        # Check if note exists
        existing_note = NoteRepository.get_by_id(note_id)
        if not existing_note:
            return jsonify({'error': 'Note not found'}), 404

        # Handle form data
        title = request.form.get('title')
        content = request.form.get('content')
        color = request.form.get('color')
        deleted_image_urls = request.form.getlist('deleted_image_urls')

        # Prepare update data (only include provided fields)
        update_data = {}
        if title is not None:
            update_data['title'] = title.strip()
        if content is not None:
            update_data['content'] = content.strip()
        if color is not None:
            # Validate color
            if color not in [c['value'] for c in AVAILABLE_COLORS]:
                return jsonify({'error': 'Invalid color'}), 400
            update_data['color'] = color

        # Handle image deletions
        current_image_urls = existing_note.image_urls.copy() if existing_note.image_urls else []

        if deleted_image_urls:
            # Remove deleted images from current list
            current_image_urls = [url for url in current_image_urls if url not in deleted_image_urls]

            # Delete images from storage
            try:
                delete_note_images(deleted_image_urls)
            except Exception as e:
                print(f"Failed to delete images: {e}")
                # Continue with update even if image deletion fails

        # Handle new image uploads
        if 'images' in request.files:
            files = request.files.getlist('images')
            max_new_images = 3 - len(current_image_urls)

            if len(files) > max_new_images:
                return jsonify({'error': f'Too many images. Can add maximum {max_new_images} more images'}), 400

            # Process new uploads
            valid_files = []
            filenames = []
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    valid_files.append(file.read())
                    filenames.append(filename)

            if valid_files:
                try:
                    new_image_urls = upload_note_images(valid_files, filenames, note_id)
                    current_image_urls.extend(new_image_urls)
                except Exception as e:
                    print(f"Image upload failed: {e}")
                    return jsonify({'error': 'Failed to upload new images'}), 500

        update_data['image_urls'] = current_image_urls

        # Update the note
        updated_note = NoteRepository.update(note_id, **update_data)
        if not updated_note:
            return jsonify({'error': 'Note not found'}), 404

        return jsonify(updated_note.to_dict())

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error updating note {note_id}: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to update note'}), 500

@api_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note and its associated images"""
    try:
        # Check if note exists and get image URLs
        note = NoteRepository.get_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        # Delete associated images
        if note.image_urls:
            try:
                delete_note_images(note.image_urls)
            except Exception as e:
                print(f"Failed to delete images for note {note_id}: {e}")
                # Continue with note deletion even if image deletion fails

        # Delete the note
        success = NoteRepository.delete(note_id)
        if not success:
            return jsonify({'error': 'Failed to delete note'}), 500

        return jsonify({'success': True})

    except Exception as e:
        print(f"Error deleting note {note_id}: {e}")
        traceback.print_exc()
        return jsonify({'error': 'Failed to delete note'}), 500

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ColorNote API'
    })
