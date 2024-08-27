#!/usr/bin/python3
from models.base_model import BaseModel

class Note(BaseModel):
    """
    Note model representing notes attached to tasks, goals, or general notes.
    """
    content = ""
    task_id = ""  # Optional foreign key to Task model
    goal_id = ""  # Optional foreign key to Goal model
    user_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
