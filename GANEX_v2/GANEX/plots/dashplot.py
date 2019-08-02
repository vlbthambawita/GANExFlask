import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
from dash import Dash

from flask import Blueprint, request, current_app


import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


#bp = Blueprint('dashplot', __name__)

#@bp.route('/dash')
#def dash():
 #   redire


def dashapp1(app):

    dashapp = Dash( __name__,
                server=app,
                routes_pathname_prefix='/dash/'
            )

    

    dashapp.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(id='live-update-text'),
        

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        ),
        dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
    ])

    @dashapp.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
    def update_metrics(n):
        print("this is interval")

        print(request.args.get("pid"))

        randnumber = np.random.rand(1)
        style = {'padding': '5px', 'fontSize': '16px'}
        return [
            html.Span('Longitude: {0:.2f}'.format(randnumber[0]), style=style)
        ]


def dashapp2(app):

    dashapp = Dash( __name__,
                server=app,
                routes_pathname_prefix='/dash2/'
            )

    dashapp.layout = html.Div(children=[
        dcc.Location(id='url', refresh=False),
        html.H1(children='Hello Dash'),

        html.Div(id='live-update-text'),
        

        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 4, 4], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])

    @dashapp.callback(Output('live-update-text', 'children'),
    [Input('url', 'pathname')])
    def test(pathname):
        print(request.args.get('pid'))
        print("This is callback function -", pathname)
        return pathname


# plotly 
def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON