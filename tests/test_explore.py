from dash_html_components.Div import Div

import apps.explore as page


def test_layout():
    """
    Does my layout render as a Div?
    """
    assert isinstance(page.layout[0], Div)
