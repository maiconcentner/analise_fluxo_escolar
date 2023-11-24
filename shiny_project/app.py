from shiny import App, render, ui
import func_sql as sql
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import re

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
    ui.markdown("""________________________________________"""),
    ui.h2("Análise do fluxo escolar no estado de São Paulo"),
    ui.markdown("""
        Repositório do projeto disponível no [github][0]
        
        [0]:https://github.com/maiconcentner/analise_fluxo_escolar
    """),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider('x1', 'Ano', value=(2014,2019), min=2014, max=2019),
            ui.input_selectize("x2", "Munícipio", choices, multiple=True),
        ),
    
    ui.output_table('df_prop_aprovacao_munic'),
    ),
    
)

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

app = App(app_ui, server)

