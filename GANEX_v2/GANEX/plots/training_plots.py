import numpy as np
import pandas as pd

import plotly
import plotly.graph_objs as go
import json

from GANEX.db import get_db

# training plot using database data
def trainLossPlot(db, expid):

    
    data = [] 
    for r in db["trainstats"].find({"expid":expid},{"_id": 0, "value": 1}):
        data.append(r["value"])

    
    x = np.linspace(0, len(data), len(data))
    y = data
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Scatter(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
