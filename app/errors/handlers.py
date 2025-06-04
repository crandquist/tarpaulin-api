"""Error handlers for the application."""
from flask import jsonify
from app.errors.exceptions import (
    BadRequestError, UnauthorizedError, ForbiddenError, 
    NotFoundError, ConflictError
)


def register_error_handlers(app):
    """Register error handlers with the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(BadRequestError)
    def handle_bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({"Error": "The request body is invalid"}), 400
    
    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return jsonify({"Error": "Unauthorized"}), 401
    
    @app.errorhandler(ForbiddenError)
    def handle_forbidden(error):
        """Handle 403 Forbidden errors."""
        return jsonify({"Error": "You don't have permission on this resource"}), 403
    
    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({"Error": "Not found"}), 404
    
    @app.errorhandler(ConflictError)
    def handle_conflict(error):
        """Handle 409 Conflict errors."""
        return jsonify({"Error": str(error)}), 409
    
    @app.errorhandler(400)
    def handle_400(error):
        """Handle generic 400 errors."""
        return jsonify({"Error": "The request body is invalid"}), 400
    
    @app.errorhandler(401)
    def handle_401(error):
        """Handle generic 401 errors."""
        return jsonify({"Error": "Unauthorized"}), 401
    
    @app.errorhandler(403)
    def handle_403(error):
        """Handle generic 403 errors."""
        return jsonify({"Error": "You don't have permission on this resource"}), 403
    
    @app.errorhandler(404)
    def handle_404(error):
        """Handle generic 404 errors."""
        return jsonify({"Error": "Not found"}), 404
    
    @app.errorhandler(500)
    def handle_500(error):
        """Handle generic 500 errors."""
        return jsonify({"Error": "Internal server error"}), 500