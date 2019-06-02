import dash_table

from turtle_manager import Turtle_Manager

df = Turtle_Manager().get_turtles()

layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
