RELATE_HOBBIES_WITH_EMPLOYEES="""
MATCH(e:employees {EName: $employee_name})
MATCH(h:hobbies {Hname: $hobby_name})
CREATE(e)-[:Has_Hobbies]->(h)
"""