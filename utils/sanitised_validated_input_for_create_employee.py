from flask import request, jsonify
from html import escape
from datetime import datetime
from functools import wraps
from models.employee_model import check_phone
from werkzeug.security import generate_password_hash 


def retrieve_validate_employee_data_for_create(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve and sanitize form data
        ename = request.form.get("name")
        ephone = request.form.get("phone_no")
        ebirth_date = request.form.get("birth_date")
        egender = request.form.get("gender")
        edescription = request.form.get("description")
        password = request.form.get("password")
        hobbies = request.form.get("hobbies")
        education = request.form.get("education")

        ename = escape(ename.strip()) if ename else None
        ephone = ephone.strip() if ephone else None
        ebirth_date = ebirth_date.strip() if ebirth_date else None
        egender = escape(egender.strip()) if egender else None
        edescription = escape(edescription.strip()) if edescription else None
        password = generate_password_hash(escape(password.strip())) if password else None
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
        if not password:
            return jsonify({"error":"Password is required!"}), 400
        if not hobbies:
            return jsonify({"error": "Hobbies are required"}), 400
        if not education:
            return jsonify({"error": "Education is required"}), 400

        # Validate and format the birth_date
        try:
            formatted_birth_date = datetime.strptime(ebirth_date, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Birth date must be in the format YYYY-MM-DD"}), 400

        # Check if the phone number already exists
        if check_phone(ephone):
            return jsonify({"error": "Phone number already exists"}), 400

        # Pass the validated data to the wrapped function
        return func(
            ename=ename,
            ephone=ephone,
            formatted_birth_date=formatted_birth_date,
            egender=egender,
            edescription=edescription,
            hobbies=hobbies,
            education=education,
            password=password,
            *args,
            **kwargs,
        )

    return wrapper