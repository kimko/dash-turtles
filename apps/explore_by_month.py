from calendar import month_name

from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html

from app import app
import apps.utils as utils
from turtle_manager import Turtle_Manager as tm
from turtle_manager import get_count_per_period_and_year

turtles = tm()

layout = [
    # top controls
    html.Div(
        [
            utils.drpdwn_frequency("exp_dwn_freq", option='MQ'),
            utils.drpdwn_LocationPicker("exp_dwn_location"),
        ],
        className="row",
        style={"marginBottom": "10"},
    ),

    html.Div(id='by-period-chart-container'),

]


@app.callback(
    Output('by-period-chart-container', 'children'),
    [Input('exp_dwn_freq', 'value'),
        Input('exp_dwn_location', 'value')])
def update_by_month_chart(period, locations):
    caption = {'M': 'Count per Month',
               'Q': 'Count per Quarter'}
    df = turtles.get_df()
    if len(locations) > 0:
        df = df[df['Capture Location'].isin(locations)]
    df = get_count_per_period_and_year(df, period)
    years = df.Year.unique()
    years.sort()
    data = [
        go.Bar(
            x=df[df.Year == year].Period,
            y=df[df.Year == year].Count,
            name=str(year)
        ) for year in years]
    layout = go.Layout(
        barmode='group',
        hovermode='closest',
        title=caption[period],
        xaxis={
            "type": "category",
            "categoryorder": "array",
            "categoryarray": month_name[1:13]
        },
        yaxis={'title': 'Count'}
    )

    fig = go.Figure(data=data, layout=layout)
    graph = dcc.Graph(
        id='by-period-chart',
        figure=fig
    )
    return graph
