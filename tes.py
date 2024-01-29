import requests
import json

firebase_url = 'https://config-94ecb-default-rtdb.firebaseio.com/.json'
response = requests.get(firebase_url)

if response.text.strip():
    print(f'Conteúdo da resposta: {response.text}')
    api_data = json.loads(response.text)
else:
    print('A resposta do servidor está vazia.')
    api_data = None

print(api_data)
