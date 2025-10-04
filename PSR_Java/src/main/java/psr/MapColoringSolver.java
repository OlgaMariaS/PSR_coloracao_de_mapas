package psr;

import org.chocosolver.solver.Model;
import org.chocosolver.solver.search.strategy.Search;
import org.chocosolver.solver.search.strategy.selectors.values.IntValueSelector;
import org.chocosolver.solver.search.strategy.selectors.variables.DomOverWDeg;
import org.chocosolver.solver.variables.IntVar;
import org.chocosolver.util.iterators.DisposableValueIterator;

import java.util.*;

/**
 Solver com seleção de variável Dom/Wdeg e ordenação de valores LCV (Least Constraining Value).
 */
public class MapColoringSolver {

    public static class Result {
        public final List<Map<String, String>> solucoes; // Lista de atribuições Região → Cor.
        public final long tempoExecucaoMs;               // Tempo total de execução em milissegundos.
        public final long totalFalhas;                   // Número de falhas ocorridas na busca.

        public Result(List<Map<String, String>> solucoes, long tempoExecucaoMs, long totalFalhas) {
            this.solucoes = solucoes;
            this.tempoExecucaoMs = tempoExecucaoMs;
            this.totalFalhas = totalFalhas;
        }
    }

    public static Result solve(Instancia instancia) {
        // 1) Modelagem do problema no Choco Solver.
        Model modelo = new Model("MapColoring");

        // Mapeamento: região -> variável inteira (valor = índice da cor escolhida).
        Map<String, IntVar> variaveisPorRegiao = new LinkedHashMap<>();             // Variáveis no solver.
        Map<String, List<String>> coresDisponiveisPorRegiao = new LinkedHashMap<>(); // Paleta de cores por região.

        // Cria variáveis para cada região com base no domínio de cores permitido.
        for (String regiao : instancia.variaveis) {
            List<String> coresDaRegiao = new ArrayList<>(instancia.dominios.get(regiao));
            int[] dominioInteiros = new int[coresDaRegiao.size()];
            for (int i = 0; i < coresDaRegiao.size(); i++) dominioInteiros[i] = i; // Índices 0..n-1.

            IntVar variavelRegiao = modelo.intVar(regiao, dominioInteiros);

            variaveisPorRegiao.put(regiao, variavelRegiao);
            coresDisponiveisPorRegiao.put(regiao, coresDaRegiao);
        }

        // 2) Restrições: vizinhos não podem ter a mesma cor.
        for (Map.Entry<String, List<String>> entradaVizinhanca : instancia.vizinhos.entrySet()) {
            String regiaoA = entradaVizinhanca.getKey();
            for (String regiaoB : entradaVizinhanca.getValue()) {
                if (regiaoA.compareTo(regiaoB) < 0) { // Evita duplicar restrições.
                    IntVar varA = variaveisPorRegiao.get(regiaoA);
                    IntVar varB = variaveisPorRegiao.get(regiaoB);
                    List<String> coresA = coresDisponiveisPorRegiao.get(regiaoA);
                    List<String> coresB = coresDisponiveisPorRegiao.get(regiaoB);

                    // Restringe apenas as cores em comum entre A e B.
                    for (int idxA = 0; idxA < coresA.size(); idxA++) {
                        String corEmA = coresA.get(idxA);
                        int idxB = coresB.indexOf(corEmA);
                        if (idxB >= 0) {
                            modelo.or(
                                    modelo.arithm(varA, "!=", idxA),
                                    modelo.arithm(varB, "!=", idxB)
                            ).post();
                        }
                    }
                }
            }
        }

        // 3) Cria vizinhança simétrica para cálculo do impacto (LCV).
        Map<String, Set<String>> vizinhancaSimetrica = new HashMap<>();
        for (String regiao : instancia.vizinhos.keySet()) {
            vizinhancaSimetrica.computeIfAbsent(regiao, k -> new LinkedHashSet<>()).addAll(instancia.vizinhos.get(regiao));
            for (String vizinho : instancia.vizinhos.get(regiao)) {
                vizinhancaSimetrica.computeIfAbsent(vizinho, k -> new LinkedHashSet<>()).add(regiao);
            }
        }

        // 4) Heurísticas de busca:
        // - Variáveis: Dom/Wdeg (variável mais restrita).
        // - Valores: LCV (cor que restringe menos os vizinhos).
        DomOverWDeg seletorDeVariavel = new DomOverWDeg(variaveisPorRegiao.values().toArray(new IntVar[0]), 0);

        IntValueSelector seletorDeValorLCV = (IntVar variavelAtual) -> {
            String nomeRegiao = variavelAtual.getName();
            List<String> coresDaRegiao = coresDisponiveisPorRegiao.get(nomeRegiao);

            int melhorIndice = Integer.MAX_VALUE;
            int menorImpacto = Integer.MAX_VALUE;

            DisposableValueIterator iteradorValores = variavelAtual.getValueIterator(true);
            try {
                while (iteradorValores.hasNext()) {
                    int valorCandidato = iteradorValores.next();
                    String corCandidata = coresDaRegiao.get(valorCandidato);

                    // Impacto = número de vizinhos que perderiam essa cor.
                    int impacto = 0;
                    for (String vizinho : vizinhancaSimetrica.getOrDefault(nomeRegiao, Set.of())) {
                        IntVar variavelVizinho = variaveisPorRegiao.get(vizinho);
                        if (variavelVizinho.isInstantiated()) continue;

                        List<String> coresDoVizinho = coresDisponiveisPorRegiao.get(vizinho);
                        int idCorVizinho = coresDoVizinho.indexOf(corCandidata);
                        if (idCorVizinho >= 0 && variavelVizinho.contains(idCorVizinho)) {
                            impacto++;
                        }
                    }

                    if (impacto < menorImpacto || (impacto == menorImpacto && valorCandidato < melhorIndice)) {
                        menorImpacto = impacto;
                        melhorIndice = valorCandidato;
                    }
                }
            } finally {
                iteradorValores.dispose();
            }
            return melhorIndice;
        };

        modelo.getSolver().setSearch(
                Search.intVarSearch(seletorDeVariavel, seletorDeValorLCV, variaveisPorRegiao.values().toArray(new IntVar[0]))
        );

        // 5) Execução da busca com todas as soluções.
        long inicio = System.nanoTime();
        List<Map<String, String>> todasSolucoes = new ArrayList<>();

        while (modelo.getSolver().solve()) {
            Map<String, String> atribuicao = new LinkedHashMap<>();
            for (String regiao : variaveisPorRegiao.keySet()) {
                IntVar var = variaveisPorRegiao.get(regiao);
                int indiceCor = var.getValue(); // variável está instanciada na solução corrente
                String nomeCor = coresDisponiveisPorRegiao.get(regiao).get(indiceCor);
                atribuicao.put(regiao, nomeCor);
            }
            todasSolucoes.add(atribuicao);
        }

        long fim = System.nanoTime();
        long falhas = modelo.getSolver().getMeasures().getFailCount();
        long tempoGastoMs = (fim - inicio) / 1_000_000L;

        return new Result(todasSolucoes, tempoGastoMs, falhas);
    }
}