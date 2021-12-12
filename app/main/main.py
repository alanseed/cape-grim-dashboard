# Routes to manage the views for the various charts  

from flask import (
    Blueprint, g, render_template, request, session, url_for, current_app, jsonify
) 
from flask_login import login_required,current_user 

from app.db import get_chart, is_valid_date, get_latest_chart, get_dates 
from app.user import User 
from app.chart import make_charts  
from app.main.forms import DateForm
import datetime

bp = Blueprint('main', __name__, url_prefix='/main') 

@bp.route('/chart_date', methods=['GET','POST'])
def chart_date(): 
    start = request.args.get("start") 
    end = request.args.get("end") 
    dates = get_dates(start,end) 
    response = jsonify(dates)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 

# Returns the JSON data for the chart from the cache 
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

# return the view with the weather (meteorological) observations 
@bp.route('/met')
def met():

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date 

    return render_template('main/index_met.html', init=True, date=date)

# return the view with the atmospheric composition (the gasses in the air) observations 
@bp.route('/comp')
def comp():

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date 
       
    return render_template('main/index_comp.html', init=True, date=date)

# return the view with the diagnostics for the various instruments 
@bp.route('/diag')
def diag():

    if 'date' in session:
        date = session['date']
    else:
        date = get_latest_chart().strftime("%Y-%m-%d")
        session['date'] = date

    return render_template('main/index_diag.html', init=True, date=date)


# select a new date for the charts 
@bp.route('/setdate', methods=['GET', 'POST'])
@login_required
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

# Add new charts to the cache 
@bp.route('/adddate', methods=['GET','POST']) 
@login_required
def adddate():
    if current_user.administrator:
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
    else:
        return ("<h1>Access denied: Do not have admin role</h1>") 
