from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
env_name = path.join(basedir, '.env') 
print(env_name)
load_dotenv(env_name)
DEBUG=True
FLASK_ENV='development'

SECRET_KEY=environ.get('SECRET_KEY')
USERNAME=environ.get('USERNAME')
PASSWORD=environ.get('PASSWORD') 
MONGO_USER=environ.get('MONGO_USER')
MONGO_PASS=environ.get('MONGO_PASS')
print(f" Secret key = {SECRET_KEY}") 