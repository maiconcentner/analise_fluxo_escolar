## Resumo

A base de dados analisada oferece informações abrangentes sobre o fluxo escolar em São Paulo, coletadas pelo Censo Escolar desde 2011 até 2020. Os dados estão segmentados por diretoria de ensino, escola e município, abrangendo as séries iniciais e finais do Ensino Fundamental, bem como o Ensino Médio. Ao explorar esses dados, é possível realizar comparações entre as taxas de aprovação em diferentes escolas, municípios e diretorias de ensino. Isso permitirá identificar variações significativas e possíveis áreas de melhoria. Além disso, a análise temporal das taxas de aprovação ao longo dos anos pode revelar tendências e mudanças no sistema educacional. Para uma compreensão mais aprofundada, poderemos investigar os fatores que possam influenciar as discrepâncias nas taxas de aprovação. Aspectos como o tamanho da escola, localização geográfica e o contexto socioeconômico dos alunos podem desempenhar papéis importantes. Essa abordagem mais detalhada ajudará a formar *insights* valiosos para orientar políticas educacionais e práticas escolares.

## Dados
A base de dados é fornecida pelo Departamento de Tecnologia de Sistemas e Incl administrado pela Secretaria da Educação - Sede, disponível [neste link](http://catalogo.governoaberto.sp.gov.br/dataset/fluxo-escolar-por-escola). Estaremos utilizando os dados já tratados, fornecidos pelo Instituto Base dos Dados, você pode acessar [clicando aqui](https://basedosdados.org/dataset/6afcbdcb-5f30-477c-bd0f-c6a002e464df?table=f50c5690-2450-4975-9c6a-b42882a8e8e4).

### Tabela *escola*
A tabela contém dados do fluxo escolar agregado a nível de ensino de cada escola. Para quantificar o fluxo, utiliza-se 3 variáveis para cada nível de ensino: a proporção de alunos aprovados, a proporção de alunos reprovados e a proporção de alunos que abandonaram o ano escolar:

| Nome                              | Tipo de dado | Descrição                                       |
| --------------------------------- | ------------ | ----------------------------------------------- |
| ano                               | INT64        | Ano                                             |
| sigla\_uf                         | STRING       | Sigla da Unidade da Federação                   |
| rede                              | STRING       | Rede de ensino                                  |
| diretoria                         | STRING       | Diretoria de ensino                             |
| id\_municipio                     | INT64        | ID Município - IBGE 7 Dígitos                  |
| id\_escola                        | INT64        | ID Escola - INEP                                |
| id\_escola\_sp                    | INT64        | ID Escola - específico para o estado de SP      |
| codigo\_tipo\_escola              | INT64        | Código identificador do tipo de escola         |
| prop\_aprovados\_anos\_iniciais\_ef | FLOAT64    | Prop. alunos aprov. nos anos iniciais do EF    |
| prop\_reprovados\_anos\_iniciais\_ef | FLOAT64    | Prop. alunos reprov. nos anos iniciais do EF   |
| prop\_abandono\_anos\_iniciais\_ef   | FLOAT64  | Prop. alunos aband. nos anos iniciais do EF    |
| prop\_aprovados\_anos\_finais\_ef    | FLOAT64  | Prop. alunos aprov. nos anos finais do EF      |
| prop\_reprovados\_anos\_finais\_ef   | FLOAT64  | Prop. alunos reprov. nos anos finais do EF     |
| prop\_abandono\_anos\_finais\_ef     | FLOAT64  | Prop. alunos aband. nos anos finais do EF     |
| prop\_aprovados\_em                  | FLOAT64  | Prop. alunos aprovados nos anos do EM         |
| prop\_reprovados\_em                 | FLOAT64  | Prop. alunos reprovados nos anos do EM        |
| prop\_abandono\_em                   | FLOAT64  | Prop. de alunos que abandonaram no EM        |


### Tabela *municipio*
A tabela disponibiliza dados sobre o fluxo escolar a nível de município. O fluxo escolar consiste em um conjunto de variáveis que indica a taxa de aprovação, reprovação e abandono para cada nível do ensino escolar.

| Nome                              | Tipo de dado | Descrição                                       |
| --------------------------------- | ------------ | ----------------------------------------------- |
| ano                               | INT64        | Ano                                             |
| sigla\_uf                         | STRING       | Sigla da Unidade da Federação                   |
| rede                              | STRING       | Rede de ensino                                  |
| diretoria                         | STRING       | Diretoria de ensino                             |
| id\_municipio                     | INT64        | ID Município - IBGE 7 Dígitos                  |
| prop\_aprovados\_anos\_iniciais\_ef | FLOAT64    | Prop. alunos aprov. nos anos iniciais do EF    |
| prop\_reprovados\_anos\_iniciais\_ef | FLOAT64    | Prop. alunos reprov. nos anos iniciais do EF   |
| prop\_abandono\_anos\_iniciais\_ef   | FLOAT64  | Prop. alunos aband. nos anos iniciais do EF    |
| prop\_aprovados\_anos\_finais\_ef    | FLOAT64  | Prop. alunos aprov. nos anos finais do EF      |
| prop\_reprovados\_anos\_finais\_ef   | FLOAT64  | Prop. alunos reprov. nos anos finais do EF     |
| prop\_abandono\_anos\_finais\_ef     | FLOAT64  | Prop. alunos aband. nos anos finais do EF     |
| prop\_aprovados\_em                  | FLOAT64  | Prop. alunos aprovados nos anos do EM         |
| prop\_reprovados\_em                 | FLOAT64  | Prop. alunos reprovados nos anos do EM        |
| prop\_abandono\_em                   | FLOAT64  | Prop. de alunos que abandonaram no EM        |


## Sugestão de Análises
Com uma base de dados sobre o fluxo escolar por escola em São Paulo, há diversas análises e insights que podem ser extraídos. Aqui estão algumas sugestões:

1. **Análise Temporal:**
   Avaliar as tendências temporais nas taxas de aprovação ao longo dos anos. Isso pode revelar padrões ou mudanças significativas.

2. **Comparação por Níveis e Séries:**
   Comparar as taxas de aprovação entre as séries iniciais e finais do Ensino Fundamental e o Ensino Médio. Isso pode destacar áreas específicas que podem precisar de atenção.

3. **Variações por Rede de Ensino:**
   Analisar as diferenças nas taxas de aprovação entre escolas públicas e privadas. Isso pode indicar disparidades no sistema educacional.

4. **Análise Geográfica:**
   Avaliar as diferenças nas taxas de aprovação entre municípios. Isso pode destacar áreas geográficas que podem precisar de intervenções específicas.

5. **Relação com Tamanho da Escola:**
   Investigar como o tamanho da escola se relaciona com as taxas de aprovação. Escolas menores ou maiores têm padrões diferentes?

6. **Análise de Fatores Contribuintes:**
   Identificar e analisar possíveis fatores que contribuem para diferenças nas taxas de aprovação, como localização geográfica, tamanho da escola, infraestrutura, entre outros.

7. **Análise Socioeconômica:**
   Avaliar como o nível socioeconômico dos alunos pode influenciar nas taxas de aprovação. Escolas em áreas de baixo índice socioeconômico podem apresentar desafios diferentes.

8. **Correlações com Outras Variáveis:**
   Explorar correlações entre as taxas de aprovação e outras variáveis presentes nos dados. Pode haver relações interessantes a serem descobertas.

9. **Identificação de Escolas com Desempenho Excepcional ou Precário:**
   Identificar escolas que se destacam positivamente ou que possam precisar de atenção especial com base em suas taxas de aprovação.

Observação: as análises específicas dependem da natureza exata dos dados disponíveis na base de dados. Antes de realizar qualquer análise, é importante compreender bem os dados e considerar a qualidade da coleta de dados. Além disso, a colaboração com especialistas em educação pode enriquecer a interpretação dos resultados.

**Referências:**
- [Portal Governo Aberto SP](http://catalogo.governoaberto.sp.gov.br/dataset/fluxo-escolar-por-escola)
- [Instituto Base dos Dados](https://basedosdados.org/dataset/6afcbdcb-5f30-477c-bd0f-c6a002e464df?table=f50c5690-2450-4975-9c6a-b42882a8e8e4)
- [Base dados IBGE](https://www.ibge.gov.br/cidades-e-estados/sp/sao-paulo.html)
