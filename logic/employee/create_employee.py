from flask import jsonify, request
from html import escape
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid
from application import app
from connectors.db import db
from models.models import Employee

from utils.allowed_extentions import ALLOWED_EXTENSIONS
from middleware.allowed_file import allowed_file

from models.model_operations.check_phone import check_phone
from models.model_operations.add_employee import add_employee
from models.model_operations.education import *
from models.model_operations.hobby import *

 

def create_employee():
    # Retrieve and sanitize form data
    ename = request.form.get("name")
    ebirth_date = request.form.get("birth_date")
    ephone = request.form.get("phone_no")
    egender = request.form.get("gender")
    edescription = request.form.get("description")
    hobbies = request.form.get("hobbies")
    education = request.form.get("education")

    ename = escape(ename.strip()) if ename else None
    ephone = ephone.strip() if ephone else None
    ebirth_date = ebirth_date.strip() if ebirth_date else None
    egender = escape(egender.strip()) if egender else None
    edescription = escape(edescription.strip()) if edescription else None
    hobbies = [escape(hobby.strip()) for hobby in hobbies.split(",")] if hobbies else []
    education = [escape(edu.strip()) for edu in education.split(",")] if education else []

    # Validate form data
    if not ename:
        return jsonify({"error": "Name is required and must contain only alphabetic characters"}), 400
    if not ephone or not ephone.isdigit() or len(ephone) != 10:
        return jsonify({"error": "Phone number is required and must be 10 numeric characters"}), 400
    if not ebirth_date:
        return jsonify({"error": "Birth date is required"}), 400
    if not egender:
        return jsonify({"error": "Gender is required"}), 400
    if not edescription:
        return jsonify({"error": "Description is required"}), 400

    # Validate and format the birth_date
    try:
        formatted_birth_date = datetime.strptime(ebirth_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Birth date must be in the format YYYY-MM-DD"}), 400

    # Check if the phone number already exists
    if check_phone(ephone):
        return jsonify({"error": "Phone number already exists"}), 400

    # Create the employee
    employee = Employee(
        name=ename,
        phone_no=ephone,
        birth_date=formatted_birth_date,
        gender=egender,
        description=edescription,
    )

    # Handle file upload
    if "file" in request.files:
        file = request.files["file"]
        if file.filename != "":
            if not allowed_file(file.filename):
                return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
            unique_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            unique_filename = f"{unique_id}_{filename}"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            file.save(file_path)
            employee.file_path = file_path

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        # Add the employee to the session
        add_employee(employee)
        db.session.flush()  # Flush to get the employee ID

        # Add hobbies
        for hobby_name in hobbies:
            hobby = get_hobby(hobby_name)
            if hobby:
                employee_hobby = get_employee_hobby(employee,hobby)
                db.session.add(employee_hobby)
            else:
                return jsonify({"error": f"Hobby '{hobby_name}' does not exist"}), 400

        # Add education
        for edu_name in education:
            edu = get_education(edu_name)
            if edu:
                employee_education = get_employee_education(employee,edu)
                db.session.add(employee_education)
            else:
                return jsonify({"error": f"Education '{edu_name}' does not exist"}), 400

    # Commit the transaction
    db.session.commit()

    return jsonify({"message": "Employee created successfully"}), 201