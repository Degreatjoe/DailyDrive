#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

class Plan(BaseModel, Base):
    """
    Plan model representing a user's daily or weekly plan.
    """
    __tablename__ = 'plans'

    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", backref="plans")

    def __init__(self, *args, **kwargs):
        """
        Initialize Plan instance.
        """
        if getenv('DD_TYPE_STORAGE') != 'db':
            from datetime import date
            self.date = kwargs.get('date', None)
            self.tasks = kwargs.get('tasks', [])  # List of task IDs
            self.user_id = kwargs.get('user_id', "")
        super().__init__(*args, **kwargs)