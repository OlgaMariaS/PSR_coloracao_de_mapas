from json import load
import os
import time
import json
import networkx as nx
import matplotlib.pyplot as plt
from constraint import Problem, BacktrackingSolver, Constraint
from src import resultados


class ContadorBacktrackingSolver(BacktrackingSolver):
    """
    Um BacktrackingSolver customizado para contar o número de falhas (backtracks).
    """

    def __init__(self, forwardcheck=False):
        super().__init__(forwardcheck)
        self._num_falhas = 0

    def get_num_falhas(self):
        return self._num_falhas

    def recursive_search(self, domains, assignments, _unassigned):
        # O ponto de falha ocorre quando uma busca recursiva retorna sem solução.
        # Nós contamos isso como um "retorno" ou "falha".
        if not domains:
            self._num_falhas += 1

        # Chama o método original da superclasse para continuar a busca
        return super().recursive_search(domains, assignments, _unassigned)

class MaxCardinalityConstraint(Constraint):
    """
    Restrição customizada para garantir que um valor específico não apareça mais
    do que um número máximo de vezes em uma atribuição.
    Esta classe garante que a verificação é feita em tempo de busca (em atribuições parciais).
    """
    def __init__(self, cor_restringida, maximo):
        self.cor = cor_restringida
        self.maximo = maximo

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        # Este método é chamado pelo solver a cada passo da busca.
        # 'assignments' contém uma atribuição parcial atual (ex: {'V1':'azul', 'V2':'verde'})

        # Contamos quantas vezes a cor restrita aparece na solução parcial
        contagem = list(assignments.values()).count(self.cor)

        # Se a contagem já excedeu o máximo, este caminho é inválido.
        # Retornar False aqui força o backtracking imediato.
        if contagem > self.maximo:
            return False

        # Se não, o caminho ainda é potencialmente válido.
        return True


class MinCardinalityConstraint(Constraint):
    def __init__(self, cor_restringida, minimo):
        self._cor = cor_restringida
        self._minimo = minimo
        self._num_variaveis = 0

    def preProcess(self, variables, domains, constraints, vconstraints):
        self._num_variaveis = len(variables)

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        contagem = list(assignments.values()).count(self._cor)

        # Verifica se ainda é POSSÍVEL atingir o mínimo
        variaveis_restantes = self._num_variaveis - len(assignments)
        if (contagem + variaveis_restantes) < self._minimo:
            return False  # Impossível atingir o mínimo, falha.

        # Se todas as variáveis foram atribuídas, verifica a condição final
        if len(assignments) == self._num_variaveis:
            return contagem >= self._minimo

        return True

def carregar_instancia(caminho_arquivo):
    """
    Carrega uma instância de coloração de mapa a partir de um arquivo JSON/TXT.
    Retorna: variáveis, domínios, vizinhos, restrições extras.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        dados = load(arquivo)
    return (
        dados["variaveis"],
        dados["dominios"],
        dados["vizinhos"],
        dados["restricoes_extras"]
    )


def gerar_visualizacao_mapa(vizinhos, solucao, nome_instancia):
    """
    Cria e salva uma imagem do grafo do mapa em uma pasta de resultados.
    """
    # --- NOVO: Definir e criar a pasta de resultados ---
    pasta_resultados = "resultados"
    os.makedirs(pasta_resultados, exist_ok=True)  # Cria a pasta se ela não existir

    G = nx.Graph()

    for no, lista_vizinhos in vizinhos.items():
        G.add_node(no)
        for vizinho in lista_vizinhos:
            G.add_edge(no, vizinho)

    cores_map = {
        "vermelho": "red",
        "verde": "green",
        "azul": "blue",
        "amarelo": "yellow"
    }
    cores_dos_nos = [cores_map.get(solucao.get(no), "grey") for no in G.nodes()]

    # Ajuste para grafos maiores
    tamanho_figura = max(8, len(vizinhos) / 10)
    tamanho_fonte = max(8, 16 - len(vizinhos) / 10)
    plt.figure(figsize=(tamanho_figura, tamanho_figura))

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=cores_dos_nos, node_size=1500, font_size=tamanho_fonte,
            font_color='black',
            width=1.5, edge_color='gray')
    plt.title(f"Solução para Instância: {nome_instancia}", size=20)

    # --- ALTERADO: Construir o caminho completo e salvar o arquivo ---
    # Limpa o nome da instância para criar um nome de arquivo válido
    nome_arquivo_base = f"mapa_solucao_{nome_instancia.lower().replace(' ', '_').replace(':', '')}.png"
    caminho_completo = os.path.join(pasta_resultados, nome_arquivo_base)

    plt.savefig(caminho_completo)
    plt.close()

    # Retorna o caminho completo para a mensagem de log
    return caminho_completo
