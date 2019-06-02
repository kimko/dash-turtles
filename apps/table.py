import dash_table

from turtle_manager import Turtle_Manager

df = Turtle_Manager().get_turtles()

layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
    # n_fixed_rows=1,
    filtering=True,
    sorting=True,
    sorting_type="multi",
    pagination_mode="fe",
    pagination_settings={
        "current_page": 0,
        "page_size": 20,
    },
)
