import unittest
from flask import Flask
from logic.user.user import login, create_user

class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_login(self):
        with self.app.test_request_context('/login', method='POST', data={
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }):
            response = login()
            self.assertEqual(response.status_code, 200)
            self.assertIn('Login successful', response.get_json()['message'])

    def test_create_user(self):
        with self.app.test_request_context('/create-user', method='POST', data={
            'username': 'TestUser',
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }):
            response = create_user()
            self.assertEqual(response.status_code, 201)
            self.assertIn('User created successfully', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()