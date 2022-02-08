## imports
from dash import Dash
from dash import dcc
from dash import html

import json
import pandas as pd

from utils import *
from layout import make_layout
from graphics import Graphics

## define the app instance
app = Dash(
    __name__, title = "Bundestwitter", meta_tags=[{"name": "viewport", "content": "width=device-width"}],suppress_callback_exceptions=True
    ,)
server = app.server

## Data Sources
with open("../data/intermediate/Geometrie_verkleinert.geojson") as f:
    geojson = json.load(f)

engine = connect_to_database()
wahlkreise_df = pd.read_sql("wahlkreise", engine)
users_df = pd.read_sql("user_with_metrics", engine)

## set up graphing class
draw = Graphics(wahlkreise_df, users_df, geojson)

## import the layout from layout.py
app.layout = make_layout(draw)

## callbacks

## run
if __name__ == "__main__":
    app.run_server(debug=True)

