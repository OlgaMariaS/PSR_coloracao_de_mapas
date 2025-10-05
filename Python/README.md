# Trabalho de Inteligência Artificial: Resolvedor de PSR para Coloração de Mapas

Este repositório contém a implementação de um resolvedor para o Problema de Satisfação de Restrições (PSR) focado no problema de Coloração de Mapas, como parte da disciplina de Introdução à Inteligência Artificial, do curso de Informática da Universidade Estadual de Maringá (2025).

O projeto utiliza o algoritmo de **Backtracking** com as heurísticas **Grau (Degree)** e **MRV (Minimum Remaining Values)**.

## Instalação

Para instalar as dependências necessárias, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Como Executar

As instâncias do problema estão localizadas na pasta `/instancias`. Para executar o resolvedor em todas as instâncias, rode o seguinte comando a partir da pasta raiz do projeto:

```bash
python main.py
```

As imagens dos grafos coloridos serão salvas na pasta `/resultados`.

## Ferramentas e Créditos

Este projeto utiliza a biblioteca de código aberto `python-constraint` para a implementação do solver de PSR. A biblioteca é distribuída sob a licença LGPL v2.0.

- **Repositório da Biblioteca:** [https://github.com/python-constraint/python-constraint](https://github.com/python-constraint/python-constraint)
