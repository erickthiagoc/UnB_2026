# Exercícios — Python (cheatsheet vs C)

Códigos dos exercícios práticos, comentados de forma simples para quem está
começando a programar. Recomendo testar cada um em
<https://pythontutor.com/python-compiler.html> para ver passo a passo.

---

## Exercício 1 — Estrutura mínima

```python
print("Ola, mundo!")
```

---

## Exercício 2 — Tipos dinâmicos e identidade de objeto

```python
x = 42
print(type(x))      # mostra o tipo da variável

x = "agora sou str"  # a mesma variável agora guarda outra coisa
print(type(x))

a = 1000
b = 1000
print(a == b)       # compara se os valores são iguais
print(a is b)       # compara se são exatamente o mesmo objeto
```

---

## Exercício 3 — Reatribuição e listas compartilhadas

```python
a = [1, 2, 3]   # cria uma lista
b = a            # 'b' aponta para a mesma lista que 'a'
b.append(4)
print(a)         # [1, 2, 3, 4] -> 'a' também mudou

b = [9, 9]       # agora 'b' aponta para uma lista nova
print(a)         # continua [1, 2, 3, 4]
print(b)         # [9, 9]
```

---

## Exercício 4 — Divisão, módulo, ternário e `is`

```python
a, b = 17, 5

print(a / b)     # divisão normal (com casas decimais)
print(a // b)    # divisão inteira (descarta o resto)
print(a % b)     # resto da divisão

x = 3
x += 1           # soma 1 e guarda em x
print(x)

maximo = a if a > b else b   # forma resumida de if/else
print("max =", maximo)

p = [1, 2]
q = [1, 2]
print(p == q)    # True, mesmos valores
print(p is q)    # False, são listas diferentes
```

---

## Exercício 5a — if / elif / else

```python
nota = 72

if nota >= 90:
    print("A")
elif nota >= 80:
    print("B")
elif nota >= 70:
    print("C")
else:
    print("Reprovado")
```

---

## Exercício 5b — for, break, continue e else

```python
for i in range(10):
    if i % 2 == 0:
        continue        # pula os números pares
    if i == 7:
        break           # interrompe o laço ao chegar em 7
    print(i)
else:
    print("laço completo sem break")  # não roda, pois houve break

n = 1
while n < 32:
    print(n)
    n *= 2
```

---

## Exercício 5c — match / case

```python
dia = 3   # 1=Seg ... 7=Dom

match dia:
    case 1 | 2 | 3 | 4 | 5:
        print("Dia útil")
    case 6 | 7:
        print("Fim de semana")
    case _:
        print("Inválido")
```

---

## Exercício 6a — funções com argumentos mutáveis e imutáveis

```python
def dobra_int(x):
    x *= 2       # cria um novo valor, não muda o de fora
    print("dentro:", x)

v = 7
dobra_int(v)
print("fora:", v)   # continua 7

def dobra_lista(lst):
    for i in range(len(lst)):
        lst[i] *= 2   # aqui sim muda a lista original

nums = [1, 2, 3]
dobra_lista(nums)
print(nums)   # [2, 4, 6]
```

---

## Exercício 6b — recursão

```python
def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)

print(fatorial(5))   # 120
```

---

## Exercício 7 — listas e cópia

```python
v = [10, 20, 30, 40, 50]

soma = 0
for x in v:
    soma += x
print("soma =", soma)

a = [1, 2, 3]
b = a            # mesma lista
b.append(99)
print(a)         # [1, 2, 3, 99]

c = a.copy()     # cópia separada
c.append(0)
print(a)         # [1, 2, 3, 99] -> não muda
```

---

## Exercício 8 — strings

```python
s = "Brasilia"
print(f"Comprimento: {len(s)}")

for i, c in enumerate(s):
    print(f"s[{i}] = '{c}'  (ord={ord(c)})")

t = "Brasilia"
print(s == t)        # compara o conteúdo
print(s is t)        # compara se é o mesmo objeto

try:
    s[0] = 'b'       # strings não podem ser alteradas
except TypeError as e:
    print("Erro:", e)
```

