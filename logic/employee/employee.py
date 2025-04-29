from flask import jsonify, request, session
from werkzeug.utils import secure_filename
import os
import redis
import uuid
from application import app
from connectors.db import db
from models.models import Employee
from flask_jwt_extended import  get_jwt
from utils.jwt_token_management import return_jwt_token,return_refresh_token

from utils.allowed_extentions import ALLOWED_EXTENSIONS
from utils.allowed_file import allowed_file
from utils.sanitised_validated_input_for_create_employee import retrieve_validate_employee_data_for_create
from utils.sanitised_validated_input_for_update_employee import retrieve_validate_employee_data_for_update
from utils.check_employee_credentials import check_employee_credentials

from models.employee_model import add_employee,get_employee,delete_emp
from models.employee_education import get_employee_education,add_employee_education,delete_employee_education
from models.employee_hobby import get_employee_hobby,add_employee_hobby,delete_employee_hobby
from models.education_model import get_education
from models.hobby_model import get_hobby

redis_client = redis.from_url(app.config['REDIS_URL'])

def get_all_employees():
    employees = get_employee()
    if not employees:
        return jsonify({"error": "No employees found"}), 404

    # Format the response
    result = []
    for employee in employees:
        result.append({
            "id": employee.id,
            "name": employee.name,
            "phone_no": employee.phone_no,
            "birth_date": str(employee.birth_date),
            "gender": employee.gender,
            "description": employee.description,
            "file_path": employee.file_path,
            "hobbies": [hobby.hobby.name for hobby in employee.hobbies],  # Get hobby names
            "education": [edu.education.name for edu in employee.educations]  # Get education names
        })

    return jsonify(result), 200

def get_employee_by_id(employeeid):
    employee = get_employee(employeeid)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    # Format the response
    result = {
        "id": employee.id,
        "name": employee.name,
        "phone_no": employee.phone_no,
        "birth_date": str(employee.birth_date),
        "gender": employee.gender,
        "description": employee.description,
        "file_path": employee.file_path,
        "hobbies": [hobby.hobby.name for hobby in employee.hobbies],  # Get hobby names
        "education": [edu.education.name for edu in employee.educations]  # Get education names
    }

    return jsonify(result), 200

@retrieve_validate_employee_data_for_create
def create_employee(ename, ephone, formatted_birth_date, egender, edescription, hobbies, education, password):
   
    # Create the employee
    employee = Employee(
        name=ename,
        phone_no=ephone,
        birth_date=formatted_birth_date,
        gender=egender,
        description=edescription,
        password=password
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
            # print(app.config["UPLOAD_FOLDER"])
            # print("=========================", app.config['UPLOAD_FOLDER'])

            # file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            file_path = os.path.join('D:/LetsLearnPython&Flask/Emp Mngmt Sys/tests/unit/employee/test_uploads', unique_filename) #qa
            
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
                add_employee_hobby(employee_hobby)
            else:
                return jsonify({"error": f"Hobby '{hobby_name}' does not exist"}), 400

        # Add education
        for edu_name in education:
            edu = get_education(edu_name)
            if edu:
                employee_education = get_employee_education(employee,edu)
                add_employee_education(employee_education)
            else:
                return jsonify({"error": f"Education '{edu_name}' does not exist"}), 400

    # Commit the transaction
    db.session.commit()

    return jsonify({"message": "Employee created successfully"}), 201

@retrieve_validate_employee_data_for_update
def update_employee(employeeid, ename, ephone, formatted_birth_date, egender, edescription, hobbies, education, employee):
      # Update employee details
    if ename:
        employee.name = ename
    if ephone:
        employee.phone_no = ephone
    if formatted_birth_date:
        employee.birth_date = formatted_birth_date
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

            # file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            file_path = os.path.join('D:/LetsLearnPython&Flask/Emp Mngmt Sys/tests/unit/employee/test_uploads', unique_filename) #qa
            
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

def delete_employee(employeeid):
    # Fetch the employee by ID
    employee = get_employee(employeeid)
    print(employee)
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
        delete_employee_education(employeeid)
        delete_employee_hobby(employeeid)
        # Delete the employee
        delete_emp(employee)
        # db.session.delete(employee)

    # Commit the transaction
    db.session.commit()

    return jsonify({"message": f"Employee with ID {employeeid} deleted successfully"}), 200

def employee_logout():
    jti = get_jwt()['jti']
    redis_client.set(jti, 'true', ex=app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    session.pop('employee_id', None)
    session.pop('employee_name', None)
    return jsonify({"message": "Employee logged out successfully"}), 200

def employee_login():
    if request.is_json:
        data = request.get_json()
        phone_no = data.get("phone_no")
        password = data.get("password")
    else:
        phone_no = request.form.get("phone_no")
        password = request.form.get("password")
       
    # Validate input
    if not phone_no or not password:
        return jsonify({"error": "Phone number and password are required"}), 400

    # Check employee credentials
    employee = check_employee_credentials(phone_no, password)
    if not employee:
        return jsonify({"error": "Invalid phone number or password"}), 401

    access_token = return_jwt_token(employee.phone_no,"employee")
    refresh_token = return_refresh_token(employee.phone_no)
    # Create a session for the employee
    session['employee_id'] = employee.id
    session['employee_name'] = employee.name
    session['role'] = "employee"
    response = jsonify({"message": "Employee login successful", "employee": {"id": employee.id, "name": employee.name}, 
                    "access_token": access_token,
                    "refresh_token": refresh_token})
    response.set_cookie(
            'access_token',  # Cookie name
            value=access_token,  # Value of the cookie
            max_age=60 * 60 * 24 * 7,  # 7 days
            secure=True,  # Set to True in production with HTTPS
            httponly=True,  # Prevent JavaScript access
            samesite='None'  # Adjust based on your cross-origin requirements
        )
    response.set_cookie(
            'refresh_token',  # Cookie name
            value=refresh_token,  # Value of the cookie
            max_age=60 * 60 * 24 * 7,  # 7 days
            secure=True,  # Set to True in production with HTTPS
            httponly=True,  # Prevent JavaScript access
            samesite='None'  # Adjust based on your cross-origin requirements
        )
    return  response, 200