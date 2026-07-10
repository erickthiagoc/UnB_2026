# Atividade Semanal — Algoritmos de Ordenação

**Disciplina:** Algoritmos e Programação de Computadores (APC) — UnB/CIC
**Autor:** Erick Thiago Cardoso Araujo
**Tema da semana:** Bubble Sort, Selection Sort e Insertion Sort

---

## O que foi pedido nesta semana

A atividade consistiu em visitar três páginas com visualizações interativas de
algoritmos de ordenação, ganhar intuição sobre como funcionam os três
algoritmos (Bubble Sort, Selection Sort e Insertion Sort) e executar os
exercícios prontos disponíveis nessas ferramentas. A PDAD 2024 é a base de
dados de referência da disciplina; os algoritmos de ordenação são a ferramenta
que, mais adiante, permitirá organizar recortes desses dados (por exemplo,
ordenar Regiões Administrativas por algum indicador).

Páginas visitadas:

- VisuAlgo — Sorting: https://visualgo.net/en/sorting
- USF — Comparison Sorting Visualization: https://www.cs.usfca.edu/~galles/visualization/ComparisonSort.html
- Toptal — Sorting Algorithms: https://www.toptal.com/developers/sorting-algorithms

---

## O problema da ordenação

Ordenar é reorganizar os itens de uma lista segundo algum critério (crescente,
decrescente, alfabético, etc.). É um dos problemas mais clássicos da Computação
e costuma ser usado para introduzir várias ideias de algoritmos. Os três
algoritmos desta semana — Bubble, Selection e Insertion — são chamados de
**baseados em comparação**, porque funcionam comparando pares de elementos e
decidindo se devem trocá-los de lugar. São os mais fáceis de entender e
implementar, mas não os mais eficientes: os três rodam em tempo O(N²) no pior
caso.

---

## Os três algoritmos

### Bubble Sort (ordenação por flutuação)

Percorre a lista repetidamente comparando cada par de elementos vizinhos e
trocando-os quando estão fora de ordem. A cada passagem completa, o maior valor
ainda não posicionado "flutua" até o fim da lista — daí o nome. O processo se
repete até que uma passagem inteira ocorra sem nenhuma troca, o que indica que
a lista já está ordenada.

- **Intuição:** os maiores valores vão sendo empurrados para o final, um por vez.
- **Complexidade:** O(N²) no caso médio e no pior caso; O(N) no melhor caso
  (lista já ordenada), se houver a otimização que interrompe quando não há trocas.
- **Estável:** sim (não altera a ordem relativa de elementos iguais).

### Selection Sort (ordenação por seleção)

Divide a lista em duas partes: a parte já ordenada (no início) e a parte ainda
desordenada. A cada rodada, procura o menor valor da parte desordenada e o
coloca no fim da parte ordenada, por meio de uma troca. Repete até que toda a
lista esteja ordenada.

- **Intuição:** é como o oposto do Bubble — em vez de empurrar os maiores para o
  fim, ele seleciona o menor valor a cada rodada e o traz para a frente.
- **Complexidade:** O(N²) em todos os casos, inclusive no melhor — porque ele
  sempre percorre toda a parte desordenada procurando o mínimo, mesmo que a lista
  já esteja ordenada.
- **Estável:** não, na sua forma clássica.

### Insertion Sort (ordenação por inserção)

Também trata a lista como duas partes (ordenada e desordenada). Pega o próximo
elemento da parte desordenada e o insere na posição correta dentro da parte já
ordenada, deslocando os maiores para a direita para abrir espaço. É parecido com
a forma como uma pessoa organiza cartas na mão.

- **Intuição:** vai construindo a parte ordenada um elemento por vez, encaixando
  cada novo valor no lugar certo.
- **Complexidade:** O(N²) no caso médio e no pior caso; O(N) no melhor caso
  (lista quase ordenada), o que o torna eficiente para listas pequenas ou já
  próximas da ordem.
- **Estável:** sim.

---

## Comparação rápida

| Algoritmo | Melhor caso | Caso médio | Pior caso | Estável? |
|---|---|---|---|---|
| Bubble Sort | O(N) | O(N²) | O(N²) | Sim |
| Selection Sort | O(N²) | O(N²) | O(N²) | Não |
| Insertion Sort | O(N) | O(N²) | O(N²) | Sim |

Observação: apesar de os três serem O(N²) no caso médio, isso não conta a
história toda. Para listas pequenas ou quase ordenadas, o Insertion Sort tende a
se sair melhor na prática. O Selection Sort é o único que não melhora quando a
lista já está ordenada, porque sempre varre toda a parte desordenada em busca do
mínimo.

---

## O que foi feito nesta semana

- Visitei as três páginas indicadas e acompanhei as animações passo a passo de
  cada algoritmo, observando como os elementos são comparados e trocados.
- Executei os exercícios prontos das ferramentas (arrays de exemplo), observando
  o número de comparações e de trocas em cada algoritmo e como isso muda conforme
  a lista inicial está mais ou menos ordenada.
- Registrei a intuição de cada algoritmo e as diferenças de complexidade e
  estabilidade resumidas acima.

---

## O que aprendi

- Os três algoritmos resolvem o mesmo problema, mas com estratégias diferentes:
  Bubble empurra os maiores para o fim; Selection puxa o menor para a frente;
  Insertion encaixa cada elemento no lugar certo da parte já ordenada.
- A notação Big-O (O(N²)) sozinha não distingue bem os três no caso médio; é
  preciso olhar também o melhor caso e a estabilidade para entender quando cada
  um se comporta melhor.
- Visualizar a execução ajuda a perceber por que o Selection Sort não se
  beneficia de uma lista já ordenada, enquanto Bubble e Insertion sim.

---

*APC — UnB/CIC — Atividade semanal sobre algoritmos de ordenação*
