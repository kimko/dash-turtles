import dash_html_components as html
import dash_core_components as dcc


def drpdwn_boxpoints(id):
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {"label": "Outliers", "value": "outliers"},
                {"label": "All", "value": "all"},
                {"label": "Suspected", "value": "suspectedoutliers"},
                {"label": "None", "value": False},
            ],
            value=False,
            clearable=False,
        ),
        className="two columns",
    )
    return div


def drpdwn_tDimensions(id):
    div = html.Div(
        dcc.Dropdown(
            id="box1_dwn_y",
            options=[
                {"label": "Weight", "value": "Weight"},
                {"label": "Carapace", "value": "Carapace"},
                {"label": "Plastron", "value": "Plastron"},
                {"label": "Annuli", "value": "Annuli"},
            ],
            value="Weight",
            clearable=False,
        ),
        className="two columns",
    )
    return div
