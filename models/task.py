#!/usr/bin/python3
from models.base_model import BaseModel

class Task(BaseModel):
    """
    Task model representing individual tasks in the daily planner.
    """
    title = ""
    description = ""
    start_time = None  # datetime object
    end_time = None  # datetime object
    category = ""
    status = ""  # E.g., 'pending', 'completed', 'missed'
    user_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)