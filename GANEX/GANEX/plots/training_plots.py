import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# from plotly import subplots.make_subplots
import json

from GANEX.db import get_db
from GANEX.dlexmongo import getPlotStats, getTrainStatAsList

# training plot using database data
def trainLossPlot(db, expid, statlist):

    num_plots = len(statlist)
    fig = make_subplots(rows=num_plots, cols=1)
    getTrainStatAsList(db, expid, statlist[0][0]) # only for testing
    # getPlotStats()
    for i in range(len(statlist)):
        data = [] 
        for r in db["trainstats"].find({"expid":expid},{"_id": 0, statlist[i][0]: 1}):
            data.append(r[statlist[i][0]])

    
        x = np.linspace(0, len(data), len(data))
        y = data
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

    # fig = make_subplots(rows=1, cols=2)
        fig.add_trace(go.Scatter(x=df['x'], y=df['y']), row=int(statlist[i][1]), col=1)

    # fig.add_trace(go.Scatter(x=df['x'], y=df['y']), row=1, col=2)
    fig.update_layout(height=800)


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def trainLossPlot_v2(db, expid, statlist):

    num_plots = len(statlist)
    # fig = make_subplots(rows=num_plots, cols=1)
   # getTrainStatAsList(db, expid, statlist[0][0]) # only for testing
    # getPlotStats()
    figs = {}
    graphs = []
    
    for i in range(len(statlist)):
        data_x = []
        data_y = [] 
        for r in db["trainstats"].find({"expid":expid},{"_id": 0, statlist[i][0]: 1}):
            data_x.append(r[statlist[i][0]])

    
        x = np.linspace(0, len(data), len(data))
        y = data
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

        plot_key = int(statlist[i][1]) # plot number

        if plot_key in figs.keys():
            fig = figs[plot_key]
        else:
            fig = go.Figure()
            figs[plot_key] = fig


    # fig = make_subplots(rows=1, cols=2)
        fig.add_trace(go.Scatter(x=df['x'], y=df['y']))

    # fig.add_trace(go.Scatter(x=df['x'], y=df['y']), row=1, col=2)
        fig.update_layout(height=600, width=1200)

    for fig in figs.values():
        graphs.append(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print("Grpahs===========", graphs)
    return graphs#graphJSON


###################
# Version 3 - optimized for memory usage
###################

def trainLossPlot_v3(db, expid, statlist):

    num_plots = len(statlist)
    # fig = make_subplots(rows=num_plots, cols=1)
   # getTrainStatAsList(db, expid, statlist[0][0]) # only for testing
    # getPlotStats()
    figs = {}
    graphs = []
    


            


######################################
    
    for i in range(len(statlist)):
        data_x = []
        data_y = [] 
        for r in db["trainstats"].find({"expid":expid},{"_id": 0, statlist[i][0]: 1, "iteration":1}):
            data_y.append(r[statlist[i][0]])
            data_x.append(r["iteration"])

    
       # x = np.linspace(0, len(data), len(data))
       # y = data
       # df = pd.DataFrame({'x': data, 'y': y}) # creating a sample dataframe

        plot_key = int(statlist[i][1]) # plot number

        if plot_key in figs.keys():
            fig = figs[plot_key]
        else:
            fig = go.Figure()
            figs[plot_key] = fig


    # fig = make_subplots(rows=1, cols=2)
        fig.add_trace(go.Scatter(x=data_x, y=data_y, name=str(statlist[i][0])))

    # fig.add_trace(go.Scatter(x=df['x'], y=df['y']), row=1, col=2)
        fig.update_layout(height=600, width=1200)
        fig.update_layout(showlegend=True)
        fig.update_layout(template="plotly_dark")

    for fig in figs.values():
        graphs.append(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # print("Grpahs===========", graphs)
    return graphs#graphJSON
