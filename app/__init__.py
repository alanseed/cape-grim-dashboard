import os
from flask import Flask, render_template
from app.auth.auth import bp as auth_bp 
import os
from flask import Flask, current_app
from flask_login import LoginManager
from . import db 

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader 
def load_user(user_id):
    return get_user(user_id)

def get_user(user_id): 
    user = db.get_db()["users"]
    myquery = { "_id":user_id}
    myuser = user.find_one(myquery) 
    return myuser

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        USERNAME='admin',
        PASSWORD='admin'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    # home page 
    @app.route('/')
    def home_page():
        return render_template('main/index.html')

    db.init_app(app) 
    
    app.register_blueprint(auth_bp)
    login_manager.init_app(app) 

    return app