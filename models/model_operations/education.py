from models.models import Education, EmployeeEducation

def get_education(edu_name):
    return Education.query.filter_by(name=edu_name).first()

def get_employee_education(employee,edu):
    return EmployeeEducation(employee_id=employee.id, education_id=edu.id)

def delete_employee_education(employeeid):
    EmployeeEducation.query.filter_by(employee_id=employeeid).delete()
