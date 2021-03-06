import os

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.environ.get("SECRET_KEY", "DEV")
SQLALCHEMY_TRACK_MODIFICATIONS = "False"
SQLALCHEMY_ECHO = False
