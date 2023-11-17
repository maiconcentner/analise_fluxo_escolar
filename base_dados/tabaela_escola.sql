CREATE TABLE projeto_final.b_escola (
    ano INT,
    sigla_uf VARCHAR(2),
    rede VARCHAR(30),
    diretoria VARCHAR(50),
    id_municipio INT,
    id_escola INT,
    id_escola_sp INT,
    codigo_tipo_escola INT,
    prop_aprovados_anos_iniciais_ef DOUBLE PRECISION,
    prop_reprovados_anos_iniciais_ef DOUBLE PRECISION,
    prop_abandono_anos_iniciais_ef DOUBLE PRECISION,
    prop_aprovados_anos_finais_ef DOUBLE PRECISION,
    prop_reprovados_anos_finais_ef DOUBLE PRECISION,
    prop_abandono_anos_finais_ef DOUBLE PRECISION,
    prop_aprovados_em DOUBLE PRECISION,
    prop_reprovados_em DOUBLE PRECISION,
    prop_abandono_em DOUBLE PRECISION
);

SELECT * FROM projeto_final.b_escola;

CREATE TABLE projeto_final.b_municipio (
    ano INT,
    sigla_uf VARCHAR(2),
    rede VARCHAR(30),
    diretoria VARCHAR(30),
    id_municipio INT,
    prop_aprovados_anos_iniciais_ef DOUBLE PRECISION,
    prop_reprovados_anos_iniciais_ef DOUBLE PRECISION,
    prop_abandono_anos_iniciais_ef DOUBLE PRECISION,
    prop_aprovados_anos_finais_ef DOUBLE PRECISION,
    prop_reprovados_anos_finais_ef DOUBLE PRECISION,
    prop_abandono_anos_finais_ef DOUBLE PRECISION,
    prop_aprovados_em DOUBLE PRECISION,
    prop_reprovados_em DOUBLE PRECISION,
    prop_abandono_em DOUBLE PRECISION
);

SELECT * FROM projeto_final.b_municipio;