"""User model for Datastore operations."""
from app.models.base import BaseModel


class User(BaseModel):
    """User model representing Tarpaulin users."""
    
    KIND = 'users'
    
    def __init__(self, **kwargs):
        """Initialize user with given attributes."""
        super().__init__(**kwargs)
        self.sub = kwargs.get('sub')
        self.role = kwargs.get('role')
        self.avatar_filename = kwargs.get('avatar_filename')
    
    @classmethod
    def get_by_sub(cls, sub):
        """Get user by Auth0 sub claim.
        
        Args:
            sub: Auth0 subject identifier
            
        Returns:
            User instance or None
        """
        client = cls.get_client()
        query = client.query(kind=cls.KIND)
        query.add_filter('sub', '=', sub)
        
        results = list(query.fetch(limit=1))
        if results:
            return cls.from_entity(results[0])
        return None
    
    @classmethod
    def get_all(cls):
        """Get all users.
        
        Returns:
            List of User instances
        """
        client = cls.get_client()
        query = client.query(kind=cls.KIND)
        
        users = []
        for entity in query.fetch():
            users.append(cls.from_entity(entity))
        
        return users
    
    def get_avatar_url(self, base_url):
        """Get avatar URL if user has avatar.
        
        Args:
            base_url: Base URL of the API
            
        Returns:
            str: Avatar URL or None
        """
        if self.avatar_filename:
            return f"{base_url}/users/{self.id}/avatar"
        return None
    
    def to_dict(self, include_avatar_url=False, base_url=None):
        """Convert user to dictionary.
        
        Args:
            include_avatar_url: Whether to include avatar URL
            base_url: Base URL for avatar URL
            
        Returns:
            dict: User data
        """
        data = {
            'id': self.id,
            'sub': self.sub,
            'role': self.role
        }
        
        if include_avatar_url and self.avatar_filename and base_url:
            data['avatar_url'] = self.get_avatar_url(base_url)
        
        return data