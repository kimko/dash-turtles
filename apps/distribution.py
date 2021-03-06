# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
import plotly.figure_factory as ff
import plotly_express as px

from app import app, tm
import apps.utils as utils

df = tm.get_df()

layout = html.Div([
    # Button Group 1
    html.Div(
        [
            html.Div('Select distribution dimension:'),
            utils.drpdwn_boxpoints('box1_dwn_boxpoints'),
            utils.drpdwn_tDimensions('box1_dwn_y'),
        ],
        className='row', style={'marginBottom': '10'},
    ),

    # Chart 1
    html.Div(
        html.Div(id='box_1_container', className='eight columns'),
        className='row', style={'marginBottom': '10'},
    ),

    # Button Group 2
    html.Div(
        [
            html.Div(children='Select chart type:'),
            utils.drpdwn_traceType('facet1_dwn_traceType'),
        ],
        className='row', style={'marginBottom': '10'},
    ),

    # Chart 2
    html.Div(id='facet_grid_1_container'),

    # chart 3
    html.Div(
        [
            html.Div(children='Scatter plot:'),
            utils.drpdwn_tDimensions('box2_dwn_x', 'Carapace'),
        ],
        className='row', style={'marginBottom': '10'},),
    html.Div(id='scatter_1_container'),
])


@app.callback(
    Output('box_1_container', 'children'),
    [
        Input('box1_dwn_boxpoints', 'value'),
        Input('box1_dwn_y', 'value')])
def update_box_1(boxpoints, y):
    if boxpoints == 'None':
        boxpoints = False
    box1 = [go.Box(
        y=df[df.Gender == g][y],
        name=g,
        boxpoints=boxpoints,
        # jitter=0.3,
        pointpos=-1.8) for g in ['f', 'm']]
    return dcc.Graph(
        id='box_1',
        figure=go.Figure(
            data=box1,
            layout={
                'title': 'Distributions by {} and gender'.format(y),
                'yaxis': {
                    'automargin': True,
                    'title': {'text': y}
                },
            }),
    )


@app.callback(
    Output('facet_grid_1_container', 'children'),
    [
        Input('facet1_dwn_traceType', 'value'),
        Input('box1_dwn_y', 'value')])
def update_facet_grid1(traceType, y):

    facet_hist = ff.create_facet_grid(
        df,
        y=y,
        facet_row='Gender',
        facet_col='Capture Location',
        trace_type=traceType,
    )
    facet_hist['layout']['title'] = '{} - {} by gender and location'.format(
        traceType, y)
    return dcc.Graph(
        id='facet_grid_1',
        figure=facet_hist,
    )


def scatter1_plot(df, x, y):
    '''
    Generate the plot.
    '''
    figure = go.Figure(
        px.scatter(
            df, x=x, y=y, color="Gender", trendline="ols", marginal_x="violin", marginal_y="violin"))
    return dcc.Graph(
        id='scatter_1',
        figure=figure)


@app.callback(
    Output('scatter_1_container', 'children'),
    [
        Input('box2_dwn_x', 'value'),
        Input('box1_dwn_y', 'value')])
def scatter1_update(x, y):
    '''
    Render and update the scatter plot when y-button value changes.
    '''
    return scatter1_plot(df, x, y)
