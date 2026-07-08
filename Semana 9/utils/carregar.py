"""Funções de leitura, limpeza e padronização dos dados para o sistema.

Estas funções leem os arquivos brutos e, em seguida, renomeiam as colunas
para os nomes CANÔNICOS definidos em utils/config.py. A partir daqui, todo
o resto do sistema (calcular.py, sistema.py) só enxerga os nomes canônicos
— isso é o que permite trocar de fonte de dados editando apenas config.py.
"""

import os
import pandas as pd

from . import config

# Nomes de arquivo tal como disponibilizados em https://pdad.ipe.df.gov.br
# Para usar outra fonte de dados, basta adicionar os nomes dos novos
# arquivos a estas listas (o sistema usa o primeiro que encontrar).
CANDIDATOS_MORADORES = [
    "PDAD_2024-Moradores.csv",
    "moradores.csv",
    "moradores_parcial.csv",
]
CANDIDATOS_DOMICILIOS = [
    "PDAD_2024-Domicilios.xlsx",
    "domicilios.xlsx",
    "domicilios_parcial.xlsx",
]
CANDIDATOS_DICIONARIO = [
    "Dicionario_de_variaveis_PDAD_2024.xlsx",
    "dicionario_de_variaveis_pdada_2024_público.xlsx",
    "dicionario.xlsx",
]

# Mapeamento fixo de código de localidade -> nome da RA/município (fonte:
# aba "anexo_1" do dicionário de variáveis). Mantido como fallback caso o
# arquivo do dicionário não esteja disponível na pasta dados/.
MAPA_LOCALIDADE_PADRAO = {
    5241: "Águas Lindas de Goiás", 5242: "Alexânia", 5243: "Cidade Ocidental",
    5244: "Cristalina", 5245: "Cocalzinho de Goiás", 5246: "Formosa",
    5247: "Luziânia", 5248: "Novo Gama", 5249: "Padre Bernardo",
    5250: "Planaltina de Goiás", 5251: "Santo Antônio do Descoberto",
    5252: "Valparaíso de Goiás", 5301: "Plano Piloto", 5302: "Gama",
    5303: "Taguatinga", 5304: "Brazlândia", 5305: "Sobradinho",
    5306: "Planaltina", 5307: "Paranoá", 5308: "Núcleo Bandeirante",
    5309: "Ceilândia", 5310: "Guará", 5311: "Cruzeiro", 5312: "Samambaia",
    5313: "Santa Maria", 5314: "São Sebastião", 5315: "Recanto Das Emas",
    5316: "Lago Sul", 5317: "Riacho Fundo", 5318: "Lago Norte",
    5319: "Candangolândia", 5320: "Águas Claras", 5321: "Riacho Fundo II",
    5322: "Sudoeste e Octogonal", 5323: "Varjão", 5324: "Park Way",
    5325: "SCIA", 5326: "Sobradinho II", 5327: "Jardim Botânico",
    5328: "Itapoã", 5329: "SIA", 5330: "Vicente Pires", 5331: "Fercal",
    5332: "Sol Nascente / Pôr do Sol", 5333: "Arniqueira", 5334: "Arapoanga",
    5335: "Água Quente", 5336: "Área Rural",
}


def _achar_arquivo(pasta, candidatos):
    """Procura, em ordem de preferência, qual arquivo de dados existe na pasta."""
    for nome in candidatos:
        caminho = os.path.join(pasta, nome)
        if os.path.isfile(caminho):
            return caminho
    return None


def _renomear_para_nomes_canonicos(df, mapa_colunas):
    """Renomeia apenas as colunas presentes no DataFrame, ignorando as ausentes.

    Isso permite que uma fonte de dados alternativa tenha só um subconjunto
    das colunas mapeadas em config.py sem quebrar a leitura.
    """
    mapa_existente = {origem: destino for origem, destino in mapa_colunas.items() if origem in df.columns}
    faltando = [origem for origem in mapa_colunas if origem not in df.columns]
    if faltando:
        print(f"Aviso: colunas não encontradas na fonte de dados e ignoradas: {faltando}")
    return df.rename(columns=mapa_existente)


