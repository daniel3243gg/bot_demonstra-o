from discord.ext import commands
import discord 
import random 
from comandos.Utils.interatividade.botoes import Dessistir
import secrets
from comandos.Utils.xadrez import Xadrez

"""XJOGO DE XADREZ
Esse comando e divido entre o 'Front' que essa parte onde ocorre a logica do jogo com o usuario do comando e 'back'
onde ocorre a logica da lib CHESS com o sistema. 
"""
class XadrezJogo(commands.Cog):

    def __init__(self, bot):
        """CONSTRUTOR DA CLASSE

        Args:
            bot (discord.py): Instancia as conexao com a lib do discord.py
            restante dos argumentos sao Nones para criar os atributos da classe(comando).
            users = é o ID dos usuarios que estao jogado
            user_color = é a sua cor 
            user_name = é o nick do discord dos player
            token = é o token da partida 
            chess = conexao com o 'back', instancia da classe Xadrez.
        """
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
        """XADREZ

        Args:
            Comando que cria a partida e seta o usuario1
            tags: </inicio> </comando> </envia> 
        """
        self.token = secrets.token_hex(2)#lib que gera TOKENS 
        self.user1 = ctx.author.id
        self.user1_name = ctx.author.display_name
        embed = discord.Embed(
            description=f'''
            **JOGO CRIADO**\n
            COD da partida: {self.token} 
            <@{self.user1}>
            ''',
            color= discord.Color.darker_grey(),  # Cor do embed
            )
        await ctx.send(embed=embed,delete_after=110)

    @commands.command(name='entrar_xadrez')
    async def EntrarXadrez(self, ctx, arg):
        """EntrarXadrez

        Args:
            arg (str): uma string que contem o TOKEN 
        Comando onde valida o token é seta o usuario2 porem nao é aqui que é feita a conexao com o 'back'
        ela chama o metodo iniciar().

        Tags: </comando> </envia> </validacao>
        """
        arg.strip()
        if arg == self.token:
            self.user2 = ctx.author.id
            self.user2_name = ctx.author.display_name
            embed = discord.Embed(
            description= f'''
            **<@{self.user2}>* entrou na partida de <@{self.user1}>**
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
            """Iniciar

            Args:
            é chamada pelo comando EntrarXadrez() aqui é onde acontece realmente a conexao com o 'back' é começa a partida
            faz a validação si contem dois player é depois seta as cores aleratoriamente de cada um dos player 
            é gera a primeria imagem.

            Tags: </validacao> </metodo> </envia> </conexao> </instancias>
                """
            if self.user1 and self.user2:
                seq = ['preto','branca']
                resp = random.choice(seq=seq)# seleciona aleratoriamente um valor da lista seq é depois para para o user1
                self.user1_color = resp
                self.user2_color = 'branca' if resp == 'preto' else 'preto'#seta o valor contrario do user1 no user2
                self.chess = Xadrez()
                embedconclusao = discord.Embed(
                description=f'''
                **INICIADO!**
                BRANCAS - <@{self.user2 if self.user1_color == 'preto' else self.user1 }> 
                PRETAS - <@{self.user2 if self.user1_color != 'preto' else self.user1 }> 
                brancas começam! 
                ''',
                color=discord.Color.fuchsia(),  # Cor do embed
                )

                await ctx.send(embed=embedconclusao)
                image_bytes = self.chess.gerarImagem()
                image_bytes.seek(0)
                await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))#gera a imagem em bytes é envia para o discord.
                return 

            return
    
    @commands.command(name='mover')
    async def mover(self,ctx,arg):
        """MOVER
        O comando mais complexo com varias validaçoes. contendo 6 validações sendo elas 
        1- Verificação si é uma partida nova ou nao para setar o jogador atual
        2- Verifica si existe os dois jogadores
        3- Verificação de posição válida
        4- verifica si o jogador esta na vez
        5 - verifica si o jogo acabou 
        6 - verifica si o jogo esta em check 

        Tags: </validacao> </comando> </envia> </imagem>
        """
        con = 0
        arg.strip()
        if con < 1 : #validação 1
            jogador_atual = self.user1 if self.user1_color == 'branca' else self.user2
        if self.user1 and self.user2: #validação 2
            if self.chess.movimento_legal(arg): #validação 3
                if ctx.author.id == jogador_atual:#validação 4
                    con = 3
                    self.chess.movimentar(arg)
                    self.user1, self.user2 = self.user2, self.user1
                    image_bytes = self.chess.gerarImagem()
                    image_bytes.seek(0)
                    await ctx.send(file=discord.File(image_bytes, filename='tabuleiro_xadrez.png'))
                    if self.chess.is_game_over(): #validação 5
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
                        self.finalizar(ctx)
                        return
                    if self.chess.check(self.chess.get_turn):   #validação 6
                        embedcon = discord.Embed(
                            description=f'''
                            **O JOGADOR <@{self.user1 if self.chess.turn == self.chess.WHITE else self.user2}> Esta em cheque**
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
                    **NAO ESTA NA SUA VEZ!! <@{ctx.author.id}> **
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
            description=f'''
            **CRIE UMA PARTIDA OU ENCONTRE UM PARCEIRO!! <@{ctx.author.id}>**
            ''',
            color=discord.Color.red(),  # Cor do embed
            )
            await ctx.send(embed=embedcon)
            return
        

    @commands.command(name='dessistir')
    async def dessistir(self,ctx):
            """Dessistir

        Args:
            Comando para o usuario dessistir da partida contem 3 validações 
            1 - verifica si o jogo existe é esta ativo(contem jogadores)
                apos isso ele cria uma mensagem com botoes que é instanciado com classe botoes no back.
            2 - verifica si nenhum botao foi clickado
            3 - verifica si retornou TRUE (o jogador dessistiu)
            4(else) - si caso o jogador resolveu continuar 

            Tags: </validacao> </comando> </envia> </botoes> </conexao>
        """
            if self.user1 and self.user2:#validação 1
                view = Dessistir()
                embedcon = discord.Embed(
                description=f'''
                **TEM CERTEZA QUE DESEJA DESSISTIR? <@{ctx.author.id}> **
                ''',
                color=discord.Color.red(),  # Cor do embed
                )
                await ctx.send(embed=embedcon,view=view,delete_after=10)
                await view.wait()
                if view.value is None: #validação 2
                    embedcon = discord.Embed(
                    description='''
                    **Tempo expirado... Continuando o jogo**
                    ''',
                    color=discord.Color.red(),  # Cor do embed
                    )
                    await ctx.send(embed=embedcon,delete_after=10)

                elif view.value:   #validação 3
                    await self.finalizar(ctx)
                else: #validação 4
                    
                    embedcon = discord.Embed(
                    description='''
                    **Continuando o jogo!**
                    ''',
                    color=discord.Color.red(),  # Cor do embed
                    )
                    await ctx.send(embed=embedcon,delete_after=10)

                    return
            else:            
                    
                    embedcon = discord.Embed(
                    description=f'''
                    **Você nao esta em um jogo ativo. <@{ctx.author.id}>**
                    ''',
                    color=discord.Color.red(),  # Cor do embed
                    )
                    await ctx.send(embed=embedcon,delete_after=10)

    async def finalizar(self,ctx):
        """finalizar

        Args:
            Metodo que é chamado quando o jogo acaba ou jogador resolveu dessistir, ele limpa a classe do comando de xadrez.
            
            Tags: </fim> </metodo> </envia>
        """
        embedcon = discord.Embed(
            description=f'''
            **Jogo de <@{self.user1}> finalizado.**''',
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
        self.chesss = None
        return