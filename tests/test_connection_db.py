from flask import jsonify
from application import app
from connectors.db import db
from sqlalchemy.sql import text  # Import the text function

@app.route('/test-db')
def test_db():
    try:
        # Test the database connection by executing a simple query
        db.session.execute(text("SELECT 1"))  # Wrap the raw SQL query in text()
        return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500