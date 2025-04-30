from models.models import Education

def get_education(edu_name):
    return Education.query.filter_by(name=edu_name).first()

def get_all_educations():
    educations = Education.query.all()
    return  [education.to_dict() for education in educations]