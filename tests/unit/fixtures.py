import pytest
from flask import Flask
from logic.employee.employee import employee_login, employee_logout, create_employee, update_employee
from connectors.db import db
from flask_jwt_extended import JWTManager

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'
    # app.config["TESTING"] = True
    # app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['UPLOAD_FOLDER'] = 'D:\\LetsLearnPython&Flask\\Emp Mngmt Sys\\tests\\unit\\employee\\test_uploads'
    print("=========================", app.config['UPLOAD_FOLDER'])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    JWTManager(app)
    db.init_app(app)

    @app.route("/employee/login", methods=["POST"])
    def login_route():
        return employee_login()

    @app.route("/employee/logout", methods=["GET"])  # Or POST if your logout is POST
    def logout_route():
        return employee_logout()
    
    @app.route("/createEmployee", methods=["POST"])
    def create_employee_route():
        return create_employee()

    @app.route("/updateEmployee/<int:employeeid>", methods=["PUT"])
    # @retrieve_validate_employee_data_for_update
    def update_employee_route(*args, **kwargs):
        return update_employee(*args, **kwargs)
    
    with app.app_context():
       db.create_all()
    
    return app

