import pytest
import json
from app.models import Note

class TestNotesAPI:
    """Test cases for Notes API endpoints"""

    def test_get_notes_empty(self, client, db_session):
        """Test getting notes when database is empty"""
        response = client.get('/api/notes')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'notes' in data
        assert data['notes'] == []

    def test_create_note_success(self, client, db_session):
        """Test successful note creation"""
        note_data = {
            'title': 'Test Note',
            'content': 'This is a test note content',
            'color': '#FFE57F'
        }

        response = client.post('/api/notes',
                             data=note_data,
                             content_type='multipart/form-data')

        assert response.status_code == 201

        data = json.loads(response.data)
        assert data['title'] == note_data['title']
        assert data['content'] == note_data['content']
        assert data['color'] == note_data['color']
        assert 'id' in data
        assert 'created_at' in data
        assert 'updated_at' in data
        assert data['image_urls'] == []

    def test_create_note_validation_error(self, client, db_session):
        """Test note creation with validation errors"""
        # Test missing title
        response = client.post('/api/notes',
                             data={'content': 'Content only'},
                             content_type='multipart/form-data')
        assert response.status_code == 400

        # Test missing content
        response = client.post('/api/notes',
                             data={'title': 'Title only'},
                             content_type='multipart/form-data')
        assert response.status_code == 400

        # Test title too long
        response = client.post('/api/notes',
                             data={
                                 'title': 'A' * 31,  # 31 characters
                                 'content': 'Valid content'
                             },
                             content_type='multipart/form-data')
        assert response.status_code == 400

    def test_get_notes_after_creation(self, client, db_session, sample_note_data):
        """Test getting notes after creating some"""
        # Create a note first
        response = client.post('/api/notes',
                             data=sample_note_data,
                             content_type='multipart/form-data')
        assert response.status_code == 201

        # Get all notes
        response = client.get('/api/notes')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data['notes']) == 1
        assert data['notes'][0]['title'] == sample_note_data['title']

    def test_get_single_note(self, client, db_session, sample_note_data):
        """Test getting a single note by ID"""
        # Create a note first
        create_response = client.post('/api/notes',
                                    data=sample_note_data,
                                    content_type='multipart/form-data')
        assert create_response.status_code == 201
        created_note = json.loads(create_response.data)

        # Get the specific note
        response = client.get(f'/api/notes/{created_note["id"]}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['id'] == created_note['id']
        assert data['title'] == sample_note_data['title']

    def test_get_single_note_not_found(self, client, db_session):
        """Test getting a non-existent note"""
        response = client.get('/api/notes/999')
        assert response.status_code == 404

        data = json.loads(response.data)
        assert 'error' in data

    def test_update_note_success(self, client, db_session, sample_note_data):
        """Test successful note update"""
        # Create a note first
        create_response = client.post('/api/notes',
                                    data=sample_note_data,
                                    content_type='multipart/form-data')
        assert create_response.status_code == 201
        created_note = json.loads(create_response.data)

        # Update the note
        update_data = {
            'title': 'Updated Title',
            'content': 'Updated content',
            'color': '#BAE1FF'
        }

        response = client.put(f'/api/notes/{created_note["id"]}',
                            data=update_data,
                            content_type='multipart/form-data')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['content'] == update_data['content']
        assert data['color'] == update_data['color']
        assert data['id'] == created_note['id']

    def test_update_note_partial(self, client, db_session, sample_note_data):
        """Test partial note update (only title)"""
        # Create a note first
        create_response = client.post('/api/notes',
                                    data=sample_note_data,
                                    content_type='multipart/form-data')
        assert create_response.status_code == 201
        created_note = json.loads(create_response.data)

        # Update only the title
        update_data = {'title': 'Partially Updated Title'}

        response = client.put(f'/api/notes/{created_note["id"]}',
                            data=update_data,
                            content_type='multipart/form-data')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['content'] == sample_note_data['content']  # Should remain unchanged
        assert data['color'] == sample_note_data['color']  # Should remain unchanged

    def test_update_note_not_found(self, client, db_session):
        """Test updating a non-existent note"""
        update_data = {'title': 'Updated Title'}

        response = client.put('/api/notes/999',
                            data=update_data,
                            content_type='multipart/form-data')

        assert response.status_code == 404

    def test_delete_note_success(self, client, db_session, sample_note_data):
        """Test successful note deletion"""
        # Create a note first
        create_response = client.post('/api/notes',
                                    data=sample_note_data,
                                    content_type='multipart/form-data')
        assert create_response.status_code == 201
        created_note = json.loads(create_response.data)

        # Delete the note
        response = client.delete(f'/api/notes/{created_note["id"]}')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['success'] is True

        # Verify note is deleted
        get_response = client.get(f'/api/notes/{created_note["id"]}')
        assert get_response.status_code == 404

    def test_delete_note_not_found(self, client, db_session):
        """Test deleting a non-existent note"""
        response = client.delete('/api/notes/999')
        assert response.status_code == 404

    def test_notes_ordered_by_creation_desc(self, client, db_session):
        """Test that notes are ordered by creation date (newest first)"""
        # Create notes with delays to ensure different timestamps
        import time

        note1_data = {'title': 'Note 1', 'content': 'Content 1', 'color': '#FFE57F'}
        note2_data = {'title': 'Note 2', 'content': 'Content 2', 'color': '#FFE57F'}
        note3_data = {'title': 'Note 3', 'content': 'Content 3', 'color': '#FFE57F'}

        # Create notes
        client.post('/api/notes', data=note1_data, content_type='multipart/form-data')
        time.sleep(0.01)  # Small delay
        client.post('/api/notes', data=note2_data, content_type='multipart/form-data')
        time.sleep(0.01)  # Small delay
        client.post('/api/notes', data=note3_data, content_type='multipart/form-data')

        # Get all notes
        response = client.get('/api/notes')
        assert response.status_code == 200

        data = json.loads(response.data)
        notes = data['notes']

        assert len(notes) == 3
        # Should be ordered newest first (Note 3, Note 2, Note 1)
        assert notes[0]['title'] == 'Note 3'
        assert notes[1]['title'] == 'Note 2'
        assert notes[2]['title'] == 'Note 1'

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'service' in data
