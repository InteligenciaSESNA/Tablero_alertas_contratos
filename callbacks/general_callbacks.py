


#import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np 
import pandas as pd
from app import app
from components.lights import create_traffic_light



general_df = pd.read_csv('datasets/general7.csv',sep="|")
supplier_inst = pd.read_csv('datasets/supplier_inst.csv',sep="|")
indic_gral= pd.read_csv('datasets/indicadores_gral2.csv',sep="|")
proveedor=pd.read_csv('datasets/proveedores.csv',sep="|")
items_principal=pd.read_csv('datasets/items_principal.csv',sep="|")



##########################################################################################################################
#######################################   --  L    L    A    M    A    D    A    S --     ################################
##########################################################################################################################


def register_callbacks(app):


    @app.callback(
              Output('anio_dropdown', 'options'),
        Output('anio_dropdown', 'value'),
        Input('name_dropdown', 'value'))
    def update_anio(name_dropdown):
        if name_dropdown is None:
             return [], None
        names=general_df[['name','anio']].drop_duplicates()
        list_anio=names[names['name']==name_dropdown]['anio'].values.tolist()
        anios_options=[{'label':x, 'value':x} for x in list_anio]
        return anios_options, None   



################LLAMADAS PARA LOS DESCRIPTIVOS INICIALES NARRATIVOS ######################

    @app.callback (
            Output(component_id='c1',component_property='children'),
            Output(component_id='c2',component_property='children'),
            Output(component_id='c3',component_property='children'),
            Output(component_id='e1',component_property='children'),
            Output(component_id='e2',component_property='children'),
            Output(component_id='e3',component_property='children'),
            Output(component_id='e4',component_property='children'),
            Output(component_id='resumen',component_property='children'),
            Output(component_id='alertamiento',component_property='children'),
    
    
            Input('submit-button', 'n_clicks'),
            [State(component_id='name_dropdown',component_property='value'),
             State(component_id='anio_dropdown',component_property='value')])

    def update_cards(click,name_select,anio_select): 
        name_filter = 'None'
        names=general_df.copy(deep=True)
        supplier=supplier_inst.copy(deep=True)
        if name_select:
            name_filter=name_select
            names=names[names['name']==name_select]
            supplier=supplier[supplier['name']==name_select]
        gen_df=names[['anio','procurementMethod','tipo_proc','monto_mxn','n_contratos',
                     'inst_pctn_contracts']]
        supplier_df=supplier[['anio','n_prov']]
        if anio_select:
            anio_filter="None"
            anio_filter=anio_select
            
        gen_df=gen_df[gen_df['anio']==anio_select]
        gen_df.reset_index(inplace=True)
        
        supplier_df=supplier_df[supplier_df['anio']==anio_select]
        
        t_contratos = gen_df['n_contratos'].sum()
        t_monto=round(gen_df['monto_mxn'].sum(),2)
        t_proveedores= supplier_df['n_prov'].sum()
        open1=gen_df[gen_df['procurementMethod']=="open"]
        select1=gen_df[gen_df['procurementMethod']=="selective"]
        direct1=gen_df[gen_df['procurementMethod']=="direct"]
        framework1=gen_df[gen_df['procurementMethod']=="framework"]
        
        return '{:,}'.format(t_contratos),f'${t_monto:,.2f}','{:,}'.format(t_proveedores),f'{round(direct1["inst_pctn_contracts"].sum(),1)}%', f'{round(open1["inst_pctn_contracts"].sum(),1)}%',f'{round(select1["inst_pctn_contracts"].sum(),1)}%', f'{round(framework1["inst_pctn_contracts"].sum(),1)}%',f'En el año {anio_select}, la {name_select} ejerció un total de ${t_monto:,.2f} pesos mexicanos en contrataciones públicas. En total se otorgaron {"{:,}".format(t_contratos)} contratos a {"{:,}".format(t_proveedores)} proveedores', f'Alertamientos en: {name_select}'
    


    


