import pytest
from application import app 
from models.user_model import User
from models.models import Employee

def test_test_data_creation(client):
    """Verify the test data was created properly"""
    with app.app_context():
        # Test user exists
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.username == 'testuser'
        
        # Test employee exists
        employee = Employee.query.filter_by(phone_no='1234567899').first()  # fixed phone_no
        assert employee is not None
        assert employee.name == 'Test Employee'

