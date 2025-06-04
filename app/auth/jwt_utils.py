"""JWT utilities for token validation and decoding."""
import json
from functools import wraps
from urllib.request import urlopen

from flask import current_app, request
from jose import jwt

from app.errors.exceptions import UnauthorizedError, ForbiddenError


class AuthError(Exception):
    """Authentication error exception."""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        

def get_token_auth_header():
    """Extract the Access Token from the Authorization Header.
    
    Returns: 
        str: The token part of the header
        
    Raises:
        UnauthorizedError: If no header is present or header is malformed
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise UnauthorizedError('Authorization header is expected.')
    
    parts = auth.split()
    
    if parts[0].lower() != 'bearer':
        raise UnauthorizedError('Authorization header must start with Bearer.')
    
    elif len(parts) == 1:
        raise UnauthorizedError('Token not found.')
    
    elif len(parts) > 2:
        raise UnauthorizedError('Authorization header must be Bearer token.')
    
    token = parts[1]
    return token


def verify_jwt(token):
    """Decode and verify the JWT using Auth0.
    
    Args:
        token: A json web token string
        
    Returns:
        dict: The decoded JWT payload
        
    Raises:
        UnauthorizedError: If the token is invalid
    """
    # Get public key from Auth0
    jsonurl = urlopen(f'https://{current_app.config["AUTH0_DOMAIN"]}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)
    
    # Choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise UnauthorizedError('Authorization malformed.')
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            
    if rsa_key:
        try:
            # Decode the JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=current_app.config['ALGORITHMS'],
                audience=current_app.config['AUTH0_AUDIENCE'],
                issuer=f'https://{current_app.config["AUTH0_DOMAIN"]}/'
            )
            return payload
        
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError('Token expired.')
        
        except jwt.JWTClaimsError:
            raise UnauthorizedError('Incorrect claims, please check the audience and issuer.')
        
        except Exception:
            raise UnauthorizedError('Unable to parse authentication token.')
        
    raise UnauthorizedError('Unable to find appropriate key.')

def requires_auth(f):
    """Decorator to require valid JWT for a route.
    
    Args:
        f: The function to decorate
        
    Returns:
        The decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = get_token_auth_header()
            payload = verify_jwt(token)
            request.jwt_payload = payload
            return f(*args, **kwargs)
        except UnauthorizedError:
            raise
        except Exception:
            raise UnauthorizedError('Authorization failed.')
        
    return decorated