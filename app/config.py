import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""

    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # Database configuration
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = int(os.getenv('DB_PORT', 4000))
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE = os.getenv('DB_DATABASE')
    DB_TEST_DATABASE = os.getenv('DB_TEST_DATABASE')

    # Database connection pool settings
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', 5))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', 10))
    DB_POOL_RECYCLE = int(os.getenv('DB_POOL_RECYCLE', 300))
    DB_CONNECT_TIMEOUT = int(os.getenv('DB_CONNECT_TIMEOUT', 10))

    # Vercel Blob configuration
    BLOB_READ_WRITE_TOKEN = os.getenv('BLOB_READ_WRITE_TOKEN')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """Generate database URI from environment variables"""
        if not all([self.DB_HOST, self.DB_USERNAME, self.DB_PASSWORD, self.DB_DATABASE]):
            raise ValueError("Database configuration incomplete. Please check environment variables.")

        return f'mysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}'

    @property
    def SQLALCHEMY_TEST_DATABASE_URI(self):
        """Generate test database URI"""
        if not all([self.DB_HOST, self.DB_USERNAME, self.DB_PASSWORD, self.DB_TEST_DATABASE]):
            raise ValueError("Test database configuration incomplete. Please check environment variables.")

        return f'mysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_TEST_DATABASE}'

    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': DB_POOL_SIZE,
        'max_overflow': DB_MAX_OVERFLOW,
        'pool_recycle': DB_POOL_RECYCLE,
        'connect_args': {
            'connect_timeout': DB_CONNECT_TIMEOUT,
        }
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        """Use test database for testing"""
        return self.SQLALCHEMY_TEST_DATABASE_URI


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}


def get_config(config_name=None):
    """Get configuration class based on environment"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    return config.get(config_name, config['default'])
