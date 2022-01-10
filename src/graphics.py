#%%
import pandas as pd
import json 
import plotly.express as px
import utils

from geojson_rewind import rewind

class Graphics():
    """ the central class for outsourcing all graphing capabilities"""
    margin={"r":0,"l":0,"t":0,"b":0}

    def __init__(self, wahlkreise_df, users_df, geojson, bg_color="white"):
        self.mapbox_token=utils.get_mapbox_token()
        self.wahlkreise_df = wahlkreise_df
        self.users_df = users_df
        self.bg_color = bg_color

        self._geojson = geojson

    @property
    def partei_colors(self, column="Gruppenname"):
        return {
            "CDU": "black",
            "SPD": "red",
            "GRÜNE": "green",
            "AfD": "blue",
            "FDP": "yellow",
            "DIE LINKE": "purple",
            "CSU": "grey"
            }

    @property
    def geojson(self):
        """ function to rewind (fix) the geojson and load it into the Instance, as described in this Issue: https://stackoverflow.com/questions/62719643/plotly-express-choropleth-only-shows-one-color"""

        return rewind(self._geojson, rfc7946=False)
        
    def choropleth(self, mapbox_style="carto-positron"):
        fig = px.choropleth_mapbox(
            #filter out all users with a twitter id
            self.wahlkreise_df[self.wahlkreise_df["id"].notna()],

            geojson = self.geojson,
            featureidkey = "properties.WKR_NR",
            locations = "Gebietsnummer",
            color="Gruppenname",
            color_discrete_map=self.partei_colors,
            custom_data=["Gebietsname"],
            opacity=0.6,
            #projection="mercator",
        )

        # fig.update_geos(fitbounds="geojson", visible=False,
        #     showcountries=True,
        #     bgcolor="grey",
        #     )
        fig.update_traces(
            marker_line_width=0.5,
            marker_line_color="white",
            hovertemplate = "Wahlkreis : %{customdata[0]}"
            )

        fig.update_mapboxes(
            style="mapbox://styles/pythons/cky9bifft7q2715nuxcxu7bdx",
            #custom style
            center={"lon": 10.447 , "lat": 51.1633},
            zoom=4,
            accesstoken=self.mapbox_token,
            )

        fig.update_layout(
            dragmode = False, showlegend=False,
            margin=self.margin)


        return fig


    def treemap(self):
        fig = px.treemap(
            self.users_df, 
            path=["partei", "name"], values="followers_count",
            color = "partei",color_discrete_map=self.partei_colors
            )
        fig.update_traces(hovertemplate = "%{label} <br> Follower: %{value}")

        return fig


    def bar_charts(self, column="followers_count", n=100):
        sorted_df = self.users_df.sort_values(column, ascending=False)
        sorted_df = sorted_df.reset_index()
        sorted_df = sorted_df[:n]

        fig = px.bar(
            sorted_df, y="followers_count", 
            color="partei", color_discrete_map=self.partei_colors
            )

        fig.update_layout(
        paper_bgcolor = self.bg_color,
        plot_bgcolor = self.bg_color, 
        showlegend = False
        )
        return fig
# %%

