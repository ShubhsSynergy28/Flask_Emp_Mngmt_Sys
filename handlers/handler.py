from flask import jsonify,session
from application import app  
import traceback
from flask_jwt_extended import get_jwt_identity, jwt_required


from logic.employee.employee import *
from logic.user.user import *
from logic.educationHobby.fetch_education_hobby import *

from utils.set_folder_upload_path import *
from utils.is_admin_or_employee_authorization import admin_or_employee_authorized
from utils.jwt_token_management import return_jwt_token

from models.user_model import get_user_by_id
from models.employee_model import check_phone
# from models.education_model import get_all_educations
# from models.hobby_model import get_all_hobby

# from flask_jwt_extended import jwt_refresh_token_required


@app.route('/users', methods=['GET'])
def handle_get_users():
    try:
        return get_all_users()
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/login', methods=['POST'])
def handle_user_login():
    try:
       return login()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['POST'], endpoint='user_logout')
# @jwt_required()
def handle_user_logout():
    try:
        return logout()

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/status', methods=['GET'])
def status():
    try:
        if 'user_id' in session:
            return jsonify({"logged_in": True, "user": {"id": session['user_id'], "username": session['username']}}), 200
        else:
            return jsonify({"logged_in": False}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/createEmployee', methods=['POST'])
# @admin_or_employee_authorized
def handle_create_employee():
    try:
        return create_employee()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/employees', methods=['GET'])
# @admin_or_employee_authorized
def handle_get_employees():
    try:
        return get_all_employees()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employee/<int:employeeid>', methods=['GET'])
# @admin_or_employee_authorized
def handle_get_employee_by_id(employeeid):
    try:
        return get_employee_by_id(employeeid)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500   


@app.route('/update-employee/<int:employeeid>', methods=['PUT'])
# @admin_or_employee_authorized
def handle_update_employee(employeeid):
    try:
        return update_employee(employeeid)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/delete-employee/<int:employeeid>', methods=['DELETE'])
# @admin_or_employee_authorized
def handle_delete_employee(employeeid):
    try:
        return delete_employee(employeeid)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login-emp', methods=['POST'])
def handle_employee_login():
    try:
        return employee_login()
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
        
@app.route('/logout-emp', methods=['POST'], endpoint='logout_employee')
# @jwt_required()
def handle_employee_logout():
    try:
        return employee_logout()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/create-user', methods=['POST'])
def handle_create_user():
    try:
        return create_user()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get-all-available-educations', methods=['GET'])
def get_education():
    print("hi")
    try:
        return get_all_education()  # Return the result as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-all-available-hobbies', methods=['GET'])
def get_hobbies():
    try:
        return get_all_hobby() # Return the result as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/refresh', methods=['POST'])
def refresh():
    current_user = get_jwt_identity()
    user = get_user_by_id(current_user)
    employee = check_phone(current_user)
    if user:
        new_token = return_jwt_token(current_user, "admin")
    else:
        new_token = return_jwt_token(current_user, "employee")
    return jsonify({"access_token": new_token})

@app.route('/protected', methods=['GET'])
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200





        

# @app.route('/token', methods=['POST'])
# def create_jwt_token():
#     try:
#         return return_created_jwt()
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500