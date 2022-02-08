
import pandas as pd
import json 
import plotly.express as px
import utils

from dash import html

from geojson_rewind import rewind

class Graphics():
    """ the central class for outsourcing all graphing capabilities"""
    margin={"r":0,"l":0,"t":0,"b":0}
    paper_bgcolor = "white"
    plot_bgcolor = "#f7f7f7"

    def __init__(self, wahlkreise_df, users_df, geojson):
        self.mapbox_token=utils.get_mapbox_token()
        self.wahlkreise_df = wahlkreise_df
        self.users_df = users_df

        self._geojson = geojson

    @property
    def partei_colors(self, column="Gruppenname"):
        return {
            "CDU": "#323232",
            "SPD": "#b90e0e",
            "GRÜNE": "#58af09",
            "AfD": "#2a6aca",
            "FDP": "#e2bc08",
            "DIE LINKE": "#c31570",
            "CSU": "#989898",
            '(?)': self.plot_bgcolor # for the treemap
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
            path=[px.Constant("Bundestag"),"partei","name"], values="followers_count",
            color = "partei",color_discrete_map=self.partei_colors
            )
        fig.update_traces(hovertemplate = "%{label} <br> Follower: %{value}")
        fig.update_layout(margin = self.margin)
        return fig


    def bar_charts(self, column="followers_count", n=15):
        sorted_df = self.users_df.sort_values(column, ascending=False)
        sorted_df = sorted_df.reset_index()
        sorted_df = sorted_df[:n]
        sorted_df = sorted_df.iloc[::-1]

        fig = px.bar(
            sorted_df, 
            x="followers_count", 
            color="partei", 
            color_discrete_map=self.partei_colors,
            orientation="h",
            text = "username",
            custom_data=["name"]
            )


        fig.update_layout(
        paper_bgcolor = self.paper_bgcolor,
        plot_bgcolor = self.plot_bgcolor, 
        showlegend = False, 
        margin = self.margin,
        )

        fig.update_xaxes(
            #visible = False,
            showticklabels=True,
            title = "Anzahl Follower",
            fixedrange=True,
            side="top",
        )
        fig.update_yaxes(
            visible=False,
            fixedrange = True,
            autorange="reversed",
        )

        fig.update_traces(
            textposition="auto",
            hovertemplate = "%{customdata[0]} : %{x}"
            )
        return fig


    def user_profile(self, username):
        row = self.users_df[self.users_df.username == username]

        #change the image url so it points to large file
        img_src = row.profile_image_url.item().replace("_normal", "")

        div = html.Div(children = [

            # profile image 
            html.Img(src=img_src,
            style = {"height": "110px", "width": "110px", "border-radius":"50%", "margin": "10px", "border": "1px solid"}
            ),

            html.B(row.followers_count),

        ])

        return div