from shinywidgets import output_widget, render_widget
from shiny import App, render, ui
import func_sql as sql
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import shinyswatch
import pandas as pd


# Fazendo a conecção na base de dados do PostgreSQL
conexao = sql.conectar('/home/maicon/unesp_bot/mestrado_unesp/2Sem_23/projeto_final_FCMII/acesso.txt')

b_escola = 'projeto_final.b_escola'
b_municipio = 'projeto_final.b_municipio'
cod_ibge = 'projeto_final.ibge_municipios'


"""# verificando a b_escola
query = sql.select(
    columns = '*',
    primary_table = b_escola,
    conn = conexao
)

#print(query)

# verificando a b_municipio
query = sql.select(
    columns = '*',
    primary_table = b_municipio,
    limit = 10,
    conn = conexao
)
#print(query)

# verificando a cod_ibge
query = sql.select(
    columns = '*',
    primary_table = cod_ibge,
    conn = conexao
)
#print(query)"""

#! Query principal
# realizando um join da base b_escola com a cod_ibge
query = sql.select(
    primary_table = b_escola,
    join_table = cod_ibge,
    join_condition = b_escola +'.id_municipio =' + cod_ibge +'.cod_ibge',
    columns = b_escola +'.*,'+ cod_ibge +'.municipio',
    conn = conexao
)

#print(query)

# Salvando consulta como um df
df_escola = query

#df_escola.to_csv('df_analise.csv', index=False)

#df_escola = pd.read_csv('df_analise.csv')

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
    #flatly -> top
    #journal
    #litera -> top
    #zephyr
    shinyswatch.theme.journal(),
    # style ----
    ui.markdown("""________________________________________"""),
    ui.h2("ANÁLISE DO FLUXO ESCOLAR NO ESTADO DE SÃO PAULO"),
    ui.markdown("""
        <b> REPOSITÓRIO DO PROJETO DISPONÍVEL NO <a href="https://github.com/maiconcentner/analise_fluxo_escolar" target="_blank">GITHUB</a> </b>

        Maicon Centner Germano, Pós-graduação em Biometria - IBB Unesp Botucatu

        Ferramentas Computacionais de Modelagem II, Prof. Thomas N. Vilches
    """),
    ui.markdown("""________________________________________"""),

    # Aba da tabela
    ui.navset_tab(
        ui.nav(
            ui.markdown("<b>Tabela de dados</b>"),
            ui.layout_sidebar(
                ui.panel_sidebar(
                    ui.input_slider('x1', 'Ano', value=(2011,2019), min=2011, max=2019),
                    ui.input_selectize("x2", "Munícipio", choices, multiple=True),
                ),

            ui.output_table('df_prop_aprovacao_munic'),
            ),
                ),

        # Aba dos gráficos
        ui.nav(
            ui.markdown("<b>Vizualização gráfica</b>"),
            ui.markdown("""________________________________________"""),
            ui.layout_sidebar(
                ui.panel_sidebar(
            ui.div(
                ui.input_slider('y1', 'Ano', value=(2011, 2019), min=2011, max=2019),
                class_="d-flex flex-column align-items-start"
            ),

            ui.div(
                ui.input_selectize(
                    "y2", label="Município",
                    choices=choices,
                    multiple=True,
                ),

                class_="d-flex flex-column align-items-start"
            ),
        ),
        output_widget("my_widget"),
        output_widget("my_widget2"),
    ),
),

        # Aba dos municipios
        ui.nav(
            ui.markdown("<b>Análise dos munícipios</b>"),
            ui.markdown("""________________________________________"""),
            ui.markdown("Fonte: IBGE 2020"),
            ui.layout_sidebar(
                ui.panel_sidebar(
            ui.div(
                ui.input_selectize(
                    "y4", label="Município",
                    choices=choices,
                    multiple=True,
                ),
                class_="d-flex flex-column align-items-start"
            ),
            ),
                output_widget("my_widget3"),
                output_widget("my_widget5"),

            ),
            ui.layout_sidebar(
                ui.panel_sidebar(

            ui.div(
                ui.input_slider('y5','Bins', value=1500,min=0,max=2000),
                ui.input_slider("y6", "Escala do eixo x", value=(-100, 500), min=-100, max=4000)

            ),
        ),

            output_widget("my_widget4"),
        ),
        ),

    )
)


