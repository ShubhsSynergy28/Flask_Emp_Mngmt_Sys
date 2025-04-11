from models.models import Employee

def check_phone(ephone):
    return Employee.query.filter_by(phone_no=ephone).first()