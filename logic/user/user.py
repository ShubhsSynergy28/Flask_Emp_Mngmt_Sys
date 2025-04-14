from flask import jsonify,session, request
import bcrypt
from connectors.db import db

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
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('username', None)
    return jsonify({"message": "Logout successful"}), 200

def create_user():
    # Retrieve form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')  # Plain-text password from the user

    # Validate input
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if the email already exists
    if get_user_by_id(email):
        return jsonify({"error": "Email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create the user
    user = User(username=username, email=email, password=hashed_password.decode('utf-8'))
    add_user(user)

    # Commit the transaction
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": {"username": user.username, "email": user.email}}), 201