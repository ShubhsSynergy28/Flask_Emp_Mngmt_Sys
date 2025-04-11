from flask import jsonify,session

def logout():
    # Clear the session
    session.clear()
    return jsonify({"message": "Logout successful"}), 200