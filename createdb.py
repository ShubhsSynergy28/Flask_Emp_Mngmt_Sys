from application import app
from connectors.db import db

# Push the application context
with app.app_context():
    db.create_all()