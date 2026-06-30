---
title: "Exercícios de Programação com Microdados do PDAD 2024"
subtitle: "Distrito Federal — Algoritmos e Programação de Computadores"
author: "Erick Araujo"
    toc: true
    toc-depth: 3
---

## Sobre este repositório

Este repositório guarda os exercícios que venho desenvolvendo na disciplina de Algoritmos e Programação de Computadores, usando como base os microdados da PDAD-A 2024 (Pesquisa Distrital por Amostra de Domicílios Ampliada), do IPEDF.

A ideia da disciplina foi sair do exemplo genérico de sala de aula e trabalhar com um dataset real do Distrito Federal — então, em vez de listas soltas de números, os exercícios usam dados de domicílios e moradores das RAs. Isso ajuda a fixar tanto a parte de programação (leitura de dados, filtros, dicionários, ordenação) quanto a de entender o que cada variável realmente significa antes de sair calculando qualquer coisa.

## Sobre os dados

A PDAD é feita pelo IPEDF (Instituto de Pesquisa e Estatística do Distrito Federal) para traçar o perfil socioeconômico da população do DF. A edição de 2024 é a PDAD-A (Ampliada), porque foi a primeira a incluir áreas rurais e os 12 municípios da Periferia Metropolitana de Brasília. No total a pesquisa visitou cerca de 25 mil domicílios espalhados pelas 35 Regiões Administrativas.

Os microdados completos e o dicionário de variáveis são públicos e estão em:

> <https://pdad.ipe.df.gov.br>

Os arquivos usados aqui são amostras parciais desses dados, recortadas para os exercícios da disciplina — não o dataset completo.

### Arquivos

| Arquivo | O que é |
|---|---|
| `moradores_parcial.csv` | um registro por pessoa entrevistada (separador `;`, decimal `,`, 134 colunas) |
| `domicilios_parcial.xlsx` | um registro por domicílio visitado |
| `dicionario_de_variaveis_pdad_2024.xlsx` | descrição de cada coluna das duas tabelas |

Os arquivos de dados não estão versionados aqui no repositório. Quem quiser reproduzir os exercícios precisa baixar os microdados completos no site do IPEDF (ou pedir as amostras parciais usadas em aula).

### Como as duas tabelas se relacionam

domicílios e moradores são tabelas separadas, ligadas pela coluna `A01nficha` (número da ficha do domicílio): cada domicílio pode ter vários moradores, mas cada morador pertence a só um domicílio. Cruzar as duas é uma junção (join) — no pandas isso é o `pd.merge()`.

### Blocos do questionário

As colunas seguem a estrutura do questionário de campo, organizadas por letra:

Domicílios:

| Bloco | Letra | Temas |
|---|---|---|
| Identificação | A | ficha, UF, localidade, setor, contagem de moradores |
| Domicílio | B | tipo de imóvel, posse, aluguel, infraestrutura |
| Equipamentos | C | eletrodomésticos, veículos, internet |
| Saneamento | D | coleta de lixo, abastecimento de água |
| Renda domiciliar | — | renda total, per capita, deflacionada (derivadas) |

Moradores:

| Bloco | Letra | Temas |
|---|---|---|
| Identificação | A | ficha, localidade, id do morador |
| Composição | E | idade, gênero, cor/raça, naturalidade, religião, deficiência |
| Migração | F | naturalidade, tempo de residência no DF |
| Saúde | G | plano de saúde, uso de serviços |
| Educação | H | frequência escolar, escolaridade, curso atual |
| Trabalho e renda | I | ocupação, setor, renda individual |
| Derivadas | — | `renda_ind`, `escolaridade`, `id_genero`, `lgbtqiam`, `peso_mor` |

### Valores ausentes

Os dados não usam NA, usam dois códigos sentinela que precisam ser filtrados antes de qualquer conta:

- `99999` — não se aplica (a pergunta não era válida pra aquela pessoa/domicílio)
- `88888` — não declarado / recusou responder

Esse é provavelmente o erro mais comum no começo: calcular média de idade ou renda sem tirar esses valores antes.

### Peso amostral

As colunas `peso_mor` e `peso_dom` trazem o peso amostral de cada registro — quanto cada entrevistado representa na população real do DF. Nos exercícios deste repositório eu não uso o peso, trabalho só com contagens da amostra mesmo, mas é importante saber que ele existe (estimativas oficiais de população precisam multiplicar por ele).

