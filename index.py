# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import turtles

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
                    dcc.Tab(label="Turtles", value="turtles_tab"),
                    dcc.Tab(label="Other", value="other_tab"),
                ],
                value="turtles_tab",
            )

        ],
            className="row tabs_div"
        ),


        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "2% 3%"}),

        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css", rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)

server = app.server

@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "turtles_tab":
        return turtles.layout
    elif tab == "other_tab":
        return []
    else:
        return turtles.layout


if __name__ == "__main__":
    app.run_server(debug=True)
