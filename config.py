"""Configuration management for Tarpaulin API."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Google Cloud settings
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')
    STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET')
    
    # Auth0 settings
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
    ALGORITHMS = ['RS256']
    
    # Pagination settings
    DEFAULT_PAGE_SIZE = 3
    
    # API settings
    API_TITLE = 'Tarpaulin API'
    API_VERSION = '1.0'


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATASTORE_EMULATOR_HOST = os.environ.get('DATASTORE_EMULATOR_HOST')


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATASTORE_EMULATOR_HOST = 'localhost:8081'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}