from flask_sqlalchemy import SQLAlchemy
from application import app  
from dotenv import load_dotenv
import os
import secrets

load_dotenv()
app.secret_key = secrets.token_hex(16)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)