#!/usr/bin/python3
from models.base_model import BaseModel

class Category(BaseModel):
    """
    Category model representing categories of tasks (e.g., work, personal).
    """
    name = ""
    color = ""  # Color code associated with the category
    description = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)