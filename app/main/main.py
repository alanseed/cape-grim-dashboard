from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from app.db import get_db
bp = Blueprint('main', __name__, url_prefix='/main')

# Display the main page to the dashboard 
@bp.route('/index', methods=('GET', 'POST'))
def index():
    return render_template('main/index.html')
