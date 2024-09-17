import dash
from dash import  html
import app

def create_logo(): 
    sesna_logo=html.Img(src='assets/Logo_SNA.svg',

    style={'width':'80%','height':'25%',"background-color": "white",'margin-top': '0px'})



    return sesna_logo
