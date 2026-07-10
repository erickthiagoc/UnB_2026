# Exercícios — Microdados PDAD 2024 (Python)

Códigos dos exercícios práticos com os dados do PDAD-A 2024 (IPEDF).
Arquivos usados: `moradores_parcial.csv` e `domicilios_parcial.xlsx`.

---

## 🟢 Nível 1 — Trivial

### Exercício 1.1 — Lendo os dados

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")
print(moradores.head())   # mostra as 5 primeiras linhas
```

---

### Exercício 1.2 — Selecionando colunas

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

colunas = ["morador_id", "localidade", "idade_calculada", "id_genero", "escolaridade", "renda_ind"]
print(moradores[colunas])   # exibe só as colunas escolhidas
```

---

### Exercício 1.3 — Contando moradores por domicílio

```python
import pandas as pd

domicilios = pd.read_excel("domicilios_parcial.xlsx")

for _, linha in domicilios.iterrows():
    print(f"Domicílio {linha['A01nficha']}: {linha['A01npessoas']} moradores, {linha['A01ncriancas']} crianças")
```

---

### Exercício 1.4 — Exibindo idades

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

# 99999 significa que a pergunta não se aplicava à pessoa
adultos = moradores[moradores["idade_calculada"] != 99999]
print(adultos[["morador_id", "idade_calculada"]])
```

---

## 🟡 Nível 2 — Básico

### Exercício 2.1 — Calculando a idade média

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

idades = moradores[moradores["idade_calculada"] != 99999]["idade_calculada"].tolist()

soma = 0
for idade in idades:
    soma = soma + idade

media = soma / len(idades)
print(f"Total de moradores com idade declarada: {len(idades)}")
print(f"Soma das idades: {soma}")
print(f"Média de idade: {media:.1f} anos")
```

---

### Exercício 2.2 — Contando por escolaridade

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

escolaridade_nome = {
    1: "Sem instrução",
    2: "Fundamental incompleto",
    3: "Fundamental completo",
    4: "Médio incompleto",
    5: "Médio completo",
    6: "Superior incompleto",
    7: "Superior completo",
    8: "Sem classificação",
}

contagem = {}
for _, linha in moradores.iterrows():
    nivel = linha["escolaridade"]
    if nivel in escolaridade_nome:
        if nivel not in contagem:
            contagem[nivel] = 0
        contagem[nivel] += 1

print("Escolaridade dos moradores:")
for nivel, total in contagem.items():
    print(f"  {escolaridade_nome[nivel]}: {total} moradores")
```

---

### Exercício 2.3 — Filtrando por Região Administrativa

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

ra_alvo = 5320  # Gama

filtro = moradores[moradores["localidade"] == ra_alvo]

print(f"Moradores da RA {ra_alvo}:")
for _, linha in filtro.iterrows():
    print(f"  {linha['morador_id']} — {linha['idade_calculada']} anos — escolaridade: {linha['escolaridade']}")
```

---

### Exercício 2.4 — Renda dos moradores declarantes

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

com_renda = moradores[(moradores["renda_ind"] > 0) & (moradores["renda_ind"] != 99999)]

print(f"Moradores com renda declarada: {len(com_renda)}")
for _, linha in com_renda.iterrows():
    print(f"  {linha['morador_id']} — R$ {linha['renda_ind']:,.0f}")
```

---

## 🟠 Nível 3 — Intermediário (Algoritmos de Ordenação)

### Exercício 3.1 — Ordenando por idade (Bubble Sort)

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

validos = moradores[moradores["idade_calculada"] != 99999].copy()
lista = validos[["morador_id", "idade_calculada"]].to_dict("records")

# Bubble Sort por idade: a cada passagem, troca vizinhos fora de ordem
n = len(lista)
for i in range(n):
    for j in range(n - i - 1):
        if lista[j]["idade_calculada"] > lista[j + 1]["idade_calculada"]:
            lista[j], lista[j + 1] = lista[j + 1], lista[j]

print("Moradores ordenados do mais novo ao mais velho:")
for m in lista:
    print(f"  {m['morador_id']}: {m['idade_calculada']} anos")
```

---

### Exercício 3.2 — Ordenando por renda (Selection Sort)

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

com_renda = moradores[(moradores["renda_ind"] > 0) & (moradores["renda_ind"] != 99999)].copy()
lista = com_renda[["morador_id", "renda_ind"]].to_dict("records")

# Selection Sort: encontra o menor da parte restante e o coloca na posição certa
n = len(lista)
for i in range(n):
    idx_min = i
    for j in range(i + 1, n):
        if lista[j]["renda_ind"] < lista[idx_min]["renda_ind"]:
            idx_min = j
    lista[i], lista[idx_min] = lista[idx_min], lista[i]

print("Moradores ordenados por renda (menor para maior):")
for m in lista:
    print(f"  {m['morador_id']}: R$ {m['renda_ind']:,.0f}")
