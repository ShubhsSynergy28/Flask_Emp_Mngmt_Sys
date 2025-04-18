from tests.integration.conftest import *

@pytest.mark.parametrize(("username, email, password, expected_status_code, expected_response_JSON"),
[
    #"""Successful insertion of data"""
    ("Sam Wilson", "sam@gmail.com", "Sam@2002", 201, {"message": "User created successfully", "user": {"username": "Sam Wilson", "email": "sam@gmail.com"}}),
    # """Empty credentials should return status code as 400"""
    ("", "", "", 400, {"error": "Username, email, and password are required"}),
    ("", "", "Sam@2002", 400, {"error": "Username, email, and password are required"}),
    ("Sam Wilson", "", "", 400, {"error": "Username, email, and password are required"}),
    ("Sam Wilson", "sam@gmail.com", "", 400, {"error": "Username, email, and password are required"}),
    ("", "", "Sam@2002", 400, {"error": "Username, email, and password are required"}),
    
 ])
def test_create_user(username, email, password, expected_status_code, expected_response_JSON, client):
    """Test insertion or creation of users data returns JSON object """
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    data = { "username" : username,
             "email" : email,
             "password": password
            }
    response = client.post('/create-user', data=data)

    assert response.status_code == expected_status_code
    assert response.get_json() == expected_response_JSON