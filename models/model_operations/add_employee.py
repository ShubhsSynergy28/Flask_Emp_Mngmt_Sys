from connectors.db import db

def add_employee(employee):
    db.session.add(employee)
