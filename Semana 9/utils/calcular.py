"""Funções de análise estatística e agregação para o Recorte F.

Nenhuma função aqui depende de tkinter, e nenhuma usa nomes de coluna do
PDAD diretamente — todas trabalham com os nomes CANÔNICOS produzidos por
utils/carregar.py (ex.: "idade", "genero", "chave_domicilio") e com os
rótulos de categoria definidos em utils/config.py. Isso é o que permite
trocar a fonte de dados (config.py) sem alterar este arquivo.
"""

import pandas as pd

from . import config

# Rótulo usado na interface e nos filtros para indicar "sem filtro de RA"
# (considerar todas as localidades). Definido uma única vez para evitar
# repetição da string em vários arquivos.
ROTULO_TODAS = "Todas as RAs/municípios"

FAIXAS_ETARIAS = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 200]
ROTULOS_FAIXAS = [
    "0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
    "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+",
]


def filtrar_por_localidade(df, localidade_nome=None):
    """Retorna subconjunto do DataFrame para a RA/município informado (ou tudo)."""
    if not localidade_nome or localidade_nome == ROTULO_TODAS:
        return df
    return df[df["localidade_nome"] == localidade_nome]


def calcular_piramide_etaria(moradores, localidade_nome=None):
    """Retorna DataFrame com contagem de moradores por faixa etária e gênero.

    Linhas com genero ausente (sentinela já convertido em NA por
    limpar_sentinelas) são descartadas apenas para este cálculo, pois não é
    possível compor a pirâmide sem a informação de gênero.
    """
    df = filtrar_por_localidade(moradores, localidade_nome)
    df = df.dropna(subset=["genero", "idade"])
    df = df.copy()
    df["faixa"] = pd.cut(df["idade"], bins=FAIXAS_ETARIAS, labels=ROTULOS_FAIXAS, right=True)
    df["genero_nome"] = df["genero"].map(config.CATEGORIAS_GENERO).fillna("Outro")
    tabela = df.groupby(["faixa", "genero_nome"], observed=False).size().unstack(fill_value=0)
    tabela = tabela.reindex(ROTULOS_FAIXAS)
    for col in config.CATEGORIAS_GENERO.values():
        if col not in tabela.columns:
            tabela[col] = 0
    return tabela


def calcular_distribuicao_arranjos(domicilios, localidade_nome=None):
    """Retorna Series com a contagem de domicílios por tipo de arranjo familiar."""
    df = filtrar_por_localidade(domicilios, localidade_nome)
    df = df.dropna(subset=["arranjo_familiar"])
    contagem = df["arranjo_familiar"].map(config.CATEGORIAS_ARRANJO).value_counts()
    return contagem.reindex(list(config.CATEGORIAS_ARRANJO.values())).fillna(0)


def calcular_estatisticas_gerais(moradores, domicilios, localidade_nome=None):
    """Retorna dicionário com estatísticas descritivas do recorte selecionado."""
    mor = filtrar_por_localidade(moradores, localidade_nome)
    dom = filtrar_por_localidade(domicilios, localidade_nome)

    idade_media = mor["idade"].mean()
    idade_mediana = mor["idade"].median()
    pct_criancas = (mor["idade"] <= 12).mean() * 100 if len(mor) else 0
    tamanho_medio_domicilio = dom["tamanho_domicilio"].mean()
    pct_domicilios_com_crianca = (dom["criancas_domicilio"] > 0).mean() * 100 if len(dom) else 0

    return {
        "n_moradores": len(mor),
        "n_domicilios": len(dom),
        "idade_media": idade_media,
        "idade_mediana": idade_mediana,
        "pct_criancas": pct_criancas,
        "tamanho_medio_domicilio": tamanho_medio_domicilio,
        "pct_domicilios_com_crianca": pct_domicilios_com_crianca,
    }


def calcular_perfil_por_arranjo(moradores, domicilios):
    """Cruza moradores x domicílios (merge pela chave_domicilio) e retorna
    idade média e % de crianças por tipo de arranjo domiciliar.

    Este cálculo exige as duas tabelas: a idade vem de moradores, o tipo de
    arranjo familiar vem de domicílios; nenhuma das duas contém as duas
    informações isoladamente.
    """
    dom_reduzido = domicilios[["chave_domicilio", "arranjo_familiar"]].dropna(subset=["arranjo_familiar"])
    combinado = moradores.merge(dom_reduzido, on="chave_domicilio", how="inner")
    combinado["arranjo_nome"] = combinado["arranjo_familiar"].map(config.CATEGORIAS_ARRANJO)

    resultado = combinado.groupby("arranjo_nome").agg(
        idade_media=("idade", "mean"),
        pct_criancas=("idade", lambda s: (s <= 12).mean() * 100),
        n_moradores=("idade", "count"),
    )
    return resultado.reindex(list(config.CATEGORIAS_ARRANJO.values()))


def calcular_ranking_ras(domicilios, metrica="tamanho_medio"):
    """Retorna ranking de RAs/municípios ordenado do maior para o menor valor.

    metrica: 'tamanho_medio' (média de tamanho_domicilio) ou
             'pct_com_criancas' (% de domicílios com ao menos 1 criança).
    """
    grupos = domicilios.dropna(subset=["tamanho_domicilio"]).groupby("localidade_nome")

    pares = []
    for nome, grupo in grupos:
        if len(grupo) < 5:
            continue  # amostra pequena demais para um ranking confiável
        if metrica == "pct_com_criancas":
            valor = (grupo["criancas_domicilio"] > 0).mean() * 100
        else:
            valor = grupo["tamanho_domicilio"].mean()
        pares.append((nome, round(float(valor), 2)))

    return sorted(pares, key=lambda par: par[1], reverse=True)
