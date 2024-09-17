from dash import dcc
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
#import dash_html_components as html
import pandas as pd
import dash_mantine_components as dmc
from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Format
from dash_iconify import DashIconify
import dash_daq as daq
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np 
from app import app
from components.lights import create_traffic_light
from components.logo import create_logo


general_df = pd.read_csv('datasets/general7.csv',sep="|")
supplier_inst = pd.read_csv('datasets/supplier_inst.csv',sep="|")
indic_gral= pd.read_csv('datasets/indicadores_gral2.csv',sep="|")
proveedor=pd.read_csv('datasets/proveedores.csv',sep="|")
items_principal=pd.read_csv('datasets/items_principal.csv',sep="|")

money = FormatTemplate.money(2)
#percentage = FormatTemplate.percentage(2)
actualizado="21-Septiembre-2023"

##Columnas para tabla de estadisticas por tipo de procedimiento
columns = [
    dict(id='tipo_proc', name='Procedimiento'),
    dict(id='monto_mxn', name='Monto', type='numeric', format=money),
    dict(id='n_contratos', name='Número de contratos', type='numeric',format=Format(group=True, groups=[3]))
]

##columnas para tabla de proveedores
columns_prov = [
    dict(id='suppliers_name', name='Proveedor'),
    dict(id='monto_supp', name='Monto', type='numeric', format=money),
    dict(id='n_contracts', name='Número de contratos', type='numeric',format=Format(group=True, groups=[3]))
]

