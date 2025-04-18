from tests.integration.conftest import *

@pytest.mark.parametrize(("phone_no, password, expected_status_code, expected_response_json"),[
    # """Correct credentials"""
    ('1234567899','Securep@ss', 200, {'employee': {'id': 1, 'name': "Test Employee"}, 'message': "Employee login successful"}),
    # """Wrong credentials"""
    ('1234567890','wrong@cred', 401, {"error": "Invalid phone number or password"}),
    # """Blank Credentials"""
    ('','',400,{"error": "Phone number and password are required"})
    ])
def test_employee_login(phone_no, password, expected_status_code, expected_response_json, client):
    """Test employe login which returns a json object"""
    response = client.post('/login-emp', data={
        'phone_no': phone_no,
        'password': password
    })
    assert response.status_code == expected_status_code
    assert response.get_json() == expected_response_json


@pytest.mark.parametrize(("expected_status, expected_response_text"),[(200, {"message": "Employee logged out successfully"})])
def test_employee_logout(expected_status, expected_response_text, client):
    """Test Employee logout returns a json object"""
    response = client.post('/logout-emp')

    assert response.status_code == expected_status
    assert response.get_json() == expected_response_text
