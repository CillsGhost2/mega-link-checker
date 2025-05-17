import re
import requests
import time
import json

regex = r"https:\/\/mega\.nz\/(file|folder)\/[\s\S]*#[\s\S]*"
api = 'https://g.api.mega.co.nz'

def is_mega_url_valid(url: str) -> bool:
    match = re.match(regex, url)
    if not match:
        return False 

    urltype = url.split("/")[3]
    id = url.split("/")[4].split("#")[0]

    if urltype == 'folder':
        data = { "a": "f", "c": 1, "r": 1, "ca": 1 }
    else:
        data = { "a": 'g', "p": id } 
    params = {
        'id': ''.join([str(randint(0, 9)) for _ in range(10)]),
        'n': id
    }

    try:
        response = requests.post('https://g.api.mega.co.nz/cs', params=params, data=data, timeout=10)
        response.raise_for_status()
        response_json = response.json()

        # Verifica se a resposta é -2 (Resposta para links válidos)
        return response_json == -2

    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição: {url} - {e}")
        return False
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Erro de JSON: {url} - {e}")
        return False
    except Exception as e:
         print(f"Outro erro: {url} - {e}")
         return False


def check_urls_from_list(lines: list[str], delay: int = 10):
    for line in lines:
        line = line.strip()
        match = re.search(regex, line)
        if match:
            url = match.group(0)
            if is_mega_url_valid(url):
                print(line)
            time.sleep(delay)


def check_urls_from_file(filepath: str, delay: int = 10):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            check_urls_from_list(lines, delay)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {filepath}")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

print("Verificando URLs do arquivo:")
check_urls_from_file('mega.txt')