from sqlalchemy import PrimaryKeyConstraint
from connectors.db import db

# Employee model
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column('Eid', db.Integer, primary_key=True)
    name = db.Column('EName', db.String(100), nullable=False)
    phone_no = db.Column('Ephone', db.String(10), unique=True, nullable=False)
    birth_date = db.Column('Ebirth_date', db.Date, nullable=False)
    gender = db.Column('Egender', db.String(10), nullable=False)
    description = db.Column('Edescription', db.Text, nullable=False)
    file_path = db.Column('Efile_path', db.String(255), nullable=True)
    password = db.Column('password', db.String(255), nullable=False)

    hobbies = db.relationship('EmployeeHobby', backref='employee', lazy=True)
    educations = db.relationship('EmployeeEducation', backref='employee', lazy=True)

# Hobby model
class Hobby(db.Model):
    __tablename__ = 'hobbies'
    id = db.Column('Hid', db.Integer, primary_key=True)
    name = db.Column('Hname', db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
# Employee-Hobby association model
class EmployeeHobby(db.Model):
    __tablename__ = 'employee_hobbies'
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.Eid'), nullable=False)
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.Hid'), nullable=False)

    # Define relationship to Hobby
    hobby = db.relationship('Hobby', backref='employee_hobbies', lazy=True)

    __table_args__ = (
        PrimaryKeyConstraint('employee_id', 'hobby_id'),
    )

# Education model
class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column('Eduid', db.Integer, primary_key=True)
    name = db.Column('Eduname', db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
         }

# Employee-Education association model
class EmployeeEducation(db.Model):
    __tablename__ = 'employee_educations'
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.Eid'), nullable=False)
    education_id = db.Column(db.Integer, db.ForeignKey('educations.Eduid'), nullable=False)

    # Define relationship to Education
    education = db.relationship('Education', backref='employee_educations', lazy=True)

    __table_args__ = (
        PrimaryKeyConstraint('employee_id', 'education_id'),
    )

# Users database
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)