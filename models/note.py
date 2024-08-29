#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Note(BaseModel, Base):
    """
    Note model representing notes attached to tasks, goals, or general notes.
    """
    __tablename__ = 'notes'

    content = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    goal_id = Column(Integer, ForeignKey('goals.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    task = relationship("Task", backref="notes")
    goal = relationship("Goal", backref="notes")
    user = relationship("User", backref="notes")

    def __init__(self, *args, **kwargs):
        """
        Initialize Note instance.
        """
        if getenv('DD_TYPE_STORAGE') != 'db':
            self.content = kwargs.get('content', "")
            self.task_id = kwargs.get('task_id', "")
            self.goal_id = kwargs.get('goal_id', "")
            self.user_id = kwargs.get('user_id', "")
        super().__init__(*args, **kwargs)