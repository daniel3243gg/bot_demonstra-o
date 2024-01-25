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
        await ctx.send(embed=embed,delete_after=120)

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
        con = 0
        arg.strip()
        if con < 1 :
            jogador_atual = self.user1 if self.user1_color == 'branca' else self.user2
        if self.user1 and self.user2:
            if self.chess.movimento_legal(arg):
                if ctx.author.id == jogador_atual:
                    con = 3
                    self.chess.movimentar(arg)
                    self.user1, self.user2 = self.user2, self.user1
                    image_bytes = self.chess.gerarImagem()
                    image_bytes.seek(0)
                    await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))
                    if self.chess.is_game_over():
                        embedcon = discord.Embed(
                        description=f'''
                        **JOGO FINALIZADO!**
                        RESULTADO: {self.chess.is_game_over()}
                        ''',
                        color=discord.Color.blue(),  # Cor do embed
                        )
                        await ctx.send(embed=embedcon)
                        image_bytes = self.chess.gerarImagem()
                        image_bytes.seek(0)
                        await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))
                        return

                    if self.chess.check():  
                        embedcon = discord.Embed(
                            description=f'''
                            **O JOGADOR @{self.user1_name if self.chess.turn == chess.WHITE else self.user2_name} Esta em cheque**
                            ''',
                            color=discord.Color.red(),  # Cor do embed
                        )
                        await ctx.send(embed=embedcon)
                        image_bytes = self.chess.gerarImagem()
                        image_bytes.seek(0)
                        await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))
                else:
                    embedcon = discord.Embed(
                    description=f'''
                    **NAO ESTA NA SUA VEZ!! @{ctx.author.display_name} **
                    ''',
                    color=discord.Color.red(),  # Cor do embed
                    )
                    await ctx.send(embed=embedcon)
                    return     
            else:
                embedcon = discord.Embed(
                description='''
                **Movimento nao permitido! Tente novamente.**
                ''',
                color=discord.Color.red(),  # Cor do embed
                )
                await ctx.send(embed=embedcon)
                image_bytes = self.chess.gerarImagem()
                image_bytes.seek(0)
                await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))
                return
        else:
            embedcon = discord.Embed(
            description='''
            **CRIE UMA PARTIDA OU ENCONTRE UM PARCEIRO!!**
            ''',
            color=discord.Color.red(),  # Cor do embed
            )
            await ctx.send(embed=embedcon)
            return
        

    @commands.command(name='dessistir')
    async def dessistir(self,ctx):
            view = discord.ui.View()

            button1 = discord.ui.Button(style=discord.ButtonStyle.danger, label='SIM!', custom_id='sim')
            button2 = discord.ui.Button(style=discord.ButtonStyle.success, label='NÃO!', custom_id='nao')
            view.add_item(button1)
            view.add_item(button2)

            embedcon = discord.Embed(
            description='''
            **TEM CERTEZA QUE DESEJA DESSISTIR?**
            ''',
            color=discord.Color.red(),  # Cor do embed
            )
            await ctx.send(embed=embedcon,view=view)
    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        ctx = await self.bot.get_context(interaction)
        if interaction.custom_id == "sim":
            
            await self.finalizar(ctx)

    async def finalizar(self,ctx):
        embedcon = discord.Embed(
            description=f'''
            **Jogo de @{self.user1_name} finalizado.**''',
            color=discord.Color.red(),  # Cor do embed
            )
        await ctx.send(embed=embedcon)
        self.bot = None
        self.user1 = None
        self.user2 = None
        self.user1_color = None
        self.user2_color = None
        self.user1_name = None
        self.user2_name = None
        self.token = None
        del self.chesss
        return