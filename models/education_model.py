from models.models import Education

def get_education(edu_name):
    return Education.query.filter_by(name=edu_name).first()

