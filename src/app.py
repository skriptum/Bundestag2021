from dash import Dash
from dash import dcc
from dash import html

import json
import pandas as pd

import graphics
from utils import *

app = Dash(
    __name__, title = "Bundestwitter", meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True
    ,)
server = app.server

## Data Sources
with open("../data/intermediate/Geometrie_verkleinert.geojson") as f:
    geojson = json.load(f)

engine = connect_to_database()
wahlkreise_df = pd.read_sql("wahlkreise", engine)
users_df = pd.read_sql("users", engine)

## set up graphing Class
draw = graphics.Graphics(wahlkreise_df, users_df, geojson)

app.layout = html.Div(children=[
    html.Div(
        dcc.Graph(
            figure=draw.choropleth(),
            config={"displayModeBar":False}
        )
    ),
    html.Div(
        dcc.Graph(
            figure=draw.bar_charts()
        )
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)

