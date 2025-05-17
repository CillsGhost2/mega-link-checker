import re
from random import randint
import requests
import json

regex = r"https:\/\/mega\.nz\/(file|folder)\/[\s\S]*#[\s\S]*"
api = 'https://g.api.mega.co.nz'

def get_mega_api_response(url: str) -> tuple[bool, dict | list | int | None]:

    match = re.match(regex, url)
    if not match:
        return False, None 

    urltype = url.split("/")[3]
    id = url.split("/")[4].split("#")[0]

    if (urltype == 'folder'):
        data = { "a": "f", "c": 1, "r": 1, "ca": 1 }
    else:
        data = { "a": 'g', "p": id }
    params = {
        'id': ''.join(["{}".format(randint(0, 9)) for num in range(0, 10)]),
        'n': id
    }

    try:
        response = requests.post('https://g.api.mega.co.nz/cs', params=params, data=data, timeout=10)
        response.raise_for_status()
        return True, response.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição: {url} - {e}")
        return False, None
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Erro de JSON: {url} - {e}")
        return False, None
    except Exception as e:
        print(f"Outro Erro: {url} - {e}")
        return False, None

def test_urls(urls: list[str]):

    for url in urls:
        print(f"Verificando URL: {url}")
        success, response = get_mega_api_response(url)
        if success:
            print("Resposta da API:")
            print(json.dumps(response, indent=4))
        else:
            print("Falha ao obter resposta da API.")
        print("-" * 40)

# URLs de Teste
test_links = [
    "https://mega.nz/folder/0j9wBYDZ#7pozGnhWxsb7XbzLYvkRPg",  # Pasta removida/inválida 
    "https://mega.nz/folder/x7t0hI7C#ImdZmRuigmaK1JwFYB688Q",  # Pasta removida/inválida 
    "https://mega.nz/folder/LN5y1RYT#VNpu1Nvnt8igY0OLWOndtA", #Arquivo removido/inválido 
    "https://mega.nz/folder/dYljgCIS#DEEE2-xBAj9wdyekxr8MBA", #Arquivo Valido 
]

test_urls(test_links)