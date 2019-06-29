from dash_html_components.Div import Div
from dash_core_components.Graph import Graph

import apps.explore_by_month as page
from turtle_manager import Turtle_Manager as tm

TURTLES = tm(test=True)


def test_layout():
    """
    Does my layout render as a Div?
    """
    assert isinstance(page.layout[0], Div)


def test_by_month_plot():
    """
    Do I render the bar plot?
    """
    df = TURTLES.get_df()
    df, years, caption = page.by_month_chart_format_data(df)
    by_moth_plot = page.by_month_plot(df, years, caption, 'Q')
    assert isinstance(by_moth_plot, Graph)
