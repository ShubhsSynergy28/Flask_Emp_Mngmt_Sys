from functools import wraps
from flask import session, jsonify
from utils.check_login_status import check_login_status

def admin_or_employee_authorized(func):
    @wraps(func)
    def wrapper(employeeid=None, *args, **kwargs):
        # Check if the user is logged in as an admin
        if check_login_status():
            return func(*args, **kwargs)

        # Check if the user is logged in as an employee and authorized
        if 'employee_id' in session:
            if employeeid is None or session['employee_id'] == employeeid:
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "You are not authorized to access this data."}), 403

        # If neither condition is met, return unauthorized
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    return wrapper