CREATE_USER="""
CREATE(u:users {username: $username, password: $password, email: $email, id: $id})
"""

GET_USER_BY_EMAIL="""
MATCH(u:users {email: $email})
RETURN u
"""

GET_ALL_USERS="""
MATCH(u:users)
RETURN u
"""