def server(input, output, session):
    @output
    @render.table
    #? Tabela de dados
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
    #? Gráfico de linhas
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
        title_text='<b>PROPORÇÃO MÉDIA DE APROVADOS</b>',
        title_x=0.5,  # Define o título como centralizado
        title_font=dict(size=25, family='Arial'),  # Ajusta o tamanho, a fonte e a cor do título
        xaxis=dict(title='Ano'),
        yaxis=dict(title='Proporção de Aprovados (%)'),
        template='ggplot2',  # Pode personalizar o modelo conforme necessário
        )
        return fig

    @output
    @render_widget
    #? Gráfico de barras
    def my_widget2():
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
        df_11 = df_filtrado[['municipio','prop_aprovados_anos_iniciais_ef']].groupby('municipio').mean().reset_index()
        # Ordenar o DataFrame pelo valor desejado em ordem decrescente
        df_1_sorted = df_11.sort_values(by='prop_aprovados_anos_iniciais_ef', ascending=False)
        # Pegar as 10 primeiras cidades
        df_11_s = df_1_sorted.head(10)
        # prop_aprovados_anos_finais_ef
        df_22 = df_filtrado[['municipio','prop_aprovados_anos_finais_ef']].groupby('municipio').mean().reset_index()
        # Ordenar o DataFrame pelo valor desejado em ordem decrescente
        df_2_sorted = df_22.sort_values(by='prop_aprovados_anos_finais_ef', ascending=False)
        # Pegar as 10 primeiras cidades
        df_22_s = df_2_sorted.head(10)

        # prop_aprovados_em
        df_33 = df_filtrado[['municipio','prop_aprovados_em']].groupby('municipio').mean().reset_index()
        df_3_sorted = df_33.sort_values(by='prop_aprovados_em', ascending=False)
        # Pegar as 10 primeiras cidades
        df_33_s = df_3_sorted.head(10)

        # Criar os traços individuais
        trace1 = go.Bar(x=df_11_s['municipio'], y=df_11_s['prop_aprovados_anos_iniciais_ef'], name='Anos iniciais_ef',visible='legendonly')
        trace2 = go.Bar(x=df_22_s['municipio'], y=df_22_s['prop_aprovados_anos_finais_ef'], name='Anos finais_ef',visible='legendonly')
        trace3 = go.Bar(x=df_33_s['municipio'], y=df_33_s['prop_aprovados_em'], name='Ensino médio',visible=True)

        # Criar a figura combinando os traços
        fig2 = go.Figure(data=[trace1, trace2, trace3])

        # Atualizar o layout
        fig2.update_layout(
        height=600,
        xaxis_title='Município',
        title_text='<b>RANKING DE APROVAÇÃO POR MUNICÍPIO - TOP 10</b>',
        title_font=dict(size=25, family='Arial'),  # Ajusta o tamanho, a fonte e a cor do título
        xaxis=dict(title='Município'),
        yaxis=dict(title='Proporção de Aprovados (%)', range=[0, 102]),
        title_x=0.5,  # Alinha o título à esquerda
        barmode='group',
        template='ggplot2',
        )

        return fig2

    #? Municipios

    @output
    @render_widget
    def my_widget3():
        cidades_selecionadas = input.y4()

        municipios_ibge = pd.read_csv("/home/maicon/unesp_bot/mestrado_unesp/2Sem_23/projeto_final_FCMII/base_dados/cod_municipios.csv",delimiter=';')

        df_novo = municipios_ibge[['municipio', 'den_demografica_hab/km', 'idhm']]

        # Filtrar para incluir apenas as cidades selecionadas, se necessário
        if cidades_selecionadas:
            df_novo = df_novo[df_novo['municipio'].isin(cidades_selecionadas)]

        # Gráfico de Dispersão (Scatter Plot)
        fig_a = px.scatter(df_novo, x='den_demografica_hab/km', y='idhm', labels={'den_demografica_hab/km': 'Densidade Demográfica (hab/km²)', 'idhm': 'IDHM'},
                        hover_data=['municipio'],color='municipio')

        fig_a.update_layout(height=600,title='<b>DENSIDADE DEMOGRÁFICA VS IDHM</b>',
                            template='ggplot2',
                            title_font=dict(size=25, family='Arial'),  # Ajusta o tamanho, a fonte e a cor do título
)

        return fig_a

    @output
    @render_widget
    def my_widget4():
        cidades_selecionadas = input.y4()
        bins = input.y5()
        inter = input.y6()

        municipios_ibge = pd.read_csv("/home/maicon/unesp_bot/mestrado_unesp/2Sem_23/projeto_final_FCMII/base_dados/cod_municipios.csv",delimiter=';')

        df_novo = municipios_ibge[['municipio', 'den_demografica_hab/km', 'idhm']]

        # Filtrar para incluir apenas as cidades selecionadas, se necessário
        if cidades_selecionadas:
            df_novo = df_novo[df_novo['municipio'].isin(cidades_selecionadas)]

        # Histograma - Densidade Demográfica
        fig_b = px.histogram(df_novo, x='den_demografica_hab/km', nbins=bins,
                    labels={'den_demografica_hab/km': 'Densidade Demográfica (hab/km²)', 'count': 'Frequência'},
                    range_x=inter)  # Definindo a faixa do eixo x

        fig_b.update_layout(height=600,title='<b>HISTOGRAMA - DENSIDADE DEMOGRÁFICA</b>',
                            template='ggplot2',
                            title_font=dict(size=25, family='Arial'),
                        )
        fig_b.update_traces(marker=dict(color='#f8766d'))
        return fig_b

    @output
    @render_widget

    def my_widget5():
        cidades_selecionadas = input.y4()

        municipios_ibge = pd.read_csv("/home/maicon/unesp_bot/mestrado_unesp/2Sem_23/projeto_final_FCMII/base_dados/cod_municipios.csv",delimiter=';')

        # Filtrar para incluir apenas as cidades selecionadas, se necessário
        if cidades_selecionadas:
            municipios_ibge = municipios_ibge[municipios_ibge['municipio'].isin(cidades_selecionadas)]

        # Ordenar o DataFrame pela coluna 'receitas_realizadas_1000' em ordem decrescente
        municipios_ibge_sorted = municipios_ibge.sort_values(by='receitas_realizadas_1000', ascending=False)

        # Pegar os top 20 registros
        top_20_municipios = municipios_ibge_sorted.head(20)

        # Gráfico de Barras - Receitas Realizadas (x1000) por Município - Top 20
        bar_fig = px.bar(top_20_municipios, x='municipio', y='receitas_realizadas_1000', labels={'receitas_realizadas_1000': 'Receitas Realizadas (x1000)'})
        bar_fig.update_layout(height=600,title='<b>TOP 20 MUNICÍPIOS COM MAIORES RECEITAS REALIZADAS</b>',
                            template='ggplot2',
                            title_font=dict(size=25, family='Arial'),  # Ajusta o tamanho, a fonte e a cor do título

                            )
        # Atualiza a cor das barras para verde
        bar_fig.update_traces(marker=dict(color='#00bf7d'))

        return bar_fig


app = App(app_ui, server)