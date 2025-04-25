import os
from application import app
from dotenv import load_dotenv
from handlers.handler import *
from utils.set_folder_upload_path import *

# app=create_app()
load_dotenv()

if __name__ == '__main__':
    from pathlib import Path

    watched_files = [str(p) for p in Path("D:\\LetsLearnPython&Flask\\Emp Mngmt Sys").rglob("*.py")]
    app.debug = False
    host = os.environ.get('IP', os.getenv('IP'))
    port = int(os.environ.get('PORT', os.getenv('PORT')))
    app.run(host = host, port = port)