layout = html.Div(
    children=[

#########################################      LOGO Y TITULO  ########################################################## 
    dmc.Grid(
        children=[
        dmc.Col(html.Div(create_logo()), span=4),
        dmc.Col(html.Div(
            html.H1('Sistema de Alertamiento de Riesgos de Corrupción en Contrataciones Públicas',
                          style={"color":"#5c2335", 'textAlign': 'center',
                                 'font-family': 'Montserrat','font-size': '40px', 'font-weight': 'bold', 'margin-top': '100px'}
                                 )), span=8),
        ],gutter="xs", align="stretch",grow=True,
    ),


     #dbc.Row([dbc.Col(html.Div(create_logo()), width=3,# style={'display': 'flex', 'alignItems': 'center'}
      #                ),
       #       dbc.Col(html.Div(
                  #dmc.Space(h=20),

        #          html.H1('Sistema de Alertamiento de Riesgos de Corrupción en Contrataciones Públicas',
         #                 style={"color":"#5c2335", 'textAlign': 'center',
          #                       'font-family': 'Montserrat','font-size': '35px', 'font-weight': 'bold', 'margin': '0'}
           #                      )
            #  ), 
             # width="auto",
              # # style={'display': 'flex', 'alignItems': 'center'},
              #       )],
            # className="g-0"),
    dmc.Space(h=20),
#############################################     SECCIÓN INTRODUCTORIA   ############################################
    dbc.Row(
            html.H1(
            "Conoce los datos de las contrataciones del sector público, así como el nivel de riesgo institucional, a través de índices e indicadores basados en buenas prácticas nacionales e internacionales.",
                style={ 'textAlign': 'justify','font-family': 'Montserrat','font-size': '30px', 'font-weight': '600','color':'#56565A'})),
    dbc.Row([
        dbc.Col(html.H1(""),width=9),
        dbc.Col(dmc.Button("Conoce más",id="metodologia",style={'backgroundColor': '#5c2335', 'borderColor': '#5c2335'}, 
                           className="mr-2"),
                width=3),
    ]),
        
    dmc.Space(h=40),
    
    dmc.Tooltip(
        label="El buscador permite seleccionar una institución pública y un ejercicio fiscal para obtener los datos, "
        " gráficas y análisis de las contrataciones públicas de dicha institución. Los años fiscales que aparecen ahí varían "
        " dependiendo de la información que las mismas instituciones públicas hayan cargado o interconectado a la "
        " plataforma de CompraNet y a la Plataforma Digital Nacional.", 
        position="bottom",
        withArrow=True,
        transition="fade",
        transitionDuration=200,
        multiline=True,
        closeDelay=600,
        color="gray",
        style={"fontFamily": "Montserrat", "font-size": "15px", "textAlign": "justify",
                        "textJustify":"inter-word"},
        children=dmc.Group([
            dmc.Text("Buscador de instituciones:", ta="left", size="xl",fw=600,
                     style={'font-family': 'Montserrat'},
                    ),
            DashIconify(icon='typcn:info-outline', width=20, id="info-icon")],position="left",)
    ),
    
    dmc.Text("Selecciona institución y año", ta="left", size="xl",c="gray",fw=600,style={'font-family': 'Montserrat' }),    
             
    dmc.Space(h=10),

################################################  S E L E C T O R E S  ############################################
    dmc.Grid(
        children=[
        dmc.Col(dcc.Dropdown(
            general_df.sort_values('name').name.unique(),id='name_dropdown', 
              style={'background-color':'#F6FBFF', 'font-size': 20},
              placeholder="Selecciona una institución"), span=8),
        dmc.Col(dcc.Dropdown(id='anio_dropdown', style={'background-color':'#F6FBFF','color':'black','font-size': 20},
                             placeholder="Selecciona un año"), span=2),
        dmc.Col(dmc.Button("Actualizar",id="submit-button", variant="filled"),span=2),
        ],gutter="xs", align="stretch",grow=True,
    ),   
    dmc.Space(h=15),  



    dmc.Space(h=15),
    
    #html.Div([
     #   dbc.Row([
      #      dbc.Col(
       #         dcc.Dropdown(
        #            #options=[{'label': name, 'value': name} for name in general_df.sort_values('name').name.unique()],
         #            general_df.sort_values('name').name.unique(),id='name_dropdown', 
          #           style={'background-color':'#F6FBFF'},
           #          placeholder="Selecciona una institución"),width=8),
            #dbc.Col(dcc.Dropdown(id='anio_dropdown',
             #                    style={'background-color':'#F6FBFF','color':'black'},
              #                   placeholder="Selecciona un año"),width=2),
            #dbc.Col(dmc.Button("Actualizar",id="submit-button", variant="filled"),width=2),
            #]),
      #  dmc.Space(h=15),
    #]),
    
##################################  CIFRAS NARRATIVAS DE LA INSTITUCIÓN    #############################################    
    html.Div([
        dmc.Card( 
            children=[
                dmc.Space(h=15),
                
                dmc.Center("Cifras acumuladas de la institución",style={'font-family': 'Montserrat', "width": "100%",
                                                                         'color':'white','font-size': '30px', 'font-weight': 'bold'}),
                dmc.Space(h=15),
                #dmc.Group([
                 #   DashIconify(icon='material-symbols:summarize-outline-sharp', width=50,height=50, id="info-icon",color='white'),
                 #   html.Div(["Cifras acumuladas de la institución",
                  #            ],style={'font-family': 'Montserrat','font-size':'35px','color':'white','font-weight': 'bold'}),
                    #],position="center",),
                dmc.Group([
                    DashIconify(icon='ant-design:alert-twotone', width=25, id="info-icon",color='#f1e5e5'),
                    html.Div(["Los resultados pueden no contemplar el total de contratos de la institución; únicamente se incluyen los registrados bajo el Estandar de Datos de Contrataciones Abiertas en CompraNet, seleccionando aquellos con estatus registrado como completo",
                              ],style={'font-family': 'Montserrat','font-size':'18px','color':'#f1e5e5','textAlign': 'justify'}),

                    ],position="left",spacing="xs"),
                      
                      
                

                dmc.Space(h=20),                                                      
                dmc.CardSection(
                dmc.SimpleGrid(cols=3,
                              children=[
                                  html.Div([
                                  dmc.Text("Total de contratos",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Space(h=10),
                                  dmc.Text("",id="c1",color="white",
                                           style={'font-family': 'Montserrat','font-size': '25px', 'font-weight': 'bold',
                                                  'textAlign': 'center'}),]),
                                  html.Div([
                                  dmc.Text("Monto de los contratos",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Space(h=10),
                                  dmc.Text("",id="c2",color="white",
                                           style={'font-family': 'Montserrat', 'font-size': '25px', 'font-weight': 'bold',
                                                 'textAlign': 'center'}),
                                  ]),
                                  html.Div([
                                  dmc.Text("Proveedores únicos",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Space(h=10),
                                  dmc.Text("",id="c3",color="white",
                                           style={'font-family': 'Montserrat' ,'font-size': '25px', 'font-weight': 'bold',
                                                 'textAlign': 'center'})]),
                              ])
                ),
                dmc.Space(h=15),
            ],style={'backgroundColor': '#5c2335', 'borderColor': '#5c2335'}
        ), 
        
        
    ],),
   

#####################################ESTADISTICAS POR TIPO DE PROCEDIMIENTO NARRATIVAS######################################

    html.Div([
        
        dmc.Card( 
            children=[
                dmc.Center("Porcentaje de contratos por tipo de procedimiento",style={'font-family': 'Montserrat', "width": "100%",
                                                                       'color':'white','font-size': '30px', 'font-weight': 'bold'}),
                dmc.Space(h=20),
                                                                       
                dmc.CardSection(
                dmc.SimpleGrid(cols=4,
                              children=[
                                  html.Div([
                                   dmc.Text("Adjudicación directa",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Text("",id="e1",color="white",
                                           style={'font-family': 'Montserrat','font-size': '25px', 'font-weight': 'bold',
                                                  'textAlign': 'center'}),]),
                                  html.Div([
                                   dmc.Text("Licitación pública",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Text("",id="e2",color="white",
                                           style={'font-family': 'Montserrat', 'font-size': '25px', 'font-weight': 'bold',
                                                 'textAlign': 'center'}),
                                  ]),
                                  html.Div([
                                  dmc.Text("Invitación a cuando menos tres personas",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Text("",id="e3",color="white",
                                           style={'font-family': 'Montserrat' ,'font-size': '25px', 'font-weight': 'bold',
                                                 'textAlign': 'center'})]),
                                  html.Div([
                                  dmc.Text("Contratos marco",size="xl",color="#f1e5e5",ta="center",style={'font-family': 'Montserrat' }),
                                  dmc.Text("",id="e4",color="white",
                                           style={'font-family': 'Montserrat' ,'font-size': '25px', 'font-weight': 'bold',
                                                 'textAlign': 'center'})]),
                                  
                              ])
                ),
                dmc.Space(h=20),
                dmc.Text(id="resumen",size="xl",color="white",ta="center",style={'font-family': 'Montserrat'}),
                dmc.Space(h=15),
                dmc.Tooltip(
                label="Fuente: CompraNet", 
                position="bottom",
                withArrow=True,
                transition="fade",
                transitionDuration=200,
                multiline=True,
                closeDelay=600,
                color="gray",
                style={"fontFamily": "Montserrat", "font-size": "15px", "textAlign": "justify",
                        "textJustify":"inter-word"},
                children=dmc.Group([
                    dmc.Text("Última actualización: 21-Septiembre-2023", ta="left", size="sm",color="white",
                         style={'font-family': 'Montserrat'},
                        ),
                    DashIconify(icon='typcn:info-outline', width=20, id="info-icon",color="white")],position="left",)
                ),                
            ],style={'backgroundColor': '#5c2335', 'borderColor': '#5c2335'}
        ), 
       
        
        
    ],),
    dmc.Space(h=15),
    dmc.Divider(variant="solid",color="rgb(100,67,97)"),
    dmc.Space(h=15),
    
####################################################################################################################################
   ################################      SISTEMA DE ALERTAMIENTO         ############################################################### 
    dmc.Text(id="alertamiento" ,color="#5c2335",ta="center",fw=500,style={'font-family': 'Montserrat',"fontSize": 30}),
    dmc.Space(h=20),
        #######################################################################################################################
    dmc.Grid(
    children=[
        dmc.Col(
            dmc.Accordion(
                dmc.AccordionItem([
                    dmc.AccordionControl("Conoce más",
                                        icon=DashIconify(icon="codicon:book",color="#5c2335",width=20,)
                                         ,),
                    dmc.AccordionPanel( 
                        dmc.Text(
                            "Con el objetivo de generar y proponer una serie de indicadores que señalen banderas rojas dentro de las instituciones "
                            "a nivel nacional para la identificación de riesgos en procedimientos de contrataciones públicas, se revisaron diversas "
                            "metodologías y buenas prácticas nacionales e internacionales que han sido probadas en casos. Después de la revisión de "
                            "diversas metodologías y de la identificación de variables, se compararon los indicadores encontrados en las buenas "
                            "prácticas para analizar similitudes y concordancia entre ellos. Lo anterior se realizó con base en los conceptos: "
                            "competencia o falsa competencia; irregularidades en la asignación, transparencia; cumplimiento de la ley; "
                            "modificaciones al contrato preferencia por un proveedor; inconsistencias de información; corrupción; y adjudicaciones "
                            "directas injustificadas. A partir de lo anterior, se clasificaron los indicadores en las tres fases de un proceso de "
                            "contratación: a) planeación o pre-procedimiento; b) procedimiento; y c) conclusión o post-procedimiento. Asimismo, "
                            "se decidió agrupar los indicadores en cinco índices: un índice para la etapa de pre-procedimiento; tres índices para la "
                            "fase de procedimiento; y un índice para el post-procedimiento. En esta primera etapa de implementación de la Acción 2, "
                            "los indicadores relacionados con la pre-contratación y la post-contratación no pudieron ser piloteados, ya que no existen "
                            "datos en fuentes públicas para las variables que integran esos indicadores. Sin embargo, se espera que, una vez que se "
                            "concluya con los procesos de interconexión al S6 de la PDN, éstos podrán ser calculados para todas las instituciones y "
                            "entidades federativas. Para la obtención de la información de contrataciones para la primera fase, se desarrolló un "
                            "proceso de extracción y transformación de datos a partir de las fuentes públicas disponibles. Lo anterior con la finalidad "
                            "de que las bases de datos utilizadas para calcular los indicadores contaran con un modelo de datos estructurados y "
                            "relacionados.", size="lg", style={'font-family': 'Montserrat'},ta="justify")
                            ),
                    
                ],value="customization"
                ),chevronPosition='right'
            ), span=12),
    ],
    gutter="xl",
    ),
    dmc.Space(h=30),
    
    ##########################  ESPECIFICAR UNIVERSO ##############################################################
    
    dmc.Group([
        DashIconify(icon='typcn:info-outline', width=20, id="info-icon"),
        html.Div([
                "Universo: El universo de cálculo de alertamientos excluye ",
            html.Span("los contratos marco", style={"color": "red"}), " debido a que éstos no dependen de la institución pública analizada.",
            ], style={'font-family': 'Montserrat','font-weight': 'bold'}),
        ],position="left",),
    dmc.Space(h=25),
    
    
    #####################################   KPIS  ##################################################################
    dmc.Grid(
        children=[
            dmc.Col(
                dmc.Card(
                    children=[
                        dmc.CardSection([
                            dmc.Center(
                                dmc.Tooltip(
                                    dmc.Text("Índice de Transparencia                                      ",
                                     ta="center",style={'font-family': 'Montserrat'},fw=600,size="lg"),
                                    label=
                                    """
                                    Índice de transparencia: evalúa qué tan transparente ha sido una institución a lo largo de sus procedimientos de
                                    contratación. Por una parte, busca medir si la institución hace pública la documentación relacionada con los
                                    procedimientos de contratación como lo son: convocatoria, acta de fallo, y contrato. Asimismo, evalúa la coherencia
                                    entre las fechas de publicación de la convocatoria, del fallo y el inicio del contrato con la finalidad de identificar si se
                                    intentó realizar alguna acción opaca.
                                    """,
                                    position="bottom",
                                    withArrow=True,
                                    transition="fade",
                                    transitionDuration=200,
                                    multiline=True,
                                    closeDelay=600,
                                    color="gray",
                                    style={"fontFamily": "Montserrat", "font-size": "15px", "textAlign": "justify",
                                           "textJustify":"inter-word"}),
                            ),
                            dmc.Space(h=8),
                            dmc.Center(                                                              
                                daq.Gauge(id='our-gauge',                                      
                                min=0,
                                max=100,
                                showCurrentValue=True,
                                label="",
                                units="%",
                                color={'gradient':True,
                                       'ranges':{ "green":[0, 20],
                                                 "#7cae2f":[20, 40],
                                                 "yellow":[40, 60],
                                                 "orange":[60, 80],
                                                 'darkred':[80, 100],
                                                      },},
                                style={"align": "center",'font-family': 'Montserrat','color':'black',
                                      "display": "flex",'font':'70'},
                                         ),
                            ),
                            #dcc.Graph(id='kpi-transparencia'),# Gráfico KPI
                            
                            ########################################################################################
                            dmc.CardSection(children=[
                                dmc.SimpleGrid(cols=1,
                                                children=[
                                                    html.Div([
                                                        dmc.Text("AD sin publicación de contrato",ta="center",
                                                                     size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(dmc.Center(html.Div(id='semaforo-t1')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-t1",size="sm",fw=500,color="#515151",
                                                                             #ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ] ),
                                                            
                                                                                                                
                                                        
                                                         #################################################
                                                        dmc.Space(h=10),
                                                        dmc.Text("LP/INV3 sin publicación de convocatoria",ta="center",
                                                                 size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-t2')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-t2",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),
                                                        
                                                        
                                                        ########################################################
                                                        dmc.Space(h=10), 
                                                        dmc.Text("LP/INV3 sin publicación del fallo",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-t3')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-t3",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),                                                      
                                                                                                               
                                                        
                                                        
                                                        ###################################################
                                                         dmc.Space(h=10),
                                                        dmc.Text("Convocatoria de LP/INV3 publicada tras inicio del contrato",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                         dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-t4')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-t4",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                         ]),
                                                        
                                                        
                                                        ########################################################
                                                        dmc.Space(h=10),
                                                        dmc.Text( "LP/INV3 con publicación de fallo posterior al inicio del contrato",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-t5')),width=12),
                                                           # dbc.Col(dmc.Text(id="label-t5",size="sm",fw=500,color="#515151",
                                                            #                 ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),
                                                        
                                                        
                                                            ]),                                                   
                                                ],),
                                
                        ])
                    ])
                ]),span=4),
            
            
            ##############################################################################################################
            dmc.Col(
                dmc.Card(
                    children=[
                        dmc.CardSection([
                            dmc.Center(
                            dmc.Tooltip(
                            dmc.Text("Índice de Competencia",
                                      ta="center",style={'font-family': 'Montserrat'},fw=600,size="lg"),
                                label=
                                """
                                Índice de competencia: identifica la existencia de una diversidad de proveedores que presenten propuestas de bienes y
                                servicios con diferentes precios y calidad en un procedimiento de contratación pública. Se toman en cuenta el número                      
                                de adjudicaciones directas se han realizado en una institución, así como si éstas cuentan con la publicación del
                                fundamento legal correspondiente. Respecto a los procedimientos en los que debería haber más de un participante
                                (licitación pública e invitación a cuando menos tres personas), se evalúa que el número de licitantes no sea uno. De
                                igual manera, se analiza si el periodo de apertura de proposiciones es corto. Por último, se evalúa la proporción
                                respecto del total de monto utilizado en procedimientos de contrataciones que corresponde a adjudicaciones directas y
                                a invitación a cuando menos tres personas.
                                """,
                                position="bottom",
                                withArrow=True,
                                transition="fade",
                                transitionDuration=200,
                                multiline=True,
                                closeDelay=600,
                                color="gray",
                                style={"fontFamily": "Montserrat"},
                            ), ),
                            
                            dmc.Center(                                                              
                                daq.Gauge(id='our-gauge2',                                      
                                min=0,
                                max=100,
                                showCurrentValue=True,
                                label="",
                                units="%",
                                color={'gradient':True,
                                       'ranges':{ "green":[0, 20],
                                                 "#7cae2f":[20, 40],
                                                 "yellow":[40, 60],
                                                 "orange":[60, 80],
                                                 'darkred':[80, 100],
                                                      },},
                                style={"align": "center",'font-family': 'Montserrat','color':'black',
                                      "display": "flex",'font':'70'},
                                         ),
                            ),
                                                       
                                                        

                            dmc.CardSection(children=[
                                dmc.SimpleGrid(cols=1,
                                                children=[
                                                    html.Div([
                                                        dmc.Text("Expedientes asignados por AD",ta="center",
                                                                    size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-c1')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-c1",size="sm",fw=500,color="#515151",
                                                                        #     ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),
                                                                                                        
                                                        ##################################################   
                                                        dmc.Space(h=10), 
                                                        dmc.Text("AD sin fundamento legal",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-c2')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-c2",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),  
                                                        
                                                        

                                                        ##################################################
                                                        
                                                        dmc.Space(h=10), 
                                                        dmc.Text("LP/INV3 con un solo participante",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-c3')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-c3",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),  
                                                        
                                                        

                                                        ##################################################
                                                        
                                                        dmc.Space(h=10), 
                                                        dmc.Text("LP/INV3 con periodos de apertura de proposiciones inferior al esperado",ta="center",
                                                                 size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-c4')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-c4",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),  
                                                        
                                                        

                                                        ##################################################
                                                        
                                                        dmc.Space(h=10), 
                                                        dmc.Text( "Proporción de monto por AD e INV3  respecto al total",ta="center",
                                                                 size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-c5')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-c5",size="sm",fw=500,color="#515151",
                                                                            # ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),  
                                                        
                                                        ]),                                                   
                                                ],),
                                
                        ])
                    ])
                ],),span=4),
            dmc.Col(
                dmc.Card(
                    children=[
                        dmc.CardSection([
                            dmc.Center(
                                dmc.Tooltip(
                                    dmc.Text("Índice de Irregularidades", 
                                             ta="center",style={'font-family': 'Montserrat'},fw=600,size="lg"),
                                    label=
                                    """Índice de irregularidades en la contratación: busca identificar si los proveedores seleccionados se encuentran en las
                                    listas de contribuyentes con operaciones presuntamente inexistentes del Servicio de Administración Tributaria (SAT),
                                    proveedores sancionados o inhabilitados por la Secretaría de la Función Pública (SFP) y en el Registro Único de Proveedores
                                    y Contratistas (RUPC). El índice también mide las posibles inconsistencias de las empresas proveedoras como si éstas son
                                    de reciente creación o si la información de la dirección es incompleta.
                                    """,
                                    position="bottom",
                                    withArrow=True,
                                    transition="fade",
                                    transitionDuration=200,
                                    multiline=True,
                                    closeDelay=600,
                                    color="gray",
                                    style={"fontFamily": "Montserrat"},                               
                                ),
                            ),
                            dmc.Center(                                                              
                                daq.Gauge(id='our-gauge3',                                      
                                min=0,
                                max=100,
                                showCurrentValue=True,
                                label="",
                                units="%",
                                color={'gradient':True,
                                       'ranges':{ "green":[0, 20],
                                                 "#7cae2f":[20, 40],
                                                 "yellow":[40, 60],
                                                 "orange":[60, 80],
                                                 'darkred':[80, 100],
                                                      },},
                                style={"align": "center",'font-family': 'Montserrat','color':'black',
                                      "display": "flex",'font':'70'},
                                         ),
                            ),
                            

                            dmc.CardSection(children=[
                                dmc.SimpleGrid(cols=1,
                                                children=[
                                                    html.Div([
                                                        #######################################
                                                        dmc.Text("Adjudicaciones a proveedores sancionados/inhabilitados",ta="center",
                                                                    size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-i1')),width=12),
                                                           # dbc.Col(dmc.Text(id="label-i1",size="sm",fw=500,color="#515151",
                                                            #                 ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),

                                                        

                                                        #######################################
                                                        dmc.Space(h=10), 
                                                        dmc.Text("Adjudicaciones a proveedores con operaciones presuntamente inexistentes",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-i2')),width=12),
                                                           # dbc.Col(dmc.Text(id="label-i2",size="sm",fw=500,color="#515151",
                                                            #                 ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]), 
                                                        

                                                        #######################################
                                                        dmc.Space(h=10), 
                                                        dmc.Text("Adjudicaciones a proveedores no registrados en padrón de proveedores",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-i3')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-i3",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]), 
                                                        
                                                        

                                                        #######################################
                                                        dmc.Space(h=10), 
                                                        dmc.Text("Adjudicaciones a empresas de reciente creación",ta="center",
                                                                 size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-i4')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-i4",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]), 
                                                        
                                                        

                                                        #######################################
                                                        dmc.Space(h=10), 
                                                        dmc.Text("Expedientes sin información del domicilio del proveedor",ta="center",
                                                                size="lg",fw=500,color="#515151",style={'font-family': 'Montserrat'}),
                                                        dbc.Row([
                                                            dbc.Col(
                                                                dmc.Center(html.Div(id='semaforo-i5')),width=12),
                                                            #dbc.Col(dmc.Text(id="label-i5",size="sm",fw=500,color="#515151",
                                                             #                ta="left",style={'font-family': 'Montserrat'}),width=1)
                                                        ]),
                                                    ]),                                                   
                                                ],),
                                
                        ])
                    ])
                ]),span=4),     
   
    ]),
   
#############################################
    
    dmc.Space(h=150), 
    ########################## EMPIEZAN  DESCRIPTIVOS ############################################################
    
    dmc.Text("Análisis descriptivo" ,color="#5c2335",ta="center",fw=500,
             style={'font-family': 'Montserrat',"fontSize": 35}),
    dmc.Space(h=20), 
    
    ##################################################################################################################
    ################################### P R O V E E D O R E S ####################################################
  
    dmc.Center([
        dmc.Tooltip(
            label="Ultima actualización:21-Septiembre-2023",
            position="top",
            withArrow=True,
            transition="fade",
            transitionDuration=200,
            multiline=True,
            closeDelay=600,
            color="gray",
            style={"fontFamily": "Montserrat", "font-size": "15px", "textAlign": "justify",
                        "textJustify":"inter-word"},
            children=[
                dmc.Group([
                    DashIconify(icon='typcn:info-outline', width=20, id="info-icon"),
                    dmc.Text("¿Quiénes fueron los proveedores?",fw=500,ta="center",
                             style={'font-family': 'Montserrat', "font-size": "25px",},)],position="center",),
            ]
        ),
    ]),
    
    dmc.Center(
        
        dash_table.DataTable(proveedor.head().to_dict('records'),columns_prov,
                             id='tabla_prov',style_as_list_view=True,
                             fixed_rows={'headers': True},
                             style_table={'height': 550},
                             style_data={'whiteSpace': 'normal','height': 'auto'},
                             style_header={ "color": "#515151",'fontWeight': 'bold','padding':'10px',
                                           'backgroundColor': 'lightgray','font-family': 'Montserrat'},
                             style_cell={'padding': '8px','textAlign': 'left','font-family': 'Montserrat',
                                         'minWidth': 400, 'maxWidth': 600, 'width': 600,},
                             fill_width=False,
                             style_cell_conditional=[
                                 {'if': {'column_id': 'n_contracts'},
                                  'width': '15%','textAlign': 'center'},
                                 {'if': {'column_id': 'suppliers_name'},
                                  'width': '50%'},
                                 {'if': {'column_id': 'monto_supp'},
                                  'width': '10%','textAlign': 'center'},
                             ]
                            
                                                
                                                    ),
    ),
    dmc.Space(h=15),
    
    ##########################   I  T  E  M  S ################################################################
    
    dmc.Center([
        dmc.Tooltip(
            label="Ultima actualización:21-Septiembre-2023",
            position="top",
            withArrow=True,
            transition="fade",
            transitionDuration=200,
            multiline=True,
            closeDelay=600,
            color="gray",
            style={"fontFamily": "Montserrat", "font-size": "15px", "textAlign": "justify",
                        "textJustify":"inter-word"},
            children=[
                dmc.Group([
                    DashIconify(icon='typcn:info-outline', width=20, id="info-icon"),
                    dmc.Text("¿Qué se contrató?",fw=500,ta="center",
                             style={'font-family': 'Montserrat', "font-size": "25px",},)],position="center",),
            ]
        ),
    ]),

    
    dcc.Graph(id='bar1',style={'backgroundColor': 'rgb(100,67,97)'}),
    dmc.Space(h=40),

    dmc.Text('Histórico del número de contrataciones realizadas',
             fw=500,ta="center",style={'font-family': 'Montserrat', "font-size": "20px"}),
    dcc.Graph(id='p1'),
    dmc.Text('Histórico del monto gastado en contrataciones',
             fw=500,ta="center",style={'font-family': 'Montserrat', "font-size": "20px"}),
    dcc.Graph(id='p2'),
    
 
    
],style={'paddingRight':'10px','paddingLeft':'10px'})



