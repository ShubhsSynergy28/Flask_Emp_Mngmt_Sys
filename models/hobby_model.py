from models.models import Hobby

def get_hobby(hobby_name):
    return Hobby.query.filter_by(name=hobby_name).first()
