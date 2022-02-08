from dash import dcc
from dash import html

def make_layout(draw):

    app_layout = html.Div(children=[
        html.Div(
            dcc.Graph(
                figure=draw.choropleth(),
                config={"displayModeBar":False}
            )
        ),
        html.Div(
            dcc.Graph(
                figure=draw.bar_charts(),
                config = {"responsive": False, "displayModeBar": False},
            )
        ),
        html.Div(
            dcc.Graph(
                figure=draw.treemap(),
                config = {"responsive": False, "displayModeBar": False},
            )
        ),

        html.Div(
            draw.user_profile("johannesvogel")
        )
    ])
    return app_layout