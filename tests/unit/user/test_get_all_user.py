import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from logic.user.user import get_all_users  # adjust the path based on your structure
from tests.fixtures import app


@pytest.mark.parametrize("mocked_users, expected_status, expected_response", [
    # Case: No users found
    ([], 404, {"error": "No users found"}),

    # Case: One user
    ([MagicMock(id=1, username="user1", email="user1@example.com")], 200,
     [{"id": 1, "username": "user1", "email": "user1@example.com"}]),

    # Case: Multiple users
    ([
        MagicMock(id=1, username="user1", email="user1@example.com"),
        MagicMock(id=2, username="user2", email="user2@example.com")
    ], 200,
     [
         {"id": 1, "username": "user1", "email": "user1@example.com"},
         {"id": 2, "username": "user2", "email": "user2@example.com"}
     ]),
])
@patch('logic.user.user.get_all_user')
def test_get_all_users(mock_get_all_user, mocked_users, expected_status, expected_response, app):
    mock_get_all_user.return_value = mocked_users

    with app.test_request_context('/users', method='GET'):
        response, status_code = get_all_users()

        assert status_code == expected_status
        assert response.get_json() == expected_response
