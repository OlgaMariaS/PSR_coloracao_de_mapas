package psr;

public class Main {

    public static void main(String[] args) {
        String[] nomes  = {"Fácil", "Média", "Difícil", "Muito difícil"};
        String[] paths  = {"instancia_facil.json", "instancia_media.json", "instancia_dificil.json", "instancia_muito_dificil.json"};

        for (int i = 0; i < paths.length; i++) {
            System.out.println("\n📌 ==========================================");
            System.out.println("📌 Executando instância: " + nomes[i]);
            System.out.println("📌 ==========================================");

            try {
                Instancia inst = LeitorInstancia.carregar(paths[i]);

                System.out.println("   - Variáveis: " + inst.variaveis);
                System.out.println("   - Vizinhos: " + inst.vizinhos + "\n");

                psr.MapColoringSolver.Result r = psr.MapColoringSolver.solve(inst);

                System.out.println("--- Resultados ---");
                if (r.atribuicaoDeCores != null) {
                    System.out.println("✅ Solução encontrada:");
                    r.atribuicaoDeCores.keySet().stream().sorted()
                            .forEach(v -> System.out.println("   " + v + ": " + r.atribuicaoDeCores.get(v)));
                } else {
                    System.out.println("❌ Nenhuma solução encontrada.");
                }

                System.out.printf("⏱️  Tempo de execução: %d ms%n", r.tempoExecucaoMs);
                System.out.printf("📉 Contagem de falhas/retornos: %d%n", r.totalFalhas);

            } catch (Exception e) {
                System.out.println("Erro ao processar " + nomes[i] + ": " + e.getMessage());
            }
        }
    }
}