import dash_bootstrap_components as dbc
from dash import html
#import dash_html_components as html
import dash_mantine_components as dmc
from components.logo import create_logo


layout = html.Div([
    #########################################      LOGO Y TITULO  ########################################################## 
     dbc.Row([dbc.Col(html.Div(create_logo()),width=4),
              dbc.Col(dmc.Center(html.H1('Sistema de Alertamiento de Riesgos de Corrupción en Contrataciones Públicas',
                                       style={"color":"#5c2335", 'textAlign': 'center',
                                             'font-family': 'Montserrat','font-size': '30px', 'font-weight': 'bold'})),
                      width=8)],
              className="g-0"),
#############################################     SECCIÓN INTRODUCTORIA   ############################################
    dbc.Row(
            html.H1(
            "Conoce los datos de las contrataciones del sector público, así como el nivel de riesgo institucional, a través de índices e indicadores basados en buenas prácticas nacionales e internacionales.",
                style={ 'textAlign': 'justify','font-family': 'Montserrat','font-size': '20px', 'font-weight': 'bold'})),
    dbc.Row([
        dbc.Col(html.H1(""),width=9),
        dbc.Col(dmc.Button("Conoce más",id="metodologia-home",style={'backgroundColor': '#5c2335', 'borderColor': '#5c2335'}, 
                           className="mr-2"),
                width=3),
    ]),
    
])