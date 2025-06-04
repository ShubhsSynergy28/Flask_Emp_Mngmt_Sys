import json

class SnowEmployee:
    def __init__(self, row):
        self.id = row['EID']
        self.name = row['ENAME']
        self.phone_no = row['EPHONE']
        self.birth_date = row['EBIRTH_DATE']
        self.gender = row['EGENDER']
        self.description = row['EDESCRIPTION']
        self.file_path = row['EFILE_PATH']
        self.password = row['PASSWORD']

        # Convert hobbies and education from JSON string to Python list
        self.hobbies = json.loads(row['HOBBIES']) if row['HOBBIES'] else []
        self.educations = json.loads(row['EDUCATIONS']) if row['EDUCATIONS'] else []
