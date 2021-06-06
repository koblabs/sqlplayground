from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY") or "secret_key"

    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_PORT = int(environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    ADMINS = environ.get("MAIL_ADMINS") or ["koowusuboaky@gmail.com"]
