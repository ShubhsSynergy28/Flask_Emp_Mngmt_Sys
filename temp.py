from models.models import Employee
from werkzeug.security import generate_password_hash
from connectors.db import db

def temp():
    # Fetch all employees
    employees = Employee.query.all()

    # Hash plain-text passwords
    for employee in employees:
        if employee.password:  # Ensure the password is not empty
            employee.password = generate_password_hash(employee.password)

# Commit the changes
    db.session.commit()
    print("All passwords have been hashed successfully.")