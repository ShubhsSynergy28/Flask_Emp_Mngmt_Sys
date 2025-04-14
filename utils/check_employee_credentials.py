from models.models import Employee
from werkzeug.security import check_password_hash

def check_employee_credentials(phone_no, password):
    # Fetch the employee by phone number
    employee = Employee.query.filter_by(phone_no=phone_no).first()
    if employee and check_password_hash(employee.password, password):  # Compare hashed password
        return employee
    return None