#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship


class Task(BaseModel, Base):
    """
    Task model representing individual tasks in the daily planner.
    """
    __tablename__ = 'tasks'

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", backref="tasks")

    def __init__(self, *args, **kwargs):
        """
        Initialize Task instance.
        """
        if getenv('DD_TYPE_STORAGE') != 'db':
            self.title = kwargs.get('title', "")
            self.description = kwargs.get('description', "")
            self.start_time = kwargs.get('start_time', None)
            self.end_time = kwargs.get('end_time', None)
            self.category = kwargs.get('category', "")
            self.status = kwargs.get('status', "")
            self.user_id = kwargs.get('user_id', "")
        super().__init__(*args, **kwargs)