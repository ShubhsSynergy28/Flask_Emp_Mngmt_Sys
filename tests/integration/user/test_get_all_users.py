from tests.integration.conftest import *

@pytest.mark.parametrize(("expected_status_code"),[(200)])
def test_get_user_details(expected_status_code, client):
    response = client.get('/users')
    assert response.status_code == expected_status_code