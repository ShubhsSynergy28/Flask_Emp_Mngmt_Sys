from flask import jsonify
from application import app  

from logic.employee.create_employee import create_employee
from logic.employee.get_all_employees import get_all_employees
from logic.employee.get_employee_by_id import get_employee_by_id
from logic.employee.update_employee import update_employee
from logic.employee.delete_employee import delete_employee

from middleware.check_login_status import login_required
from utils.set_folder_upload_path import *


@app.route('/createEmployee', methods=['POST'])
@login_required
def handle_create_employee():
    try:
        return create_employee()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/employees', methods=['GET'])
@login_required
def handle_get_employees():
    try:
        return get_all_employees()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employee/<int:employeeid>', methods=['GET'])
@login_required
def handle_get_employee_by_id(employeeid):
    try:
        return get_employee_by_id(employeeid)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500   


@app.route('/update-employee/<int:employeeid>', methods=['PUT'])
@login_required
def handle_update_employee(employeeid):
    try:
        return update_employee(employeeid)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/employee/<int:employeeid>', methods=['DELETE'])
@login_required
def handle_delete_employee(employeeid):
    try:
        return delete_employee(employeeid)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
