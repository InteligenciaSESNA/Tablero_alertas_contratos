import dash
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html


app=dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
                                             meta_tags=[{'name':'viewport','content':'width=device-width, initial-scale = 1.0, maximum-scale=1.5, minimum-scale=1.0'}
                                                        ]
                                                        )
app.config.suppress_callback_exceptions=True

