from models.education_model import get_all_educations
from models.hobby_model import get_all_hobbys
from flask import jsonify

def get_all_hobby():
    try:
        data = get_all_hobbys()
        return jsonify(data),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_education():
    try:
        data = get_all_educations()
        return jsonify(data),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
