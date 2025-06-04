"""Auth0 integration for user authentication."""
import requests
from flask import current_app

from app.errors.exceptions import UnauthorizedError, BadRequestError



def login_user(username, password):
    """Authenticate user with Auth0 and get JWT token.
    
    Args:
        username: User's email/username
        password: User's password
        
    Returns:
        dict: Contains the JWT token
        
    Raises:
        BadRequestError: If username or password is missing
        UnauthorizedError: If credentials are invalid
    """
    if not username or not password:
        raise BadRequestError('Username and password are required.')

    # Auth0 token endpoint
    url = f'https://{current_app.config["AUTH0_DOMAIN"]}/oauth/token'
    
    # Request body for password grant
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': current_app.config['AUTH0_CLIENT_ID'],
        'client_secret': current_app.config['AUTH0_CLIENT_SECRET'],
        'audience': current_app.config['AUTH0_AUDIENCE'],
        'scope': 'openid profile email'
    }
    
    # Make request to Auth0
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return {
            'token': result['access_token']
        }
    elif response.status_code == 403 or response.status_code == 401:
        raise UnauthorizedError('Invalid username or password')
    else:
        raise UnauthorizedError('Authentication failed')
