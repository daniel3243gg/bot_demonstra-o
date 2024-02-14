from discord.ext import commands
from comandos.Utils.coins import Coins
import discord
from discord.ext import commands

from comandos.Utils.classeEmail import EmailsFacil
from comandos.Utils.interatividade.embeds.embed_coins import ComandosCoins


class CoinsUser(commands.Cog):
    def __init__(self, bot):
        """
        onexao com o 'back', instancia da classe Xadrez.
        """
        self.bot = bot
        self.id = None



    @commands.group(name='coins', invoke_without_command=True)
    async def coins_grupo(self, ctx):
        await ctx.send("Comando dos coins")
        await ctx.send(embed=ComandosCoins())



    @coins_grupo.command()
    async def coins(self, ctx):
        coins = Coins()
        self.id= ctx.author.id

        await coins.start(str(self.id))

        resp = await coins.consultarCoins()
        await ctx.send(f"{ctx.author.mention} seu saldo é de: {resp}")



    @coins_grupo.command()
    async def consul(self, ctx, pessoa: discord.Member):
        pessoa_id = pessoa.id
        coins = Coins()
        self.id= ctx.author.id

        await coins.start(str(pessoa_id))

        resp = await coins.consultarCoins()
        await ctx.send(f"Consulta realizada com sucesso{ctx.author.mention}, o saldo de {pessoa.mention} é: {resp}")


    @coins_grupo.command()
    async def trans(self, ctx, pessoa: discord.Member, qnt):
        pessoa_id = pessoa.id
        coins = Coins()
        coins2 = Coins()
        self.id= ctx.author.id
        await coins.start(str(self.id))
        resp = await coins.consultarCoins()
        if int(resp) < int(qnt):
            await ctx.send(f"Saldo insuficiente {ctx.author.mention}")
        else:
            if self.id == pessoa_id :
                await ctx.send(f"Você não pode transferir para você né!!! {ctx.author.mention}")
            else:
                await coins.removerCoins(int(qnt))
                await coins2.start(str(pessoa_id))
                await coins2.inserirCoins(int(qnt))
                await ctx.send(f"Transferencia realizada com sucesso {ctx.author.mention}, {pessoa.mention} recebeu {qnt}")
