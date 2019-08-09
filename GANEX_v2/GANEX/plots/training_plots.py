import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json

from GANEX.db import get_db
from GANEX.dlexmongo import getPlotStats

# training plot using database data
def trainLossPlot(db, expid, statlist):

    num_plots = len(statlist)
    fig = make_subplots(rows=num_plots, cols=1)
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
