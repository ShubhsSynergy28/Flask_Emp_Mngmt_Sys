from flask import jsonify,session, request
import bcrypt
from connectors.db import db
from flask_jwt_extended import  get_jwt
import redis

from application import app

from models.user_model import *

from utils.jwt_token_management import  return_jwt_token, return_refresh_token
# from flask_jwt_extended import set_access_cookies, set_refresh_cookies

# redis_client = redis.from_url(app.config['REDIS_URL'])


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
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')  # Plain-text password from the user

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check user credentials in the database
    user = get_user_by_id(email)

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = return_jwt_token(user.email,"admin")
        refresh_token = return_refresh_token(user.email)
        
        # Store user details in the session
        session['user_id'] = user.id
        session['email'] = user.email
        session['username'] = user.username
        session['role'] =  "admin"

        response = jsonify({
            "message": "Login successful",
            "user": {"username": user.username},
            "access_token": access_token,
            "refresh_token": refresh_token
        }) 
        # response.set_cookie(
        #     'access_token_cookie',  # Cookie name
        #     value=access_token,  # Value of the cookie
        #     max_age=60 * 60 * 24 * 7,  # 7 days
        #     secure=False,  # Set to True in production with HTTPS
        #     httponly=True,  # Prevent JavaScript access
        #     samesite='Lax'  # Adjust based on your cross-origin requirements
        # )
        # response.set_cookie(
        #     'refresh_token_cookie',  # Cookie name
        #     value=refresh_token,  # Value of the cookie
        #     max_age=60 * 60 * 24 * 7,  # 7 days
        #     secure=False,  # Set to True in production with HTTPS
        #     httponly=True,  # Prevent JavaScript access
        #     samesite='Lax'  # Adjust based on your cross-origin requirements
        # )
          
        return response, 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401

def logout():
    try:
        # jti = get_jwt()['jti']
        # redis_client.set(jti, 'true', ex=app.config['JWT_ACCESS_TOKEN_EXPIRES'])
        session.pop('user_id', None)
        session.pop('email', None)
        session.pop('username', None)
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        print(f"Error during logout: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

def create_user():
    # Retrieve and clean form data
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()  # Plain-text password from the user

    # Validate input
    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if the email already exists
    if get_user_by_id(email):
        return jsonify({"error": "Email already exists"}), 400
    
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create the user
    user = User(username=username, email=email, password=hashed_password.decode('utf-8'))
    add_user(user)

    # Commit the transaction
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": {"username": user.username, "email": user.email}
    }), 201
