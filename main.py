import discord
from discord.ext import commands
import json
import asyncio
import requests
from comandos.especiais.email import ComandosEspeciais
from comandos.jogos.JogoXadrez import XadrezJogo
from comandos.Utils.funcoesUteisR import carregar_configuracoes
intents = discord.Intents.default()
intents.message_content = True


"""ABAIXO ESTA O CODIGO QUE ATUALIZA SUAS CONFIG COM O BANCO DE DADOS CORRETO.
"""
try:
    with open('config.json', 'r+') as local_file:
        local_data = json.load(local_file)
        if not local_data:
            local_data = {}  # Inicializa como um dicionário vazio se o arquivo estiver vazio
except json.JSONDecodeError:
    print('Erro ao decodificar o JSON')
except Exception as e:
    print(f'Erro desconhecido: {e}')
    local_data = None

# Dados da API (Firebase)
firebase_url = 'https://config-94ecb-default-rtdb.firebaseio.com/.json'
response = requests.get(firebase_url)

if response.status_code == 200:
    try:
        # Converte o conteúdo da resposta para um objeto Python (por exemplo, um dicionário)
        api_data = json.loads(response.text)
        
        # Criar uma cópia dos dados locais para evitar a substituição total
        updated_data = local_data.copy() if local_data else {}

        # Atualiza apenas a parte relacionada ao banco de dados em updated_data
        updated_data['database'] = api_data.get('database', {})

        # Sobrescreve o arquivo 'config.json' com os dados atualizados
        with open('config.json', 'w') as local_file:
            json.dump(updated_data, local_file, indent=2)

    except json.JSONDecodeError as e:
        print(f'Erro ao decodificar JSON: {e}')
else:
    print(f'A requisição falhou com o código de status: {response.status_code}')


# Crie a instância do bot com o prefixo
prefixo = '?'
client = commands.Bot(command_prefix=commands.when_mentioned_or(prefixo), intents=intents)

#async def load_extensions():
 #   for filename in os.listdir('./comandos'):
  #         if filename != '__init__.py':
   #             await client.load_extension(f'comandos.{filename[:-3]}')
    # client.load_extension('comandosEspeciais')
async def setup(): 
    config = await carregar_configuracoes()
    client.config = config

    # Eventos e comandos vão aqui
    comandos_especiais = ComandosEspeciais(client)
    await client.add_cog(comandos_especiais)

    xadrez = XadrezJogo(client)
    await client.add_cog(xadrez)

@client.event
async def on_ready():
    print('-----------------')
    print('BOT ONLINE')
    print(client.user.name)
    print(client.user.id)
    print('Prefixo:', prefixo)
    print('-----------------')
# Dados do banco de dados local

    

@client.event
async def on_message(message):
    # Não esqueça de adicionar isso para garantir que os comandos funcionem
    await client.process_commands(message)
   
    #if message.content.lower().startswith('!bomdia'):
     #   await message.channel.send('ola mundo, bom dia!')

    #if message.content.lower().startswith('!moeda'):
      

# Comando básico usando o prefixo configurado
@client.command(name='?ajuda')
async def diga(ctx, *, mensagem):
    await ctx.send(mensagem)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup())
    try:
        client.run(client.config['token_bot'])
    except:
        print('INSIRA NO config.json O SEU TOKEN DE BOT COM a chave "token_bot" : "seu token" ')
