from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
env_name = path.join(basedir, '.env') 
load_dotenv(env_name)
DEBUG=True
FLASK_ENV='development'

SECRET_KEY=environ.get('SECRET_KEY')
DB_URI=environ.get('DB_URI')
DB_NAME=environ.get('DB_NAME') 

# USERNAME=environ.get('USERNAME')
# PASSWORD=environ.get('PASSWORD') 
# MONGO_USER=environ.get('MONGO_USER')
# MONGO_PASS=environ.get('MONGO_PASS')