import discord
from discord.ext import commands
import json
import asyncio
import requests
import os
from comandos.especiais.email import ComandosEspeciais
from comandos.jogos.JogoXadrez import XadrezJogo
from comandos.Utils.funcoesUteisR import carregar_configuracoes
from comandos.jogos.jogoRonda import RondaJogo
from comandos.especiais.coins import CoinsUser

intents = discord.Intents.default()
intents.message_content = True


"""ABAIXO ESTA O CODIGO QUE ATUALIZA SUAS CONFIG COM O BANCO DE DADOS CORRETO.
"""
firebase_url = 'https://config-94ecb-default-rtdb.firebaseio.com/.json'
response = requests.get(firebase_url)
api_data = json.loads(response.text)


if not os.path.exists('config.json') or os.path.getsize('config.json') == 0:
    # Se o arquivo estiver vazio ou não existir, preencha-o diretamente com os dados da API
    with open('config.json', 'w') as arquivo:
        json.dump(api_data, arquivo, indent=2)
else:
    try:
        with open('config.json', 'r') as local_file:
            local_data = json.load(local_file)
    except FileNotFoundError:
        local_data = None

    # Dados da API (Firebase)


    if response.status_code == 200:
        try:
            api_data = json.loads(response.text)

            # Mescla os dados locais com os dados do banco de dados
            for key, value in api_data.items():
                local_data[key] = value

            # Escreve os dados mesclados no arquivo JSON
            with open('config.json', 'w') as local_file:
                json.dump(local_data, local_file, indent=2)

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

    coins = CoinsUser(client)
    await client.add_cog(coins)

    ronda = RondaJogo(client)
    await client.add_cog(ronda)

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
        print('INSIRA NO config.json O SEU TOKEN DE BOT COM a "token_bot" : "seu token" ')
