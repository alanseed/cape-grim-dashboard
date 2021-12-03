from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

bp = Blueprint('main', __name__, url_prefix='/main')

# # Display the main page to the dashboard 
# @bp.route('/index', methods=('GET', 'POST'))
# def index():
#     chart_name = "ws-comparison" 
#     # start = datetime.datetime.fromisoformat("2021-01-01T00:00:00") 
#     # end = datetime.datetime.fromisoformat("2021-01-03T00:00:00") 
#     # fig = make_chart(chart_name, start, end) 
#     # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) 
#     file_name = "/home/awseed/src/cape-grim-dashboard/charts/" + chart_name + ".json" 
#     with open(file_name) as f:
#         graphJSON = f.read() 
#     return render_template('main/index.html', graphJSON = graphJSON, chart_name=chart_name)

@bp.route('/')
def get_chart():
    chart_name = request.args.get("chart_name")
    file_name = "/home/awseed/src/cape-grim-dashboard/charts/" + chart_name + ".json" 
    with open(file_name) as f:
        graphJSON = f.read() 
    return render_template('main/index.html', graphJSON = graphJSON)
    