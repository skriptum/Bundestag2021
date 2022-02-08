from dash import dcc
from dash import html

def make_layout(draw):

    app_layout = html.Div(children=[

        ## left side
        html.Div(className = "four columns", children = [

            html.Div(children = [
                draw.user_profile("johannesvogel")
            ])
        ]),

        ## right side
        html.Div(className = "eight columns", children= [
            html.Div(children = [

                dcc.Graph(
                    figure=draw.choropleth(),
                    config={"displayModeBar":False}
                )
            ]),
            html.Div(children = [
                dcc.Graph(
                    figure=draw.bar_charts(),
                    config = {"responsive": False, "displayModeBar": False},
                )
            ]),
            html.Div(
                dcc.Graph(
                    figure=draw.treemap(),
                    config = {"responsive": False, "displayModeBar": False},
                )
            ),
        ]),
        
    ])
    return app_layout