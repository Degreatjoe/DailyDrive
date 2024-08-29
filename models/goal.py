#!/usr/bin/python3
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship

class Goal(BaseModel, Base):
    """
    Goal model representing long-term or short-term goals in the daily planner.
    """
    __tablename__ = 'goals'

    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    goal = Column(Integer, nullable=True)
    progress = Column(Integer, nullable=True)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize Goal instance.
        """
        if getenv('DD_TYPE_STORAGE') != 'db':
            self.title = kwargs.get('title', "")
            self.category = kwargs.get('category', "")
            self.description = kwargs.get('description', "")
            self.start_date = kwargs.get('start_date', None)
            self.end_date = kwargs.get('end_date', None)
            self.goal = kwargs.get('goal', 0)
            self.progress = kwargs.get('progress', 0)
            self.user_id = kwargs.get('user_id', "")
        super().__init__(*args, **kwargs)