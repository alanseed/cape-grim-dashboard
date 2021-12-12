import os
from flask import Flask, render_template, session
from flask_login import LoginManager 
from flask_cors import CORS  
from flask_bootstrap import Bootstrap

from app.auth.auth import bp as auth_bp 
from app.main.main import bp as main_bp 
from app.db import get_latest_chart 
from app.user import User

from . import db 
from . import chart 

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
@login_manager.user_loader 
def load_user(user_id):
        return User(user_id)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 
    CORS(app,support_credentials=True) 
    
    # make the name of the config file 
    basedir = os.path.abspath(os.path.dirname(__file__))
    config_name = os.path.join(basedir,"config.py")
    app.config.from_pyfile(config_name)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass

    # home page 
    @app.route('/')
    def index():
        date = get_latest_chart()
        if date is not None:
            session['date'] = date.strftime("%Y-%m-%d") 
        return render_template('main/index_met.html', init=True, date=date)

    db.init_app(app) 
    chart.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    login_manager.init_app(app) 
    Bootstrap(app) 
    return app