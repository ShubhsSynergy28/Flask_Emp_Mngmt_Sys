from flask import jsonify
from models.models import User  # Assuming you have a User model defined in your models.py


def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"error": "No users found"}), 404

    # Format the response
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    return jsonify(result), 200