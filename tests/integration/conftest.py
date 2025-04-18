import pytest
from application import app
from connectors.db import db
from models.user_model import User
from models.models import Employee, Hobby, Education
import bcrypt
from datetime import datetime
import os
from handlers.handler import *
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['UPLOAD_FOLDER'] = 'tests/test_uploads'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            create_test_data()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Clean up upload folder
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def create_test_data():
    """Function to create initial test data"""
    hashed_password = bcrypt.hashpw(b'Securep@ss', bcrypt.gensalt()).decode('utf-8')
    user = User(username='testuser', email='test@example.com', password=hashed_password)
    db.session.add(user)

    employee_hashed_password = generate_password_hash('Securep@ss')
    ebirth_date = "28/05/2002"
    formatted_birth_date = datetime.strptime(ebirth_date, "%d/%m/%Y").date()

    employee = Employee(
        name='Test Employee',
        phone_no='1234567899',
        birth_date=formatted_birth_date,
        gender="male",
        description="Hey there its test user here",
        password=employee_hashed_password
    )
    db.session.add(employee)

    hobby1 = Hobby(name='test_Reading')
    hobby2 = Hobby(name='test_Sports')
    db.session.add_all([hobby1, hobby2])

    edu1 = Education(name='test_Bachelor')
    edu2 = Education(name='test_Master')
    db.session.add_all([edu1, edu2])

    db.session.commit()

@pytest.fixture
def auth_client(client):
    """Client with authenticated user session"""
    with client:
        client.post('/login', data={
            'email': 'test@example.com',
            'password': 'Securep@ss'
        })
        yield client
        client.post('/logout')

@pytest.fixture
def emp_auth_client(client):
    with client:
        client.post('/login-emp', data={
            'phone_no': '1234567899',
            'password': 'Securep@ss'
        })
        yield client
        client.post('/logout-emp')

