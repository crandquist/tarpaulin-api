"""Authentication decorators for role-based access control."""
from functools import wraps
from flask import request, current_app

from app.auth.jwt_utils import requires_auth
from app.errors.exceptions import ForbiddenError
from app.models.user import User


def requires_role(*allowed_roles):
    """Decorator to require specific user role(s).
    
    Args:
        *allowed_roles: Variable number of allowed roles
        
    Returns:
        The decorated function
    """
    def decorator(f):
        @wraps(f)
        @requires_auth
        def decorated_function(*args, **kwargs):
            # Get user from JWT payload
            payload = request.jwt_payload
            sub = payload.get('sub')
            
            # Get user from datastore
            user = User.get_by_sub(sub)
            
            if not user:
                raise ForbiddenError('User not found')
            
            # Check if user has required role
            if user.role not in allowed_roles:
                raise ForbiddenError('Insufficient permissions')
            
            # Add user to request context
            request.current_user = user
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def requires_admin(f):
    """Decorator to require admin role.
    
    Args:
        f: The function to decorate
        
    Returns:
        The decorated function
    """
    return requires_role('admin')(f)


def requires_instructor(f):
    """Decorator to require instructor role.
    
    Args:
        f: The function to decorate
        
    Returns:
        The decorated function
    """
    return requires_role('instructor', 'admin')(f)


def requires_self_or_admin(user_id_param='user_id'):
    """Decorator to require that user is accessing their own resource or is admin.
    
    Args:
        user_id_param: Name of the URL parameter containing user ID
        
    Returns:
        The decorator function
    """
    def decorator(f):
        @wraps(f)
        @requires_auth
        def decorated_function(*args, **kwargs):
            # Get user from JWT payload
            payload = request.jwt_payload
            sub = payload.get('sub')
            
            # Get user from datastore
            user = User.get_by_sub(sub)
            
            if not user:
                raise ForbiddenError('User not found')
            
            # Get user_id from URL parameters
            user_id = kwargs.get(user_id_param)
            
            # Check if user is accessing their own resource or is admin
            if str(user.id) != str(user_id) and user.role != 'admin':
                raise ForbiddenError('Access denied')
            
            # Add user to request context
            request.current_user = user
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator