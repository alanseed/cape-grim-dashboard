from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

DEBUG=True
FLASK_ENV='development'

SECRET_KEY=environ.get('SECRET_KEY')
USERNAME=environ.get('USERNAME')
PASSWORD=environ.get('PASSWORD') 
MONGO_USER=environ.get('MONGO_USER')
MONGO_PASS=environ.get('MONGO_PASS')
