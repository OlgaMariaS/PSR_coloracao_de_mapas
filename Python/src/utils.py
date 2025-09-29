from json import load
import networkx as nx
import matplotlib.pyplot as plt
from constraint import Problem, BacktrackingSolver

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
    Cria e salva uma imagem do grafo do mapa com as cores da solução.
    """
    G = nx.Graph()

    # Adiciona nós e arestas ao grafo a partir da definição dos vizinhos
    for no, lista_vizinhos in vizinhos.items():
        G.add_node(no)
        for vizinho in lista_vizinhos:
            G.add_edge(no, vizinho)

    # Mapeia os nomes das cores da solução para cores que o matplotlib entende
    cores_map = {
        "vermelho": "red",
        "verde": "green",
        "azul": "blue",
        "amarelo": "yellow"
    }
    cores_dos_nos = [cores_map.get(solucao[no], "grey") for no in G.nodes()]

    # Desenha o grafo
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=cores_dos_nos, node_size=2000, font_size=16, font_color='white',
            width=2.0, edge_color='gray')
    plt.title(f"Solução para Instância: {nome_instancia}", size=20)

    # Salva a imagem em um arquivo
    nome_arquivo = f"mapa_solucao_{nome_instancia.lower()}.png"
    plt.savefig(nome_arquivo)

    plt.show()

    plt.close()

    return nome_arquivo

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