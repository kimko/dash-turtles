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

turtles = tm()

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

    # Turtle button
    html.Div(
        [
            html.Div(dcc.Input(id='turtle-id', type='text'), className="one columns")
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    html.Div(id='explore-chart-container'),

]


@app.callback(
    Output('explore-chart-container', 'children'),
    [Input('turtle-id', 'n_submit')],
    [State('turtle-id', 'value')])
def table(ns, turtleID):
    turtleID = str(turtleID)
    df = turtles.get_df().set_index('ID').copy()
    if df.loc[turtleID].shape[0] == 0:
        return
    return dcc.Graph(
        id='turtle-graph',
        figure={
            'data': [
                go.Scatter(
                    x=df.loc[turtleID, 'Date'],
                    y=df.loc[turtleID, 'Weight'],
                    text=df.loc[turtleID, 'Carapace'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name="Turtle " + turtleID
                )
            ],
        }
    )


@app.callback(
    Output('table1-container', 'children'),
    [Input('bar_1', 'clickData'),
     Input('dwn_freq', 'value')])
def table(clickData, frequency):
    df = turtles.get_df().sort_values('Date').copy()
    if clickData:
        endDate = clickData['points'][0]['x']
    else:
        return ""
    filter = filter_from_periodStart_to_endDate(df, endDate, frequency)
    data = df[filter].to_dict('records')

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
    df = turtles.get_df()
    if len(locations) > 0:
        df = df[df['Capture Location'].isin(locations)].copy()
    else:
        df = df.copy()
    captureCount = df.copy()
    captureCount = captureCount.set_index('Date')['ID']
    captureCount = captureCount.groupby(pd.Grouper(freq=frequency)).count()
    captureCount = captureCount[captureCount > 0]

    box1 = go.Scatter(
        x=captureCount.index,
        y=captureCount.values,
        name='Captures',
        line={'width': 6},
    )
    dateCount = df.copy()
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
