# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import turtles, table

app.layout = html.Div(
    [
        # header
        html.Div([

            html.Span("Turtle Barf", className='app-title'),

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
                    dcc.Tab(label="Table", value="table_tab"),
                ],
                value="turtles_tab",
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
    if tab == "turtles_tab":
        return turtles.layout
    elif tab == "table_tab":
        return table.layout
    else:
        return turtles.layout


if __name__ == "__main__":
    app.run_server(debug=True)
