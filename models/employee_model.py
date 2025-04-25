from connectors.db import db
from models.models import Employee

# Employee model
def add_employee(employee):
    db.session.add(employee)

def check_phone(ephone):
    return Employee.query.filter_by(phone_no=ephone).first()

def get_employee(employeeid=None):
    
    if employeeid:
        return db.session.get(Employee, employeeid)

    else:
        return Employee.query.all()


def delete_emp(employee):
    db.session.delete(employee)
