from flask import jsonify

from models.model_operations.get_employee import get_employee

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