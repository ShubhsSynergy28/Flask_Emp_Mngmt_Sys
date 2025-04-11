from models.models import Hobby, EmployeeHobby

def get_hobby(hobby_name):
    return Hobby.query.filter_by(name=hobby_name).first()

def get_employee_hobby(employee,hobby):
    return EmployeeHobby(employee_id=employee.id, hobby_id=hobby.id)

def delete_employee_hobby(employeeid):
    EmployeeHobby.query.filter_by(employee_id=employeeid).delete()