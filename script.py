import func_sql as sql
import pandas as pd

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