### RAs presentes na amostra

| Código | RA | Observação |
|---|---|---|
| 5249 | Arniqueira | RA mais nova, criada em 2019 |
| 5314 | Sobradinho II | região satélite ao norte |
| 5315 | Jardim Botânico | área de alta renda ao leste |
| 5319 | Lago Sul | uma das RAs de maior renda do DF |
| 5320 | Gama | uma das cidades-satélite mais antigas |
| 5326 | Samambaia | segunda maior população do DF |
| 5330 | São Sebastião | crescimento acelerado nas últimas décadas |

## Estrutura dos exercícios

Os exercícios seguem quatro níveis de dificuldade:

- Nível 1 — trivial: leitura e exibição de dados
- Nível 2 — básico: filtragem e cálculos simples
- Nível 3 — intermediário: algoritmos de ordenação implementados à mão
- Nível 4 — avançado: relatórios completos via linha de comando

| # | Nível | Conceito principal | Algoritmo |
|---|---|---|---|
| 1.1 | trivial | leitura de CSV | — |
| 1.2 | trivial | seleção de colunas | — |
| 1.3 | trivial | leitura de Excel | — |
| 1.4 | trivial | filtragem + valores especiais | — |
| 2.1 | básico | média aritmética manual | soma acumulada |
| 2.2 | básico | contagem com dicionário | varredura linear |
| 2.3 | básico | filtro por RA | busca linear |
| 2.4 | básico | múltiplas condições | — |
| 3.1 | intermediário | ordenação por idade | bubble sort |
| 3.2 | intermediário | ordenação por renda | selection sort |
| 3.3 | intermediário | ordenação alfabética | insertion sort |
| 3.4 | intermediário | análise de complexidade | os três juntos |
| 4.1 | avançado | relatório TXT + CLI | insertion sort |
| 4.2 | avançado | menu interativo | — |
| 4.3 | avançado | programa completo por RA | bubble sort |

Cada exercício tem um objetivo, o que dá pra aprender com ele, um código de partida já comentado e uma tarefa pra estender esse código.

## Rodando os exercícios

Precisa de Python 3.10+ e:

```bash
pip install pandas openpyxl
```

(o `openpyxl` é só pra ler os `.xlsx` com `pd.read_excel`)

Passo a passo:

1. Baixar os microdados em <https://pdad.ipe.df.gov.br> (ou usar as amostras parciais passadas em aula) e colocar `moradores_parcial.csv`, `domicilios_parcial.xlsx` e `dicionario_de_variaveis_pdad_2024.xlsx` na raiz do repositório.
2. Dar uma olhada no dicionário de variáveis antes de programar — vale a pena entender o que cada coluna significa antes de sair filtrando.
3. Rodar os scripts dos níveis 1 a 3 normalmente:

   ```bash
   python exercicio_1_1.py
   ```

4. Os exercícios do nível 4 recebem argumentos por linha de comando:

   ```bash
   python relatorio_moradores.py relatorio_moradores.txt
   python analise_ra.py 5320 relatorio_gama.txt
   ```

## Organização do repositório

```
.
├── README.qmd
├── Exercicios_pdad2024__primeira_etapa_.md
├── moradores_parcial.csv          (não versionado, baixar separadamente)
├── domicilios_parcial.xlsx        (não versionado, baixar separadamente)
├── dicionario_de_variaveis_pdad_2024.xlsx
└── solucoes/
    ├── nivel1/
    ├── nivel2/
    ├── nivel3/
    └── nivel4/
```

## O que fui praticando aqui

- leitura e manipulação de dados com pandas (`read_csv`, `read_excel`)
- filtragem booleana e tratamento de valores ausentes/sentinela
- listas, dicionários e listas de dicionários
- implementação manual de bubble sort, selection sort e insertion sort
- comparação empírica de complexidade entre os algoritmos
- programas de linha de comando com `sys.argv` e `input()`
- escrita de relatórios em arquivo `.txt`
- junção de tabelas relacionadas por chave em comum

## Fonte dos dados

Pesquisa Distrital por Amostra de Domicílios Ampliada (PDAD-A 2024) — IPEDF: <https://pdad.ipe.df.gov.br>
