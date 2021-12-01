# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pymongo 
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# %%
def make_chart(chart_name, start, end):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["cg_data"] 
    
    # check if we have a valid chart_name 
    count = db.charts.count_documents(filter={"ChartName":chart_name}) 
    if count == 0:
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
        # read in the values for this line 
        myquery = {'DataName':chart["DataName"],'Time':{'$gte':start,"$lte":end}}
        docs = db.obs_data.find(myquery, {"Time":1,"Value":1})   
        
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
                dict(count=1,label="1d",step="day",stepmode="backward"),
                dict(count=7,label="7d",step="day",stepmode="backward")
            ])
        ),
        rangeslider=dict(visible=True),
        type = "date"
        )
    )
    
    # set the titles - manage the degree symbol if needed 
    left_title = format_title(chart["LeftTitle"]) 
        
    # set up the y-axis 
    if secondary_y:
        right_title = format_title(chart["RightTitle"])
        fig.update_layout(
            yaxis=dict(
                range=[chart["LeftMin"],chart["LeftMax"]],
                title=left_title
            )
        )
        fig.update_layout(
            yaxis2=dict(
                range=[chart["RightMin"],chart["RightMax"]],
                title=right_title
            )
        )        
    else:     
        fig.update_layout(
            yaxis=dict(
                range=[chart["LeftMin"],chart["LeftMax"]],
                title=left_title
            )
        )
    
    # set the title     
    fig.update_layout(title_text=chart["Title"])
    client.close()        
    return fig             


# %%
# function to return a list of enabled charts from the database 
def list_charts():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["cg_data"] 
    charts = []
    docs = db.charts.find() 
    for doc in docs:
        this_chart = doc["ChartName"]
        enable = doc["Enable"]
        if (this_chart not in charts) and (enable == 1) : 
            charts.append(this_chart)
    client.close() 
    return charts


# %%
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


# %%
start = datetime.datetime.fromisoformat("2021-01-01T00:00:00") 
end = datetime.datetime.fromisoformat("2021-01-07T00:00:00")
charts = list_charts()

# fig = make_chart("merc-fullscale-data", start, end)

for chart_name in charts:
    fig = make_chart(chart_name, start, end)
    if fig != None:
        fig.show()
    else:
        print("Error in making chart")
        break     


# %%



# %%



