from models.models import User
from connectors.db import db

def get_user_by_id(email):
    return User.query.filter_by(email=email).first()

def get_all_user():
    return User.query.all()

def add_user(user):
    db.session.add(user)