import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from tests.fixtures import app

@pytest.mark.parametrize(
    "employeeid, employee_exists, form_data, file_data, hobbies_exist, education_exist, expected_status, expected_response",
    [
        (
            1,
            True,
            {
                "name": "Jane Doe",
                "phone_no": "9876543210",
                "birth_date": "1995-05-05",
                "gender": "Female",
                "description": "Updated employee",
                "hobbies": "Cooking,Traveling",
                "education": "MBA,PhD",
            },
            {"filename": "new_profile.jpg"},
            True,
            True,
            200,
            {"message": "Employee updated successfully"},
        ),
        (
            2,
            False,
            {
                "name": "Jane Doe",
                "phone_no": "9876543210",
                "birth_date": "1995-05-05",
                "gender": "Female",
                "description": "Updated employee",
                "hobbies": "Cooking,Traveling",
                "education": "MBA,PhD",
            },
            {"filename": "new_profile.jpg"},
            True,
            True,
            404,
            {"error": "Employee not found"},
        ),
    ],
)
@patch("utils.sanitised_validated_input_for_update_employee.get_employee")
@patch("logic.employee.employee.get_hobby")
@patch("logic.employee.employee.get_education")
@patch("logic.employee.employee.delete_employee_hobby")
@patch("logic.employee.employee.delete_employee_education")
@patch("logic.employee.employee.db.session.commit")
@patch("logic.employee.employee.allowed_file")
def test_update_employee(
    mock_allowed_file,
    mock_commit,
    mock_delete_employee_education,
    mock_delete_employee_hobby,
    mock_get_education,
    mock_get_hobby,
    mock_get_employee,
    employeeid,
    employee_exists,
    form_data,
    file_data,
    hobbies_exist,
    education_exist,
    expected_status,
    expected_response,
    app,
):
    client = app.test_client()

    # Prepare a fake file upload
    file_stream = BytesIO(b"dummy image data")
    file_stream.name = file_data["filename"]

    data = {
        **form_data,
        "file": (file_stream, file_data["filename"])
    }

    # Mock functions
    if employee_exists:
        mock_employee = MagicMock()
        mock_employee.id = employeeid
        mock_employee.name = "Old Name"
        mock_employee.phone_no = "0000000000"
        mock_employee.birth_date = "1990-01-01"
        mock_employee.gender = "Other"
        mock_employee.description = "Old Description"
        mock_employee.file_path = None  # or set a dummy file path to test file deletion
        mock_get_employee.return_value = mock_employee
    else:
        mock_get_employee.return_value = None

    # Mock other logic as needed
    mock_allowed_file.return_value = True
    mock_get_hobby.side_effect = lambda name: MagicMock() if hobbies_exist else None
    mock_get_education.side_effect = lambda name: MagicMock() if education_exist else None

    # Perform PUT request
    response = client.put(
        f"/updateEmployee/{employeeid}",
        data=data,
        content_type='multipart/form-data',
    )

    assert response.status_code == expected_status
    assert response.get_json() == expected_response
