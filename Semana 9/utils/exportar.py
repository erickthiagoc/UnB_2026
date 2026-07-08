"""Funções de exportação de dados e estatísticas filtradas para arquivo."""

import csv
import datetime

from . import config
from .calcular import ROTULO_TODAS


def exportar_mini_relatorio_txt(caminho, localidade_nome, stats_local, stats_df):
    """Gera um mini relatório .txt explicando os números do recorte filtrado.

    Além dos valores numéricos, o relatório descreve o que cada indicador
    significa, qual filtro foi aplicado e como ele se compara à média do
    Distrito Federal como um todo — para ser lido e entendido mesmo por
    quem não está com o programa aberto.
    """
    nome_recorte = localidade_nome if localidade_nome and localidade_nome != ROTULO_TODAS else None

    def comparar(valor_local, valor_df, unidade):
        """Descreve em texto a diferença entre o valor local e a média do DF."""
        diferenca = valor_local - valor_df
        if abs(diferenca) < 0.05:
            return "praticamente igual à média do DF"
        direcao = "acima" if diferenca > 0 else "abaixo"
        return f"{abs(diferenca):.1f}{unidade} {direcao} da média do DF ({valor_df:.1f}{unidade})"

    linhas = []
    linhas.append("=" * 60)
    linhas.append("MINI RELATÓRIO — PDAD 2024")
    linhas.append("Perfil Demográfico e Composição Domiciliar do DF (Recorte F)")
    linhas.append("=" * 60)
    linhas.append("Gerado em: {}".format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))
    linhas.append("")

    linhas.append("1. FILTRO APLICADO")
    linhas.append("-" * 60)
    if nome_recorte:
        linhas.append(f"Recorte selecionado: {nome_recorte}")
        linhas.append(
            "Todos os números abaixo consideram apenas os moradores e domicílios "
            f"cuja variável 'localidade' corresponde a {nome_recorte}."
        )
    else:
        linhas.append("Recorte selecionado: Todas as RAs/municípios (Distrito Federal completo)")
        linhas.append("Os números abaixo somam todas as RAs do DF e municípios de Goiás amostrados pela pesquisa.")
    linhas.append("")

    linhas.append("2. DADOS DO RECORTE")
    linhas.append("-" * 60)
    linhas.append(f"Moradores no recorte: {stats_local['n_moradores']}")
    linhas.append(f"Domicílios no recorte: {stats_local['n_domicilios']}")
    linhas.append(f"Idade média: {stats_local['idade_media']:.1f} anos")
    linhas.append(f"Idade mediana: {stats_local['idade_mediana']:.1f} anos")
    linhas.append(f"Percentual de crianças (até 12 anos): {stats_local['pct_criancas']:.1f}%")
    linhas.append(f"Tamanho médio do domicílio: {stats_local['tamanho_medio_domicilio']:.2f} pessoas")
    linhas.append(f"Domicílios com ao menos 1 criança: {stats_local['pct_domicilios_com_crianca']:.1f}%")
    linhas.append("")

    linhas.append("3. O QUE ESTES NÚMEROS SIGNIFICAM")
    linhas.append("-" * 60)
    linhas.append(
        "- Idade média/mediana: resumem o quão jovem ou envelhecida é a "
        "população do recorte. Mediana é o valor que separa a metade mais "
        "jovem da metade mais velha, e é menos sensível a poucos casos extremos."
    )
    linhas.append(
        "- % de crianças: proporção de moradores com até 12 anos — um "
        "indicador de quão jovem é a base populacional do recorte."
    )
    linhas.append(
        "- Tamanho médio do domicílio: quantas pessoas moram, em média, na "
        "mesma residência no recorte selecionado."
    )
    linhas.append(
        "- % de domicílios com criança: proporção de domicílios em que mora "
        "pelo menos uma criança, independentemente do tamanho da família."
    )
    linhas.append("")

    if nome_recorte:
        linhas.append("4. COMPARAÇÃO COM A MÉDIA DO DF")
        linhas.append("-" * 60)
        linhas.append(
            f"Idade média em {nome_recorte}: "
            + comparar(stats_local["idade_media"], stats_df["idade_media"], " anos")
        )
        linhas.append(
            f"% de crianças em {nome_recorte}: "
            + comparar(stats_local["pct_criancas"], stats_df["pct_criancas"], " p.p.")
        )
        linhas.append(
            f"Tamanho médio do domicílio em {nome_recorte}: "
            + comparar(stats_local["tamanho_medio_domicilio"], stats_df["tamanho_medio_domicilio"], " pessoas")
        )
        linhas.append("")

    linhas.append("5. NOTA METODOLÓGICA")
    linhas.append("-" * 60)
    descricao_sentinelas = " e ".join(
        f"{valor} ('{config.DESCRICAO_SENTINELAS.get(valor, 'sentinela')}')" for valor in config.SENTINELAS
    )
    linhas.append(
        f"Antes de qualquer cálculo, os valores sentinela {descricao_sentinelas} "
        "foram removidos das variáveis utilizadas. Em especial, a variável de "
        "identidade de gênero não é perguntada a crianças pequenas, então "
        "esses registros não entram nos cálculos que dependem dela (ex.: "
        "pirâmide etária)."
    )
    linhas.append("Fonte dos dados: PDAD 2024 (Pesquisa Distrital por Amostra de Domicílios), CODEPLAN/IPEDF.")
    linhas.append("=" * 60)

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return caminho


def exportar_ranking_csv(caminho, ranking, rotulo_metrica="valor"):
    """Grava uma lista de tuplas (rotulo, valor) do ranking de RAs em CSV."""
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f, delimiter=";")
        escritor.writerow(["posicao", "localidade", rotulo_metrica])
        for posicao, (nome, valor) in enumerate(ranking, start=1):
            escritor.writerow([posicao, nome, valor])
    return caminho
