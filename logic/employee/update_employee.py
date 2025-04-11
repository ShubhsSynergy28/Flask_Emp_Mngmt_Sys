from flask import jsonify, request
from html import escape
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid
from application import app
from models.models import db, Employee
from middleware.allowed_file import allowed_file
from models.model_operations.education import *
from models.model_operations.hobby import *
from utils.allowed_extentions import ALLOWED_EXTENSIONS


def update_employee(employeeid):
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
            ebirth_date = datetime.strptime(ebirth_date.strip(), "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Fetch the employee by ID
    employee = Employee.query.get(employeeid)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    # Check if the phone number already exists for another employee
    if ephone and Employee.query.filter(Employee.phone_no == ephone, Employee.id != employeeid).first():
        return jsonify({"error": "Phone number already exists for another employee"}), 400

    # Update employee details
    if ename:
        employee.name = ename
    if ephone:
        employee.phone_no = ephone
    if ebirth_date:
        employee.birth_date = ebirth_date
    if egender:
        employee.gender = egender
    if edescription:
        employee.description = edescription

    # Handle file upload
    if "file" in request.files:
        file = request.files["file"]
        if file.filename != "":
            if not allowed_file(file.filename):
                return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400

            # Delete the previous file if it exists
            if employee.file_path and os.path.exists(employee.file_path):
                try:
                    os.remove(employee.file_path)
                except Exception as e:
                    return jsonify({"error": f"Failed to delete previous file: {str(e)}"}), 500

            # Save the new file
            unique_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            unique_filename = f"{unique_id}_{filename}"

            file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            file.save(file_path)
            employee.file_path = file_path

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        # Update hobbies
        delete_employee_hobby(employeeid)
        for hobby_name in hobbies:
            hobby = get_hobby(hobby_name)
            if hobby:
                employee_hobby = get_employee_hobby(employee, hobby)
                db.session.add(employee_hobby)
            else:
                return jsonify({"error": f"Hobby '{hobby_name}' does not exist"}), 400

        # Update education
        delete_employee_education(employeeid)
        for edu_name in education:
            edu = get_education(edu_name)
            if edu:
                employee_education = get_employee_education(employee, edu)
                db.session.add(employee_education)
            else:
                return jsonify({"error": f"Education '{edu_name}' does not exist"}), 400

    # Commit the transaction
    db.session.commit()

    return jsonify({"message": "Employee updated successfully"}), 200