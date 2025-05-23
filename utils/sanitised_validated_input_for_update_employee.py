from flask import request, jsonify
from html import escape
from datetime import datetime
from functools import wraps
from models.models import Employee
from models.employee_model import get_employee


def retrieve_validate_employee_data_for_update(func):
    @wraps(func)
    def wrapper(employeeid, *args, **kwargs):
        # Retrieve and sanitize form data
        if request.is_json:
            data = request.get_json()
            ename = data.get("name")
            ephone = data.get("phone_no")
            ebirth_date = data.get("birth_date")
            egender = data.get("gender")
            edescription = data.get("description")
            hobbies = data.get("hobbies").split(",") if data.get("hobbies") else []
            education = data.get("education").split(",") if data.get("education") else []
        else:
            # Retrieve and sanitize form data
            ename = request.form.get("name")
            ephone = request.form.get("phone_no")
            ebirth_date = request.form.get("birth_date")
            egender = request.form.get("gender")
            edescription = request.form.get("description")
            hobbies = request.form.get("hobbies").split(",") if request.form.get("hobbies") else []
            education = request.form.get("education").split(",") if request.form.get("education") else []

        ename = escape(ename.strip()) if ename else None
        ephone = ephone.strip() if ephone else None
        egender = escape(egender.strip()) if egender else None
        edescription = escape(edescription.strip()) if edescription else None
        hobbies = [escape(hobby.strip()) for hobby in hobbies]
        education = [escape(edu.strip()) for edu in education]

        # Validate and format birth_date
        if ebirth_date:
            try:
                formatted_birth_date = datetime.strptime(ebirth_date.strip(), "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        else:
            formatted_birth_date = None

        # Fetch the employee by ID
        employee = get_employee(employeeid)
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # Check if the phone number already exists for another employee
        if ephone and Employee.query.filter(Employee.phone_no == ephone, Employee.id != employeeid).first():
            return jsonify({"error": "Phone number already exists for another employee"}), 400

        # Pass the validated data to the wrapped function
        return func(
            employeeid=employeeid,
            ename=ename,
            ephone=ephone,
            formatted_birth_date=formatted_birth_date,
            egender=egender,
            edescription=edescription,
            hobbies=hobbies,
            education=education,
            employee=employee,
            *args,
            **kwargs,
        )

    return wrapper