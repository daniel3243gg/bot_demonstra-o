import discord

def embedRonda():
        url = 'https://i.pinimg.com/originals/ed/24/92/ed2492a95b2bd98d0d73cec490bc37cc.gif'
        embedcon = discord.Embed(
                    title="Comandos do Ronda",
                    color=discord.Color.blue(),  # Cor do embed
                )
        msg = '''Cria a partida, si nao for definido nenhum valor sera criado
                    uma partida simples valendo 50 Coins, caso queira uma partida com aposta fixa deve ser
                    usado da seguinte maneira:
                    ex: ronda ronda <valor da aposta>
                    '''
        msg2 = ''' cria uma partida livre que cada jogador pode decidir quanto apostar.'''

        embedcon.add_field(name="?ronda ronda", value=msg, inline=True)
        embedcon.add_field(name="?ronda livre", value=msg2, inline=False)
        embedcon.add_field(name="?ronda livre", value='sasassa', inline=False)

        embedcon.set_thumbnail(url=url)

        return embedcon


def embedRondaJogar(ctx, aposta: str, users: list = None , autor=None):
    embedcon = discord.Embed(
        title="Partida de Ronda",
        color=discord.Color.green()
    )
    if autor: 
        embedcon.add_field(name="Criador", value=f"<@{autor}>", inline=True)
    else:
        embedcon.add_field(name="Criador", value=f"<@{ctx.author.id}>", inline=True)
    embedcon.add_field(name="Aposta", value=aposta, inline=False)
    if users:
        print(users)
        users_mention = '\n'.join([f'<@{user.id}>' for user in users])
        embedcon.add_field(name="Jogadores", value=users_mention, inline=False)

    embedcon.add_field(name='Max de jogadores', value= '10',inline=False )
    return embedcon

def embedRondaAbortar(ctx):
    url = 'https://i.gifer.com/origin/2b/2bef5dcb100766198394e5bd1bcff395_w200.gif'
    embedcon = discord.Embed(
        title="Partida de Ronda",
        description='PARTIDA DESTRUIDA PELO DONO!!!' ,
        color=discord.Color.red()
    )
    author_mention = f"<@{ctx.author.id}>"
    embedcon.add_field(name='Dono', value=author_mention, inline=True)
    embedcon.set_thumbnail(url=url)
    return embedcon


def embedRondaJogarBotoes(ctx, aposta: str, autor=None, users: list = None ):
    embedcon = discord.Embed(
        title="Round de ronda",
        color=discord.Color.green()
    )
    if autor: 
        embedcon.add_field(name="Criador", value=f"<@{autor}>", inline=True)
    else:
        embedcon.add_field(name="Criador", value=f"<@{ctx.author.id}>", inline=True)
    embedcon.add_field(name="Valor da partida", value=aposta, inline=False)
    if users:
        users_mention = '\n'.join([f'<@{user['jogador']}>' for user in users])
        embedcon.add_field(name="Jogadores do round", value=users_mention, inline=False)

    return embedcon

def embedRondaVencedor(venc,valor,dic):
     
    embedcon = discord.Embed(
        title=f'GANHOUUUUUUUU!',
        color=discord.Color.green(),
        description= f'GANHO: {valor}'
    )
    if venc == 666:
        embedcon.add_field(name="Vencedor:",value=f'<@{venc}>', inline=False)
    else:
        embedcon.add_field(name="Vencedor:",value=f'O BOT VENCEU', inline=False)

    embedcon.add_field(name="CARTA DA MESA:",value='--------------------', inline=False)
    embedcon.set_image(url=dic[0]['carta'])

    return embedcon


     


