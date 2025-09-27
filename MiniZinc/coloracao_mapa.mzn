% Algoritmo para o problema de coloração de mapas

% Dominio das variáveis
enum Cores = {Vermelho, Verde, Azul};

% Número de variáveis
int: n;
int: m;

set of int: V = 1..n;

array[1..m] of int: regiao1;
array[1..m] of int: regiao2;

% conjunto de cores restritas para cada variável
array[V] of set of Cores: restricoes;

% variáveis de decisão
array[V] of var Cores: cor;

% Restrição: vizinhos não podem ter mesma cor
constraint
  forall(k in 1..m) (
    cor[regiao1[k]] != cor[regiao2[k]]
  );

% restrições extras de domínio
constraint
  forall(i in V) (
    not (cor[i] in restricoes[i])
  );

solve satisfy;

output [ "V" ++ show(i) ++ ": " ++ show(cor[i]) ++ "\n" | i in V ];

