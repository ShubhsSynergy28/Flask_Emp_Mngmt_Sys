from flask import jsonify,session, request
import bcrypt

from models.user_model import *

def get_all_users():
    users = get_all_user()
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

def login():
    # Retrieve form data
    email = request.form.get('email')
    password = request.form.get('password')  # Plain-text password from the user

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check user credentials in the database
    user = get_user_by_id(email)

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # Store user details in the session
        session['user_id'] = user.id
        session['email'] = user.email
        session['username'] = user.username
        return jsonify({"message": "Login successful", "user": {"username": user.username}}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

def logout():
    # Clear the session
    session.clear()
    return jsonify({"message": "Logout successful"}), 200