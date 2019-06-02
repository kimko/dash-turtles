import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd

from app import app
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
    table(),

    html.Div(id='datatable-interactivity-container')

]


@app.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('table_1', "derived_virtual_data"),
     Input('table_1', "derived_virtual_selected_rows"),
     Input('table_1', "ID")])
def update_bar1(data, selected_rows, ID):
    captureCount = df.set_index('Date')['ID']
    captureCount = captureCount.groupby(pd.Grouper(freq='Q')).count()
    captureCount = captureCount[captureCount > 0]
    box1 = go.Bar(
        x=captureCount.index,
        y=captureCount.values,
        name='Captures'
    )

    dateCount = pd.DataFrame(df.Date.unique())
    dateCount['ID'] = '1'
    dateCount = dateCount.set_index(0)['ID']
    dateCount = dateCount.groupby(pd.Grouper(freq='Q')).count()
    dateCount = dateCount[dateCount > 0]
    box2 = go.Bar(
        x=dateCount.index,
        y=dateCount.values,
        name='Capture Days'
    )

    data = [box1, box2]
    layout = go.Layout(
        barmode='group',
    )
    graph = dcc.Graph(
        id='bar_1',
        figure=go.Figure(
            data=data,
            layout=layout)
    )

    return graph
