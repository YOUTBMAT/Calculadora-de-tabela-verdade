# 📑 Calculadora de Tabela Verdade

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Linguagem Principal">
  <img src="https://img.shields.io/github/repo-size/YOUTBMAT/Calculadora-de-tabela-verdade?color=blue&style=for-the-badge" alt="Tamanho do Repositório">
</p>

## 📌 Sobre o Projeto

Este projeto consiste em uma **Calculadora de Tabela Verdade** desenvolvida em Python. A aplicação automatiza o processo de análise lógica de proposições, gerando tabelas completas a partir de expressões lógicas informadas, mapeando todas as combinações possíveis de valores lógicos para as variáveis envolvidas.

Esta ferramenta é extremamente útil para estudantes de Ciência da Computação e Engenharia que lidam com disciplinas como **Raciocínio Algorítmico, Matemática Discreta e Circuitos Digitais**.

### 🧠 Conceitos e Operações Suportadas:
O script é capaz de processar os principais conectivos da lógica proposicional:
- **Negação ($\neg$ ou `NOT`)** — Inverte o valor lógico da proposição.
- **Conjunção ($\wedge$ ou `AND`)** — Verdadeiro apenas se ambas as proposições forem verdadeiras.
- **Disjunção ($\vee$ ou `OR`)** — Falso apenas se ambas as proposições forem falsas.
- **Condicional ($\rightarrow$ ou `IF...THEN`)** — Falso apenas se a primeira for verdadeira e a segunda for falsa.
- **Bicondicional ($\leftrightarrow$ ou `IFF`)** — Verdadeiro se ambas as proposições tiverem o mesmo valor lógico.

---

## 📐 Lógica de Escopo e Complexidade

Para gerar uma tabela verdade, o algoritmo analisa a quantidade de variáveis distintas ($n$) presentes na expressão lógica. A partir disso, o número total de linhas da tabela é determinado pela função exponencial:

$$\text{Linhas} = 2^n$$

O programa então realiza a varredura e a avaliação da expressão para cada uma das combinações através de uma árvore de prioridades, respeitando o uso de **parênteses** e a ordem correta de precedência dos operadores lógicos.

---

## ⚙️ Funcionalidades do Algoritmo

*   **Identificação de Variáveis:** Detecção automática de proposições simples (como $p$, $q$, $r$).
*   **Avaliação de Expressões:** Processamento sequencial considerando a prioridade dos conectivos.
*   **Formatação Dinâmica:** Exibição organizada no terminal das colunas de entrada, passos intermediários e o resultado final da proposição composta.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** — Linguagem utilizada para implementar a lógica de parser e avaliação de expressões.
- **Git & GitHub** — Para controle de versão e documentação do projeto.

---

<p align="center">
  Desenvolvido com lógica e precisão por <a href="https://github.com/YOUTBMAT">Mateus Weiss</a> 🚀
</p>
