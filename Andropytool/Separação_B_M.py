import os
import shutil

# Definir os caminhos das pastas
apk_folder = "C:/Users/vinik/Downloads/Banco de Dados/M"  # Pasta contendo os arquivos APK
json_folder = "C:/Users/vinik/Downloads/appk/Malignos"  # Pasta contendo os arquivos JSON
destination_folder = "C:/Users/vinik/Downloads/Banco de Dados"  # Pasta de destino para os arquivos JSON

# Garantir que a pasta de destino exista
os.makedirs(destination_folder, exist_ok=True)

# Iterar sobre cada arquivo na pasta de APKs
for apk_filename in os.listdir(apk_folder):
    if apk_filename.endswith(".apk"):  # Verificar se é um arquivo APK
        # Gerar o nome correspondente do arquivo JSON
        json_filename = os.path.splitext(apk_filename)[0] + ".json"

        # Caminho completo para o arquivo JSON na pasta de JSONs
        json_filepath = os.path.join(json_folder, json_filename)

        # Verificar se o arquivo JSON correspondente existe
        if os.path.exists(json_filepath):
            # Caminho completo para o arquivo JSON na pasta de destino
            destination_filepath = os.path.join(destination_folder, json_filename)

            # Mover o arquivo JSON para a pasta de destino
            shutil.move(json_filepath, destination_filepath)
            print(f"Movido: {json_filename} para {destination_folder}")
        else:
            print(f"Arquivo JSON correspondente não encontrado: {json_filename}")

print("Processo concluído!")
