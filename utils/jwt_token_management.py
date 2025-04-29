from flask_jwt_extended import  (
    create_access_token, create_refresh_token
)
import redis
from application import jwt,app

redis_client = redis.from_url(app.config['REDIS_URL'])

def return_jwt_token(identity, role="employee"):
    return create_access_token(identity=identity, additional_claims={"role":role})

def return_refresh_token(identity):
    return create_refresh_token(identity=identity)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_client.get(jti)
    return entry is not None
