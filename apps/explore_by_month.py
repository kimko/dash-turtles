from calendar import month_name

from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html

from app import app
from app import tm as turtles
import apps.utils as utils


layout = [
    # top controls
    html.Div(
        [
            utils.drpdwn_frequency('exp_dwn_freq', option='MQS'),
            utils.drpdwn_LocationPicker('exp_dwn_location'),
        ],
        className='row',
        style={'marginBottom': '10'},
    ),

    html.Div(id='by-period-chart-container'),

]


def by_month_plot(df, years, caption, period):
    """
    Generat a plotly bar chart
    """
    data = [
        go.Bar(
            x=df[df.Year == year].Period,
            y=df[df.Year == year].Count,
            name=str(year)
        ) for year in years]

    xaxis = {
        'type': 'category',
        'categoryorder': 'array',
        'categoryarray': month_name[1:13],
    }
    if period == 'S':
        xaxis['title'] = '"Early" means all data before September'

    layout = go.Layout(
        barmode='group',
        hovermode='closest',
        title=caption[period],
        xaxis=xaxis,
        yaxis={'title': 'Count'}
    )

    fig = go.Figure(data=data, layout=layout)
    graph = dcc.Graph(
        id='by-period-chart',
        figure=fig
    )
    return graph


def by_month_chart_format_data(period='Q', locations=[]):
    """
    Generate the data needed for the by_month chart.
    """
    caption = {'M': 'Count per Month',
               'Q': 'Count per Quarter',
               'S': 'Count per Season',
               }
    df = turtles.get_count_per_period_and_year(period, locations)
    # TODO move further data manipulation to service
    years = df.Year.unique()
    years.sort()
    return df, years, caption


@app.callback(
    Output('by-period-chart-container', 'children'),
    [Input('exp_dwn_freq', 'value'),
        Input('exp_dwn_location', 'value')])
def by_month_chart_update(period, locations):
    """
    Update and Render by_month chart everytime the frequency or location dropdown changes value
    """
    # df = turtles.get_df()
    df, years, caption = by_month_chart_format_data(period, locations)

    return by_month_plot(df, years, caption, period)
