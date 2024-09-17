import app
import dash
from dash import html,dcc
import dash_mantine_components as dmc
from dash.dependencies import Input, Output
from dash_iconify import DashIconify
from layouts.home_layout import layout as home_layout
from layouts.general_layout import layout as general_layout
from layouts.proveedores_layout import layout as proveedores_layout
from layouts.redes_layout import layout as redes_layout
from layouts.conoce_layout import layout as conoce_layout
from callbacks.general_callbacks import register_callbacks as register_callbacks_general





app=dash.Dash(__name__)
  # Definición de la aplicación Dash
app.config.suppress_callback_exceptions=True
app.layout = html.Div([
    dmc.Tabs(
        [
            dmc.TabsList([
                dmc.Tab("Home",icon=DashIconify(icon="mdi:home-variant",color="#5c2335"),value="tab-home"),
                dmc.Tab("Instituciones públicas",icon=DashIconify(icon="material-symbols:contract",color="#5c2335"),value="tab-contratos"),
                dmc.Tab("Proveedores",icon=DashIconify(icon="mdi:person-badge-outline",color="#5c2335"),value="tab-proveedor"),
                dmc.Tab("Redes",icon=DashIconify(icon="carbon:network-4",color="#5c2335"),value="tab-redes"),
                dmc.Tab("Conoce más",icon=DashIconify(icon="ph:question-fill",color="#5c2335"),value="tab-conoce"),
            ],position="apart",),
        ],id="tabs", value="tab-contratos",
    ),
    
    html.Div(id='tabs-content')
])

####################################  LLAMADA    GENERAL   #################################### 

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')])

def render_content(tab):
    if tab == 'tab-home':
        return home_layout
    if tab == 'tab-contratos':
        return general_layout
    elif tab == 'tab-proveedor':
        return proveedores_layout
    elif tab == 'tab-redes':
        return redes_layout
    elif tab == 'tab-conoce':
        return conoce_layout
    else:
        return '404 Page Not Found'

# Registrar los callbacks
register_callbacks_general(app)

if __name__ == '__main__':
    app.run_server(debug=True)
    