from flask import jsonify

from models.model_operations.get_employee import get_employee

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
