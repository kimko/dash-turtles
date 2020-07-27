import flask
import dash

from turtle_manager import Turtle_Manager

# TODO figure out why this gets currently called twice
# caller name: <frozen importlib._bootstrap>

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)
app.config.suppress_callback_exceptions = True
tm = Turtle_Manager()
