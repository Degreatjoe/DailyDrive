#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    User class that inherits from BaseModel.
    Defines user-specific attributes.
    """
    __tablename__ = 'users'

    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    def __init__(self, *args, **kwargs):
        """
        Initialize User instance.
        """
        if getenv('DD_TYPE_STORAGE') != 'db':
            self.email = kwargs.get('email', "")
            self.username = kwargs.get('username', "")
            self.password = kwargs.get('password', "")
            self.first_name = kwargs.get('first_name', "")
            self.last_name = kwargs.get('last_name', "")
        super().__init__(*args, **kwargs)
