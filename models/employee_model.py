from connectors.db import db
from models.models import Employee
from connectors.db import snowflake
from models.query.query_employee import *

from models.models_for_snowflake import SnowEmployee

# Employee model
def add_employee(employee):
    db.session.add(employee) #xampp
    query= CREATE_EMPLOYEE.format(ename=employee.name, ephone= employee.phone_no, birth_date=employee.birth_date, gender=employee.gender, description=employee.description, password=employee.password, file_path=employee.file_path)
    snowflake.query(query) #SnowFlaKE 

def check_phone(ephone):
    return Employee.query.filter_by(phone_no=ephone).first()

def get_employee(employeeid=None):
    
    if employeeid:
        query = READ_EMPLOYEE_BY_ID.format(eid = employeeid)
        # print(snowflake.query(query))
        # print(db.session.get(Employee, employeeid))
        result = snowflake.query(query)
        return SnowEmployee(result[0]) if result else None
        # return db.session.get(Employee, employeeid) #xampp

    else:
        # print(snowflake.query(READ_EMPLOYEES))
        # print(Employee.query.all())
        results = snowflake.query(READ_EMPLOYEES)
        return [SnowEmployee(row) for row in results]
        # return Employee.query.all()#xampp

def delete_emp(employee):
    # db.session.delete(employee) #xampp
    # print(employee)
    query = DELETE_EMPLOYEE_BY_ID.format(eid=employee)
    snowflake.query(query)

def update_emp(employeeid, ename, ephone, formatted_birth_date, egender, edescription,file_path):
    query = UPDATE_EMPLOYEE.format(ename=ename,ephone=ephone,gender=egender,description=edescription,birth_date=formatted_birth_date,file_path=file_path,eid=employeeid)
    snowflake.query(query)