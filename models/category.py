#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv

class Category(BaseModel, Base):
    """
    Category model representing categories of tasks (e.g., work, personal).
    """
    __tablename__ = 'categories'
    
    name = Column(String(50), nullable=False)
    color = Column(String(10), nullable=False)  # assuming a 6-digit hex code (e.g., #FF0000)
    description = Column(String(200), nullable=True)

    def __init__(self, *args, **kwargs):
        """
        Initialize Category instance.
        """
        if getenv('DD_TYPE_STORAGE') != 'db':
            self.name = kwargs.get('name', "")
            self.color = kwargs.get('color', "")
            self.description = kwargs.get('description', "")
        super().__init__(*args, **kwargs)