def carregar_dicionario_localidades(pasta_dados="dados"):
    """Lê a aba anexo_1 do dicionário de variáveis; usa mapa fixo se ausente."""
    caminho = _achar_arquivo(pasta_dados, CANDIDATOS_DICIONARIO)
    if caminho is None:
        return dict(MAPA_LOCALIDADE_PADRAO)
    try:
        anexo1 = pd.read_excel(caminho, sheet_name="anexo_1")
        mapa = dict(zip(anexo1["Valor"], anexo1["Descrição do valor"]))
        return mapa if mapa else dict(MAPA_LOCALIDADE_PADRAO)
    except Exception:
        return dict(MAPA_LOCALIDADE_PADRAO)


def carregar_moradores(pasta_dados="dados"):
    """Lê o CSV de moradores e retorna um DataFrame com colunas canônicas."""
    caminho = _achar_arquivo(pasta_dados, CANDIDATOS_MORADORES)
    if caminho is None:
        raise FileNotFoundError(
            "Nenhum arquivo de moradores encontrado em '{}'. Baixe os dados em "
            "https://pdad.ipe.df.gov.br e coloque-os na pasta dados/, ou ajuste "
            "CANDIDATOS_MORADORES/COLUNAS_MORADORES para outra fonte.".format(pasta_dados)
        )
    df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", decimal=",", low_memory=False)
    return _renomear_para_nomes_canonicos(df, config.COLUNAS_MORADORES)


def carregar_domicilios(pasta_dados="dados"):
    """Lê a planilha de domicílios (.xlsx) e retorna um DataFrame com colunas canônicas."""
    caminho = _achar_arquivo(pasta_dados, CANDIDATOS_DOMICILIOS)
    if caminho is None:
        raise FileNotFoundError(
            "Nenhum arquivo de domicílios encontrado em '{}'. Baixe os dados em "
            "https://pdad.ipe.df.gov.br e coloque-os na pasta dados/, ou ajuste "
            "CANDIDATOS_DOMICILIOS/COLUNAS_DOMICILIOS para outra fonte.".format(pasta_dados)
        )
    df = pd.read_excel(caminho)
    return _renomear_para_nomes_canonicos(df, config.COLUNAS_DOMICILIOS)


def limpar_sentinelas(df, colunas):
    """Substitui os valores sentinela (definidos em config.py) por NA nas colunas dadas."""
    df = df.copy()
    for col in colunas:
        if col in df.columns:
            df[col] = df[col].where(~df[col].isin(config.SENTINELAS), pd.NA)
    return df


def mapear_localidade(df, mapa_localidades, coluna="localidade"):
    """Adiciona a coluna 'localidade_nome' traduzindo o código da RA/município."""
    df = df.copy()
    df["localidade_nome"] = df[coluna].map(mapa_localidades).fillna("Desconhecida")
    return df


def carregar_dados(pasta_dados="dados", callback_progresso=None):
    """Carrega, limpa e padroniza moradores e domicílios; retorna (moradores, domicilios).

    callback_progresso, se fornecido, é chamado com (etapa:int, total:int,
    mensagem:str) após cada etapa, para alimentar uma barra de progresso na
    interface gráfica.
    """
    etapas = 5
    if callback_progresso:
        callback_progresso(1, etapas, "Lendo dicionário de RAs...")
    mapa = carregar_dicionario_localidades(pasta_dados)

    if callback_progresso:
        callback_progresso(2, etapas, "Lendo arquivo de moradores...")
    moradores = carregar_moradores(pasta_dados)

    if callback_progresso:
        callback_progresso(3, etapas, "Lendo arquivo de domicílios...")
    domicilios = carregar_domicilios(pasta_dados)

    if callback_progresso:
        callback_progresso(4, etapas, "Tratando valores sentinela...")
    moradores = limpar_sentinelas(moradores, config.COLUNAS_NUMERICAS_MORADORES)
    domicilios = limpar_sentinelas(domicilios, config.COLUNAS_NUMERICAS_DOMICILIOS)

    if callback_progresso:
        callback_progresso(5, etapas, "Mapeando localidades...")
    moradores = mapear_localidade(moradores, mapa)
    domicilios = mapear_localidade(domicilios, mapa)

    return moradores, domicilios
