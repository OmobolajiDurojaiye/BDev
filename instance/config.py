import os

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

MAIL_DEFAULT_SENDER = ("Bolaji's Portfolio", os.environ.get("MAIL_USERNAME"))
