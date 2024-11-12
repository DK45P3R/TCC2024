import csv
import json
import os

# Caminho do arquivo JSON
json_filename = 'permissions_m.json'  # Altere para o nome correto do seu arquivo JSON

# Lendo os dados do arquivo JSON
with open(json_filename, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Criar um conjunto de todas as permissões únicas
permissions_set = set()
for item in data:
    permissions_set.update(item.get('Permissions', []))

# Converter o conjunto de permissões em uma lista
permissions_list = list(permissions_set)

# Nome do arquivo CSV que será gerado
csv_filename = 'permissions_from_json.csv'

# Criar e escrever no arquivo CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')

    # Escrever o cabeçalho
    header = ['Nome do Arquivo'] + permissions_list
    writer.writerow(header)

    # Iterar sobre cada item no JSON
    for item in data:
        nome_arquivo = item.get('Nome do Arquivo', '')
        row = [nome_arquivo]

        # Verificar a presença de cada permissão
        for permission in permissions_list:
            if permission in item.get('Permissions', []):
                row.append(1)  # Presente
            else:
                row.append(0)  # Ausente

        writer.writerow(row)

# Ajustar permissões do arquivo CSV (opcional)
os.chmod(csv_filename, 0o644)  # Ajusta permissões

print(f"Arquivo CSV gerado: {csv_filename}")

