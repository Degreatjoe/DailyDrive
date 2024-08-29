#!/usr/bin/python3
import json

class FileStorage:
    """Serializes instances to a JSON file and deserializes JSON file to instances."""
    __file_path = "file.json"
    __objects = {}

    @property
    def classes(self):
        """Returns a dictionary of class names to class objects."""
        from models.user import User
        from models.category import Category
        from models.goal import Goal
        from models.note import Note
        from models.task import Task
        from models.plan import Plan

        return {
            "User": User,
            "Category": Category,
            "Goal": Goal,
            "Note": Note,
            "Task": Task,
            "Plan": Plan
        }

    def all(self, cls=None):
        """Returns a dictionary of all objects or all objects of a specified class."""
        if cls is None:
            return FileStorage.__objects
        from models.base_model import BaseModel
        if isinstance(cls, str):
            cls = eval(cls)
        if issubclass(cls, BaseModel):
            return {k: v for k, v in FileStorage.__objects.items() if isinstance(v, cls)}
        return {}

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
        classes = self.classes  # Use the classes property

        try:
            with open(self.__file_path, 'r') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value.pop('__class__', None)  # Remove __class__ from the value dictionary
                    if class_name and class_name in classes:
                        self.__objects[key] = classes[class_name](**value)
        except FileNotFoundError:
            pass  # If the file doesn't exist, skip reloading

    def delete(self, obj=None):
        """Deletes an object from storage if it exists."""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()
