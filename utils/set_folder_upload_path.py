from application import app
import os
from dotenv import load_dotenv

load_dotenv()

# app = create_app()

UPLOAD_FOLDER = os.getenv('UPLOAD_PATH')
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER