from tests.integration.conftest import *


@pytest.mark.parametrize(("email, password, expected_status, expected_response_text"),[
    ('test@example.com', 'Securep@ss', 200, {"message":"Login successful","user":{"username":"testuser"}}),
    ('wrong@example.com','wrong@pass', 401, {"error": "Invalid email or password"}),
    ('','', 400, {"error": "Email and password are required"}),
])
def test_user_login(email, password, expected_status, expected_response_text, client):
    """Test successful user login"""
    response = client.post('/login', data={
        'email': email,
        'password': password
    })
    assert response.status_code == expected_status
    data = response.get_json()
    if expected_status == 200:
        # Check static parts
        assert data["message"] == expected_response_text["message"]
        assert data["user"] == expected_response_text["user"]
        # Check tokens exist and are non-empty strings
        assert isinstance(data["access_token"], str) and data["access_token"]
        assert isinstance(data["refresh_token"], str) and data["refresh_token"]
    else:
        assert data == expected_response_text

@pytest.mark.parametrize(("expected_status, expected_response_text"), [(200, {"message": "Logout successful"})])
def test_user_logout(expected_status,expected_response_text,client):
    """Test user logout returns 200 everytime even if he is loggedin or logged out"""
    response = client.post('/logout')

    assert response.status_code == expected_status
    assert response.get_json() == expected_response_text