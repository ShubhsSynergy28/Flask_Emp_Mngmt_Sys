from functools import wraps
from flask import session, jsonify
from utils.check_login_status import login_required

def admin_or_employee_authorized(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the user is logged in as an admin
        if 'user_id' in session:  # Admin login
            return func(*args, **kwargs)

        # Check if the user is logged in as an employee
        if 'employee_id' in session:  # Employee login
            # Restrict access to endpoints that are not allowed for employees
            restricted_endpoints = ['handle_create_employee', 'handle_get_employees']
            if func.__name__ in restricted_endpoints:
                return jsonify({"error": "You are not authorized to access this endpoint."}), 403

            # Allow access to endpoints specific to the logged-in employee
            employeeid = kwargs.get('employeeid')  # Get employeeid from kwargs
            if employeeid is None or session['employee_id'] == employeeid:
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "You are not authorized to access this data."}), 403

        # If neither admin nor employee is logged in, return unauthorized
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    return wrapper