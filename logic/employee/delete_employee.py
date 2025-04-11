from flask import jsonify
from models.models import db
from models.model_operations.delete import delete_emp
from models.model_operations.get_employee import get_employee
import os

def delete_employee(employeeid):
    # Fetch the employee by ID
    employee = get_employee(employeeid)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    # Delete the associated file if it exists
    if employee.file_path and os.path.exists(employee.file_path):
        try:
            os.remove(employee.file_path)
        except Exception as e:
            return jsonify({"error": f"Failed to delete associated file: {str(e)}"}), 500

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        # Delete associated hobbies and education using composite keys
        delete_emp(employeeid)
        # Delete the employee
        db.session.delete(employee)

    # Commit the transaction
    db.session.commit()

    return jsonify({"message": f"Employee with ID {employeeid} deleted successfully"}), 200