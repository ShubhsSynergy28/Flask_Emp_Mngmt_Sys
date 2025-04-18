import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from logic.employee.employee import delete_employee
from tests.fixtures import app


@pytest.fixture
def mock_employee():
    employee = MagicMock()
    employee.id = 1
    employee.file_path = (
        "D:\\LetsLearnPython&Flask\\Emp Mngmt Sys\\tests\\unit\\employee\\test_uploads\\"
        "c1fe6992-ff48-4233-982b-da51b94b11d7_download.jpg"
    )
    return employee


@pytest.mark.parametrize(
        "employee_exists, file_exists, file_remove_success, expected_status, expected_message",
    [
        # Test Case 1: Employee exists, file exists, file deletion successful
        (True, True, True, 200, "Employee with ID 1 deleted successfully"),
        
        # Test Case 2: Employee exists, file exists, file deletion fails
        (
            True, True, False, 500,
            "Failed to delete associated file: [Errno 2] No such file or directory: "
            "'D:\\LetsLearnPython&Flask\\Emp Mngmt Sys\\tests\\unit\\employee\\test_uploads\\"
            "c1fe6992-ff48-4233-982b-da51b94b11d7_download.jpg'"
        ),
        
        # Test Case 3: Employee exists, file does not exist
        (True, False, True, 200, "Employee with ID 1 deleted successfully"),
        
        # Test Case 4: Employee does not exist
        (False, False, True, 404, "Employee not found"),
    ]
)
@patch("logic.employee.employee.get_employee")
@patch("logic.employee.employee.os.remove")
@patch("logic.employee.employee.os.path.exists")
@patch("logic.employee.employee.delete_employee_hobby")
@patch("logic.employee.employee.delete_employee_education")
@patch("logic.employee.employee.delete_emp")
@patch("logic.employee.employee.db.session.commit")
def test_delete_employee(
    mock_commit,
    mock_delete_emp,
    mock_delete_education,
    mock_delete_hobby,
    mock_exists,
    mock_remove,
    mock_get_employee,
    app,  # app context fixture
    mock_employee,
    employee_exists,
    file_exists,
    file_remove_success,
    expected_status,
    expected_message
):
    # Setup mocks
    mock_get_employee.return_value = mock_employee if employee_exists else None
    mock_exists.return_value = file_exists
    mock_remove.side_effect = OSError(
        f"[Errno 2] No such file or directory: '{mock_employee.file_path}'"
    ) if not file_remove_success else None
    mock_employee.file_path = (
        "D:\\LetsLearnPython&Flask\\Emp Mngmt Sys\\tests\\unit\\employee\\test_uploads\\"
        "c1fe6992-ff48-4233-982b-da51b94b11d7_download.jpg"
        if file_exists else None
    )

    with app.app_context():
        response, status = delete_employee(mock_employee.id)

    # Assertions
    assert status == expected_status
    assert response.get_json() == (
        {"message": expected_message}
        if expected_status == 200
        else {"error": expected_message}
    )