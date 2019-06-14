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


def drpdwn_traceType(id):
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {"label": "Histogram", "value": "histogram"},
                {"label": "Bar", "value": "bar"},
                {"label": "Box", "value": "box"},
            ],
            value='histogram',
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


def drpdwn_frequency(id, option='all'):
    options = [
        {"label": "Daily", "value": "D"},
        {"label": "Weekly", "value": "W"},
        {"label": "Monthly", "value": "M"},
        {"label": "Quartlery", "value": "Q"},
        {"label": "Anually", "value": "A"},
    ]
    # Use Month and Quarter Only
    if option == 'MQ':
        options = options[2:4]
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=options,
            value='Q',
            clearable=False,
        ),
        className="two columns",
    )
    return div


def drpdwn_LocationPicker(id):
    # TODO use parameter for locations
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {"label": "Gresham","value": "Gresham"},
                {"label": "Mason Flats", "value": "Mason Flats"},
                {"label": "Whitaker Ponds", "value": "Whitaker Ponds"},
            ],
            multi=True,
            value=['Gresham', 'Mason Flats', 'Whitaker Ponds'],
        ),
        className="four columns",
    )
    return div
