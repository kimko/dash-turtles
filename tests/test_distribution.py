import dash
import dash_html_components as html

import apps.distribution as page


def test_layout():
    """
    Does my layout render as a Div?
    """
    assert isinstance(page.layout, html.Div)


def test_distribution_page(dash_duo):

    app = dash.Dash(__name__)
    app.layout = page.layout

    dash_duo.start_server(app)

    assert dash_duo.find_element("#box1_dwn_y").text == "Weight"
    assert dash_duo.find_element("#box1_dwn_boxpoints").text == "None"
    assert dash_duo.find_element("#box_1_container").text != "None"
    assert dash_duo.get_logs() == [], "browser console should contain no error"

    dash_duo.percy_snapshot("distribution_page")
