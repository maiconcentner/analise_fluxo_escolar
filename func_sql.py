from sqlalchemy import create_engine
import pandas as pd

def conectar(acesso):
    with open(acesso, "r") as arquivo:
        texto = arquivo.read()
        texto = texto.split(',')
        
    usuario = texto[0]
    senha =  texto[1]

    engine = create_engine(f'postgresql://{usuario}:{senha}@localhost:5432/aula_thomas')


    return engine

""""
def sql_select(tabela, colunas = '*', conn=None):
    consulta = f"SELECT {colunas} FROM {tabela};"
    
    query = pd.read_sql_query(consulta, con=conn)
    
    return query
"""

import pandas as pd

def select(primary_table, conn, join_table=None, join_condition=None, columns='*', where=None, order_by=None, limit=None):
    """
    Executa uma consulta SELECT no banco de dados, com opção de JOIN.

    Parâmetros:
    - primary_table (str): Nome da tabela principal a ser consultada.
    - conn: Conexão com o banco de dados.
    - join_table (str, optional): Nome da tabela para realizar o JOIN.
    - join_condition (str, optional): Condição de JOIN.
    - columns (str, optional): Colunas a serem selecionadas (padrão é '*' para todas as colunas).
    - where (str, optional): Condição WHERE da consulta.
    - order_by (str, optional): Coluna pela qual ordenar os resultados.
    - limit (int, optional): Número máximo de linhas a serem retornadas.

    Retorna:
    - DataFrame contendo o resultado da consulta.
    """
    try:
        # Construir a consulta SQL com base nos parâmetros fornecidos
        consulta = f"SELECT {columns} FROM {primary_table}"

        if join_table and join_condition:
            consulta += f" JOIN {join_table} ON {join_condition}"

        if where:
            consulta += f" WHERE {where}"

        if order_by:
            consulta += f" ORDER BY {order_by}"

        if limit:
            consulta += f" LIMIT {limit}"

        consulta += ";"

        # Executar a consulta e retornar o resultado como DataFrame
        query = pd.read_sql_query(consulta, con=conn)
        return query
    except Exception as e:
        print(f"Erro ao executar a consulta: {str(e)}")
        return None

