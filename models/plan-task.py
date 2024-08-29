#!/usr/bin/python3
from models.base_model import BaseModel, Base
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

class PlanTask(BaseModel, Base):
    __tablename__ = 'plan_tasks'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)

    plan = relationship("Plan", backref="plan_tasks")
    task = relationship("Task", backref="plan_tasks")