from json import loads

from dash_html_components.Div import Div

import index


APP = index.app


def test_layout():
    """
    Does my layout render as a Div?
    """
    assert isinstance(APP.layout, Div)


def test_tab_content():
    """
    Do I render layout for all tab values?
    """
    tabs = ['explore_by_month_tab', 'distributions_tab', 'explore_tab']
    for tab in tabs:
        layout = loads(index.render_content(tab))
        assert len(layout['response']['props']['children']) > 0
