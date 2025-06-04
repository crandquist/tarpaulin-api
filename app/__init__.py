"""Application factory for Tarpaulin API."""
from flask import Flask
from flask_cors import CORS

from config import config
from app.extensions import init_extensions
from app.errors.handlers import register_error_handlers


def create_app(config_name='default'):
    """Create and configure the Flask application.
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Flask application instance
    """
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    init_extensions(app)
    
    # Enable CORS
    CORS(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    register_blueprints(app)
    
    return app


def register_blueprints(app):
    """Register all blueprints with the application.
    
    Args:
        app: Flask application instance
    """
    # Import blueprints here to avoid circular imports
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import users_bp
    from app.routes.course_routes import courses_bp
    from app.routes.avatar_routes import avatar_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(avatar_bp)