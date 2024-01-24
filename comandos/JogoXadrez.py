from discord.ext import commands
import discord 
import random 
import io
import asyncio
import secrets
from comandos.Utils.xadrez import Xadrez
class XadrezJogo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.user1 = None
        self.user2 = None
        self.user1_color = None
        self.user2_color = None
        self.user1_name = None
        self.user2_name = None
        self.token = None
        self.chess = None
    @commands.command(name='criar_partida_de_xadrez')
    async def Xadrez(self, ctx):
        self.token = secrets.token_hex(2)
        self.user1 = ctx.author.id
        self.user1_name = ctx.author.display_name
        embed = discord.Embed(
            description=f'''
            **JOGO CRIADO**\n
            COD da partida: {self.token}
            ''',
            color= discord.Color.darker_grey(),  # Cor do embed
            )
        await ctx.send(embed=embed)

    @commands.command(name='entrar_xadrez')
    async def EntrarXadrez(self, ctx, arg):
        arg.strip()
        if arg == self.token:
            self.user2 = ctx.author.id
            self.user2_name = ctx.author.display_name
            embed = discord.Embed(
            description= f'''
            **{self.user2_name}* entrou na partida de {self.user1_name}**
            ''',
            color=discord.Color.fuchsia(),  # Cor do embed
            )
            await ctx.send(embed=embed)
            await self.iniciar(ctx)
            return
        else:
            embedcon = discord.Embed(
            description='''
            **Token invalido**
            ''',
            color=discord.Color.red(),  # Cor do embed
            )
            await ctx.send(embed=embedcon)
            return
    
    async def iniciar(self,ctx):
            
            if self.user1 and self.user2:
                seq = ['preto','branca']
                resp = random.choice(seq=seq)
                self.user1_color = resp
                self.user2_color = 'branca' if resp == 'preto' else 'preto'
                self.chess = Xadrez()
                embedconclusao = discord.Embed(
                description=f'''
                **INICIADO!**
                BRANCAS - {self.user2_name if self.user1_color == 'preto' else self.user1_name } 
                PRETAS - {self.user2_name if self.user1_color != 'preto' else self.user1_name } 
                brancas começam! 
                ''',
                color=discord.Color.fuchsia(),  # Cor do embed
                )

                await ctx.send(embed=embedconclusao)
                image_bytes = self.chess.gerarImagem()
                image_bytes.seek(0)
                await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))
                return 

            return
    @commands.command(name='mover')
    async def mover(self,ctx,arg):
        if self.user1 and self.user2:
            exit
        else:
            embedcon = discord.Embed(
            description='''
            **CRIE UMA PARTIDA OU ENCONTRE UM PARCEIRO!!**
            ''',
            color=discord.Color.red(),  # Cor do embed
            )
            await ctx.send(embed=embedcon)
            return
