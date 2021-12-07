import os
from flask import Flask, render_template, session, g
from flask_login import LoginManager 
from flask_cors import CORS  
from flask_bootstrap import Bootstrap

from app.auth.auth import bp as auth_bp 
from app.main.main import bp as main_bp 
from app.data.data import bp as data_bp 
from app.auth.auth import close_user 
from app.db import close_db, get_latest_chart

from . import db 
from . import chart 

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
@login_manager.user_loader 
def load_user(user_id):
    return db.get_user(user_id)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) 
    CORS(app,support_credentials=True) 
    

    # make the name of the config file 
    basedir = os.path.abspath(os.path.dirname(__file__))
    config_name = os.path.join(basedir,"config.py")
    app.config.from_pyfile(config_name, silent=True)

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
    def index():
        close_user()
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date
        return render_template('main/index_diag.html', init=True, date=date)

    db.init_app(app) 
    chart.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(data_bp)
    login_manager.init_app(app) 
    Bootstrap(app) 
    return app