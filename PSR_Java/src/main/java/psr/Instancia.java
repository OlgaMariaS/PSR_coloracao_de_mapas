package psr;

import java.util.List;
import java.util.Map;

public class Instancia {
    public List<String> variaveis;
    public Map<String, List<String>> dominios;
    public Map<String, List<String>> vizinhos;
    public List<Object> restricoes_extras; // Se precisar no futuro...

    public Instancia() {}
}
