#!/usr/bin/python3
from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import InstanceState

Base = declarative_base()

class BaseModel(Base):
    """Base class for all models."""
    
    __abstract__ = True  # Mark this class as an abstract base class

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of BaseModel."""
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at'] and isinstance(value, str):
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def save(self):
        """Updates the updated_at timestamp and saves the instance."""
        self.updated_at = datetime.utcnow()
        from models import storage  # Local import to avoid circular import issues
        storage.new(self)
        storage.save()

    def to_dict(self):
        dict_copy = self.__dict__.copy()
        for key in list(dict_copy.keys()):  # Iterate over a list of keys to modify dict_copy during iteration
            if isinstance(dict_copy[key], InstanceState):
                del dict_copy[key]
            elif key in ['created_at', 'updated_at']:
                dict_copy[key] = dict_copy[key].isoformat()
        dict_copy['__class__'] = self.__class__.__name__
        return dict_copy

    def delete(self):
        """Deletes the current instance from the storage."""
        from models import storage  # Local import to avoid circular import issues
        storage.delete(self)

    def __str__(self):
        """String representation of the BaseModel instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
