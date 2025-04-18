import pytest
from unittest.mock import patch, MagicMock
from logic.employee.employee import get_all_employees, get_employee_by_id
from tests.fixtures import app  # assumes you have a fixture for your Flask app


def create_mock_employee(id, name, phone_no, birth_date, gender, description, file_path, hobbies, educations):
    employee = MagicMock()
    employee.id = id
    employee.name = name
    employee.phone_no = phone_no
    employee.birth_date = birth_date
    employee.gender = gender
    employee.description = description
    employee.file_path = file_path

    employee.hobbies = []
    for hobby_name in hobbies:
        hobby_obj = MagicMock()
        hobby_obj.hobby = MagicMock()
        hobby_obj.hobby.name = hobby_name
        employee.hobbies.append(hobby_obj)

    employee.educations = []
    for edu_name in educations:
        edu_obj = MagicMock()
        edu_obj.education = MagicMock()
        edu_obj.education.name = edu_name
        employee.educations.append(edu_obj)

    return employee


# =================== Test: get_all_employees ===================
@pytest.mark.parametrize("mocked_employees, expected_status, expected_response", [
    # No employees found
    ([], 404, {"error": "No employees found"}),

    # One employee with no hobbies or education
    ([create_mock_employee(
        id=1,
        name="John Doe",
        phone_no="1234567890",
        birth_date="1990-01-01",
        gender="Male",
        description="Test employee",
        file_path="/path/to/file",
        hobbies=[],
        educations=[]
    )], 200, [{
        "id": 1,
        "name": "John Doe",
        "phone_no": "1234567890",
        "birth_date": "1990-01-01",
        "gender": "Male",
        "description": "Test employee",
        "file_path": "/path/to/file",
        "hobbies": [],
        "education": []
    }]),

    # One employee with hobbies and education
    ([create_mock_employee(
        id=2,
        name="Jane Smith",
        phone_no="0987654321",
        birth_date="1985-05-05",
        gender="Female",
        description="Senior dev",
        file_path="/file/jane.png",
        hobbies=["Reading", "Gaming"],
        educations=["B.Tech", "M.Tech"]
    )], 200, [{
        "id": 2,
        "name": "Jane Smith",
        "phone_no": "0987654321",
        "birth_date": "1985-05-05",
        "gender": "Female",
        "description": "Senior dev",
        "file_path": "/file/jane.png",
        "hobbies": ["Reading", "Gaming"],
        "education": ["B.Tech", "M.Tech"]
    }]),
])
@patch('logic.employee.employee.get_employee')
def test_get_all_employees(mock_get_employee, mocked_employees, expected_status, expected_response, app):
    mock_get_employee.return_value = mocked_employees

    with app.test_request_context('/employees', method='GET'):
        response, status_code = get_all_employees()

        assert status_code == expected_status
        assert response.get_json() == expected_response


# =================== Test: get_employee_by_id ===================
@pytest.mark.parametrize("mock_employee, expected_status, expected_response", [
    # Employee found
    (
        create_mock_employee(
            1, "Alice", "9876543210", "1992-05-15", "Female", "Designer",
            "path/to/alice.jpg", ["Sketching", "Yoga"], ["BFA", "MFA"]
        ),
        200,
        {
            "id": 1,
            "name": "Alice",
            "phone_no": "9876543210",
            "birth_date": "1992-05-15",
            "gender": "Female",
            "description": "Designer",
            "file_path": "path/to/alice.jpg",
            "hobbies": ["Sketching", "Yoga"],
            "education": ["BFA", "MFA"]
        }
    ),
    # Employee not found
    (
        None,
        404,
        {"error": "Employee not found"}
    )
])
@patch('logic.employee.employee.get_employee')  # adjust if path differs
def test_get_employee_by_id(mock_get_employee, mock_employee, expected_status, expected_response, app):
    mock_get_employee.return_value = mock_employee

    with app.test_request_context('/employee/1', method='GET'):
        response, status_code = get_employee_by_id(1)

        assert status_code == expected_status
        assert response.get_json() == expected_response
