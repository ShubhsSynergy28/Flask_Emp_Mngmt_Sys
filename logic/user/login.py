from flask import jsonify, session, request
import bcrypt
from models.models import User  # Assuming you have a User model defined in your models.py


def login():
    # Retrieve form data
    email = request.form.get('email')
    password = request.form.get('password')  # Plain-text password from the user

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check user credentials in the database
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # Store user details in the session
        session['user_id'] = user.id
        session['email'] = user.email
        session['username'] = user.username
        return jsonify({"message": "Login successful", "user": {"username": user.username}}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401