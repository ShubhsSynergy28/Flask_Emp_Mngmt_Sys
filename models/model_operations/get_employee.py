from models.models import Employee

def get_employee(employeeid=None):
    if employeeid:
        return Employee.query.get(employeeid)

    else:
        return Employee.query.all()
