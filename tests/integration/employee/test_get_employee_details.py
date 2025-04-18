from tests.integration.conftest import *

@pytest.mark.parametrize(("emp_id, field, url, log_email, log_password, expected_status_code"),
                         [
                            # """user accessing employee detail"""
                        (1,"email","/login","test@example.com","Securep@ss", 200),
                        # """employee accessing his.her own detail"""
                        (1,"phone_no","/login-emp","1234567899", "Securep@ss", 200),
                        # """wrong emp trying too access another emp detail"""
                        (1,"phone_no","/login-emp","1234567890", "Securep@sss", 401),
                        # """Accessing without any creds"""
                        (1,"","/login","","",401),
                        # """Wrong employee: employee not found"""
                        (2,"email","/login","test@example.com","Securep@ss", 404),
                        ])
def test_get_employee_by_id(emp_id, field, url, log_email, log_password, expected_status_code, client):
    """"Get employee details by id"""
    client.post(url, data={
        field : log_email,
        'password': log_password
    })
    response= client.get(f"/employee/{emp_id}")

    assert response.status_code == expected_status_code


@pytest.mark.parametrize(("field, url, log_email, log_password, expected_status_code"),
                         [
                        # """user accessing employee detail"""
                        ("email","/login","test@example.com","Securep@ss", 200),
                        # """employee accessing details"""
                        ("phone_no","/login-emp","1234567899", "Securep@ss", 403),
                        # """wrong emp trying too access another emp detail"""
                        ("phone_no","/login-emp","1234567890", "Securep@sss", 401),
                        # """Accessing without any creds"""
                        ("","/login","","",401),
                        ])
def test_get_all_employees(field, url, log_email, log_password, expected_status_code, client):
    """Get all employeess"""
    client.post(url, data={
        field : log_email,
        'password': log_password
    })

    response= client.get('/employees')

    assert response.status_code == expected_status_code