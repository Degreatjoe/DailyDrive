#!/usr/bin/python3
from models.base_model import BaseModel

class Plan(BaseModel):
    """
    Plan model representing a user's daily or weekly plan.
    """
    date = None  # Date object for the plan
    tasks = []  # List of task IDs associated with this plan
    user_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)