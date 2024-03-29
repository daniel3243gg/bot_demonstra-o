import os
# import asyncio
import random

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

# Defina o prefixo desejado
prefixo = '?'

# Crie a instância do bot com o prefixo
client = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefixo), intents=intents
)


async def load_extensions():
    for filename in os.listdir('./comandos'):
        if filename.endswith('.py'):
            await client.load_extension(f'comandos.{filename[:-3]}')

    await client.load_extension('comandosEspeciais')


@client.event
async def on_ready():
    print('-----------------')
    print('BOT ONLINE')
    print(client.user.name)  # type: ignore
    print(client.user.id)  # type: ignore
    print('Prefixo:', prefixo)
    print('-----------------')

    await load_extensions()


@client.event
async def on_message(message):
    # Não esqueça de adicionar isso para garantir que os comandos funcionem
    await client.process_commands(message)

    if message.content.lower().startswith('!bomdia'):
        await message.channel.send('ola mundo, bom dia!')

    if message.content.lower().startswith('!moeda'):
        if message.author.id == 79943294200630478:
            choice = random.randint(1, 2)

            if choice == 1:
                await message.add_reaction('😢')
            if choice == 2:
                await message.add_reaction('😢')
        else:
            await message.channel.send(
                f"SEM PERMISSÃO, user do id: {message.author.id}"
            )


# Comando básico usando o prefixo configurado
@client.command(name='diga')
async def diga(ctx, *, mensagem):
    await ctx.send(mensagem)

client.run('MTE4OTMzMDMyMDM5MTE0NzY2MA.GembW2.lKZTMlk9f--spS7Yx2eFK9DKlBorUJ0JB1dKWk')  # noqa: E501
