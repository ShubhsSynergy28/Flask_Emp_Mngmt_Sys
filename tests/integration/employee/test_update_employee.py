import io
import pytest
from models.models import Employee
from tests.integration.conftest import *
from utils.allowed_extentions import ALLOWED_EXTENSIONS

@pytest.mark.parametrize(
    "login_route, login_payload, form_data, file_upload, expected_status, expected_response",
    [
        #  Admin login + valid data + file upload
        (
            "/login",
            {"email": "test@example.com", "password": "Securep@ss"},
            {
                "name": "Updated Name",
                "phone_no": "9876543210",
                "birth_date": "2002-05-28",
                "gender": "female",
                "description": "Updated description",
                "hobbies": "test_Reading,test_Sports",
                "education": "test_Bachelor,test_Master"
            },
            {"file": (io.BytesIO(b"updated content"), "updated_resume.pdf")},
            200,
            {"message": "Employee updated successfully"}
        ),

        #  Employee login + valid data, no file upload
        (
            "/login-emp",
            {"phone_no": "1234567899", "password": "Securep@ss"},
            {
                "name": "Emp Updated",
                "phone_no": "9988776655",
                "birth_date": "2002-05-28",
                "gender": "male",
                "description": "Emp updated desc",
                "hobbies": "test_Sports",
                "education": "test_Master"
            },
            None,
            200,
            {"message": "Employee updated successfully"}
        ),

        #  No login, expect 401
        (
            "",
            {},
            {
                "name": "Unauthorized update",
                "phone_no": "1111111111",
                "birth_date": "2002-05-28",
                "gender": "male",
                "description": "No session",
                "hobbies": "test_Reading",
                "education": "test_Bachelor"
            },
            None,
            401,
            {"error": "Unauthorized access. Please log in."}
        ),

        #  Invalid date format
        (
            "/login",
            {"email": "test@example.com", "password": "Securep@ss"},
            {
                "name": "Bad Date",
                "phone_no": "1234509876",
                "birth_date": "28-05-2002",  # wrong format
                "gender": "male",
                "description": "Bad date format",
                "hobbies": "test_Reading",
                "education": "test_Bachelor"
            },
            None,
            400,
            {"error": "Invalid date format. Use YYYY-MM-DD."}
        ),

        #  Phone number not changed
        (
            "/login",
            {"email": "test@example.com", "password": "Securep@ss"},
            {
                "name": "Duplicate Phone",
                "phone_no": "1234567899",  # already in use by same employee
                "birth_date": "2002-05-28",
                "gender": "male",
                "description": "Dup phone",
                "hobbies": "test_Reading",
                "education": "test_Bachelor"
            },
            None,
            200,
            {'message': 'Employee updated successfully'}
        ),

        #  Invalid file extension
        (
            "/login",
            {"email": "test@example.com", "password": "Securep@ss"},
            {
                "name": "Invalid File",
                "phone_no": "8765432109",
                "birth_date": "2002-05-28",
                "gender": "female",
                "description": "Bad file",
                "hobbies": "test_Sports",
                "education": "test_Bachelor"
            },
            {"file": (io.BytesIO(b"malicious"), "script.exe")},
            400,
            {"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}
        ),
    ]
)
def test_update_employee(client, login_route, login_payload, form_data, file_upload, expected_status, expected_response):
    if login_route:
        client.post(login_route, data=login_payload)

    data = form_data.copy()
    if file_upload:
        data.update(file_upload)

    response = client.put('/update-employee/1', data=data, content_type='multipart/form-data')
    
    assert response.status_code == expected_status
    assert response.get_json() == expected_response
