GET_HOBBY_BY_NAME="""
MATCH(h:hobbies {Hname: $hobby_name})
RETURN h
"""

GET_ALL_HOBBIES="""
MATCH(h:hobbies)
RETURN h
"""