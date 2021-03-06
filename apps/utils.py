import inspect

import dash_html_components as html
import dash_core_components as dcc


def drpdwn_boxpoints(id):
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {'label': 'Outliers', 'value': 'outliers'},
                {'label': 'All', 'value': 'all'},
                {'label': 'Suspected', 'value': 'suspectedoutliers'},
                {'label': 'None', 'value': 'None'},
            ],
            value='all',
            clearable=False,
        ),
        className='two columns',
    )
    return div


def drpdwn_traceType(id):
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {'label': 'Histogram', 'value': 'histogram'},
                {'label': 'Bar', 'value': 'bar'},
                {'label': 'Box', 'value': 'box'},
            ],
            value='histogram',
            clearable=False,
        ),
        className='two columns',
    )
    return div


def drpdwn_tDimensions(id, default='Weight'):
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {'label': 'Weight', 'value': 'Weight'},
                {'label': 'Carapace', 'value': 'Carapace'},
                {'label': 'Plastron', 'value': 'Plastron'},
                {'label': 'Annuli', 'value': 'Annuli'},
            ],
            value=default,
            clearable=False,
        ),
        className='two columns',
    )
    return div


def drpdwn_oDimensions(id, default='None'):
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {'label': 'Annuli', 'value': 'Annuli'},
                {'label': 'Capture Location', 'value': 'Capture Location'},
                {'label': 'Gender', 'value': 'Gender'},
                {'label': 'None', 'value': 'None'},
            ],
            value=default,
            clearable=False,
        ),
        className='two columns',
    )
    return div


def drpdwn_frequency(id, option='all'):

    # Use Month and Quarter Only
    if option == 'MQS':
        options = [
            {'label': 'Monthly', 'value': 'M'},
            {'label': 'Quartlery', 'value': 'Q'},
            {'label': 'Seasonaly', 'value': 'S'},
        ]
    else:
        options = [
            {'label': 'Daily', 'value': 'D'},
            {'label': 'Weekly', 'value': 'W'},
            {'label': 'Monthly', 'value': 'M'},
            {'label': 'Quartlery', 'value': 'Q'},
            {'label': 'Anually', 'value': 'A'},
        ]

    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=options,
            value='Q',
            clearable=False,
        ),
        className='two columns',
    )
    return div


def drpdwn_LocationPicker(id):
    # TODO use parameter for locations
    div = html.Div(
        dcc.Dropdown(
            id=id,
            options=[
                {'label': 'Gresham', 'value': 'Gresham'},
                {'label': 'Mason Flats', 'value': 'Mason Flats'},
                {'label': 'Whitaker Ponds', 'value': 'Whitaker Ponds'},
            ],
            multi=True,
            value=['Gresham', 'Mason Flats', 'Whitaker Ponds'],
        ),
        className='four columns',
    )
    return div

def helper_print_caller():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print('caller name:', calframe[2][1])
