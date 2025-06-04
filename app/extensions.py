"""Initialize Flask extensions."""
from google.cloud import datastore
from google.cloud import storage


# Global instances
datastore_client = None
storage_client = None


def init_extensions(app):
    """Initialize all Flask extensions.
    
    Args:
        app: Flask application instance
    """
    global datastore_client, storage_client
    
    # Initialize Google Cloud Datastore client
    if app.config.get('DATASTORE_EMULATOR_HOST'):
        # Use emulator in development
        datastore_client = datastore.Client(project=app.config['PROJECT_ID'])
    else:
        # Use production Datastore
        datastore_client = datastore.Client()
    
    # Initialize Google Cloud Storage client
    storage_client = storage.Client(project=app.config['PROJECT_ID'])
    
    # Store clients in app context for easy access
    app.datastore_client = datastore_client
    app.storage_client = storage_client