"""Application entry point."""
import os
from app import create_app

# Get configuration name from environment variable
config_name = os.environ.get('FLASK_ENV', 'development')

# Create application instance
app = create_app(config_name)

if __name__ == '__main__':
    # Run the application
    app.run(
        host='127.0.0.1',
        port=8080,
        debug=app.config['DEBUG']
    )