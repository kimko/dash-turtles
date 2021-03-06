import json

import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go
import dash_html_components as html
import pandas as pd

from app import app
from app import tm as turtles
import apps.utils as utils


layout = [
    # top controls
    html.Div(
        [
            utils.drpdwn_frequency('dwn_freq'),
            utils.drpdwn_LocationPicker('dwn_location'),
        ],
        className='row',
        style={'marginBottom': '10'},
    ),

    html.Div(id='survey-chart-container'),

    html.Div(id='table1-container'),

    html.Div(id='explore-chart-container'),

]


@app.callback(
    Output('explore-chart-container', 'children'),
    [Input('table_1', 'derived_virtual_data'),
        Input('table_1', 'derived_virtual_selected_rows')])
def update_explore_chart(rows, selected):
    turtleIDs = [rows[i]['ID'] for i in selected]
    df = turtles.get_df().copy()
    if len(turtleIDs) == 0:
        return
    return dcc.Graph(
        id='turtle-graph',
        figure={
            'data': [
                go.Scatter(
                    x=df.loc[df.ID == str(turtleID), 'Date'],
                    y=df.loc[df.ID == str(turtleID), 'Weight'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='Turtle ' + str(turtleID)
                ) for turtleID in turtleIDs],
            'layout': {
                'title': 'Individual turtles',
                'yaxis': {
                    'automargin': True,
                    'title': {'text': 'Weight'}
                },
            },
        }
    )


@app.callback(
    Output('table1-container', 'children'),
    [Input('bar_1', 'clickData'),
     Input('dwn_freq', 'value')])
def update_table(clickData, frequency):
    columns = ['ID', 'Date', 'Capture Location', 'Gender', 'Annuli',
               'Annuli_orig', 'Weight', 'Carapace', 'Plastron', 'Gravid']
    df = turtles.get_df()
    df = df[columns].copy()
    if clickData:
        endDate = clickData['points'][0]['x']
        print(endDate)
    else:
        return ''
    data = turtles.filter_from_periodStart_to_endDate(endDate, frequency)
    data = data.to_dict('records')

    table = dash_table.DataTable(
        id='table_1',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=data,
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        row_selectable='multi',
        selected_rows=[0, 1],  # select furst two records
        page_action='native',
        page_current=0,
        page_size=20,
    )
    return table


@app.callback(
    Output('click-data', 'children'),
    [Input('bar_1', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('survey-chart-container', 'children'),
    [Input('dwn_freq', 'value'),
     Input('dwn_location', 'value')])
def update_bar1(frequency, locations):
    caption = {'D': 'Count day',
               'W': 'Count and surveys per week',
               'M': 'Count and surveys per month',
               'Q': 'Count and surveys per quarter',
               'A': 'Count and surveys per year'}
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
        title=caption[frequency],
        xaxis={'type': 'category'},
        yaxis={'title': 'Count'},
        yaxis2={'title': 'Days',
                'overlaying': 'y',
                'side': 'right'},
    )
    graph = dcc.Graph(
        id='bar_1',
        figure=go.Figure(
            data=data,
            layout=layout)
    )

    return graph
