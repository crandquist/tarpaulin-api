"""Base model class for Datastore entities."""
from flask import current_app
from google.cloud import datastore


class BaseModel:
    """Base class for all Datastore models."""
    
    # Override in subclasses
    KIND = None
    
    def __init__(self, **kwargs):
        """Initialize model with given attributes."""
        self.id = kwargs.get('id')
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def get_client(cls):
        """Get Datastore client from app context."""
        return current_app.datastore_client
    
    @classmethod
    def get_by_id(cls, entity_id):
        """Get entity by ID.
        
        Args:
            entity_id: The entity ID
            
        Returns:
            Model instance or None
        """
        client = cls.get_client()
        key = client.key(cls.KIND, int(entity_id))
        entity = client.get(key)
        
        if entity:
            return cls.from_entity(entity)
        return None
    
    @classmethod
    def from_entity(cls, entity):
        """Create model instance from Datastore entity.
        
        Args:
            entity: Datastore entity
            
        Returns:
            Model instance
        """
        data = dict(entity)
        data['id'] = entity.key.id
        return cls(**data)
    
    def to_dict(self):
        """Convert model to dictionary.
        
        Returns:
            dict: Model data
        """
        data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and value is not None:
                data[key] = value
        return data
    
    def save(self):
        """Save model to Datastore."""
        client = self.get_client()
        
        if self.id:
            # Update existing entity
            key = client.key(self.KIND, self.id)
        else:
            # Create new entity
            key = client.key(self.KIND)
        
        entity = datastore.Entity(key=key)
        
        # Copy attributes to entity
        for key, value in self.to_dict().items():
            if key != 'id':  # Don't store id as property
                entity[key] = value
        
        client.put(entity)
        self.id = entity.key.id
        
        return self
    
    def delete(self):
        """Delete model from Datastore."""
        if not self.id:
            return
        
        client = self.get_client()
        key = client.key(self.KIND, self.id)
        client.delete(key)