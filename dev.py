import os
from application import app
from dotenv import load_dotenv
from handlers.handle_employee import *
from handlers.handle_user import * 
from tests.test_connection_db import * 
from utils.set_folder_upload_path import *

# app=create_app()
load_dotenv()

if __name__ == '__main__':
    app.debug = False
    host = os.environ.get('IP', os.getenv('IP'))
    port = int(os.environ.get('PORT', os.getenv('PORT')))
    app.run(host = host, port = port)