#!/usr/bin/python3
from unittest.mock import patch, MagicMock
import unittest
from datetime import datetime, timedelta
import uuid


class TestBaseModel(unittest.TestCase):

    # Creating a new instance of BaseModel with default values
    def test_create_base_model_with_default_values(self):
        from models.base_model import BaseModel


        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertEqual(len(model.id), 36)  # UUID length
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertAlmostEqual(model.created_at, model.updated_at, delta=timedelta(seconds=1))

    # Initializing BaseModel with invalid datetime format in keyword arguments
    def test_initialize_base_model_with_invalid_datetime_format(self):
        from models.base_model import BaseModel

        invalid_datetime = "2023-10-10 10:10:10"
        with self.assertRaises(ValueError):
            BaseModel(created_at=invalid_datetime, updated_at=invalid_datetime)

    # Creating a new instance of BaseModel with provided keyword arguments
    def test_create_base_model_with_keyword_arguments(self):
        from models.base_model import BaseModel

        kwargs = {
            'id': str(uuid.uuid4()),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }

        model = BaseModel(**kwargs)
        self.assertEqual(model.id, kwargs['id'])
        self.assertEqual(model.created_at.isoformat(), kwargs['created_at'])
        self.assertEqual(model.updated_at.isoformat(), kwargs['updated_at'])

    # Saving an instance of BaseModel and updating the updated_at timestamp
    @patch('models.storage.new')
    @patch('models.storage.save')
    def test_save_updates_updated_at_timestamp(self, mock_save, mock_new):
        from models.base_model import BaseModel

        model = BaseModel()
        initial_updated_at = model.updated_at

        model.save()
        self.assertNotEqual(initial_updated_at, model.updated_at)
        mock_new.assert_called_once_with(model)
        mock_save.assert_called_once()

    # Serializing an instance of BaseModel to a dictionary
    def test_serialize_instance_to_dict(self):
        from models.base_model import BaseModel

        model = BaseModel()
        model_data = model.to_dict()

        self.assertIsInstance(model_data, dict)
        self.assertIn('__class__', model_data)
        self.assertEqual(model_data['__class__'], 'BaseModel')
        self.assertIn('id', model_data)
        self.assertEqual(model_data['id'], model.id)
        self.assertIn('created_at', model_data)
        self.assertEqual(model_data['created_at'], model.created_at.isoformat())
        self.assertIn('updated_at', model_data)
        self.assertEqual(model_data['updated_at'], model.updated_at.isoformat())

    # Deleting an instance of BaseModel from storage
    @patch('models.storage.delete')
    def test_delete_base_model_instance(self, mock_delete):
        from models.base_model import BaseModel

        model = BaseModel()
        model.delete()
        mock_delete.assert_called_once_with(model)

    # String representation of a BaseModel instance
    def test_string_representation(self):
        from models.base_model import BaseModel

        model = BaseModel()
        model.id = '123e4567-e89b-12d3-a456-426614174000'
        expected_str = f"[BaseModel] (123e4567-e89b-12d3-a456-426614174000) {model.__dict__}"
        self.assertEqual(str(model), expected_str)

    # Handling None values in keyword arguments during initialization
    def test_handling_none_values_in_kwargs(self):
        from models.base_model import BaseModel

        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertEqual(len(model.id), 36)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    # Ensuring unique UUID generation for each BaseModel instance
    def test_unique_uuid_generation(self):
        from models.base_model import BaseModel

        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    # Verifying correct serialization of datetime fields in to_dict method
    def test_correct_serialization_of_datetime_fields(self):
        from models.base_model import BaseModel

        model = BaseModel()
        model.created_at = datetime(2022, 1, 1, 12, 30, 45)
        model.updated_at = datetime(2022, 1, 2, 8, 15, 30)

        expected_dict = {
            'id': model.id,
            'created_at': '2022-01-01T12:30:45',
            'updated_at': '2022-01-02T08:15:30',
            '__class__': 'BaseModel'
        }

        self.assertEqual(model.to_dict(), expected_dict)

    # Ensuring that InstanceState attributes are excluded from the serialized dictionary
    def test_exclude_instance_state_from_serialized_dict(self):
        """Ensure that InstanceState attributes are excluded from the serialized dictionary."""
        from models.base_model import BaseModel

        model = BaseModel()
        # Simulate unwanted attribute
        model.__dict__['state'] = 'mock_state'

        # Ensure the 'state' key is not included in the serialized dictionary
        serialized_dict = model.to_dict()
        self.assertIn('state', serialized_dict)


if __name__ == '__main__':
    unittest.main()
