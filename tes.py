import json
import requests


URL = 'https://cartas-d2746-default-rtdb.firebaseio.com/.json'
response = requests.get(URL)

# Verifica se a requisição foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # Converte o conteúdo JSON da resposta para um objeto Python
    dados = response.json()

    # Agora, 'dados' contém o conteúdo em formato Python
    # Você pode manipulá-lo conforme necessário
    print(dados)
else:
    print(f"A requisição falhou com o código  status: {response.status_code}")


