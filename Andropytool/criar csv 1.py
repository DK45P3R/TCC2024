import csv
import json

# Lendo os dados do arquivo JSON que foi enviado pelo usuário
json_filename = 'api_calls_m.json'

with open(json_filename, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Nome do arquivo CSV
csv_filename = 'api_calls_from_json.csv'

# Extrair os campos e gerar o CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')

    # Escrever o cabeçalho
    header = ['Nome do Arquivo'] + list(data[0]['API calls'].keys())
    writer.writerow(header)

    # Escrever os dados
    for item in data:
        row = [item['Nome do Arquivo']] + list(item['API calls'].values())
        writer.writerow(row)

csv_filename  # Retornar o caminho do arquivo gerado

