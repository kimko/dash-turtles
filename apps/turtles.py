# -*- coding: utf-8 -*-
import json
import math

import pandas as pd
import flask
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
from plotly import graph_objs as go
from turtle_manager import Turtle_Manager
import plotly.figure_factory as ff
from app import app, indicator, millify, df_to_table
import numpy as np

import apps.utils as utils

df = Turtle_Manager().get_turtles()


facet_hist = ff.create_facet_grid(
    df,
    y='Weight',
    facet_row='Gender',
    facet_col='Capture Location',
    trace_type='histogram',
)

facet_box = ff.create_facet_grid(
    df,
    y='Weight',
    facet_row='Gender',
    facet_col='Capture Location',
    trace_type='box',
)


y0 = np.random.randn(50)-1
y1 = np.random.randn(50)+1

trace0 = go.Box(
    y=y0
)
trace1 = go.Box(
    y=y1
)


layout = [

    html.Div(children=''' simple box '''),

    # top controls
    html.Div(
        [
            utils.drpdwn_boxpoints("box1_dwn_boxpoints"),

            utils.drpdwn_tDimensions("box1_dwn_y"),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    dcc.Graph(
        id='box_1',
    ),

    html.Div(children=''' Histogram, Weight by Gender and Location. '''),
    dcc.Graph(
        id='facet_grid_1',
        figure=facet_hist,
    ),

    html.Div(children=''' Box, Weight by Gender. '''),
    dcc.Graph(
        id='facet_grid_2',
        figure=facet_box,
    )
]


@app.callback(
    Output('box_1', 'figure'),
    [
        Input('box1_dwn_boxpoints', 'value'),
        Input('box1_dwn_y', 'value')])
def update_box_1(boxpoints, y):

    box1 = [go.Box(
        y=df[df.Gender == g][y],
        name=g,
        boxpoints=boxpoints,
        # jitter=0.3,
        pointpos=-1.8) for g in ['f', 'm']]

    return {'data': box1}
