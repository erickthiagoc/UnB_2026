"""
Sistema de Exploração dos Microdados PDAD 2024 — Interface Gráfica
Recorte F — Perfil Demográfico e Composição Domiciliar do DF

Disciplina: Algoritmos e Programação de Computadores (APC 2026/1) — UnB/CIC
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from utils import carregar
from utils import calcular
from utils import exportar
from utils.calcular import ROTULO_TODAS

PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")

# Autor do trabalho — exibido na tela inicial e usado no rodapé dos
# relatórios exportados.
AUTORES = ["Erick Thiago Cardoso Araujo"]


# ---------------------------------------------------------------------------
# Carregamento com barra de progresso (Diferencial D6)
# ---------------------------------------------------------------------------

def exibir_splash_e_carregar(root):
    """Mostra uma janela de progresso enquanto lê e limpa os dados PDAD."""
    splash = tk.Toplevel(root)
    splash.title("Carregando PDAD 2024...")
    splash.geometry("420x120")
    splash.resizable(False, False)

    tk.Label(splash, text="Carregando microdados do PDAD 2024", font=("Segoe UI", 11, "bold")).pack(pady=(15, 5))
    label_etapa = tk.Label(splash, text="Iniciando...")
    label_etapa.pack()

    barra = ttk.Progressbar(splash, orient="horizontal", length=360, mode="determinate")
    barra.pack(pady=15)

    splash.update()

    def callback_progresso(etapa, total, mensagem):
        """Atualiza a barra de progresso e o rótulo de status da splash screen."""
        barra["maximum"] = total
        barra["value"] = etapa
        label_etapa.config(text=mensagem)
        splash.update()

    try:
        moradores, domicilios = carregar.carregar_dados(PASTA_DADOS, callback_progresso)
    except FileNotFoundError as erro:
        splash.destroy()
        messagebox.showerror("Erro ao carregar dados", str(erro))
        root.destroy()
        sys.exit(1)

    splash.destroy()
    return moradores, domicilios


# ---------------------------------------------------------------------------
# Aba 1 — Pirâmide etária e comparação entre RAs (Requisitos 2, 3 · Diferencial D2)
# ---------------------------------------------------------------------------

def construir_aba_piramide(pai, moradores, domicilios, lista_localidades):
    """Monta a aba de pirâmide etária, com filtro de RA e comparação entre duas RAs."""
    aba = ttk.Frame(pai)

    frame_filtros = ttk.Frame(aba)
    frame_filtros.pack(fill="x", padx=10, pady=8)

    ttk.Label(frame_filtros, text="RA / município:").grid(row=0, column=0, sticky="w")
    combo_ra1 = ttk.Combobox(frame_filtros, values=[ROTULO_TODAS] + lista_localidades, state="readonly", width=28)
    combo_ra1.current(0)
    combo_ra1.grid(row=0, column=1, padx=5)

    ttk.Label(frame_filtros, text="Comparar com (opcional):").grid(row=0, column=2, sticky="w", padx=(15, 0))
    combo_ra2 = ttk.Combobox(frame_filtros, values=["Nenhuma"] + lista_localidades, state="readonly", width=28)
    combo_ra2.current(0)
    combo_ra2.grid(row=0, column=3, padx=5)

    frame_stats = ttk.Frame(aba)
    frame_stats.pack(fill="x", padx=10, pady=(0, 8))
    label_stats = tk.Label(frame_stats, text="", justify="left", font=("Consolas", 9))
    label_stats.pack(anchor="w")

    figura = Figure(figsize=(8, 4.2), dpi=100)
    canvas = FigureCanvasTkAgg(figura, master=aba)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

    def desenhar_piramide(eixo, tabela, titulo, compacto=False):
        """Desenha, em um eixo do matplotlib, a pirâmide etária mirrorada.

        compacto=True reduz fontes e encurta o título — usado quando há duas
        pirâmides lado a lado, para nada ficar cortado ou sobreposto.
        """
        fonte_titulo = 10 if compacto else 12
        fonte_rotulo = 6 if compacto else 7
        fonte_eixo = 7 if compacto else 9

        if tabela.empty or tabela.sum().sum() == 0:
            eixo.text(0.5, 0.5, "Sem dados\nsuficientes", ha="center", va="center", fontsize=fonte_eixo)
            eixo.set_title(titulo, fontsize=fonte_titulo)
            return
        cis = tabela.get("Cisgênero", 0)
        outros = tabela.get("Transgênero", 0) + tabela.get("Outro", 0)
        posicoes = range(len(tabela.index))
        eixo.barh(posicoes, -cis, color="#2b6cb0", label="Cisgênero")
        eixo.barh(posicoes, outros, color="#dd6b20", label="Trans/Outro")
        eixo.set_yticks(list(posicoes))
        eixo.set_yticklabels(tabela.index, fontsize=fonte_eixo)
        eixo.axvline(0, color="black", linewidth=0.8)
        eixo.set_title(titulo, fontsize=fonte_titulo)
        eixo.set_xlabel("Nº de moradores", fontsize=fonte_eixo)
        eixo.tick_params(axis="x", labelsize=fonte_eixo)
        eixo.legend(fontsize=fonte_rotulo, loc="lower right")
        eixo.margins(x=0.18)

        # Rótulos numéricos ao lado de cada barra — sem eles, a barra
        # laranja (Trans/Outro) fica fina demais para se ler visualmente.
        maior_valor = max(int(cis.max()) if len(cis) else 0, int(outros.max()) if len(outros) else 1, 1)
        deslocamento = maior_valor * 0.02
        for i, (valor_cis, valor_outros) in enumerate(zip(cis, outros)):
            if valor_cis > 0:
                eixo.text(-valor_cis - deslocamento, i, f"{int(valor_cis)}", ha="right", va="center", fontsize=fonte_rotulo)
            if valor_outros > 0:
                eixo.text(valor_outros + deslocamento, i, f"{int(valor_outros)}", ha="left", va="center", fontsize=fonte_rotulo)

        # O eixo X usa valores negativos só para espelhar a barra da esquerda
        # (efeito visual de pirâmide); os rótulos mostram o valor absoluto
        # para não confundir "contagem negativa" com "menos pessoas".
        ticks_atuais = eixo.get_xticks()
        eixo.set_xticks(ticks_atuais)
        eixo.set_xticklabels([f"{int(abs(t))}" for t in ticks_atuais])

    def atualizar_grafico(*_):
        """Recalcula estatísticas e redesenha a(s) pirâmide(s) etária(s) conforme o filtro."""
        ra1 = combo_ra1.get()
        ra2 = combo_ra2.get()

        # clear() remove todos os eixos anteriores; sem isso, alternar entre
        # 1 e 2 gráficos deixaria "fantasmas" do desenho anterior na figura.
        figura.clear()

        if ra2 and ra2 != "Nenhuma":
            eixo1 = figura.add_subplot(1, 2, 1)
            eixo2 = figura.add_subplot(1, 2, 2)
            desenhar_piramide(eixo1, calcular.calcular_piramide_etaria(moradores, ra1), ra1, compacto=True)
            desenhar_piramide(eixo2, calcular.calcular_piramide_etaria(moradores, ra2), ra2, compacto=True)
        else:
            eixo1 = figura.add_subplot(1, 1, 1)
            desenhar_piramide(eixo1, calcular.calcular_piramide_etaria(moradores, ra1), ra1, compacto=False)

        figura.tight_layout()
        canvas.draw()

        stats = calcular.calcular_estatisticas_gerais(moradores, domicilios, ra1)

        def fmt(valor, casas=1, sufixo=""):
            """Formata um número, exibindo '—' quando o valor é NaN/ausente."""
            if valor is None or (isinstance(valor, float) and pd.isna(valor)):
                return "—"
            return f"{valor:.{casas}f}{sufixo}"

        label_stats.config(text=(
            f"Moradores no recorte: {stats['n_moradores']:>6} | "
            f"Idade média: {fmt(stats['idade_media'], 1, ' anos')} | "
            f"Idade mediana: {fmt(stats['idade_mediana'], 1, ' anos')} | "
            f"% de crianças (até 12 anos): {fmt(stats['pct_criancas'], 1, '%')}"
        ))

    def exportar_estatisticas_atuais():
        """Abre diálogo para salvar um mini relatório do filtro atual em .txt."""
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            title="Exportar mini relatório",
        )
        if not caminho:
            return
        stats_local = calcular.calcular_estatisticas_gerais(moradores, domicilios, combo_ra1.get())
        stats_df = calcular.calcular_estatisticas_gerais(moradores, domicilios)
        exportar.exportar_mini_relatorio_txt(caminho, combo_ra1.get(), stats_local, stats_df)
        messagebox.showinfo("Exportado", f"Mini relatório salvo em:\n{caminho}")

    combo_ra1.bind("<<ComboboxSelected>>", atualizar_grafico)
    combo_ra2.bind("<<ComboboxSelected>>", atualizar_grafico)

    ttk.Button(frame_filtros, text="Exportar mini relatório...", command=exportar_estatisticas_atuais).grid(row=0, column=4, padx=(15, 0))

    atualizar_grafico()
    return aba


# ---------------------------------------------------------------------------
# Aba 2 — Composição domiciliar (Diferencial D3 — merge entre as tabelas)
# ---------------------------------------------------------------------------

def construir_aba_composicao(pai, moradores, domicilios, lista_localidades):
    """Monta a aba de composição domiciliar: tamanho, arranjo familiar e cruzamento com moradores."""
    aba = ttk.Frame(pai)

    frame_filtros = ttk.Frame(aba)
    frame_filtros.pack(fill="x", padx=10, pady=8)
    ttk.Label(frame_filtros, text="RA / município:").pack(side="left")
    combo_ra = ttk.Combobox(frame_filtros, values=[ROTULO_TODAS] + lista_localidades, state="readonly", width=28)
    combo_ra.current(0)
    combo_ra.pack(side="left", padx=5)

    figura = Figure(figsize=(7.5, 3.8), dpi=100)
    canvas = FigureCanvasTkAgg(figura, master=aba)
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

    label_merge = tk.Label(aba, text="", justify="left", font=("Consolas", 9))
    label_merge.pack(anchor="w", padx=10, pady=(0, 10))

    def atualizar_composicao(*_):
        """Redesenha o gráfico de arranjo familiar e o indicador que cruza
        moradores e domicílios (Diferencial D3)."""
        ra = combo_ra.get()
        figura.clear()

        eixo_arranjo = figura.add_subplot(1, 1, 1)
        arranjos = calcular.calcular_distribuicao_arranjos(domicilios, ra)
        barras = eixo_arranjo.bar(range(len(arranjos)), arranjos.values, color="#2f855a")
        eixo_arranjo.set_xticks(range(len(arranjos)))
        eixo_arranjo.set_xticklabels(arranjos.index, rotation=20, ha="right", fontsize=8)
        eixo_arranjo.set_title("Distribuição dos domicílios por arranjo familiar")
        eixo_arranjo.set_xlabel("Tipo de arranjo familiar")
        eixo_arranjo.set_ylabel("Nº de domicílios")

        # Rótulo numérico no topo de cada barra, para leitura direta do valor.
        eixo_arranjo.bar_label(barras, fmt="%d", fontsize=8, padding=2)
        eixo_arranjo.margins(y=0.12)

        figura.tight_layout()
        canvas.draw()

        # Diferencial D3: cruzamento (merge) entre moradores e domicílios.
        # filtrar_por_localidade já devolve o conjunto completo quando ra
        # é o rótulo "todas", então não é preciso testar isso aqui.
        perfil = calcular.calcular_perfil_por_arranjo(
            calcular.filtrar_por_localidade(moradores, ra),
            calcular.filtrar_por_localidade(domicilios, ra),
        )
        linhas = ["Idade média e % de crianças por arranjo familiar (merge moradores × domicílios):"]
        for nome, linha in perfil.dropna(how="all").iterrows():
            if linha["n_moradores"] and linha["n_moradores"] > 0:
                linhas.append(
                    f"  {nome:<20} idade média: {linha['idade_media']:>5.1f} anos | "
                    f"% crianças: {linha['pct_criancas']:>5.1f}% | n={int(linha['n_moradores'])}"
                )
        label_merge.config(text="\n".join(linhas))

    combo_ra.bind("<<ComboboxSelected>>", atualizar_composicao)
    atualizar_composicao()
    return aba


# ---------------------------------------------------------------------------
# Aba 3 — Ranking de RAs por indicadores de composição domiciliar
# ---------------------------------------------------------------------------

def construir_aba_ranking(pai, moradores, domicilios):
    """Monta a aba de ranking de RAs por indicadores de composição domiciliar."""
    aba = ttk.Frame(pai)

    frame_topo = ttk.Frame(aba)
    frame_topo.pack(fill="x", padx=10, pady=8)
    ttk.Label(frame_topo, text="Ordenar por:").pack(side="left")
    combo_metrica = ttk.Combobox(
        frame_topo,
        values=["Tamanho médio do domicílio", "% de domicílios com criança"],
        state="readonly",
        width=32,
    )
    combo_metrica.current(0)
    combo_metrica.pack(side="left", padx=5)

    colunas = ("posicao", "localidade", "valor")
    tabela = ttk.Treeview(aba, columns=colunas, show="headings", height=15)
    tabela.heading("posicao", text="#")
    tabela.heading("localidade", text="RA / Município")
    tabela.heading("valor", text="Valor")
    tabela.column("posicao", width=40, anchor="center")
    tabela.column("localidade", width=220)
    tabela.column("valor", width=200, anchor="center")
    tabela.pack(fill="both", expand=True, padx=10, pady=5)

    ranking_atual = {"dados": [], "rotulo": ""}

    def metrica_selecionada():
        """Converte o texto do combobox na chave interna de métrica usada em calcular.py."""
        return "pct_com_criancas" if "criança" in combo_metrica.get() else "tamanho_medio"

    def atualizar_ranking(*_):
        """Recalcula o ranking de RAs conforme a métrica escolhida e repopula a Treeview."""
        for item in tabela.get_children():
            tabela.delete(item)

        metrica = metrica_selecionada()
        if metrica == "pct_com_criancas":
            rotulo = "% de domicílios com criança"
            formatar_valor = lambda v: f"{v:.1f}%"
        else:
            rotulo = "Tamanho médio do domicílio (pessoas)"
            formatar_valor = lambda v: f"{v:.2f} pessoas"

        tabela.heading("valor", text=rotulo)
        ranking = calcular.calcular_ranking_ras(domicilios, metrica)
        ranking_atual["dados"] = ranking
        ranking_atual["rotulo"] = rotulo

        for posicao, (nome, valor) in enumerate(ranking, start=1):
            tabela.insert("", "end", values=(posicao, nome, formatar_valor(valor)))

    def exportar_ranking_atual():
        """Abre diálogo para salvar o ranking atualmente exibido em .csv."""
        if not ranking_atual["dados"]:
            return
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exportar ranking",
        )
        if not caminho:
            return
        exportar.exportar_ranking_csv(caminho, ranking_atual["dados"], ranking_atual["rotulo"])
        messagebox.showinfo("Exportado", f"Ranking salvo em:\n{caminho}")

    ttk.Button(frame_topo, text="Exportar ranking...", command=exportar_ranking_atual).pack(side="left", padx=(15, 0))

    combo_metrica.bind("<<ComboboxSelected>>", atualizar_ranking)

    atualizar_ranking()
    return aba


# ---------------------------------------------------------------------------
# Janela principal (Requisito 1)
# ---------------------------------------------------------------------------

def construir_janela_principal(root, moradores, domicilios):
    """Monta o cabeçalho e as três abas da janela principal do sistema."""
    root.title("PDAD 2024 — Perfil Demográfico e Composição Domiciliar do DF")
    root.geometry("980x680")

    frame_cabecalho = ttk.Frame(root)
    frame_cabecalho.pack(fill="x", padx=10, pady=(10, 0))
    tk.Label(
        frame_cabecalho,
        text="Recorte F — Perfil Demográfico e Composição Domiciliar",
        font=("Segoe UI", 14, "bold"),
    ).pack(anchor="w")
    tk.Label(
        frame_cabecalho,
        text="Como é a composição etária e familiar dos domicílios do Distrito Federal? (PDAD 2024)",
        font=("Segoe UI", 9),
        foreground="#555",
    ).pack(anchor="w")
    tk.Label(
        frame_cabecalho,
        text="Autor: " + " · ".join(AUTORES),
        font=("Segoe UI", 8),
        foreground="#777",
    ).pack(anchor="w", pady=(2, 0))
    tk.Label(
        frame_cabecalho,
        text=f"{len(moradores):,} moradores · {len(domicilios):,} domicílios carregados".replace(",", "."),
        font=("Segoe UI", 9, "italic"),
    ).pack(anchor="w", pady=(2, 8))

    lista_localidades = sorted(domicilios["localidade_nome"].dropna().unique().tolist())

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    aba_piramide = construir_aba_piramide(notebook, moradores, domicilios, lista_localidades)
    aba_composicao = construir_aba_composicao(notebook, moradores, domicilios, lista_localidades)
    aba_ranking = construir_aba_ranking(notebook, moradores, domicilios)

    notebook.add(aba_piramide, text="Pirâmide Etária")
    notebook.add(aba_composicao, text="Composição Domiciliar")
    notebook.add(aba_ranking, text="Ranking de RAs")


def main():
    """Ponto de entrada do sistema: cria a janela raiz, carrega dados e monta a UI."""
    root = tk.Tk()
    root.withdraw()

    moradores, domicilios = exibir_splash_e_carregar(root)

    root.deiconify()
    construir_janela_principal(root, moradores, domicilios)
    root.mainloop()


if __name__ == "__main__":
    main()
