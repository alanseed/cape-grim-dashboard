# This module builds the html for a chart 
import click
import plotly 
from flask.cli import with_appcontext
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime,timedelta 
from app.db import add_chart, get_db

# flask command to make the charts ie flask make-charts from a terminal to generate a cache of charts 
@click.command('make-charts',help="START: yyyy-mm-dd")
@click.argument("start")
@with_appcontext
def make_charts_command(start):
    make_charts(start)   
    return
def init_app(app):
    app.cli.add_command(make_charts_command)

# add all the charts for a particular day to the cache 
def make_charts(start):
    start_time = datetime.strptime(start,"%Y-%m-%d") 
    time_length = timedelta(days=1)
    end_time = start_time + time_length 
    end = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    start = start_time.strftime("%Y-%m-%dT%H:%M:%S")

    click.echo(f"Making charts for {start}")

    # get the list of charts to make 
    chart_list = list_charts()
    for chart in chart_list:
        click.echo(f"Adding {chart}")
        fig = make_chart(chart, start_time, end_time)  
        if fig is None:
            click.echo("Error making chart")
            return
        else:
            # write the chart to the database 
            data = plotly.io.to_json(fig,engine="orjson") 
            add_chart(chart,start_time, end_time, data)   
    return 


# function to return a list of enabled charts from the database 
def list_charts():
    db = get_db()
    charts = []
    docs = db.charts.find() 
    for doc in docs:
        this_chart = doc["ChartName"]
        enable = doc["Enable"]
        if (this_chart not in charts) and (enable == 1) : 
            charts.append(this_chart)
    return charts

# function to take care of the special characters in the title 
def format_title(title):
    
    # manage the degree symbol
    deg_pos = title.find("DEGREE SIGN")
    if deg_pos > 0:
        degree_sign = '\N{DEGREE SIGN}' 
        my_title = title[0:deg_pos-3] + degree_sign + title[deg_pos+12:]
        return my_title
    
    exp_pos = title.find("^{-1}")
    if exp_pos > 0:
        my_title = title[0:exp_pos-1] + "<sup>-1</sup>" + title[exp_pos+5:]
        return my_title
    
    exp_pos = title.find("^3")
    if exp_pos > 0:
        my_title = title[0:exp_pos] + "<sup>3</sup>" + title[exp_pos+5:]
        return my_title        
    
    return title

# Return a chart as a plotly graphic object that can then be stored in the cache 
# returns None on error 
def make_chart(chart_name, start, end):
    db= get_db()
    
    # check if we have a valid chart_name 
    count = db.charts.count_documents(filter={"ChartName":chart_name}) 
    if count == 0:
        click.echo(f"Chart not found {chart_name}")
        return None

    # get the list of chart configurations, one per DataName
    chart_list = []
    docs = db.charts.find({"ChartName":chart_name}) 
    for doc in docs:
        chart_list.append(doc) 

    # check if we have multiple Y axes 
    if (chart_list[0]["L/R"] == "L") or (chart_list[0]["L/R"] == "R"):
        secondary_y = True
    else: 
        secondary_y = False
    
    if secondary_y: 
        fig = make_subplots(specs=[[{"secondary_y":True}]])
    else: 
        fig = go.Figure() 
        
    for chart in chart_list:    
        # read in the values for this line and sort 
        myquery = {'DataName':chart["DataName"],'Time':{'$gte':start,"$lte":end}}
        docs = db.obs_data.find(myquery, {"Time":1,"Value":1}).sort("Time")   
        
        # load the time and values into lists 
        times = []
        values = []
        for doc in docs:
            times.append(doc["Time"])
            values.append(doc["Value"])

        # add the line to the plot  
        if secondary_y:
            if chart["L/R"] == "L":
                fig.add_trace(go.Scatter(x=times, y=values,name=chart["Legend"]),secondary_y=False)
            if chart["L/R"] == "R":
                fig.add_trace(go.Scatter(x=times, y=values,name=chart["Legend"]),secondary_y=True)
        else:   
            fig.add_trace(go.Scatter(x=times, y=values,name=chart["Legend"]))
        
    # add the slider
    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([ 
                dict(count=6,label="6h",step="hour",stepmode="backward"),
                dict(count=12,label="12h",step="hour",stepmode="backward"),
                dict(count=1,label="1d",step="day",stepmode="backward")
            ])
        ),
        rangeslider=dict(visible=True),
        type = "date"
        )
    )
    
    # format the y axis 
    yl_dict = {}
    if not np.isnan(float(chart["LeftLog"])):
        yl_dict["type"]="log"
    left_title = format_title(chart["LeftTitle"]) 
    yl_dict["title"] = left_title 
    if not np.isnan(float(chart["LeftMin"])):
        yl_dict["range"] = [chart["LeftMin"],chart["LeftMax"]]
    fig.update_layout(yaxis=yl_dict)

    # set up the y-axis 
    if secondary_y:
        yr_dict = {}
        if not np.isnan(float(chart["RightLog"])):
            yr_dict["type"] = "log"
        right_title = format_title(chart["RightTitle"]) 
        yr_dict["title"]=right_title 
        if not np.isnan(float(chart["RightMin"])):
            yr_dict["range"] = [chart["RightMin"],chart["RightMax"]]
        fig.update_layout(yaxis2=yr_dict)
    
    # set the title     
    fig.update_layout(title_text=chart["Title"])     
    return fig             
