from flask import session, jsonify
from functools import wraps

def status():
    try:
        # Check if 'user_id' exists in the session
        if 'user_id' in session:
            return True
        else:
            return False
    except Exception:
        return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not status():
            return jsonify({"error": "Unauthorized access. Please log in."}), 401
        return f(*args, **kwargs)
    return decorated_function