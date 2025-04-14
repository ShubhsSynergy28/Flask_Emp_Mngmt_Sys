from flask import session, jsonify

def login_required():
    try:
        # Check if 'user_id' exists in the session
        if 'user_id' in session:
            return True
        else:
            return jsonify({"error": "Unauthorized access. Please log in."}), 401
    except Exception:
        return jsonify({"error": "An error occurred while checking login status."}), 500