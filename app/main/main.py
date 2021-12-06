from flask import (
    Blueprint, flash, g, render_template, request, session, url_for, current_app, jsonify
)
from app.db import User, get_user_id, get_chart
import datetime 

bp = Blueprint('main', __name__, url_prefix='/main')

@bp.route('/chart',methods=('GET', 'POST'))
def chart():
    chart_name = request.args.get("chart_name") 
    start = "2021-06-01" 
    start_time = datetime.datetime.fromisoformat(start)  
    chart_data = get_chart(chart_name, start_time) 

    response = jsonify(chart_data['Data']) 
    response.headers.add('Access-Control-Allow-Origin','*') 
    return response
    
@bp.route('/index',methods=('GET','POST'))
def index(): 
    if 'username' in session:
        username = session['username'] 
        user_id = get_user_id(username) 
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username 
    return render_template('main/index_met.html',init=True)

@bp.route('/test',methods=('GET','POST'))
def test(): 
    return jsonify("test")        

@bp.route('/met',methods=('GET','POST'))
def met():
    if 'username' in session:
        print(session['username'])
        username = session['username'] 
        user_id = get_user_id(username) 
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username 

    return render_template('main/index_met.html', init=True) 

@bp.route('/comp',methods=('GET','POST'))
def comp():
    if 'username' in session:
        username = session['username'] 
        user_id = get_user_id(username) 
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username 

    return render_template('main/index_comp.html', init =True)  

@bp.route('/diag',methods=('GET','POST'))
def diag():
    if 'username' in session:
        username = session['username'] 
        user_id = get_user_id(username) 
        session['user_id'] = user_id
        g.user = User(user_id)
        g.username = username 

    return render_template('main/index_diag.html', init =True)     