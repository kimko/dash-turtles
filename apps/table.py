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


def table():
    table = dash_table.DataTable(
        id='table_1',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
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


layout = [
    # top controls
    html.Div(
        [
            utils.drpdwn_frequency("dwn_freq"),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    html.Div(id='datatable-interactivity-container'),

    table(),
]


@app.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('table_1', "derived_virtual_data"),
     Input('table_1', "derived_virtual_selected_rows"),
     Input('table_1', "ID"),
     Input('dwn_freq', 'value')])
def update_bar1(data, selected_rows, ID, frequency):
    captureCount = df.set_index('Date')['ID']
    captureCount = captureCount.groupby(pd.Grouper(freq=frequency)).count()
    captureCount = captureCount[captureCount > 0]
    box1 = go.Bar(
        x=captureCount.index,
        y=captureCount.values,
        name='Captures',
        opacity=0.5,
    )

    dateCount = pd.DataFrame(df.Date.unique())
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

    data = [box1, box2]
    layout = go.Layout(
        barmode='group',
        xaxis={'type': 'category'},
        yaxis2={'overlaying': 'y',
                'side': 'right'}
    )
    graph = dcc.Graph(
        id='bar_1',
        figure=go.Figure(
            data=data,
            layout=layout)
    )

    return graph
