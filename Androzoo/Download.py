import csv
from datetime import datetime
import argparse
import requests
import concurrent.futures
from tqdm import tqdm
import os

API_KEY = "0a896c23a132a15f742da449c16774d3ab25739f748f3e10bd304e9fa1b4992c"
DOWNLOAD_URL = "https://androzoo.uni.lu/api/download?apikey={}&sha256={}"
DOWNLOAD_LOG = "downloaded_sha256.txt"
SKIP_COUNT = 10001  # Número de arquivos a serem ignorados

def load_downloaded_sha256(log_file):
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            return set(f.read().splitlines())
    return set()

def save_downloaded_sha256(log_file, sha256):
    with open(log_file, 'a') as f:
        f.write(sha256 + '\n')

def process_csv(file_name, num_results, date_filter, size_filter, domains, downloaded_sha256):
    results = []
    sha256_list = []
    date_filter = datetime.strptime(date_filter, "%Y-%m-%d")
    domains = domains.split(',')
    skip_counter = 0  # Contador para ignorar os primeiros 1910 arquivos

    with open(file_name, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        total_rows = sum(1 for _ in reader)
        csvfile.seek(0)  # Voltar ao início do arquivo após contar as linhas

        # Ignorar a primeira linha de cabeçalhos
        headers = next(reader)

        processed_rows = 0
        with tqdm(total=total_rows, desc="Processing CSV") as pbar:
            for row in reader:
                processed_rows += 1
                pbar.update(1)  # Atualizar a barra de progresso

                # Conversão das colunas relevantes
                try:
                    row_date = datetime.strptime(row['dex_date'], "%Y-%m-%d %H:%M:%S")
                    row_size = int(row['apk_size'])
                    row_domains = row['markets'].split(';')  # Assumindo que os domínios estão separados por ponto e vírgula
                    sha256 = row['sha256']

                    # Verificação das condições e se o SHA256 já foi baixado
                    if sha256 not in downloaded_sha256 and row_date.date() >= date_filter.date() and row_size <= size_filter and any(domain in domains for domain in row_domains):
                        if skip_counter < SKIP_COUNT:
                            skip_counter += 1
                            continue  # Ignorar os primeiros 1910 arquivos que correspondem aos requisitos

                        results.append(row)
                        sha256_list.append(sha256)

                        if len(results) >= num_results:
                            break  # Parar a leitura do CSV se o número desejado de resultados for alcançado
                except ValueError as e:
                    print(f"Error processing row: {row}, error: {e}")

    print(f"Total results found: {len(results)}")
    return results, sha256_list

def download_apk(sha256):
    url = DOWNLOAD_URL.format(API_KEY, sha256)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(f"{sha256}.apk", 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        save_downloaded_sha256(DOWNLOAD_LOG, sha256)
        print(f"Downloaded APK with SHA256: {sha256}")
    else:
        print(f"Failed to download APK with SHA256: {sha256}, Status Code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Process a CSV file with filters.")
    parser.add_argument('-n', '--number', type=int, default=10, help='Number of results to return')
    parser.add_argument('-d', '--date', type=str, default='2015-12-11', help='Filter date (YYYY-MM-DD)')
    parser.add_argument('-s', '--size', type=int, default=3000000, help='Maximum size filter')
    parser.add_argument('-m', '--domains', type=str, default='play.google.com,appchina', help='Comma-separated list of domains')
    parser.add_argument('file_name', type=str, help='CSV file name')

    args = parser.parse_args()

    print(f"Filtering for files smaller than or equal to {args.size} bytes")

    # Carregar os SHA256 já baixados
    downloaded_sha256 = load_downloaded_sha256(DOWNLOAD_LOG)

    results, sha256_list = process_csv(args.file_name, args.number, args.date, args.size, args.domains, downloaded_sha256)

    print("Downloading APK files...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_apk, sha256) for sha256 in sha256_list]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
