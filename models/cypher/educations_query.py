GET_EDUCATION_BY_NAME="""
MATCH(edu: educations {Eduname: $edu_name})
RETURN edu
"""

GET_ALL_EDUCATIONS="""
MATCH(edu:educations)
RETURN edu
"""