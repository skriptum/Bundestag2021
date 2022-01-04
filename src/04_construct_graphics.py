import pandas as pd
import json 
import plotly.express as px
from utils import *

#%%
with open("../data/intermediate/Geometrie_Verkleinert.geojson") as f:
    geojs = json.load(f)

engine = connect_to_database()
wahlkreise_df = pd.read_sql("wahlkreise", engine)
users_df = pd.read_sql("users", engine)


mapbox_token = get_mapbox_token()

#%%

#partei color Map

partei_colors = {
        "CDU": "black",
        "SPD": "red",
        "GRÜNE": "green",
        "AfD": "blue",
        "FDP": "yellow",
        "DIE LINKE": "purple",
        "CSU": "grey"
}

#%%
###########################################################
# Chloropleth Map

fig = px.choropleth_mapbox(
    wahlkreise_df, geojson = geojs,
    featureidkey = "properties.WKR_NR",
    locations = "Gebietsnummer",
    color="Gruppenname",
    color_discrete_map=partei_colors,
    custom_data=["Gebietsname"]
)
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox = {
        "center": {"lon": 10.447 , "lat": 51.1633},
        "zoom": 4 },
    mapbox_accesstoken=mapbox_token,
    showlegend = False
    )

fig.update_traces(
       hovertemplate = "Wahlkreis : %{customdata[0]}"
    )
fig.show()


# %%
##########################################################

fig = px.treemap(
    users_df, path=["partei", "name"], values="followers_count",
    color = "partei",color_discrete_map=partei_colors 
    )
fig.update_traces(hovertemplate = "%{label} <br> Follower: %{value}")
fig.show()