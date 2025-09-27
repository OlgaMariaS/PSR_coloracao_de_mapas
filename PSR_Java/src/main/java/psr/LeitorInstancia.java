package psr;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;

public class LeitorInstancia {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    public static Instancia carregar(String path) throws IOException {
        return MAPPER.readValue(new File(path), Instancia.class);
    }
}
