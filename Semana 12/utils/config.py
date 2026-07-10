"""
Configuração do modelo de dados.

Este é o ÚNICO arquivo que sabe os nomes reais das colunas, os valores
sentinela e os códigos de categoria da fonte de dados atual (PDAD 2024).
Todo o resto do sistema (utils/calcular.py, sistema.py) trabalha apenas com
os nomes CANÔNICOS definidos abaixo (ex.: "idade", "genero",
"chave_domicilio"), nunca com os nomes originais das colunas.

Para plugar uma fonte de dados diferente (outro levantamento, outro ano,
outra cidade), basta:
  1. Atualizar COLUNAS_MORADORES / COLUNAS_DOMICILIOS com o mapeamento
     "nome da coluna na fonte nova" -> "nome canônico usado pelo sistema".
  2. Atualizar SENTINELAS, CATEGORIAS_GENERO e CATEGORIAS_ARRANJO se os
     códigos da fonte nova forem diferentes.
  3. Ajustar CANDIDATOS_* em utils/carregar.py com os nomes dos arquivos.
Nenhuma linha de utils/calcular.py ou sistema.py precisa mudar.
"""

# --- Mapeamento: nome da coluna na fonte de dados -> nome canônico interno ---
# Chave = nome da coluna como está no arquivo original.
# Valor = nome canônico que o resto do sistema usa.

COLUNAS_MORADORES = {
    "idade_calculada": "idade",
    "id_genero": "genero",
    "localidade": "localidade",
    "A01nficha": "chave_domicilio",
    "E05": "raca_cor",
    "escolaridade": "escolaridade",
}

COLUNAS_DOMICILIOS = {
    "A01nficha": "chave_domicilio",
    "localidade": "localidade",
    "A01npessoas": "tamanho_domicilio",
    "A01ncriancas": "criancas_domicilio",
    "arranjos": "arranjo_familiar",
}

# --- Valores sentinela da fonte atual ---
SENTINELAS = [99999, 88888]

# Descrição de cada sentinela, usada nos relatórios exportados. Se a nova
# fonte de dados usar outros códigos/significados, basta atualizar aqui.
DESCRICAO_SENTINELAS = {
    99999: "não se aplica",
    88888: "não declarado",
}

# --- Colunas canônicas em que sentinelas devem ser verificadas ---
COLUNAS_NUMERICAS_MORADORES = ["idade", "raca_cor", "escolaridade", "genero"]
COLUNAS_NUMERICAS_DOMICILIOS = ["tamanho_domicilio", "criancas_domicilio", "arranjo_familiar"]

# --- Categorias codificadas da fonte atual ---
CATEGORIAS_GENERO = {1: "Cisgênero", 2: "Transgênero", 3: "Outro"}

CATEGORIAS_ARRANJO = {
    1: "Unipessoal", 2: "Monoparental fem.", 3: "Casal c/ 1 filho",
    4: "Casal c/ 2 filhos", 5: "Casal c/ 3+ filhos", 6: "Casal sem filhos",
    7: "Outro perfil",
}

# RAs oficiais do DF começam em 53xx; códigos 52xx são municípios de Goiás
# amostrados pela pesquisa. Usado apenas para referência/documentação.
CODIGO_MIN_RA_DF = 5301
