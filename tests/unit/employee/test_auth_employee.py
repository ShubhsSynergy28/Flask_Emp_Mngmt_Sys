import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session, request, jsonify
from logic.employee.employee import employee_login, employee_logout  # Your actual logic
from tests.unit.fixtures import app
# from tests.fixtures import app


@pytest.mark.parametrize("phone_no, password, expected_status, expected_response", [
    ("1234567890", "password123", 200, {"message": "Employee login successful"}),  # Valid credentials
    ("", "password123", 400, {"error": "Phone number and password are required"}),  # Missing phone_no
    ("1234567890", "", 400, {"error": "Phone number and password are required"}),  # Missing password
    ("1234567890", "wrongpass", 401, {"error": "Invalid phone number or password"}),  # Invalid creds
])
@patch("logic.employee.employee.check_employee_credentials")
def test_employee_login(mock_check_credentials, app, phone_no, password, expected_status, expected_response):
    # Setup mock
    employee_mock = MagicMock()
    employee_mock.id = 1
    employee_mock.name = "John Doe"

    def credentials_side_effect(phone, pwd):
        if phone == "1234567890" and pwd == "password123":
            return employee_mock
        elif phone and pwd:
            return None

    mock_check_credentials.side_effect = credentials_side_effect

    with app.test_client() as client:
        response = client.post("/employee/login", data={
            "phone_no": phone_no,
            "password": password
        })
        json_data = response.get_json()

        assert response.status_code == expected_status
        for key, value in expected_response.items():
            assert json_data[key] == value

        if expected_status == 200:
            with client.session_transaction() as sess:
                assert sess['employee_id'] == employee_mock.id
                assert sess['employee_name'] == employee_mock.name


def test_employee_logout(app):
    with app.test_client() as client:
        # Pre-set session values
        with client.session_transaction() as sess:
            sess['employee_id'] = 1
            sess['employee_name'] = 'John Doe'

        response = client.get("/employee/logout")  # Adjust method if POST
        json_data = response.get_json()

        assert response.status_code == 200
        assert json_data["message"] == "Employee logged out successfully"

        # Confirm session was cleared
        with client.session_transaction() as sess:
            assert 'employee_id' not in sess
            assert 'employee_name' not in sess
