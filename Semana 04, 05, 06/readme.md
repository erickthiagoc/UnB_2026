# Mago Coletor (Meu Primeiro Jogo em JS)

Bem-vindo ao repositório do meu jogo em JavaScript 2D! Este projeto foi desenvolvido para praticar lógica de programação, controle de estados, colisões e sistema de coordenadas.

**[CLIQUE AQUI PARA JOGAR NO NAVEGADOR] (Cole_aqui_seu_link_do_Code_org)**

## Sobre o Jogo
Neste jogo de sobrevivência e agilidade, você controla um mago que precisa coletar o máximo de moedas possível enquanto desvia de inimigos. Se o mago tocar no inimigo 3 vezes, é Game Over!

## Controles
* **Seta para Cima (⬆️):** Move o mago para cima.
* **Seta para Baixo (⬇️):** Move o mago para baixo.
* **Seta para a Esquerda (⬅️):** Move o mago para a esquerda.
* **Seta para a Direita (➡️):** Move o mago para a direita.

## Funcionalidades e Aprendizados
Durante o desenvolvimento deste projeto, apliquei diversos conceitos fundamentais de programação:
* **Variáveis de Estado:** Controle de vidas e pontuação.
* **Funções:** Modularização do código (ex: `moverJogador()`, `baterNoInimigo()`, `coletarMoeda()`) para manter o loop principal (`draw`) limpo.
* **Estruturas Condicionais (If/Else):** Para gerenciar a mudança de cenários entre o "Nível 1" e a tela de "Game Over".
* **Colisões (Hitboxes):** Uso da propriedade `isTouching()` combinada com colisores circulares e retangulares.
* **Geração Aleatória:** Uso de `randomNumber()` para fazer as moedas e inimigos reaparecerem em locais dinâmicos.

## Tecnologias Utilizadas
* **JavaScript:** Lógica principal do jogo.
* **Code.org Game Lab:** Ambiente de desenvolvimento baseado na biblioteca *p5.play*.

---
*Projeto criado como parte dos meus estudos contínuos em lógica de programação e desenvolvimento de software.*