###########################LLAMADA PARA KPIS  ######################################################




    @app.callback (
        Output('our-gauge', 'value'),
        Output('semaforo-t1', 'children'),
        Output('semaforo-t2', 'children'),
        Output('semaforo-t3', 'children'),
        Output('semaforo-t4', 'children'),
        Output('semaforo-t5', 'children'),
        Output('our-gauge2', 'value'),
        Output('semaforo-c1', 'children'),
        Output('semaforo-c2', 'children'),
        Output('semaforo-c3', 'children'),
        Output('semaforo-c4', 'children'),
        Output('semaforo-c5', 'children'),
        Output('our-gauge3', 'value'),
        Output('semaforo-i1', 'children'),
        Output('semaforo-i2', 'children'),
        Output('semaforo-i3', 'children'),
        Output('semaforo-i4', 'children'),
        Output('semaforo-i5', 'children'),
      
        Input('submit-button', 'n_clicks'),
        [State(component_id='name_dropdown',component_property='value'),
        State(component_id='anio_dropdown',component_property='value')])
    
    def actualiza_kpi_t(clicks, name_select,anio_select):
        name_filter = 'Seleccionar todos'
        names=indic_gral.copy(deep=True)
    
        if name_select:
            name_filter=name_select
            names=names[names['name']==name_select]
        t_df=names #[['anio','transp_gral','p_t1','p_t2','p_t3','p_t4','p_t5']]
        if anio_select:
            anio_filter="None"
            anio_filter=anio_select
        t_df=t_df[t_df['anio']==anio_select]
        t_df.reset_index(inplace=True)
    
    
        t_gral=round(t_df['transp_gral'].sum(),1)
    #label=dmc.Center(dmc.Text(f"{round(t_df['transp_gral'].sum(),1)}%",color="indigo"))
    
    # Crear la gráfica del KPI
       
        val_t1=round(t_df['p_t1'].sum(),1)
        val_t2=round(t_df['p_t2'].sum(),1)
        val_t3=round(t_df['p_t3'].sum(),1)
        val_t4=round(t_df['p_t4'].sum(),1)
        val_t5=round(t_df['p_t5'].sum(),1)
    
    ############################# C O M P E T E N C I A ##########################################################
        comp_gral=round(t_df['comp_gral'].sum(),2)
    
    # Crear la gráfica del KPI
    
        val_c1=round(t_df['p_c1'].sum(),1)
        val_c2=round(t_df['p_c2'].sum(),1)
        val_c3=round(t_df['p_c3'].sum(),1)
        val_c4=round(t_df['p_c4'].sum(),1)
        val_c5=round(t_df['p_c5'].sum(),1)
    
    #####################  I R R E G U L A R I D A D E S ################
    
        irreg_gral=round(t_df['irreg_gral'].sum(),2)
    
    # Crear la gráfica del KPI
    
        val_i1=round(t_df['p_i1'].sum(),1) 
        val_i2=round(t_df['p_i2'].sum(),1)
        val_i3=round(t_df['p_i3'].sum(),1)
        val_i4=round(t_df['p_i4'].sum(),1)
        val_i5=round(t_df['p_i5'].sum(),1)
    
        return t_gral,create_traffic_light(val_t1),create_traffic_light(val_t2),create_traffic_light(val_t3),create_traffic_light(val_t4), create_traffic_light(val_t5),comp_gral,create_traffic_light(val_c1),create_traffic_light(val_c2),create_traffic_light(val_c3),create_traffic_light(val_c4),create_traffic_light(val_c5),irreg_gral,create_traffic_light(val_i1),create_traffic_light(val_i2),create_traffic_light(val_i3),create_traffic_light(val_i4),create_traffic_light(val_i5)


###############################  P R O V E E D O R E S ################################################


    @app.callback (

        Output(component_id='tabla_prov',component_property='data'),
        Input('submit-button', 'n_clicks'),
        State(component_id='name_dropdown',component_property='value'),
        State(component_id='anio_dropdown',component_property='value'))

    def update_tablaprov(click,name_select,anio_select): 
        name_filter = 'None'
        names=proveedor.copy(deep=True)
        if name_select:
            name_filter=name_select
            names=names[names['name']==name_select]
        prov_df=names[['anio','suppliers_name','monto_supp','n_contracts']]
        if anio_select:
            anio_filter="None"
            anio_filter=anio_select
        prov_df=prov_df[prov_df['anio']==anio_select]
        prov_df=prov_df[['suppliers_name','monto_supp','n_contracts']].sort_values('monto_supp',ascending=False)  
        return prov_df.to_dict('records')