```

---

### Exercício 3.3 — Ordenando por nome de RA (Insertion Sort)

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")

ra_nomes = {
    5249: "Arniqueira",    5301: "Brasília",       5303: "Taguatinga",
    5305: "Sobradinho",    5311: "Cruzeiro",        5313: "Ceilândia",
    5314: "Sobradinho II", 5315: "Jardim Botânico", 5319: "Lago Sul",
    5320: "Gama",          5326: "Samambaia",       5328: "Santa Maria",
    5330: "São Sebastião",
}

codigos = moradores["localidade"].unique().tolist()
ras = [{"codigo": c, "nome": ra_nomes.get(c, f"RA-{c}")} for c in codigos]

# Insertion Sort: pega um item de cada vez e insere na posição certa
for i in range(1, len(ras)):
    chave = ras[i]
    j = i - 1
    while j >= 0 and ras[j]["nome"] > chave["nome"]:
        ras[j + 1] = ras[j]
        j -= 1
    ras[j + 1] = chave

print("Regiões Administrativas (ordem alfabética):")
for ra in ras:
    total = (moradores["localidade"] == ra["codigo"]).sum()
    print(f"  {ra['nome']} (cód. {ra['codigo']}): {total} moradores na amostra")
```

---

### Exercício 3.4 — Comparando algoritmos de ordenação

```python
import pandas as pd

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")
validos = moradores[moradores["idade_calculada"] != 99999].copy()
idades_base = validos["idade_calculada"].tolist()

def bubble_sort_conta(lista):
    lst = lista[:]
    comparacoes = 0
    n = len(lst)
    for i in range(n):
        for j in range(n - i - 1):
            comparacoes += 1
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst, comparacoes

def selection_sort_conta(lista):
    lst = lista[:]
    comparacoes = 0
    n = len(lst)
    for i in range(n):
        idx_min = i
        for j in range(i + 1, n):
            comparacoes += 1
            if lst[j] < lst[idx_min]:
                idx_min = j
        lst[i], lst[idx_min] = lst[idx_min], lst[i]
    return lst, comparacoes

def insertion_sort_conta(lista):
    lst = lista[:]
    comparacoes = 0
    for i in range(1, len(lst)):
        chave = lst[i]
        j = i - 1
        while j >= 0 and lst[j] > chave:
            comparacoes += 1
            lst[j + 1] = lst[j]
            j -= 1
        comparacoes += 1
        lst[j + 1] = chave
    return lst, comparacoes

n = len(idades_base)
_, c_bubble    = bubble_sort_conta(idades_base)
_, c_selection = selection_sort_conta(idades_base)
_, c_insertion = insertion_sort_conta(idades_base)

print(f"Ordenando {n} elementos (idades dos moradores):")
print(f"  Bubble Sort:    {c_bubble} comparações")
print(f"  Selection Sort: {c_selection} comparações")
print(f"  Insertion Sort: {c_insertion} comparações")
print(f"  Teórico O(n²):  {n*n}  (n={n}, n²={n}²)")
```

---

## 🔴 Nível 4 — Avançado (Relatórios via CLI)

### Exercício 4.1 — Relatório em TXT por linha de comando

```python
# relatorio_moradores.py
import sys
import pandas as pd

if len(sys.argv) < 2:
    print("Uso: python relatorio_moradores.py <nome_do_arquivo.txt>")
    sys.exit(1)

arquivo_saida = sys.argv[1]

moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")
validos = moradores[moradores["idade_calculada"] != 99999]
idades = validos["idade_calculada"].tolist()
media_idade = sum(idades) / len(idades)

linhas = []
linhas.append("=" * 50)
linhas.append("RELATÓRIO PDAD 2024 — MORADORES")
linhas.append("=" * 50)
linhas.append(f"Total de moradores na amostra : {len(moradores)}")
linhas.append(f"Com idade declarada           : {len(validos)}")
linhas.append(f"Média de idade                : {media_idade:.1f} anos")
linhas.append(f"Idade mínima                  : {min(idades)} anos")
linhas.append(f"Idade máxima                  : {max(idades)} anos")
linhas.append("")

with open(arquivo_saida, "w", encoding="utf-8") as f:
    for linha in linhas:
        f.write(linha + "\n")

print(f"Relatório salvo em: {arquivo_saida}")
```

**Como executar no terminal:**
```bash
python relatorio_moradores.py relatorio_moradores.txt
```

---

### Exercício 4.2 — Relatório interativo com menu

