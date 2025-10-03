import time
import json
from constraint import Problem
from utils import *

# Caminhos das instâncias
INSTANCIAS = {
    "Fácil": "instancias/instancia_facil.json",
    "Média": "instancias/instancia_media.json",
    "Difícil": "instancias/instancia_dificil.json",
    "Muito Difícil": "instancias/instancia_muito_dificil.json",
    "Instancia Parâmetro": "instancias/instancia_parametro.json"
}

def resolver_mapa_com_mrv(variaveis, dominios, vizinhos, restricoes_extras):
    """
    Resolve o problema de coloração de mapa usando backtracking com a heurística MRV.

    A biblioteca 'python-constraint' utiliza a heurística MRV (Minimum Remaining Values)
    como estratégia padrão para a seleção de variáveis no BacktrackingSolver.
    """
    # 1. Criação do problema e do nosso solver customizado
    problema = Problem(ContadorBacktrackingSolver())

    # 2. Adição de variáveis e seus respectivos domínios
    for var in variaveis:
        problema.addVariable(var, dominios[var])

    # 3. Adição das restrições de adjacência (regiões vizinhas não podem ter a mesma cor)
    for regiao, lista_vizinhos in vizinhos.items():
        for vizinho in lista_vizinhos:
            # Adiciona a restrição apenas uma vez para cada par (ex: V1-V2 e não V2-V1)
            if regiao < vizinho:
                problema.addConstraint(lambda cor1, cor2: cor1 != cor2, (regiao, vizinho))

    # --- ESSE BLOCO É PARA AS RESTRIÇÕES EXTRAS ---
    for restricao in restricoes_extras:
        if restricao["tipo"] =="cardinalidade_max":
            params = restricao["parametros"]
            cor_restringida = params["cor"]
            maximo = params["maximo"]

            # Criamos uma INSTÂNCIA da nossa nova classe de restrição
            constraint_obj = MaxCardinalityConstraint(cor_restringida, maximo)

            # Adiciona a restrição ao problema, aplicando-a a TODAS as variáveis
            problema.addConstraint(constraint_obj, variaveis)
        elif restricao["tipo"] =="cardinalidade_min":
            params = restricao["parametros"]
            cor_restringida = params["cor"]
            minimo = params["minimo"]
            constraint_obj = MinCardinalityConstraint(cor_restringida, minimo)
            problema.addConstraint(constraint_obj, variaveis)

    # --- FIM DO NOVO BLOCO ---

    # 4. Medição do tempo e execução da busca pela solução
    tempo_inicio = time.time()
    # A biblioteca retorna a primeira solução encontrada
    solucao = problema.getSolution()
    tempo_fim = time.time()

    tempo_execucao = (tempo_fim - tempo_inicio) * 1000

    # 5. Obtenção das métricas
    # Acessa o solver para obter o número de falhas
    num_falhas = problema._solver.get_num_falhas()

    return solucao, tempo_execucao, num_falhas


def executar():
    """
    Função principal que carrega cada instância, resolve o problema e exibe os resultados.
    """
    for nome, caminho in INSTANCIAS.items():
        print(f"\n📌 ==========================================")
        print(f"📌 Executando instância: {nome}")
        print(f"📌 ==========================================")

        try:
            variaveis, dominios, vizinhos, restricoes = carregar_instancia(caminho)

            print(f"   - Variáveis: {len(variaveis)}")
            print(f"   - Vizinhos: {vizinhos}\n")
            print(f"   - Restrições Extras: {restricoes}\n")

            # Nota: a variável de tempo foi renomeada para tempo_ms para clareza
            solucao, tempo_ms, falhas = resolver_mapa_com_mrv(variaveis, dominios, vizinhos, restricoes)

            print("--- Resultados ---")
            if solucao:
                print(f"✅ Solução encontrada:")
                # Imprime a solução de forma organizada
                for var in sorted(solucao.keys()):
                    print(f"   {var}: {solucao[var]}")

                # Chama a função para criar e salvar a imagem do grafo
                nome_arquivo_mapa = gerar_visualizacao_mapa(vizinhos, solucao, nome)
                print(f"🖼️  Visualização do mapa salva em: '{nome_arquivo_mapa}'")
                # -----------------------------------------

            else:
                print("❌ Nenhuma solução encontrada.")

            print(f"⏱️  Tempo de execução: {tempo_ms:.4f} milissegundos.")
            print(f"📉 Contagem de falhas/retornos: {falhas}.")

        except FileNotFoundError:
            print(f"Erro: Arquivo da instância '{caminho}' não encontrado.")
        except Exception as e:
            print(f"Ocorreu um erro ao processar a instância {nome}: {e}")


if __name__ == "__main__":
    executar()

