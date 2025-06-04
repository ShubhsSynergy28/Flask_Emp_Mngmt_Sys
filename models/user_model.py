from models.models import User
from connectors.db import db
from connectors.db import neo4j

from models.cypher.user_query import CREATE_USER, GET_USER_BY_EMAIL,GET_ALL_USERS

import uuid


def get_user_by_id(email):
    result = neo4j.run_query(GET_USER_BY_EMAIL, {"email": email})
    if result:
        return User(**result[0]["u"])  # Convert dict to User instance
    return None
    # print(User.query.filter_by(email=email).first())
    # return User.query.filter_by(email=email).first() # sql

def get_all_user():
    raw_results = neo4j.run_query(GET_ALL_USERS)
    # users = [record['id'] for record in raw_results]
    # print(User(**record['u']) for record in raw_results)
    return [User(**record['u']) for record in raw_results]

    # print(User.query.all())
    # return User.query.all() #SQL

def add_user(user):
    params_for_neo4j= {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    neo4j.run_query(CREATE_USER, params_for_neo4j)
    db.session.add(user)