import discord
from discord.ext import commands
import os
import asyncio
import random
from comandos.comandosEspeciais import ComandosEspeciais
from comandos.comandosJogos import Xadrez
from comandos.funcoesUteis.funcoesUteisR import carregar_configuracoes
intents = discord.Intents.default()
intents.message_content = True

# Defina o prefixo desejado
prefixo = '?'

# Crie a instância do bot com o prefixo
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

    xadrez = Xadrez(client)
    await client.add_cog(xadrez)

@client.event
async def on_ready():
    print('-----------------')
    print('BOT ONLINE')
    print(client.user.name)
    print(client.user.id)
    print('Prefixo:', prefixo)
    print('-----------------')


   

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
    client.run(client.config['token_bot'])

