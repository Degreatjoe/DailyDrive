#!/usr/bin/python3
from models.engine.file_storage import FileStorage
from datetime import datetime
import os
import json
import unittest
from unittest.mock import patch
from models.user import User
from models.category import Category
from models.goal import Goal
from models.note import Note
from models.task import Task
from models.plan import Plan
import io
import threading

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        """Set up a fresh FileStorage instance before each test."""
        self.storage = FileStorage()
        self.storage._FileStorage__file_path = 'file.json'

    def tearDown(self):
        """Clean up the JSON file after each test."""
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)

    def test_serializes_objects_to_json_file_correctly(self):
        user = User(id="123", email="test@example.com", username="testuser", password="password")
        self.storage.new(user)
        self.storage.save()

        self.assertTrue(os.path.exists(self.storage._FileStorage__file_path))
        with open(self.storage._FileStorage__file_path, 'r') as f:
            data = json.load(f)
            self.assertIn("User.123", data)
            self.assertEqual(data["User.123"]["email"], "test@example.com")

    def test_deserializes_json_file_correctly(self):
        mock_data = {
            "User.1": {"__class__": "User", "id": "1", "email": "test@example.com", "username": "testuser", "password": "password"},
            "Category.1": {"__class__": "Category", "id": "1", "name": "Work", "color": "#FF0000"}
        }
        with patch('builtins.open', return_value=io.StringIO(json.dumps(mock_data))):
            self.storage.reload()

        self.assertTrue("User.1" in self.storage._FileStorage__objects)
        self.assertTrue(isinstance(self.storage._FileStorage__objects["User.1"], User))

    #def test_handles_missing_json_file_gracefully_during_reload(self):
    #    with patch("builtins.open", side_effect=FileNotFoundError):
    #        self.storage.reload()
    #        self.assertEqual(self.storage.all(), {})

    def test_adds_new_object_to_storage_dictionary(self):
        user = User(id="123", email="test@example.com", username="testuser", password="password")
        self.storage.new(user)
        self.assertIn("User.123", self.storage._FileStorage__objects)
        self.assertEqual(self.storage._FileStorage__objects["User.123"], user)

    def test_delete_object_from_storage(self):
        user = User(id="123", email="test@example.com", username="testuser", password="password")
        self.storage.new(user)
        self.storage.save()
        
        with patch.object(self.storage, 'save', return_value=None):  # Mock save to skip actual file writing
            self.storage.delete(user)
            self.assertNotIn("User.123", self.storage._FileStorage__objects)

    def test_adding_objects_with_duplicate_keys(self):
        user1 = User(id="123", email="test@example.com", username="testuser1", password="password1")
        user2 = User(id="123", email="test2@example.com", username="testuser2", password="password2")
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.save()

        with open(self.storage._FileStorage__file_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["User.123"]["email"], "test2@example.com")

    def test_delete_object_not_present(self):
        user = User(id="123", email="test@example.com", username="testuser", password="password")
        self.storage.new(user)
        self.storage.save()
        user2 = User(id="456", email="another@example.com", username="anotheruser", password="anotherpassword")
        self.storage.delete(user2)
        self.assertIn("User.123", self.storage.all())

    def test_handling_missing_attributes_deserialization(self):
        user_data = {"id": "123", "email": "test@example.com"}
        user = User(**user_data)
        self.storage.new(user)
        self.storage.save()

        with patch("models.engine.file_storage.FileStorage.reload") as mock_reload:
            self.storage.reload()
            self.assertEqual(self.storage._FileStorage__objects["User.123"].username, "")

    def test_correct_class_instantiation_during_reload(self):
        obj_dict = {'User.1': {'__class__': 'User', 'id': '1', 'email': 'test@example.com', 'username': 'testuser', 'password': 'password'}}
        with patch('builtins.open', return_value=io.StringIO(json.dumps(obj_dict))):
            self.storage.reload()
            self.assertIsInstance(self.storage._FileStorage__objects['User.1'], User)

    def test_saving_objects_with_non_serializable_attributes(self):
        user = User(id="123", email="test@example.com", username="testuser", password="password", custom_attr="SomeNonSerializableObject")
        self.storage.new(user)
        self.storage.save()

        with open(self.storage._FileStorage__file_path, 'r') as f:
            data = json.load(f)
            self.assertIn("User.123", data)

    #def test_ensures_thread_safety(self):
    #    # Assuming FileStorage is thread-safe and the code correctly handles concurrent access
    #    def add_objects():
    #        for i in range(5):
    #            obj = User()
    #            self.storage.new(obj)
    #            self.storage.save()
#
    #    threads = [threading.Thread(target=add_objects) for _ in range(5)]
    #    for thread in threads:
    #        thread.start()
    #    for thread in threads:
    #        thread.join()
#
    #    self.assertEqual(len(self.storage.all()), 5)

if __name__ == '__main__':
    unittest.main()
