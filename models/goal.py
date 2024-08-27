#!/usr/bin/python3
from models.base_model import BaseModel

class Goal(BaseModel):
    """
    Goal model representing long-term or short-term goals in the daily planner.
    """
    title = ""
    description = ""
    start_date = None  # date object
    end_date = None  # date object
    progress = 0  # Percentage or count to track goal progress
    user_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)