from app import create_app
from app.db import User, close_db, init_db_command 
app = create_app() 
