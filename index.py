# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import explore, distribution, explore_by_month, explore_3d, map_box

app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span('Turtle Dashboard', className='app-title'),

            html.Div(
                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/4/43/Painted_Turtle_%2814541060047%29.jpg', height='100%'), style={'float': 'right', 'height': '100%'})
        ],
            className='row header'
        ),

        # tabs
        html.Div([

            dcc.Tabs(
                id='tabs',
                style={'height': '20', 'verticalAlign': 'middle'},
                children=[
                    dcc.Tab(label='Explore by Month', value='explore_by_month_tab'),
                    dcc.Tab(label='Explore Surveys', value='explore_tab'),
                    dcc.Tab(label='Distributions', value='distributions_tab'),
                    dcc.Tab(label='Explore 3d', value='threeD_tab'),
                    dcc.Tab(label='Map', value='map_box_tab'),
                ],
                value='explore_tab',
            )

        ],
            className='row tabs_div'
        ),


        # Tab content
        html.Div(id='tab_content', className='row', style={'margin': '2% 3%'}),

    ],
    className='row',
    style={'margin': '0%'},
)

server = app.server


@app.callback(Output('tab_content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'distributions_tab':
        return distribution.layout
    elif tab == 'explore_by_month_tab':
        return explore_by_month.layout
    elif tab == 'explore_tab':
        return explore.layout
    elif tab == 'threeD_tab':
        return explore_3d.layout
    elif tab == 'map_box_tab':
        return map_box.layout
    else:
        return explore.layout


if __name__ == '__main__':
    app.run_server(debug=True)
