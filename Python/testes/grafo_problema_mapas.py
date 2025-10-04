import networkx as nx
import matplotlib.pyplot as plt


# Função para desenhar grafos das instâncias
def desenhar_grafo(instancia, titulo):
    G = nx.Graph()
    G.add_nodes_from(instancia["variables"])
    for v, vizinhos in instancia["neighbors"].items():
        for u in vizinhos:
            G.add_edge(v, u)

    plt.figure(figsize=(5, 5))
    pos = nx.circular_layout(G)  # layout circular para parecer pentágono
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightblue", font_size=10, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2)
    plt.title(titulo)
    plt.show()


# Instâncias (simplificadas no Python)
mapa_facil = {
    "variables": ["V1", "V2", "V3", "V4", "V5"],
    "neighbors": {
        "V1": ["V2", "V5"],
        "V2": ["V1", "V3"],
        "V3": ["V2", "V4"],
        "V4": ["V3", "V5"],
        "V5": ["V4", "V1"]
    }
}

mapa_medio = {
    "variables": ["V1", "V2", "V3", "V4", "V5"],
    "neighbors": {
        "V1": ["V2", "V5", "V3"],  # diagonal V1-V3
        "V2": ["V1", "V3", "V4"],  # diagonal V2-V4
        "V3": ["V2", "V4", "V1"],
        "V4": ["V3", "V5", "V2"],
        "V5": ["V4", "V1"]
    }
}

mapa_dificil = {
    "variables": ["V1", "V2", "V3", "V4", "V5"],
    "neighbors": {
        "V1": ["V2", "V5", "V3"],
        "V2": ["V1", "V3", "V4"],
        "V3": ["V2", "V4", "V1"],
        "V4": ["V3", "V5", "V2"],
        "V5": ["V4", "V1"]
    }
}
# Desenhar os grafos
desenhar_grafo(mapa_facil, "Instância Fácil (Ciclo 5)")
desenhar_grafo(mapa_medio, "Instância Média (Ciclo + Diagonais)")
desenhar_grafo(mapa_dificil, "Instância Difícil restringir domínio de 2 regiões (ex.: R2∈{A,B}, R4∈{A,B}).")
