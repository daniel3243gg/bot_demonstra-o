import discord

def ComandosCoins():
        

        url = 'https://i.pinimg.com/originals/63/89/fa/6389fa22ed7653c40570c98b03764afc.gif'
        embedcon = discord.Embed(
                    title="Comandos de coins",
                    color=discord.Color.blue(),  # Cor do embed
                )
        msg = '''  Consulta a quantidade de coins disponiveis. '''
        msg2 = ''' Transfere uma quantidade dos seus coins para outro usuario'''

        embedcon.add_field(name="?coins coins", value=msg, inline=True)
        embedcon.add_field(name="?coins trans [quem] [quantidade]", value=msg2, inline=False)
        embedcon.add_field(name="?coins consul [quem]", value='Consulta a quantidade coins de um player', inline=False)

        embedcon.set_thumbnail(url=url)

        return embedcon