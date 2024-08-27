#!/usr/bin/python3

from models.base_model import BaseModel

class User(BaseModel):
    """
    User class that inherits from BaseModel.
    Defines user-specific attributes.
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
