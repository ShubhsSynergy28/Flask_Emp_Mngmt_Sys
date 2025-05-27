from tests.integration.conftest import *

@pytest.mark.parametrize(("phone_no, password, expected_status_code, expected_employee, expected_message"),[
    ('1234567899','Securep@ss', 200, {'id': 1, 'name': "Test Employee"}, "Employee login successful"),
    ('1234567890','wrong@cred', 401, None, "Invalid phone number or password"),
    ('','',400, None, "Phone number and password are required")
])
def test_employee_login(phone_no, password, expected_status_code, expected_employee, expected_message, client):
    response = client.post('/login-emp', data={
        'phone_no': phone_no,
        'password': password
    })
    assert response.status_code == expected_status_code
    data = response.get_json()
    if expected_status_code == 200:
        assert data["message"] == expected_message
        assert data["employee"] == expected_employee
        assert isinstance(data["access_token"], str) and data["access_token"]
        assert isinstance(data["refresh_token"], str) and data["refresh_token"]
    else:
        assert data["error"] == expected_message

@pytest.mark.parametrize(("expected_status, expected_response_text"),[(200, {"message": "Employee logged out successfully"})])
def test_employee_logout(expected_status, expected_response_text, client):
    """Test Employee logout returns a json object"""
    response = client.post('/logout-emp')

    assert response.status_code == expected_status
    assert response.get_json() == expected_response_text
