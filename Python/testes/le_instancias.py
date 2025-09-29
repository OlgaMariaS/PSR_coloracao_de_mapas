import json

with open('../src/instancias/instancia_facil.json', 'r') as json_file:
    instancia = json.load(json_file)

print(instancia["variaveis"])