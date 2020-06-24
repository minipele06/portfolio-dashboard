# app/__init__.py

import os
from dotenv import load_dotenv

load_dotenv()

Log_status = os.getenv("Log_status", default="out")
