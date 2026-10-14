import os
from dotenv import load_dotenv
from pathlib import Path 

# define the global path 
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    # the secret key
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you_cant_see_me"
    # the path
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'database'/ 'safety.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

