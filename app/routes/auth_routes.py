"""Authentication routes."""
from flask import Blueprint, request, jsonify

from app.auth.auth0_service import login_user
from app.errors.exceptions import BadRequestError, UnauthorizedError

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/users/login', methods=['POST'])
def login():
    """User login endpoint.
    
    Authenticates user with Auth0 and returns JWT token.
    
    Returns:
        JSON response with token or error message
        
    Status Codes:
        200: Success
        400: Invalid request body
        401: Invalid credentials
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            raise BadRequestError('Request body is required')
        
        # Extract credentials
        username = data.get('username')
        password = data.get('password')
        
        # Validate required fields
        if not username or not password:
            raise BadRequestError('Username and password are required')
        
        # Authenticate with Auth0
        result = login_user(username, password)
        
        return jsonify(result), 200
        
    except BadRequestError:
        return jsonify({"Error": "The request body is invalid"}), 400
    except UnauthorizedError:
        return jsonify({"Error": "Unauthorized"}), 401
    except Exception:
        return jsonify({"Error": "The request body is invalid"}), 400