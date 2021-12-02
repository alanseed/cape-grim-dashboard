from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from app.db import get_db 
from app.chart import make_chart
import plotly 
import json 
import datetime

bp = Blueprint('main', __name__, url_prefix='/main')

# Display the main page to the dashboard 
@bp.route('/index', methods=('GET', 'POST'))
def index():
    chart_name = "ws-comparison" 
    start = datetime.datetime.fromisoformat("2021-01-01T00:00:00") 
    end = datetime.datetime.fromisoformat("2021-01-03T00:00:00") 
    fig = make_chart(chart_name, start, end)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 
    return render_template('main/index.html', graphJSON = graphJSON)
