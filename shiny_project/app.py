from shinywidgets import output_widget, render_widget
from shiny import App, render, ui
import func_sql as sql
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import shinyswatch

# Fazendo a conecção na base de dados do PostgreSQL
conexao = sql.conectar('D:\\Mestrado\\2Sem_23\\projeto_final_FCMII\\acesso.txt')

b_escola = 'projeto_final.b_escola'
b_municipio = 'projeto_final.b_municipio'
cod_ibge = 'projeto_final.ibge_municipios'

# verificando a b_escola
query = sql.select(
    columns = '*',
    primary_table = b_escola, 
    conn = conexao
)
print(query)

# verificando a b_municipio
query = sql.select(
    columns = '*',
    primary_table = b_municipio, 
    limit = 10, 
    conn = conexao
)
print(query)

# verificando a cod_ibge
query = sql.select(
    columns = '*',
    primary_table = cod_ibge,
    conn = conexao
)
print(query)

# realizando um join da base b_escola com a cod_ibge
query = sql.select(
    primary_table = b_escola,
    join_table = cod_ibge,
    join_condition = b_escola +'.id_municipio =' + cod_ibge +'.cod_ibge',
    columns = b_escola +'.*,'+ cod_ibge +'.municipio',
    conn = conexao
)

print(query)

# Salvando consulta como um df
df_escola = query

#? Análise 1
"""
Análise Temporal: Avaliar as tendências temporais nas taxas de aprovação ao 
longo dos anos. Isso pode revelar padrões ou mudanças significativas.
"""
# segrando os dados
df_aprov_munic_ano =  df_escola[
    ['municipio',
    'ano',
    'prop_aprovados_anos_iniciais_ef',
    'prop_aprovados_anos_finais_ef',
    'prop_aprovados_em']
]

# tratamento dos dados
# Substituir valores fora de um intervalo específico (por exemplo, 0 a 100) por NaN
df_aprov_munic_ano['prop_aprovados_anos_iniciais_ef'] = df_aprov_munic_ano['prop_aprovados_anos_iniciais_ef'].where((df_aprov_munic_ano['prop_aprovados_anos_iniciais_ef'] >= 0) & (df_aprov_munic_ano['prop_aprovados_anos_iniciais_ef'] <= 100), np.nan)
df_aprov_munic_ano['prop_aprovados_anos_finais_ef'] = df_aprov_munic_ano['prop_aprovados_anos_finais_ef'].where((df_aprov_munic_ano['prop_aprovados_anos_finais_ef'] >= 0) & (df_aprov_munic_ano['prop_aprovados_anos_finais_ef'] <= 100), np.nan)
df_aprov_munic_ano['prop_aprovados_em'] = df_aprov_munic_ano['prop_aprovados_em'].where((df_aprov_munic_ano['prop_aprovados_em'] >= 0) & (df_aprov_munic_ano['prop_aprovados_em'] <= 100), np.nan)

# removendo os NAN
df_aprov_munic_ano = df_aprov_munic_ano.dropna()

# agrupando por cidade e fazendo a media
df_media_aprov_cidade = df_aprov_munic_ano.groupby(['ano','municipio'])[['prop_aprovados_anos_iniciais_ef',
    'prop_aprovados_anos_finais_ef',
    'prop_aprovados_em']].mean().reset_index()

df_media_aprov_cidade.head(10)

############### SHINY ###################
choices = df_media_aprov_cidade['municipio'].unique().tolist()

app_ui = ui.page_fluid(
    #sandstone
    #flatly
    #journal
    #litera
    #zephyr
    shinyswatch.theme.sandstone(),
    # style ----
    ui.markdown("""________________________________________"""),
    ui.h2("Análise do fluxo escolar no estado de São Paulo"),
    ui.markdown("""
        Repositório do projeto disponível no [github][0]
        
        Maicon Centner Germano
        
        [0]:https://github.com/maiconcentner/analise_fluxo_escolar
    """),
    ui.markdown("""________________________________________"""),
    
    # Aba da tabela
    ui.navset_tab(
        ui.nav(
            "Tabela de dados",
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_slider('x1', 'Ano', value=(2014,2019), min=2014, max=2019),
                    ui.input_selectize("x2", "Munícipio", choices, multiple=True),
                ),
            
            ui.output_table('df_prop_aprovacao_munic'),
            ),
                ),
        
        # Aba dos gráficos
        ui.nav(
                "Vizualização gráfica",
                ui.markdown("""________________________________________"""),
                ui.div(   
                ui.input_slider('y1', 'Ano', value=(2014,2019), min=2014, max=2019),
                ui.input_selectize(
                    "y2", label="Munícipio",
                    choices=choices,
                    multiple=True,
                ),
                class_="d-flex gap-3"
            ),
            output_widget("my_widget")
        )
        
    )
)


from matplotlib import pyplot as plt


def server(input, output, session):
    @output
    @render.table    
    def df_prop_aprovacao_munic():
        anos_selecionados = input.x1()
        cidades_selecionadas = input.x2()

        # Filtrar com base no intervalo de anos selecionado
        df_filtrado = df_media_aprov_cidade[
            (df_media_aprov_cidade['ano'] >= anos_selecionados[0]) &
            (df_media_aprov_cidade['ano'] <= anos_selecionados[1])
        ]

        # Filtrar apenas se cidades selecionadas não estiverem vazias
        if cidades_selecionadas:
            df_filtrado = df_filtrado[
                df_filtrado['municipio'].isin(cidades_selecionadas)
            ]
        
        return df_filtrado
    
    @output
    @render_widget
    def my_widget():
        anos_selecionados = input.y1()
        cidades_selecionadas = input.y2()

        # Filtrar com base no intervalo de anos selecionado
        df_filtrado = df_media_aprov_cidade[
            (df_media_aprov_cidade['ano'] >= anos_selecionados[0]) &
            (df_media_aprov_cidade['ano'] <= anos_selecionados[1])
        ]
        
        # Filtrar apenas se cidades selecionadas não estiverem vazias
        if cidades_selecionadas:
            df_filtrado = df_filtrado[
                df_filtrado['municipio'].isin(cidades_selecionadas)
            ]
                
        # prop_aprovados_anos_iniciais_ef
        df_1 = df_filtrado[['ano','prop_aprovados_anos_iniciais_ef']].groupby('ano').mean().reset_index()
        
        # prop_aprovados_anos_finais_ef
        df_2 = df_filtrado[['ano','prop_aprovados_anos_finais_ef']].groupby('ano').mean().reset_index()
        
        # prop_aprovados_em
        df_3 = df_filtrado[['ano','prop_aprovados_em']].groupby('ano').mean().reset_index()
        
        
        fig = px.line()

        fig.add_trace(go.Scatter(x=df_1['ano'], y=df_1['prop_aprovados_anos_iniciais_ef'], 
                    mode='lines+markers', name='Anos iniciais_ef'))
        
        fig.add_trace(go.Scatter(x=df_2['ano'], y=df_2['prop_aprovados_anos_finais_ef'], 
                    mode='lines+markers', name='Anos finais_ef'))
        
        fig.add_trace(go.Scatter(x=df_3['ano'], y=df_3['prop_aprovados_em'], 
                    mode='lines+markers', name='Ensino médio'))
        
        fig.update_layout(
        height=600,
        xaxis_title='Ano',
        title='Proporção de Aprovados nas Escolas do Estado',
        xaxis=dict(title='Ano'),
        yaxis=dict(title='Proporção de Aprovados (%)'),
        template='ggplot2',  # Pode personalizar o modelo conforme necessário
        )
        return fig

app = App(app_ui, server)

