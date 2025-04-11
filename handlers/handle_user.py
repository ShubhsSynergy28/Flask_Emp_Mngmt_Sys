from flask import jsonify,session
from application import app  

from logic.user.login import login
from logic.user.logout import logout
from logic.user.get_all_users import get_all_users


@app.route('/users', methods=['GET'])
def handle_get_users():
    try:
        return get_all_users()
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/login', methods=['POST'])
def handle_user_login():
    try:
       return login()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout', methods=['POST'])
def handle_user_logout():
    try:
        return logout()

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/status', methods=['GET'])
def status():
    try:
        if 'user_id' in session:
            return jsonify({"logged_in": True, "user": {"id": session['user_id'], "username": session['username']}}), 200
        else:
            return jsonify({"logged_in": False}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500