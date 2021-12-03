from flask import (
    Blueprint, flash, g, redirect, request, session, url_for, current_app, jsonify
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

@bp.route('/chart',methods=('GET', 'POST'))
def get_chart():
    chart_name = request.args.get("chart_name") 
    # return jsonify("chart test") 
    file_name = "/home/awseed/src/cape-grim-dashboard/charts/" + chart_name + ".json" 
    with open(file_name) as f:
        graphJSON = f.read() 
    response = jsonify(graphJSON) 
    response.headers.add('Access-Control-Allow-Origin', '*')    
    return response
    
@bp.route('/')
def get_main(): 
        return redirect(url_for('static',filename='index.html'))

@bp.route('/test',methods=('GET','POST'))
def test(): 
    return jsonify("test")        