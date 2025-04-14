from models.models import EmployeeHobby
from connectors.db import db

def get_employee_hobby(employee,hobby):
    return EmployeeHobby(employee_id=employee.id, hobby_id=hobby.id)

def add_employee_hobby(employee_hobby):
    db.session.add(employee_hobby)

def delete_employee_hobby(employeeid):
    EmployeeHobby.query.filter_by(employee_id=employeeid).delete()