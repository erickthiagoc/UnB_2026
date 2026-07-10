# Exercícios — C (cheatsheet com pythontutor.com)

Códigos dos exercícios práticos de C. Recomendo testar cada um em
<https://pythontutor.com/c.html> para acompanhar a stack e o heap passo a passo.

---

## Exercício 1 — Olá, mundo com retorno

```c
#include <stdio.h>

int main(void) {
    printf("Ola, mundo!\n");
    return 0;   // 0 indica que o programa terminou sem erro
}
```

---

## Exercício 2 — Inspecionando tamanhos

```c
#include <stdio.h>

int main(void) {
    printf("char:   %zu byte(s)\n", sizeof(char));
    printf("int:    %zu byte(s)\n", sizeof(int));
    printf("long:   %zu byte(s)\n", sizeof(long));
    printf("float:  %zu byte(s)\n", sizeof(float));
    printf("double: %zu byte(s)\n", sizeof(double));
    return 0;
}
```

---

## Exercício 3 — Variável não inicializada vs. inicializada

```c
#include <stdio.h>

int main(void) {
    int a = 42;
    int b;          // valor lixo, não usar antes de atribuir
    b = a + 8;
    printf("a = %d\n", a);
    printf("b = %d\n", b);

    const int N = 100;   // constante, não pode ser alterada depois
    printf("N = %d\n", N);
    return 0;
}
```

---

## Exercício 4 — Divisão inteira, módulo e incremento

```c
#include <stdio.h>

int main(void) {
    int a = 17, b = 5;

    printf("%d / %d = %d\n", a, b, a / b);   // divisão inteira
    printf("%d %% %d = %d\n", a, b, a % b);  // resto da divisão

    int x = 3;
    int pre  = ++x;   // primeiro soma, depois usa: x fica 4, pre = 4
    int pos  = x++;   // primeiro usa, depois soma: pos = 4, x fica 5
    printf("pre=%d  pos=%d  x=%d\n", pre, pos, x);

    int max = (a > b) ? a : b;   // forma resumida de if/else
    printf("max(%d,%d) = %d\n", a, b, max);
    return 0;
}
```

---

## Exercício 5a — if / else if / else

```c
#include <stdio.h>

int main(void) {
    int nota = 72;

    if      (nota >= 90) printf("A\n");
    else if (nota >= 80) printf("B\n");
    else if (nota >= 70) printf("C\n");
    else                 printf("Reprovado\n");

    return 0;
}
```

---

## Exercício 5b — for com break e continue

```c
#include <stdio.h>

int main(void) {
    for (int i = 0; i < 10; i++) {
        if (i % 2 == 0) continue; // pula os números pares
        if (i == 7)     break;    // interrompe o laço ao chegar em 7
        printf("%d\n", i);
    }
    return 0;
}
```

---

## Exercício 5c — do-while

```c
#include <stdio.h>

int main(void) {
    int n = 1;
    do {
        printf("n = %d\n", n);
        n *= 2;
    } while (n < 32);
    return 0;
}
```

---

## Exercício 5d — switch com fall-through

```c
#include <stdio.h>

int main(void) {
    int dia = 3;   // 1=Seg ... 7=Dom

    switch (dia) {
        case 1: case 2: case 3: case 4: case 5:
            printf("Dia util\n");
            break;
        case 6: case 7:
            printf("Fim de semana\n");
            break;
        default:
            printf("Invalido\n");
    }
    return 0;
}
```

---

## Exercício 6 — Pilha de chamadas em ação

```c
#include <stdio.h>

int fatorial(int n) {
    if (n <= 1) return 1;
    return n * fatorial(n - 1);   // chamada recursiva
}

void dobra(int *x) { *x *= 2; }   // recebe o endereço para poder alterar o valor original

int main(void) {
    int f = fatorial(5);
    printf("5! = %d\n", f);

    int v = 7;
    dobra(&v);
    printf("dobro de 7 = %d\n", v);
    return 0;
}
```

---

## Exercício 7 — Array unidimensional e matriz

```c
#include <stdio.h>

int main(void) {
    int v[5] = {10, 20, 30, 40, 50};

    // soma dos elementos
    int soma = 0;
    for (int i = 0; i < 5; i++)
        soma += v[i];
    printf("soma = %d\n", soma);

    // matriz 2x3
    int m[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("m[1][2] = %d\n", m[1][2]);   // 6
    return 0;
}
```

---

## Exercício 8 — Percorrendo uma string caractere a caractere

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "Brasilia";
    int  len = strlen(s);

    printf("Comprimento: %d\n", len);

    for (int i = 0; i < len; i++)
        printf("s[%d] = '%c'  (ASCII %d)\n", i, s[i], s[i]);

    char t[] = "Brasilia";
    printf("strcmp: %d\n", strcmp(s, t));   // 0 significa que são iguais
    return 0;
}
```

---

## Exercício 9a — Ponteiro básico e derreferência

```c
#include <stdio.h>

int main(void) {
    int x = 10;
    int *p = &x;   // p guarda o endereço de x

    printf("x    = %d\n",  x);
    printf("&x   = %p\n",  (void*)&x);
    printf("p    = %p\n",  (void*)p);
    printf("*p   = %d\n",  *p);   // *p acessa o valor guardado no endereço

    *p = 99;   // altera x através do ponteiro
    printf("x apos *p=99: %d\n", x);
    return 0;
}
```

---

## Exercício 9b — Aritmética de ponteiros

```c
#include <stdio.h>

