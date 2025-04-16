import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request, session
from logic.user.user import login
import bcrypt


@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    return app
@pytest.mark.parametrize(('test_email', 'test_password', 'input_password', 'expected_status', 'expected_response'), [
    # Valid email & correct password
    ('user@example.com', 'Securepassword@12', 'Securepassword@12', 200, {"message": "Login successful", "user": {"username": "testuser"}}),
    # Valid email & empty input password
    ('user@example.com', 'Securepassword@12', '', 400, {"error": "Email and password are required"}),
    # Empty email & valid password
    ('', 'Securepassword@12', 'Securepassword@12', 400, {"error": "Email and password are required"}),
    # Valid email & wrong password
    ('user@example.com', 'Securepassword@12', 'wrong@password', 401, {"error": "Invalid email or password"}),
])
@patch('logic.user.user.get_user_by_id')
def test_login_function_direct(mock_get_user_by_id, test_email, test_password, input_password, expected_status, expected_response,app):
    with app.test_request_context('/login', method='POST', data={'email': test_email, 'password': input_password}):
        # Only return a user object if email is provided
        if test_email:
            hashed_password = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
            mock_user = MagicMock()
            mock_user.id = 1
            mock_user.email = test_email
            mock_user.username = 'testuser'
            mock_user.password = hashed_password.decode('utf-8')
            mock_get_user_by_id.return_value = mock_user
        else:
            mock_get_user_by_id.return_value = None

        # Call the login function directly
        response, status_code = login()

        assert status_code == expected_status
        assert response.get_json() == expected_response
