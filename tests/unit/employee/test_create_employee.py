import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from tests.unit.fixtures import *  # Ensure this fixture includes the /createEmployee route

from logic.employee.employee import create_employee
# from application import app
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.parametrize(
    "form_data, file_data, hobbies_exist, education_exist, expected_status, expected_response",
    [
        # Test Case 1: Valid input, hobbies and education exist
        (
            {
                "name": "John Doe",
                "phone_no": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "description": "Test employee",
                "password": "SecurePassword@123",
                "hobbies": "Reading,Traveling",
                "education": "B.Sc,M.Sc",
            },
            {"filename": "profile.jpg"},
            True,
            True,
            201,
            {"message": "Employee created successfully"},
        ),
        # Test Case 2: Hobby does not exist
        (
            {
                "name": "John Doe",
                "phone_no": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "description": "Test employee",
                "password": "SecurePassword123",
                "hobbies": "NonExistentHobby",
                "education": "B.Sc,M.Sc",
            },
            {"filename": "profile.jpg"},
            False,
            True,
            400,
            {"error": "Hobby 'NonExistentHobby' does not exist"},
        ),
        # Test Case 3: Education does not exist
        (
            {
                "name": "John Doe",
                "phone_no": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "description": "Test employee",
                "password": "SecurePassword123",
                "hobbies": "Reading,Traveling",
                "education": "NonExistentEducation",
            },
            {"filename": "profile.jpg"},
            True,
            False,
            400,
            {"error": "Education 'NonExistentEducation' does not exist"},
        ),
    ],
)

@patch("logic.employee.employee.allowed_file")
@patch("logic.employee.employee.db.session.add")
@patch("logic.employee.employee.db.session.commit")
@patch("logic.employee.employee.add_employee_education")
@patch("logic.employee.employee.add_employee_hobby")
@patch("logic.employee.employee.add_employee")
@patch("logic.employee.employee.get_education")
@patch("logic.employee.employee.get_hobby")
def test_create_employee(
    mock_get_hobby,
    mock_get_education,
    mock_add_employee,
    mock_add_employee_hobby,
    mock_add_employee_education,
    mock_db_commit,
    mock_db_add,
    mock_allowed_file,
    form_data,
    file_data,
    hobbies_exist,
    education_exist,
    expected_status,
    expected_response,
    app,
):

    mock_allowed_file.return_value = True
    mock_get_hobby.side_effect = lambda name: MagicMock() if hobbies_exist else None
    mock_get_education.side_effect = lambda name: MagicMock() if education_exist else None


    with app.test_client() as client:
       
        data = {
            **form_data,
            "file": (BytesIO(b"fake image"), file_data["filename"]),
        }
        response = client.post("/createEmployee", data=data, content_type="multipart/form-data")
        json_data = response.get_json()

        assert response.status_code == expected_status
        assert json_data == expected_response
