from flask import jsonify,session
from application import app  

from logic.employee.employee import *
from logic.user.user import *

# from utils.check_login_status import login_required
from utils.set_folder_upload_path import *
from utils.admin_or_employee_authorization import admin_or_employee_authorized

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

@app.route('/logout', methods=['POST'])
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
@admin_or_employee_authorized
# @login_required
def handle_create_employee():
    try:
        return create_employee()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/employees', methods=['GET'])
@admin_or_employee_authorized
# @login_required
def handle_get_employees():
    try:
        return get_all_employees()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employee/<int:employeeid>', methods=['GET'])
@admin_or_employee_authorized
# @login_required
def handle_get_employee_by_id(employeeid):
    try:
        return get_employee_by_id(employeeid)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500   


@app.route('/update-employee/<int:employeeid>', methods=['PUT'])
@admin_or_employee_authorized
# @login_required
def handle_update_employee(employeeid):
    try:
        return update_employee(employeeid)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/delete-employee/<int:employeeid>', methods=['DELETE'])
@admin_or_employee_authorized
def handle_delete_employee(employeeid):
    try:
        return delete_employee(employeeid)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login-emp', methods=['POST'])
def handle_employee_login():
    try:
        pass
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route('/logout-emp', methods=['POST'])
def handle_employee_logout():
    try:
        return employee_logout()
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500