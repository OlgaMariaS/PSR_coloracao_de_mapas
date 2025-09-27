package psr;

public class Main {

    public static void main(String[] args) {
        String[] nomes  = {"Fácil", "Média", "Difícil", "Sem solução", "Mapa do Brasil"};
        String[] paths  = {"instancia_facil.json", "instancia_media.json",  "instancia_dificil.json", "instancia_sem_solucao.json", "instancia_brasil.json",};

        for (int i = 0; i < paths.length; i++) {
            System.out.println("==========================================");
            System.out.println("Executando instância: " + nomes[i]);
            System.out.println("==========================================");

            try {
                Instancia inst = LeitorInstancia.carregar(paths[i]);

                System.out.println("   - Variáveis: " + inst.variaveis);
                System.out.println("   - Vizinhos: " + inst.vizinhos + "\n");

                psr.MapColoringSolver.Result r = psr.MapColoringSolver.solve(inst);

                System.out.println("--- Resultados ---");
                if (r.solucoes != null && !r.solucoes.isEmpty()) {
                    System.out.println("Total de soluções: " + r.solucoes.size());
                    int k = 1;
                    for (java.util.Map<String, String> sol : r.solucoes) {
                        System.out.println("Solução #" + k + ":");
                        sol.keySet().stream().sorted()
                                .forEach(v -> System.out.println("   " + v + ": " + sol.get(v)));
                        k++;
                        System.out.println();
                    }
                } else {
                    System.out.println("Nenhuma solução encontrada.");
                }

                System.out.printf("Tempo de execução: %d ms%n", r.tempoExecucaoMs);
                System.out.printf("Contagem de falhas/retornos: %d%n", r.totalFalhas);

            } catch (Exception e) {
                System.out.println("Erro ao processar " + nomes[i] + ": " + e.getMessage());
            }
        }
    }
}