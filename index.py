# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import explore, distribution

app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("Turtle Dashboard", className='app-title'),

            html.Div(
                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/4/43/Painted_Turtle_%2814541060047%29.jpg', height="100%"), style={"float": "right", "height": "100%"})
        ],
            className="row header"
        ),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(label="Explore Surveys", value="explore_tab"),
                    dcc.Tab(label="Distributions", value="distributions_tab"),
                ],
                value="explore_tab",
            )

        ],
            className="row tabs_div"
        ),


        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

    ],
    className="row",
    style={"margin": "0%"},
)

server = app.server

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "distributions_tab":
        return distribution.layout
    elif tab == "explore_tab":
        return explore.layout
    else:
        return explore.ldistribution


if __name__ == "__main__":
    app.run_server(debug=True)