```python
# menu_pdad.py
import pandas as pd

def carregar_dados():
    mor = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")
    dom = pd.read_excel("domicilios_parcial.xlsx")
    return mor, dom

def relatorio_idades(moradores):
    validos = moradores[moradores["idade_calculada"] != 99999]
    idades = validos["idade_calculada"].tolist()
    print(f"\n  Total com idade declarada: {len(idades)}")
    print(f"  Média: {sum(idades)/len(idades):.1f} anos")
    print(f"  Mínima: {min(idades)} | Máxima: {max(idades)}")

def relatorio_escolaridade(moradores):
    nomes = {1:"Sem instrução",2:"Fund. incompleto",3:"Fund. completo",
             4:"Médio incompleto",5:"Médio completo",6:"Superior incompleto",
             7:"Superior completo",8:"Pós-graduação"}
    contagem = {}
    for _, linha in moradores.iterrows():
        n = linha["escolaridade"]
        if n in nomes:
            contagem[n] = contagem.get(n, 0) + 1
    print("\n  Escolaridade:")
    for nivel, total in sorted(contagem.items()):
        print(f"    {nomes[nivel]}: {total}")

def relatorio_domicilios(domicilios):
    print(f"\n  Total de domicílios: {len(domicilios)}")
    media_pessoas = sum(domicilios["A01npessoas"]) / len(domicilios)
    print(f"  Média de moradores por domicílio: {media_pessoas:.1f}")

moradores, domicilios = carregar_dados()

while True:
    print("\n" + "=" * 40)
    print("  PDAD 2024 — Menu de Relatórios")
    print("=" * 40)
    print("  1. Relatório de idades")
    print("  2. Relatório de escolaridade")
    print("  3. Relatório de domicílios")
    print("  0. Sair")
    opcao = input("\n  Escolha uma opção: ").strip()

    if opcao == "1":
        relatorio_idades(moradores)
    elif opcao == "2":
        relatorio_escolaridade(moradores)
    elif opcao == "3":
        relatorio_domicilios(domicilios)
    elif opcao == "0":
        print("  Até logo!")
        break
    else:
        print("  Opção inválida.")
```

---

### Exercício 4.3 — Programa completo com argumento de RA

```python
# analise_ra.py
import sys
import pandas as pd

RA_NOMES = {
    5249: "Arniqueira",    5301: "Brasília",       5303: "Taguatinga",
    5305: "Sobradinho",    5311: "Cruzeiro",        5313: "Ceilândia",
    5314: "Sobradinho II", 5315: "Jardim Botânico", 5319: "Lago Sul",
    5320: "Gama",          5326: "Samambaia",       5328: "Santa Maria",
    5330: "São Sebastião",
}

ESCOLARIDADE = {1:"Sem instrução",2:"Fund. incompleto",3:"Fund. completo",
                4:"Médio incompleto",5:"Médio completo",6:"Superior incompleto",
                7:"Superior completo",8:"Pós-graduação"}

def bubble_sort_por_idade(lista):
    n = len(lista)
    for i in range(n):
        for j in range(n - i - 1):
            if lista[j]["idade"] > lista[j + 1]["idade"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def gerar_relatorio(ra_codigo):
    moradores = pd.read_csv("moradores_parcial.csv", sep=";", decimal=",", encoding="utf-8-sig")
    filtro = moradores[moradores["localidade"] == ra_codigo]

    if filtro.empty:
        print(f"Nenhum dado encontrado para a RA {ra_codigo}.")
        sys.exit(1)

    ra_nome = RA_NOMES.get(ra_codigo, f"RA-{ra_codigo}")
    validos = filtro[filtro["idade_calculada"] != 99999]
    idades = validos["idade_calculada"].tolist()

    lista_moradores = []
    for _, linha in validos.iterrows():
        lista_moradores.append({
            "id": linha["morador_id"],
            "idade": linha["idade_calculada"],
            "escolaridade": ESCOLARIDADE.get(linha["escolaridade"], "?"),
            "renda": linha["renda_ind"] if linha["renda_ind"] != 99999 else None,
        })
    lista_moradores = bubble_sort_por_idade(lista_moradores)

    linhas = []
    linhas.append("=" * 55)
    linhas.append(f"  PDAD 2024 — Análise da RA: {ra_nome} (cód. {ra_codigo})")
    linhas.append("=" * 55)
    linhas.append(f"  Total de moradores na amostra : {len(filtro)}")
    linhas.append(f"  Com idade declarada           : {len(validos)}")
    if idades:
        linhas.append(f"  Média de idade                : {sum(idades)/len(idades):.1f} anos")
        linhas.append(f"  Faixa etária                  : {min(idades)} a {max(idades)} anos")
    linhas.append("")
    linhas.append("  Moradores (ordenados por idade):")
    linhas.append("  " + "-" * 50)
    for m in lista_moradores:
        renda_str = f"R$ {m['renda']:,.0f}" if m["renda"] else "não declarada"
        linhas.append(f"  {m['id']:12s} | {m['idade']:3d} anos | {m['escolaridade']:25s} | {renda_str}")
    linhas.append("")
    return linhas, ra_nome

if len(sys.argv) < 2:
    print("Uso: python analise_ra.py <codigo_ra> [arquivo_saida.txt]")
    print("Exemplo: python analise_ra.py 5320")
    print("Exemplo: python analise_ra.py 5320 relatorio_gama.txt")
    sys.exit(1)

ra = int(sys.argv[1])
linhas, nome = gerar_relatorio(ra)

for linha in linhas:
    print(linha)

if len(sys.argv) >= 3:
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")
    print(f"\n  Relatório salvo em: {sys.argv[2]}")
```

**Como executar:**
```bash
# Só exibe na tela
python analise_ra.py 5320

# Exibe e salva em arquivo
python analise_ra.py 5320 relatorio_gama.txt

# Outra RA
python analise_ra.py 5330 relatorio_sao_sebastiao.txt
```
