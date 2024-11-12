import os
import json
import pandas as pd

# Caminho para a pasta onde os arquivos JSON estão localizados
caminho_pasta = "Features_file"

# Lista para armazenar os dados filtrados
dados_filtrados = []

# Passo 1: Iterar sobre todos os arquivos na pasta
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith(".json"):  # Verifica se o arquivo é um JSON
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        # Passo 2: Abrir e carregar o arquivo JSON
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        # Passo 3: Verifica se "Static_analysis" existe no JSON
        static_analysis = dados.get("Static_analysis", {})

        # Passo 4: Filtrar os campos desejados dentro de "Static_analysis"
        filtrado = {
            "Nome do Arquivo": arquivo,  # Adiciona o nome do arquivo
            "API calls": static_analysis.get("API calls", None),
            "Opcodes": static_analysis.get("Opcodes", None),
            "Permissions": static_analysis.get("Permissions", None)
        }

        # Passo 5: Adicionar o dicionário filtrado à lista
        dados_filtrados.append(filtrado)

# Passo 6: Salvar os dados filtrados como um arquivo JSON
with open('dados_b.json', 'w', encoding='utf-8') as f:
    json.dump(dados_filtrados, f, ensure_ascii=False, indent=4)

print("Arquivo JSON salvo com sucesso!")