######################################################################################################
##########################   ITEMS    ################################################################

    @app.callback (

        Output(component_id='bar1',component_property='figure'),
        Input('submit-button', 'n_clicks'),
        State(component_id='name_dropdown',component_property='value'),
        State(component_id='anio_dropdown',component_property='value'))

    def update_tree(click,name_select,anio_select):
        name_filter = 'Seleccionar todos'
        names=items_principal.copy(deep=True)
        if name_select:
            name_filter=name_select
            names=names[names['name']==name_select]
        item_df=names[['anio','tipo_proc','items_partida_gen','description','monto_total_gral','n_items']]
        if anio_select:
            anio_filter="None"
            anio_filter=anio_select
        item_df=item_df[item_df['anio']==anio_select]
        item_df.reset_index(inplace=True)
    
        fig_tree = px.treemap(item_df, 
                              path=[px.Constant("Total"),'tipo_proc','description'], 
                              values='monto_total_gral',color='monto_total_gral',color_continuous_scale='RdBu',
                              height=750,labels={'monto_total_gral':'Monto total por ITEM'})
                          
        fig_tree.update_traces(marker=dict(cornerradius=5),)
    
    #fig_bub=px.scatter(item_df, x="n_items", y="procurementMethod",size="monto_total_gral", color="items_partida_gen",
     #                  hover_name="description", log_x=True, size_max=60,template="simple_white")
        return fig_tree.update_layout(margin = dict(t=50, l=25, r=25, b=25))
     
#########################################################################################################
############################   LLAMADA PARA GRÁFICA HISTÓRICA###########################################


    @app.callback(
        Output(component_id='p1',component_property='figure'),
        Output(component_id='p2',component_property='figure'),
        Input('submit-button', 'n_clicks'),
        State(component_id='name_dropdown',component_property='value'),
        State(component_id='anio_dropdown',component_property='value'))
    
    def update_hist(click,name_select, anio_select):
        name_filter = 'Seleccionar todos'
        names=general_df.copy(deep=True)
    
        if name_select:
            name_filter=name_select
            names=names[names['name']==name_select]
        gen_df = names[['anio','tipo_proc','monto_mxn','n_contratos']]
        gen_df.reset_index(inplace=True)
        if anio_select:
            anio_filter="None"
            anio_filter=anio_select

        fig1=px.bar(gen_df, x='anio', y='n_contratos', 
                    color='tipo_proc',template="simple_white",barmode="group", 
                    labels={'anio':'Año','n_contratos':'Número de contratos','tipo_proc':'Tipo de procedimiento'},
                    color_discrete_map = {"Adjudicación directa":"#a8163d","Invitación a 3 o más":"gray",
                                          "Licitación abierta":"#755472","Contrato marco":"#5c2335"})
    
        fig2=px.bar(gen_df, x='anio', y='monto_mxn',
                    color='tipo_proc',template="simple_white",barmode="group", 
                    labels={'anio':'Año','monto_mxn':'Monto en pesos','tipo_proc':'Tipo de procedimiento'},
                    color_discrete_map = {"Adjudicación directa":"#a8163d","Invitación a 3 o más":"gray",
                                          "Licitación abierta":"#755472","Contrato marco":"#5c2335"})
    
        for i, data in enumerate(fig1.data):
        # Recorremos todos los valores en 'x' para ajustar su opacidad según el año seleccionado
            opacity_values = []
            for x_value in data['x']:
                if int(x_value) == anio_select:
                    opacity_values.append(1.0)
                else:
                    opacity_values.append(0.3) 

            fig1.data[i].marker.opacity = opacity_values
        for i, data in enumerate(fig2.data):
        # Recorremos todos los valores en 'x' para ajustar su opacidad según el año seleccionado
            opacity_values = []
            for x_value in data['x']:
                if int(x_value) == anio_select:
                    opacity_values.append(1.0)
                else:
                    opacity_values.append(0.3)
            fig2.data[i].marker.opacity = opacity_values
        
            fig2.update_yaxes(tickprefix="$")
        return fig1.update_layout(),fig2.update_layout()

