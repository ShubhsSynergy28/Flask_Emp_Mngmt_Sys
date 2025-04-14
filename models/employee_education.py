from models.models import EmployeeEducation
from connectors.db import db

def get_employee_education(employee,edu):
    return EmployeeEducation(employee_id=employee.id, education_id=edu.id)

def add_employee_education(employee_education):
    db.session.add(employee_education)

def delete_employee_education(employeeid):
    EmployeeEducation.query.filter_by(employee_id=employeeid).delete()
