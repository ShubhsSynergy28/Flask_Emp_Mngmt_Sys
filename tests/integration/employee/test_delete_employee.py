import pytest
from tests.integration.conftest import *

@pytest.mark.parametrize(
    (
        "emp_id", "field", "url", "log_email", "log_password",
        "expected_status_code", "expected_response_JSON"
    ),
    [
        # Admin deleting employee
        (1, "email", "/login", "test@example.com", "Securep@ss",
         200, {"message": "Employee with ID 1 deleted successfully"}),

        # Employee deleting own profile
        (1, "phone_no", "/login-emp", "1234567899", "Securep@ss",
         200, {"message": "Employee with ID 1 deleted successfully"}),

        # # Wrong employee trying to delete another employee
        # (1, "phone_no", "/login-emp", "1234567890", "Securep@sss",
        #  401, {"error": "Unauthorized access. Please log in."}),

        # # No credentials
        # (1, "", "/login", "", "",
        #  401, {"error": "Unauthorized access. Please log in."}),

        # Admin trying to delete non-existent employee
        (2, "email", "/login", "test@example.com", "Securep@ss",
         404, {"error": "Employee not found"}),
    ]
)
def test_delete_employee_by_id(
    emp_id, field, url, log_email, log_password,
    expected_status_code, expected_response_JSON, client
):
    if log_email and log_password:
        client.post(url, data={
            field: log_email,
            'password': log_password
        })

    response = client.delete(f"/delete-employee/{emp_id}")
    assert response.status_code == expected_status_code
    assert response.get_json() == expected_response_JSON
