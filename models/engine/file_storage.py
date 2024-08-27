import json
from models.base_model import BaseModel
from models.user import User
from models.category import Category
from models.goal import Goal
from models.note import Note
from models.task import Task
from models.plan import Plan

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""
    __file_path = "file.json"
    __objects = {}

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Category": Category,
        "Goal": Goal,
        "Note": Note,
        "Task": Task,
        "Plan": Plan
        # Add new classes here as needed
    }

    def all(self):
        """Returns the dictionary of all objects."""
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage dictionary."""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(obj_dict, f, indent=4)  # Pretty-print JSON

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value['__class__']
                    if class_name in self.classes:
                        self.__objects[key] = self.classes[class_name](**value)
        except FileNotFoundError:
            pass  # If the file doesn't exist, skip reloading