---

## Exercício 9 — referências, identidade e cópia profunda

```python
import copy

original = [[1, 2], [3, 4]]
rasa = original.copy()     # copia só o nível de fora
rasa[0].append(99)
print(original)    # [[1, 2, 99], [3, 4]] -> sublista foi alterada também

original2 = [[1, 2], [3, 4]]
profunda = copy.deepcopy(original2)   # copia tudo, até as sublistas
profunda[0].append(99)
print(original2)   # [[1, 2], [3, 4]] -> não muda
```

---

## Exercício 10 — ciclo de vida dos objetos

```python
a = [10, 20, 30]
b = a
print(id(a), id(b))   # mesmo endereço de memória

b = None
print(a)           # [10, 20, 30] continua existindo

a = None            # agora ninguém mais aponta para a lista

c = [1, 2]
del c               # remove a variável
```

---

## Exercício 11 — classes

```python
class Complexo:
    def __init__(self, re, im):
        self.re = re
        self.im = im

    def modulo_sq(self):
        return self.re**2 + self.im**2

    def __repr__(self):
        return f"{self.re} + {self.im}i"

c1 = Complexo(3.0, 4.0)
c2 = c1              # c2 aponta para o mesmo objeto
c2.re = 0.0
print(c1)            # também mudou
print(c1.modulo_sq())
```

---

## Exercício 12 — enums

```python
from enum import Enum

class DiaSemana(Enum):
    DOM = 0
    SEG = 1
    TER = 2
    QUA = 3
    QUI = 4
    SEX = 5
    SAB = 6

def tipo_dia(d):
    match d:
        case DiaSemana.SAB | DiaSemana.DOM:
            return "Fim de semana"
        case _:
            return "Dia útil"

for d in DiaSemana:
    print(f"{d.name}: {tipo_dia(d)}")
```

---

## Exercício 13 — entrada e saída formatada

```python
i = 255
f = 3.14159
c = 'Z'
s = "Brasilia"

print(f"Decimal:     {i}")
print(f"Hexadecimal: {i:x}")
print(f"Float 2dec:  {f:.2f}")
print(f"Char:        {c}")
print(f"String:      {s}")
print(f"Endereco:    {id(s)}")
print(f"Unicode ord: {ord(c)}")
```

---

## Exercício 14 — módulo math

```python
import math

PI = math.pi
R = 5.0

area = PI * R ** 2
print(f"Área do círculo r=5: {area:.2f}")

def quadrado(x):
    return x * x

print(f"quadrado(7+1) = {quadrado(7+1)}")

print(f"10! = {math.factorial(10)}")
```

---

## Exercício 15a — escopo (LEGB) e nonlocal

```python
def make_contador():
    n = 0

    def contador():
        nonlocal n     # avisa que 'n' não é local, é da função de fora
        n += 1
        print(f"chamada número {n}")

    return contador

c = make_contador()
c()   # 1
c()   # 2
c()   # 3
```

---

## Exercício 15b — global vs local

```python
contador = 0           # variável global

def incrementa():
    global contador    # avisa que vai usar a variável global, não criar uma nova
    contador += 1

incrementa()
incrementa()
incrementa()
print(contador)        # 3
```

---

## Exercício 16 — tuplas imutáveis e tratamento de erro

```python
PRIMOS = (2, 3, 5, 7, 11, 13)   # tupla: parecida com lista, mas não muda depois
print(PRIMOS[0])

try:
    PRIMOS[0] = 99    # vai dar erro, pois tupla não pode ser alterada
except TypeError as e:
    print("Imutável:", e)

linhas = ["linha 1\n", "linha 2\n", "linha 3\n"]
for linha in linhas:
    print(linha.strip())   # strip() remove espaços e quebras de linha extras
```
