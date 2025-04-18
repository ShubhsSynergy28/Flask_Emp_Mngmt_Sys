import io
import pytest
from tests.integration.conftest import *

@pytest.mark.parametrize(
    (
        "login_url", "login_field", "login_value", "password",
        "form_data", "file_upload", "expected_status_code", "expected_response"
    ),
    [
        #  Admin creating new employee
        (
            "/login", "email", "test@example.com", "Securep@ss",
            {
                "name": "New Employee",
                "phone_no": "9876543210",
                "birth_date": "2000-01-01",
                "gender": "male",
                "description": "A new employee",
                "password": "Test@123",
                "hobbies": "test_Reading,test_Sports",
                "education": "test_Bachelor,test_Master"
            },
            ("test.pdf", b"sample file content"),
            201,
            {"message": "Employee created successfully"}
        ),

        #  Missing name
        (
            "/login", "email", "test@example.com", "Securep@ss",
            {
                "name": "",
                "phone_no": "9876543211",
                "birth_date": "2000-01-01",
                "gender": "male",
                "description": "Missing name",
                "password": "Test@123",
                "hobbies": "test_Reading",
                "education": "test_Bachelor"
            },
            None,
            400,
            {"error": "Name is required and must contain only alphabetic characters"}
        ),

        #  Invalid phone number
        (
            "/login", "email", "test@example.com", "Securep@ss",
            {
                "name": "Test",
                "phone_no": "abc123",
                "birth_date": "2000-01-01",
                "gender": "male",
                "description": "Bad phone",
                "password": "Test@123",
                "hobbies": "test_Sports",
                "education": "test_Bachelor"
            },
            None,
            400,
            {"error": "Phone number is required and must be 10 numeric characters"}
        ),

        #  Duplicate phone number (already exists from test setup)
        (
            "/login", "email", "test@example.com", "Securep@ss",
            {
                "name": "Another",
                "phone_no": "1234567899",
                "birth_date": "2000-01-01",
                "gender": "female",
                "description": "Dup phone",
                "password": "Test@123",
                "hobbies": "test_Reading",
                "education": "test_Bachelor"
            },
            None,
            400,
            {"error": "Phone number already exists"}
        ),

        #  Unauthorized (not logged in)
        (
            "", "", "", "",
            {
                "name": "Unauthorized",
                "phone_no": "9876543222",
                "birth_date": "2000-01-01",
                "gender": "male",
                "description": "Not logged in",
                "password": "Test@123",
                "hobbies": "test_Sports",
                "education": "test_Bachelor"
            },
            None,
            401,
            {"error": "Unauthorized access. Please log in."}
        ),
    ]
)
def test_create_employee(
    client,
    login_url, login_field, login_value, password,
    form_data, file_upload,
    expected_status_code, expected_response
):
    # Log in first if credentials provided
    if login_url:
        client.post(login_url, data={
            login_field: login_value,
            "password": password
        })

    # Build form data with optional file upload
    data = dict(form_data)
    if file_upload:
        filename, file_content = file_upload
        data["file"] = (io.BytesIO(file_content), filename)

    response = client.post("/createEmployee", data=data, content_type='multipart/form-data')
    assert response.status_code == expected_status_code
    assert response.get_json() == expected_response
