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
            html.Div('Select dimensions:'),
            utils.drpdwn_tDimensions('box4_dwn_x', 'Weight'),
            utils.drpdwn_tDimensions('box5_dwn_y', 'Carapace'),
            utils.drpdwn_tDimensions('box6_dwn_z', 'Annuli'),
            utils.drpdwn_oDimensions('box7_dwn_c'),
            utils.drpdwn_oDimensions('box8_dwn_s'),
        ],
        className='row', style={'marginBottom': '10'},
    ),

    html.Div(id='threed-chart-container'),

]


def threed_plot(df, x, y, z, c, s):
    """
    Generate a plotly 3d chart
    """
    args = {
        'x': x, 'y': y, 'z': z,
        'size': 'Annuli',
        'size_max': 20,
    }
    if c != 'None':
        args['color'] = c
    if s != 'None':
        args['symbol'] = s

    fig = go.Figure(
        px.scatter_3d(df, **args)
    )
    fig['layout']['height'] = 1000
    graph = dcc.Graph(
        id='threed-chart',
        figure=fig
    )
    return graph


@app.callback(
    Output('threed-chart-container', 'children'),
    [Input('box4_dwn_x', 'value'),
        Input('box5_dwn_y', 'value'),
        Input('box6_dwn_z', 'value'),
        Input('box7_dwn_c', 'value'),
        Input('box8_dwn_s', 'value'), ])
def threed_chart_update(x, y, z, c, s):
    """
    Update and Render by_month chart everytime one of the dimensions dropdown changes value
    """
    df = turtles.get_df()

    return threed_plot(df, x, y, z, c, s)
