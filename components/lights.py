###############################alertamiento colores ############################
import dash
from dash import Dash, html

def get_opacity(value, range_min, range_max):
    if range_min <= value <= range_max:
        return 1.0
    return 0.15

# Función para crear un semáforo
def create_traffic_light(value):
    circle_style = {
        "width": "35px",
        "height": "35px",
        "borderRadius": "50%",
        "display": "inline-block",
        "margin": "8px"
    }
    return html.Div([
        html.Div(style={**circle_style, "backgroundColor": "green", "opacity": get_opacity(value, 0, 20)}),
        html.Div(style={**circle_style, "backgroundColor": "#7cae2f", "opacity": get_opacity(value, 20.001, 40)}),
        html.Div(style={**circle_style, "backgroundColor": "#F2E205", "opacity": get_opacity(value, 40.001, 60)}),
        html.Div(style={**circle_style, "backgroundColor": "#F2762E", "opacity": get_opacity(value, 60.001, 80)}),
        html.Div(style={**circle_style, "backgroundColor": "red", "opacity": get_opacity(value, 80.001, 100)}),
        html.Div(f'{value}%',style={"margin-bottom":"10px","color":"#515151", 'font-family': 'Montserrat','font-size': '20px', 'font-weight': 'bold',"display": "inline",}),
        
    ],)