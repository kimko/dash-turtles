import json

import dash_table
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd

from app import app
import apps.utils as utils
from turtle_manager import Turtle_Manager as tm
from turtle_manager import filter_from_periodStart_to_endDate
from turtle_manager import get_count_per_month_and_year

turtles = tm()

layout = [
    # top controls
    html.Div(
        [
            utils.drpdwn_LocationPicker("exp_dwn_location"),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    html.Div(id='by-month-chart-container'),

]


@app.callback(
    Output('by-month-chart-container', 'children'),
    [Input('exp_dwn_location', 'value')])
def update_by_month_chart(locations):
    df = turtles.get_df()
    df = get_count_per_month_and_year(df)

    years = df.Year.unique()
    years.sort()
    data = [
        go.Bar(
            x=df[df.Year == year].Month,
            y=df[df.Year == year].Count,
            name=str(year)
        ) for year in years]
    layout = go.Layout(
        barmode='group',
        hovermode='closest',
    )

    fig = go.Figure(data=data, layout=layout)
    graph = dcc.Graph(
        id='by-month-chart',
        figure=fig
    )
    return graph
