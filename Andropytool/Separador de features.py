
import json

def criar_arquivos_json_separados(json_arquivo):
    # Abrir o arquivo JSON e carregar os dados
    with open(json_arquivo, 'r', encoding='utf-8') as arquivo_json:
        dados = json.load(arquivo_json)

    # Estruturas para armazenar os dados separados
    api_calls_dados = []
    opcodes_dados = []
    permissions_dados = []

    # Iterar sobre os itens no JSON original e separar os dados
    for item in dados:
        nome_arquivo = item.get("Nome do Arquivo", "")

        # Coletar dados de API calls
        api_calls = item.get("API calls", {})
        if api_calls is not None:
            api_calls_dados.append({
                "Nome do Arquivo": nome_arquivo,
                "API calls": api_calls
            })

        # Coletar dados de Opcodes
        opcodes = item.get("Opcodes", {})
        if opcodes is not None:
            opcodes_dados.append({
                "Nome do Arquivo": nome_arquivo,
                "Opcodes": opcodes
            })

        # Coletar dados de Permissions
        permissions = item.get("Permissions", [])
        if permissions is not None:
            permissions_dados.append({
                "Nome do Arquivo": nome_arquivo,
                "Permissions": permissions
            })

    # Criar os arquivos JSON separados
    with open('api_calls_m.json', 'w', encoding='utf-8') as api_calls_arquivo:
        json.dump(api_calls_dados, api_calls_arquivo, ensure_ascii=False, indent=4)

    with open('opcodes_m.json', 'w', encoding='utf-8') as opcodes_arquivo:
        json.dump(opcodes_dados, opcodes_arquivo, ensure_ascii=False, indent=4)

    with open('permissions_m.json', 'w', encoding='utf-8') as permissions_arquivo:
        json.dump(permissions_dados, permissions_arquivo, ensure_ascii=False, indent=4)

# Exemplo de uso:
criar_arquivos_json_separados('dados_mal.json')

