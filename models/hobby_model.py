from models.models import Hobby

def get_hobby(hobby_name):
    return Hobby.query.filter_by(name=hobby_name).first()

def get_all_hobbys():
    hobbys = Hobby.query.all()
    return [hobby.to_dict() for hobby in hobbys]
    
