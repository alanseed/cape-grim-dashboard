from flask import (
    Blueprint, g, render_template, request, session, url_for, current_app, jsonify
)
from app.db import get_user_id, get_chart, is_valid_date, get_latest_chart, add_chart
from app.user import User 
from app.chart import make_charts  
from app.auth.forms import DateForm
import datetime

bp = Blueprint('main', __name__, url_prefix='/main')


@bp.route('/chart')
def chart():
    chart_name = request.args.get("name")
    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date 

    start_time = datetime.datetime.fromisoformat(date)
    chart_data = get_chart(chart_name, start_time)

    response = jsonify(chart_data['Data'])
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@bp.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date 

    return render_template('main/index_met.html', init=True)


@bp.route('/test')
def test():
    return jsonify("test")


@bp.route('/met')
def met():
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date 

    return render_template('main/index_met.html', init=True, date=date)


@bp.route('/comp')
def comp():
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date 
       
    return render_template('main/index_comp.html', init=True, date=date)


@bp.route('/diag')
def diag():
    if 'username' in session:
        username = session['username']
        user_id = get_user_id(username)
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date

    return render_template('main/index_diag.html', init=True, date=date)

# set the session date


@bp.route('/setdate', methods=['GET', 'POST'])
def setdate():
    form = DateForm()
    if request.method == 'POST':
        date = form.date.data
        if is_valid_date(str(date)): 
            date_string = date.strftime("%Y-%m-%d")
            session['date'] = date_string
            return render_template('main/index_met.html', init=True, date=date_string)
        else:
            return render_template('main/setdate.html', form=form, title="Select chart date", message="Date not found")
    else:
        return render_template('main/setdate.html', form=form, title="Select chart date")

# make charts for a date 
# TO DO - Give progress updates to the user 
@bp.route('/adddate', methods=['GET','POST'])
def adddate():
    form = DateForm()
    if request.method == 'POST':
        date = form.date.data
        if is_valid_date(str(date)):
            return render_template('main/setdate.html', form=form, title="Add charts", message="Date already in database")
        else:
            date_string = date.strftime("%Y-%m-%d")
            session['date'] = date_string 
            make_charts(date_string)
            return render_template('main/index_met.html', init=True, date=date_string)
    else:
        return render_template('main/setdate.html', form=form, title="Select date for new charts")