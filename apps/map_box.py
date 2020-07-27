from os import environ

from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import plotly_express as px

from app import app
from app import tm as turtles
import apps.utils as utils

layout = [
    # Button Group 1
    html.Div(
        [
            html.Div('Map:'),
            utils.drpdwn_LocationPicker('exp_dwn_location2'),
        ],
        className='row', style={'marginBottom': '10'},
    ),

    html.Div(id='map-box-container'),

]


def map_box_plot(df, locations):
    """
    Generate a map box chart
    """
    if len(locations) > 0:
        df = df[df['Capture Location'].isin(locations)]
    args = {
        'lat': 'lat',
        'lon': 'long',
        'size': 'Annuli',
        'color': 'Gender',
        'size_max': 20,
        'zoom': 10,
    }
    px.set_mapbox_access_token(environ['MAP_BOX'])
    fig = go.Figure(
        px.scatter_mapbox(df, **args)
    )
    fig['layout']['height'] = 600
    graph = dcc.Graph(
        id='map-box-chart',
        figure=fig
    )
    return graph


@app.callback(
    Output('map-box-container', 'children'),
    [Input('exp_dwn_location2', 'value'),
     ])
def map_box_update(locations):
    """
    Update and render map_box chart everytime location changes value
    """
    df = turtles.get_df()

    return map_box_plot(df, locations)
