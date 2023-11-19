CREATE TABLE projeto_final.ibge_municipios (
    cod_ibge INTEGER PRIMARY KEY,
    municipio VARCHAR(255),
    area_territorial_km2 FLOAT,
    pop_residente INTEGER,
    den_demografica_hab_km FLOAT,
    escolarizacao_6_a_14_anos_percent FLOAT,
    idhm FLOAT,
    receitas_realizadas_1000 FLOAT,
    pib_2020 FLOAT
);