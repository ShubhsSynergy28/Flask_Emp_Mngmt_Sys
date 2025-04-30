from flask import Flask
from flask_cors import CORS 
import secrets
# from datetime import timedelta  # Import timedelta for session expiration
from flask_jwt_extended import JWTManager
import datetime
import redis
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_session import Session
import bcrypt
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
app.config["JWT_SECRET_KEY"]= "standardkey"
app.secret_key = secrets.token_hex(16)

CORS(
    app, 
    resources={r"/*": {"origins": "http://localhost:5173"}},  # Your React URL
    supports_credentials=True
)

app.config['JWT_SECRET_KEY'] =os.getenv('SECRET_KEY_FOR_JWT')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=150000)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)
# app.config['JWT_COOKIE_SECURE'] = True
# app.config['JWT_ACCESS_COOKIE_NAME'] = "access_token_cookie"  # Add this line
# app.config['JWT_REFRESH_COOKIE_NAME'] = "refresh_token_cookie"  # Optional, if using refresh tokens
# app.config['REDIS_URL'] = 'redis://redis:6379/0'
# app.config['REDIS_URL'] = 'redis://redis:6379/0'



# bcrypt = Bcrypt(app)

jwt = JWTManager(app)
# app.config.update(
#     SESSION_COOKIE_NAME='session',
#     SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access for security
#     SESSION_COOKIE_SECURE=True,    # Only send over HTTPS
#     SESSION_COOKIE_SAMESITE='Lax',  # or 'None' if cross-site
#     PERMANENT_SESSION_LIFETIME=timedelta(days=7)  # Set expiration
# )