---
title: "Cheatsheet Semântico: Python vs C"
subtitle: "Comparando os dois modelos de memória direto no PythonTutor"
author: "Erick Araujo"
date: last-modified
    toc: true
    toc-depth: 3
---

## Sobre este repositório

Esse material surgiu de uma necessidade bem prática: depois de ver C na disciplina, comecei a usar Python no dia a dia (estatística, pandas, scripts) e fui sentindo falta de entender de verdade por que certas coisas se comportam diferente — por que uma função muda uma lista por fora mas não muda um número, por que `==` e `is` não são a mesma coisa, esse tipo de coisa.

Então fui montando essa cheatsheet espelhando ponto a ponto os tópicos da cheatsheet de C que já tinha da disciplina, mas explicando o lado Python sempre em cima do modelo de memória — não só "qual é a sintaxe equivalente", mas o porquê da diferença (caixa de memória fixa vs. etiqueta apontando pra objeto no heap).

A forma de estudar que mais funcionou pra mim foi colar cada trecho de código no PythonTutor (<https://pythontutor.com/python-compiler.html>) e ir passo a passo com Next/Prev vendo o que acontece no heap. Recomendo fazer o mesmo em vez de só ler.

## A diferença que explica quase tudo

Em C, uma variável é uma caixa de memória de tamanho fixo. Em Python, uma variável é uma etiqueta colada num objeto — o objeto que existe no heap, não a variável. Isso muda o raciocínio sobre tipos, cópia, mutabilidade, passagem de parâmetro, tudo.

| C | Python |
|---|---|
| variável é uma caixa de memória com tamanho fixo | variável é uma etiqueta (referência) colada em um objeto |
| `int x = 10` reserva 4 bytes e coloca 10 lá | `x = 10` cria o objeto `10` no heap e faz `x` apontar pra ele |
| tipo é da variável (estático) | tipo é do objeto (dinâmico) |
| memória gerenciada manualmente (`malloc`/`free`) | memória gerenciada pelo garbage collector (contagem de referências + GC cíclico) |
| `==` compara valores | `==` compara valores; `is` compara identidade (mesmo objeto) |

Praticamente todo o resto do material é essa ideia se repetindo em contextos diferentes.

## Como usar

Cada seção segue o mesmo formato: explico o que muda de C pra Python, mostro o trecho equivalente comentado, e no final tem um exercício pra colar no PythonTutor e observar o comportamento (geralmente é o que está escrito em "o que observar" depois do código).

```
acesse https://pythontutor.com/python-compiler.html
cole o código do exercício
clique em "Visualize Execution"
use Next/Prev pra acompanhar passo a passo
```

## Tópicos cobertos

1. Estrutura de um programa — sem `main` obrigatório, módulo de topo executado direto, `if __name__ == "__main__"`
2. Tipos e o modelo de objetos — tipo pertence ao objeto, não à variável; `int` sem tamanho fixo
3. Declaração e atribuição — não existe declarar sem valor; toda atribuição é um binding nome→objeto
4. Operadores — `/` sempre float, `//` pra divisão inteira, `and`/`or`/`not`, `is` vs `==`
5. Controle de fluxo — indentação no lugar de chaves, `match`/`case`, `else` em laços
6. Funções — passagem por referência de objeto, mutável vs imutável, lambda
7. Listas — array dinâmico e heterogêneo, slicing, aliasing vs cópia
8. Strings — imutáveis, sem `\0`, métodos no lugar das funções de `string.h`
9. Referências — sem ponteiro explícito, `id()` como o `%p` do C, shallow vs deep copy
10. Gerenciamento de memória — garbage collector no lugar de `malloc`/`free`, geradores
11. Classes — equivalente de `struct`, `self` como o `this` implícito, dataclass/namedtuple
12. Enums — `enum.Enum` como classe real, não açúcar sintático sobre `int`
13. Entrada e saída — f-strings no lugar de `printf`, `input()` sempre retorna `str`
14. Módulos — `import` em tempo de execução no lugar de `#include`/`#define`
15. Escopo e duração — regra LEGB, `nonlocal` como equivalente de `static` local
16. Boas práticas — equivalentes Python pra hábitos de C (`with`, `tuple`, `mypy`, etc.)

Cada um desses tópicos termina com pelo menos um exercício pra rodar no PythonTutor.

## Por que isso importa na prática

Algumas das coisas que mais me ajudaram a entender depois de rodar no PythonTutor:

- Um inteiro se comporta "por valor" dentro de uma função porque é imutável — qualquer operação cria um objeto novo. Uma lista se comporta "por referência" porque é mutável e a função recebe a mesma etiqueta apontando pro mesmo objeto. Não é a linguagem que muda, é o objeto.
- `a == b` compara valor, `a is b` compara se é o mesmo objeto no heap. Dois inteiros iguais podem não ser o mesmo objeto.
- `b = a` numa lista não copia nada, só cria uma segunda etiqueta pro mesmo objeto. Pra copiar de verdade precisa de `.copy()` (cópia rasa) ou `copy.deepcopy()` (cópia de toda a árvore).
- `sys.getsizeof(42)` dá algo perto de 28 bytes, não 4, porque todo objeto Python carrega metadados (contagem de referências, ponteiro pro tipo, etc.) além do valor em si.
- `for i in range(5): pass` deixa `i` vivo depois do laço — em Python `for`/`if` não criam escopo novo, diferente de C.

## Resumo comparativo

| Conceito C | Python | Diferença-chave |
|---|---|---|
| `int x = 10` | `x = 10` | Python: etiqueta apontando pra objeto; C: caixa com bytes |
| `int *p = &x` | `p = x` (objetos mutáveis) | referência implícita |
| `*p = 20` | `p[0] = 20` (lista) | sem derreferência explícita |
| `malloc`/`free` | automático (GC) | sem gestão manual de memória |
| `struct` | `class`, `@dataclass`, `namedtuple` | dados + comportamento |
| `char[]` mutável | `bytearray` | `str` é imutável |
| `#include` | `import` | acontece em tempo de execução |
| `#define MAX(a,b)` | função `def MAX(a,b)` | sem armadilha de expansão textual |
| escopo de bloco `{}` | escopo de função (LEGB) | `for`/`if` não criam escopo |
| `static` local | `nonlocal` + closure | closure substitui variável estática local |

## O que fui praticando aqui

- diferença entre modelo de "caixa" (C) e modelo de "etiqueta/objeto" (Python)
- mutabilidade como o que define se uma função altera o que foi passado
- `is` vs `==`, identidade vs igualdade
- slicing, list comprehension, geradores
- classes como equivalente de struct + comportamento, `self` vs `this`
- escopo LEGB e `nonlocal` como substituto de `static` local em C
- leitura de objetos no heap com `id()` e visualização passo a passo no PythonTutor

## Fonte

Espelha a cheatsheet de C usada na disciplina, com os exemplos rodados e confirmados no PythonTutor (<https://pythontutor.com/python-compiler.html>).
