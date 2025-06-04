RELATE_EDUCATIONS_WITH_EMPLOYEES="""
MATCH(e:employees {EName: $employee_name})
MATCH(edu:educations {Eduname: $edu_name})
CREATE(e)-[:Has_Educations]->(edu)
"""