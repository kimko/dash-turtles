import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd

from app import app
import apps.utils as utils
from turtle_manager import Turtle_Manager

df = Turtle_Manager().get_turtles()

layout = [
    # top controls
    html.Div(
        [
            utils.drpdwn_frequency("dwn_freq"),
            utils.drpdwn_LocationPicker("dwn_location"),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    html.Div(id='chart1-container'),

    html.Div(id='table1-container'),

]


@app.callback(
    Output('table1-container', 'children'),
    [Input('bar_1', 'clickData'),
     Input('dwn_freq', 'value')])
def table(clickData, frequency):
    dfL = df.sort_values('Date').copy()
    endDate = clickData['points'][0]['x']
    endDate = datetime.strptime(endDate, '%Y-%m-%d')
    startDate = str(endDate - relativedelta(months=4))
    if frequency == 'D':
        startDate = str(endDate - relativedelta(days=1))
    if frequency == 'W':
        startDate = str(endDate - relativedelta(weeks=1))
    if frequency == 'M':
        startDate = str(endDate - relativedelta(months=1))
    if frequency == 'Q':
        startDate = str(endDate - relativedelta(months=4))
    if frequency == 'A':
        startDate = str(endDate - relativedelta(years=1))
    dfL = dfL[(dfL['Date'] > startDate) & (dfL['Date'] <= endDate)]
    # dfL = dfL[(dfL['Date'] > x) & (dfL['Date'] < '2013-02-01')]
    data = dfL.to_dict('records')

    table = dash_table.DataTable(
        id='table_1',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=data,
        filtering=True,
        sorting=True,
        sorting_type="multi",
        pagination_mode="fe",
        pagination_settings={
            "current_page": 0,
            "page_size": 20,
        },
    )
    return table


@app.callback(
    Output('click-data', 'children'),
    [Input('bar_1', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('chart1-container', 'children'),
    [Input('dwn_freq', 'value'),
     Input('dwn_location', 'value')])
def update_bar1(frequency, locations):
    if len(locations) > 0:
        localdf = df[df['Capture Location'].isin(locations)].copy()
    else:
        localdf = df.copy()
    captureCount = localdf.copy()
    captureCount = captureCount.set_index('Date')['ID']
    captureCount = captureCount.groupby(pd.Grouper(freq=frequency)).count()
    captureCount = captureCount[captureCount > 0]

    box1 = go.Scatter(
        x=captureCount.index,
        y=captureCount.values,
        name='Captures',
        line={'width': 6},
    )
    dateCount = localdf.copy()
    dateCount = pd.DataFrame(dateCount.Date.unique())
    dateCount['ID'] = '1'
    dateCount = dateCount.set_index(0)['ID']
    dateCount = dateCount.groupby(pd.Grouper(freq=frequency)).count()
    dateCount = dateCount[dateCount > 0]
    box2 = go.Bar(
        x=dateCount.index,
        y=dateCount.values,
        yaxis='y2',
        name='Capture Days',
        opacity=0.5,
    )

    if (frequency != 'D'):
        data = [box1, box2]
    else:
        data = [box1]
    layout = go.Layout(
        barmode='group',
        xaxis={'type': 'category'},
        yaxis2={'overlaying': 'y',
                'side': 'right'},
    )
    graph = dcc.Graph(
        id='bar_1',
        figure=go.Figure(
            data=data,
            layout=layout)
    )

    return graph
