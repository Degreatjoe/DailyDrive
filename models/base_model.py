#!/usr/bin/python3
from datetime import datetime
import uuid

class BaseModel:
    """Base class for all models."""

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            from models import storage  # Local import to avoid circular import issue
            storage.new(self)

    def save(self):
        """Updates the updated_at timestamp and saves the instance."""
        self.updated_at = datetime.now()
        from models import storage  # Local import to avoid circular import issue
        storage.save()

    def to_dict(self):
        """Converts the instance to a dictionary format."""
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()
        return dict_copy

    def __str__(self):
        """String representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
