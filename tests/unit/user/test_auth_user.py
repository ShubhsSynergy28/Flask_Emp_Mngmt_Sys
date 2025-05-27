import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, request, session
from logic.user.user import login
from logic.user.user import create_user
from logic.user.user import logout
import bcrypt
from tests.unit.fixtures import app


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
@patch("logic.user.user.return_refresh_token", return_value="mock-refresh-token")
@patch("logic.user.user.return_jwt_token", return_value="mock-access-token")
@patch('logic.user.user.get_user_by_id')
def test_login_function_direct(
    mock_get_user_by_id, mock_jwt_token, mock_refresh_token,
    test_email, test_password, input_password, expected_status, expected_response, app
):
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
        data = response.get_json()
        # For successful login, check tokens as well
        if expected_status == 200:
            assert data["message"] == expected_response["message"]
            assert data["user"] == expected_response["user"]
            assert data["access_token"] == "mock-access-token"
            assert data["refresh_token"] == "mock-refresh-token"
        else:
            assert data == expected_response


@pytest.mark.parametrize("session_data", [
    # Case 1: Session has user data
    {'user_id': 1, 'email': 'user@example.com', 'username': 'testuser'},
    # Case 2: Session is already empty
    {}
])
def test_logout_parametrized(app, session_data):
    with app.test_request_context('/logout'):
        # Set up the session with the provided session_data
        session.clear()
        session.update(session_data)

        # Sanity check before logout
        for key in session_data:
            assert key in session

        # Call the logout function directly
        response, status_code = logout()

        # After logout, session should be cleared of specific keys
        assert 'user_id' not in session
        assert 'email' not in session
        assert 'username' not in session

        # Response should always be the same
        assert status_code == 200
        assert response.get_json() == {"message": "Logout successful"}



@pytest.mark.parametrize("username, email, password, user_exists, expected_status, expected_response", [
    # Case: Missing all fields
    ("", "", "", False, 400, {"error": "Username, email, and password are required"}),
    # Case: Missing email
    ("user1", "", "Password@123", False, 400, {"error": "Username, email, and password are required"}),
    # Case: Email already exists
    ("user1", "user@example.com", "Password@123", True, 400, {"error": "Email already exists"}),
    # Case: Valid input, user created
    ("user1", "new@example.com", "Password@123", False, 201, {
        "message": "User created successfully",
        "user": {"username": "user1", "email": "new@example.com"}
    }),
])
@patch('logic.user.user.get_user_by_id')
@patch('logic.user.user.add_user')
@patch('logic.user.user.db')
def test_create_user_parametrized(mock_db, mock_add_user, mock_get_user_by_id,
                                  username, email, password, user_exists,
                                  expected_status, expected_response, app):

    with app.test_request_context('/create', method='POST', data={
        'username': username,
        'email': email,
        'password': password
    }):
        if user_exists:
            # Simulate existing user
            mock_get_user_by_id.return_value = MagicMock()
        else:
            # Simulate no existing user
            mock_get_user_by_id.return_value = None

        mock_add_user.return_value = None  # We just patch it to prevent DB insert
        mock_db.session.commit.return_value = None  # Patch commit as well

        response, status_code = create_user()

        assert status_code == expected_status
        assert response.get_json() == expected_response