int main(void) {
    int v[4] = {10, 20, 30, 40};
    int *p = v;   // p aponta para v[0]

    printf("*p      = %d\n", *p);       // 10
    printf("*(p+1)  = %d\n", *(p+1));   // 20
    printf("*(p+2)  = %d\n", *(p+2));   // 30

    p++;   // agora aponta para v[1]
    printf("apos p++: *p = %d\n", *p);  // 20
    return 0;
}
```

---

## Exercício 9c — Ponteiro para ponteiro

```c
#include <stdio.h>

int main(void) {
    int  x  = 42;
    int *p  = &x;
    int **pp = &p;   // guarda o endereço do próprio ponteiro

    printf("x   = %d\n",   x);
    printf("*p  = %d\n",  *p);
    printf("**pp= %d\n", **pp);

    **pp = 100;   // altera x passando por dois níveis de indireção
    printf("x apos **pp=100: %d\n", x);
    return 0;
}
```

---

## Exercício 10 — Heap vs. Stack

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 4;
    int *v = malloc(n * sizeof(int));   // reserva espaço no heap

    for (int i = 0; i < n; i++)
        v[i] = (i + 1) * 10;            // 10 20 30 40

    for (int i = 0; i < n; i++)
        printf("v[%d] = %d\n", i, v[i]);

    free(v);    // devolve a memória ao sistema
    v = NULL;   // evita usar o ponteiro por acidente depois do free
    return 0;
}
```

---

## Exercício 11a — Struct com acesso direto e via ponteiro

```c
#include <stdio.h>

typedef struct {
    int x;
    int y;
} Ponto;

float distancia(Ponto *a, Ponto *b) {
    int dx = a->x - b->x;
    int dy = a->y - b->y;
    return (float)(dx*dx + dy*dy);   // sem raiz quadrada, só para simplificar
}

int main(void) {
    Ponto origem = {0, 0};
    Ponto p      = {3, 4};

    printf("p.x=%d  p.y=%d\n", p.x, p.y);

    Ponto *ptr = &p;
    ptr->x = 10;   // -> acessa o campo através do ponteiro
    printf("apos ptr->x=10: p.x=%d\n", p.x);

    printf("dist^2(origem,p) = %.0f\n", distancia(&origem, &p));
    return 0;
}
```

---

## Exercício 11b — Union: membros compartilham memória

```c
#include <stdio.h>

union Dado {
    int   i;
    float f;
    char  c;
};

int main(void) {
    union Dado d;
    d.i = 65;
    printf("d.i = %d\n",   d.i);
    printf("d.c = '%c'\n", d.c);   // mesmos bytes, interpretados como char

    d.f = 3.14f;
    printf("d.f = %.2f\n", d.f);
    // d.i agora tem valor indefinido, pois foi sobrescrito por d.f
    return 0;
}
```

---

## Exercício 12 — Enum com switch

```c
#include <stdio.h>

typedef enum { DOM=0, SEG, TER, QUA, QUI, SEX, SAB } DiaSemana;

const char *nome_dia(DiaSemana d) {
    switch (d) {
        case DOM: return "Domingo";
        case SEG: return "Segunda";
        case TER: return "Terca";
        case QUA: return "Quarta";
        case QUI: return "Quinta";
        case SEX: return "Sexta";
        case SAB: return "Sabado";
        default:  return "???";
    }
}

int main(void) {
    for (DiaSemana d = DOM; d <= SAB; d++)
        printf("%d = %s\n", d, nome_dia(d));
    return 0;
}
```

---

## Exercício 13 — Formatação de saída

```c
#include <stdio.h>

int main(void) {
    int    i = 255;
    float  f = 3.14159f;
    char   c = 'Z';
    char   s[] = "Brasilia";

    printf("Decimal:     %d\n",   i);
    printf("Hexadecimal: %x\n",   i);    // ff
    printf("Float 2dec:  %.2f\n", f);
    printf("Char:        %c\n",   c);
    printf("String:      %s\n",   s);
    printf("Ponteiro:    %p\n",   (void*)s);
    return 0;
}
```

---

## Exercício 14 — Constante e macro com parâmetro

```c
#include <stdio.h>

#define PI        3.14159
#define QUADRADO(x) ((x)*(x))
#define MAX(a,b)  ((a)>(b)?(a):(b))

int main(void) {
    double r = 5.0;
    printf("Area do circulo r=5: %.2f\n", PI * QUADRADO(r));

    int a = 7, b = 3;
    printf("MAX(%d,%d) = %d\n", a, b, MAX(a,b));

    // armadilha clássica: sem parênteses, a macro expande errado
    printf("QUADRADO(a+1) = %d\n", QUADRADO(a+1));   // (a+1)*(a+1) = 64
    return 0;
}
```

---

## Exercício 15a — Escopo de bloco

```c
#include <stdio.h>

int main(void) {
    int x = 1;
    printf("x externo = %d\n", x);

    {
        int x = 2;   // variável nova, só existe dentro deste bloco
        printf("x interno = %d\n", x);
    }

    printf("x externo apos bloco = %d\n", x);   // ainda 1
    return 0;
}
```

---

## Exercício 15b — Variável static local

```c
#include <stdio.h>

void contador(void) {
    static int n = 0;   // inicializa só uma vez, e o valor persiste entre chamadas
    n++;
    printf("chamada numero %d\n", n);
}

int main(void) {
    contador();   // 1
    contador();   // 2
    contador();   // 3
    return 0;
}
```

---

## Exercício 16 — Evitando estouro de buffer

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char destino[8];

    // strncpy limita a cópia ao tamanho do buffer, evitando overflow
    strncpy(destino, "Brasilia-DF", sizeof(destino) - 1);
    destino[sizeof(destino) - 1] = '\0';   // garante que termina corretamente

    printf("destino = '%s'\n", destino);
    printf("strlen  = %zu\n",  strlen(destino));
    return 0;
}
```
