import pytest
import os
from app import create_app
from app.models import db
from app.config import get_config

@pytest.fixture(scope='session')
def app():
    """Create and configure a test app instance."""
    # Use testing configuration
    test_app = create_app('testing')

    # Create database tables
    with test_app.app_context():
        db.create_all()

    yield test_app

    # Clean up after tests
    with test_app.app_context():
        db.drop_all()

@pytest.fixture(scope='session')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def db_session(app):
    """Create a fresh database session for each test."""
    with app.app_context():
        # Start a transaction
        connection = db.engine.connect()
        transaction = connection.begin()

        # Override the session's connection with the transaction
        db.session = db.create_scoped_session(
            options={"bind": connection, "binds": {}}
        )

        yield db.session

        # Rollback the transaction and close the connection
        transaction.rollback()
        connection.close()
        db.session.remove()

@pytest.fixture
def sample_note_data():
    """Sample note data for testing."""
    return {
        'title': '测试笔记',
        'content': '这是一个测试笔记的内容',
        'color': '#FFE57F'
    }

@pytest.fixture
def sample_note_with_images():
    """Sample note data with images."""
    return {
        'title': '图片笔记',
        'content': '包含图片的笔记',
        'color': '#BAE1FF',
        'image_urls': [
            'https://example.com/image1.jpg',
            'https://example.com/image2.jpg'
        ]
    }

@pytest.fixture
def mock_blob_service(mocker):
    """Mock Vercel Blob service for testing."""
    mock_service = mocker.patch('app.services.blob_service')

    # Mock upload method to return a fake URL
    mock_service.upload_image.return_value = 'https://test.vercel-storage.com/test-image.jpg'

    # Mock delete method
    mock_service.delete_image.return_value = True

    # Mock validation method
    mock_service.validate_image_file.return_value = (True, "")

    return mock_service

@pytest.fixture
def test_image_data():
    """Create fake image data for testing."""
    # Create a minimal valid PNG header + some data
    png_header = b'\x89PNG\r\n\x1a\n'  # PNG signature
    # Add minimal PNG data structure
    png_data = png_header + b'\x00\x00\x00\rIHDR' + b'A' * 100  # Fake PNG data
    return png_data

@pytest.fixture
def test_image_file(test_image_data, tmp_path):
    """Create a temporary image file for testing."""
    image_file = tmp_path / "test_image.png"
    image_file.write_bytes(test_image_data)
    return image_file

# Playwright fixtures for E2E tests
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, app):
    """Configure browser context for E2E tests."""
    # Get the app's test server URL
    server_url = "http://localhost:3000"  # This should match vercel dev port

    return {
        **browser_context_args,
        "base_url": server_url,
        "viewport": {"width": 375, "height": 667},  # iPhone SE viewport
    }

@pytest.fixture(autouse=True)
def run_around_tests(app):
    """Setup and teardown for each test."""
    with app.app_context():
        # Setup: Create tables
        db.create_all()

        yield

        # Teardown: Clean up data (but keep tables for next test)
        try:
            # Clear all data from tables
            db.session.execute(db.text("DELETE FROM notes"))
            db.session.commit()
        except Exception as e:
            print(f"Warning: Failed to clean up test data: {e}")
            db.session.rollback()

# Environment setup for tests
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )

# Mock environment variables if not set
@pytest.fixture(autouse=True, scope='session')
def mock_env_vars():
    """Mock required environment variables for tests."""
    env_vars = {
        'SECRET_KEY': 'test-secret-key',
        'DB_HOST': 'localhost',
        'DB_PORT': '3306',
        'DB_USERNAME': 'test_user',
        'DB_PASSWORD': 'test_password',
        'DB_DATABASE': 'colornote_test',
        'DB_TEST_DATABASE': 'colornote_test',
        'BLOB_READ_WRITE_TOKEN': 'test-blob-token'
    }

    # Set defaults if not already set
    for key, value in env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
