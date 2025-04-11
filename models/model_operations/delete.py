from models.models import EmployeeHobby, EmployeeEducation

def delete_emp(employeeid):
    EmployeeHobby.query.filter_by(employee_id=employeeid).delete()
    EmployeeEducation.query.filter_by(employee_id=employeeid).delete()
