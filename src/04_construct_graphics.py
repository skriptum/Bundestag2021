import pandas as pd
import json 
import plotly.express as px
from utils import *

#%%
with open("../data/intermediate/Geometrie_Verkleinert.geojson") as f:
    geojs = json.load(f)

engine = connect_to_database()
wahlkreise_df = pd.read_sql("wahlkreise", engine)

#%%
###########################################################
# Chloropleth Map

fig = px.choropleth_mapbox(
    wahlkreise_df, geojson = geojs,
    featureidkey = "properties.WKR_NR",
    locations = "Gebietsnummer",
    color="Gruppenname",
    color_discrete_map={
        "CDU": "black",
        "SPD": "red",
        "GRÜNE": "green",
        "AfD": "blue",
        "FDP": "yellow",
        "DIE LINKE": "purple",
        "CSU": "grey"
    },
    custom_data=["Gebietsname"]
)
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox = {
        "center": {"lon": 10.447 , "lat": 51.1633},
        "zoom": 4 },
    showlegend = False
    )

fig.update_traces(
       hovertemplate = "Wahlkreis : %{customdata[0]}"
    )
fig.show()


# %%
##########################################################

