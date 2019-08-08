import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json

from GANEX.db import get_db

# training plot using database data
def trainLossPlot(db, expid, statCol):

    
    data = [] 
    for r in db["trainstats"].find({"expid":expid},{"_id": 0, statCol: 1}):
        data.append(r[statCol])

    
    x = np.linspace(0, len(data), len(data))
    y = data
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe

    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(go.Scatter(x=df['x'], y=df['y']), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['x'], y=df['y']), row=1, col=2)


    data = [
        go.Scatter(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        ),
        go.Scatter(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
