import unittest
from flask import Flask
from app import app, db  # Import your Flask app and database instance
from models import User  # Import your User model

class UserManagementTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize a new test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite database
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

        with self.app.app_context():
            db.create_all()  # Create all tables

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables

    def test_user_signup(self):
        """Test user signup API."""
        signup_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "mysecurepassword",
            "password_verify": "mysecurepassword",
            "birthday": "1990-01-01",
            "boy_or_girl": "boy"
        }

        response = self.client.post('/api/signup', json=signup_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User created successfully', response.data)

    def test_user_login(self):
        """Test user login API."""
        # First, sign up a user
        signup_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "mysecurepassword",
            "password_verify": "mysecurepassword",
            "birthday": "1990-01-01",
            "boy_or_girl": "boy"
        }
        self.client.post('/api/signup', json=signup_data)

        # Now, test login with the created user
        login_data = {
            "email": "john.doe@example.com",
            "password": "mysecurepassword"
        }
        response = self.client.post('/api/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_user_profile(self):
        """Test retrieving user profile."""
        # First, sign up a user
        signup_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "mysecurepassword",
            "password_verify": "mysecurepassword",
            "birthday": "1990-01-01",
            "boy_or_girl": "boy"
        }
        self.client.post('/api/signup', json=signup_data)

        # Now, log in and get the JWT token
        login_data = {
            "email": "john.doe@example.com",
            "password": "mysecurepassword"
        }
        login_response = self.client.post('/api/login', json=login_data)
        token = login_response.json.get('access_token')

        # Test retrieving user profile
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.get('/api/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_user_update(self):
        """Test updating user profile."""
        # First, sign up a user
        signup_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "mysecurepassword",
            "password_verify": "mysecurepassword",
            "birthday": "1990-01-01",
            "boy_or_girl": "boy"
        }
        self.client.post('/api/signup', json=signup_data)

        # Now, log in and get the JWT token
        login_data = {
            "email": "john.doe@example.com",
            "password": "mysecurepassword"
        }
        login_response = self.client.post('/api/login', json=login_data)
        token = login_response.json.get('access_token')

        # Test updating user profile
        update_data = {
            "name": "Johnny Doe",
            "birthday": "1991-01-01",
            "boy_or_girl": "boy"
        }
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.put('/api/user', headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully', response.data)

    def test_user_delete(self):
        """Test deleting user account."""
        # First, sign up a user
        signup_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "password": "mysecurepassword",
            "password_verify": "mysecurepassword",
            "birthday": "1990-01-01",
            "boy_or_girl": "boy"
        }
        self.client.post('/api/signup', json=signup_data)

        # Now, log in and get the JWT token
        login_data = {
            "email": "john.doe@example.com",
            "password": "mysecurepassword"
        }
        login_response = self.client.post('/api/login', json=login_data)
        token = login_response.json.get('access_token')

        # Test deleting user account
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.delete('/api/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User account deleted successfully', response.data)

if __name__ == '__main__':
    unittest.main()
