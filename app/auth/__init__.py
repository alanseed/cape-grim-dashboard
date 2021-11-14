import os
from flask import Flask, current_app
from flask_login import LoginManager, current_user 
from app.auth import bp as auth_bp 

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'cg-dashboard.sqlite'),
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


    # a simple page that says hello
    @app.route('/')
    def home_page():
        return current_app.send_static_file('index.html')

    from . import db
    db.init_app(app) 
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    login_manager.init_app(app)

    return app