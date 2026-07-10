## Código Little Man Computer (LMC)

Este projeto inclui uma rotina desenvolvida para o Little Man Computer (LMC). O objetivo deste algoritmo é receber um número do usuário e imprimir uma contagem sequencial a partir de zero até esse número.

Seja $N$ o valor de entrada inserido pelo usuário e $C$ o valor do contador (CONT), onde o estado inicial é $C = 0$.
1. O limite da execução é definido como $L = N + 1$.
2. Durante o ciclo (loop), o programa imprime o valor atual de $C$ e o incrementa logicamente: $C = C + 1$.
3. A condição de parada (branch) avalia a inequação matemática: $C - L \ge 0$.
4. Substituindo a variável $L$, sabemos que o programa é interrompido se $C \ge N + 1$.
5. O resultado final gerado é a impressão do conjunto de números inteiros: $\{0, 1, 2, \dots, N\}$.

### Código Fonte

```assembly
        INP
        ADD UM
        STA LIMITE
LOOP    LDA CONT
        OUT
        ADD UM
        STA CONT
        SUB LIMITE
        BRP FIM
        BRA LOOP
FIM     HLT
CONT    DAT 0
LIMITE  DAT 0
UM      DAT 1
