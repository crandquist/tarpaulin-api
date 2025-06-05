# tests/conftest.py

import pytest
from app import create_app

@pytest.fixture
def app():
    """
    Return a Flask app instance configured for testing.
    """
    # Pass the config-name string "testing" so create_app can do:
    # app.config.from_object(config["testing"])
    app = create_app("testing")
    yield app

@pytest.fixture
def client(app):
    """
    A test client for the Flask application.
    """
    return app.test_client()
