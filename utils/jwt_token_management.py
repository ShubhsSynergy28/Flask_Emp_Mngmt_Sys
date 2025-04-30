from flask_jwt_extended import  (
    create_access_token, create_refresh_token
)
# import redis
from application import jwt,app

# redis_client = redis.from_url(app.config['REDIS_URL'])
# print(redis_client.ping()) 

def return_jwt_token(identity, role="employee"):
    return create_access_token(identity=identity, additional_claims={"role":role})

def return_refresh_token(identity):
    return create_refresh_token(identity=identity)

# @jwt.token_in_blocklist_loader
# def check_if_token_in_blocklist(jwt_header, jwt_payload):
#     try:
#         jti = jwt_payload["jti"]  # Extract the unique identifier for the token
#         token_in_blocklist = redis_client.get(jti)  # Check if the token is in Redis
#         return token_in_blocklist is not None
#     except redis.exceptions.ConnectionError as e:
#         print(f"Redis connection error: {e}")
#         return False