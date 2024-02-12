import random
import secrets

import discord
from discord.ext import commands

from comandos.Utils.interatividade.botoes import Desistir
from comandos.Utils.xadrez import Xadrez

"""
JOGO DE XADREZ
Esse comando e divido entre o 'Front' que essa parte onde ocorre a logica do
jogo com o usuario do comando e 'back onde ocorre a logica da lib CHESS com o
sestema
"""


class XadrezJogo(commands.Cog):
    def __init__(self, bot):
        """
        CONSTRUTOR DA CLASSE

        Args:
            bot (discord.py): Instancia as conexao com a lib do discord.py
            restante dos argumentos sao Nones para criar os atributos da
            classe(comando).

            users = é o ID dos usuarios que estao jogado;
            user_color = é a sua cor;
            user_name = é o nick do discord dos player;
            token = é o token da partida;
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
        """
        XADREZ

        Args:
            Comando que cria a partida e seta o usuario1
            tags: </inicio> </comando> </envia>
        """

        self.token = secrets.token_hex(2)  # lib que gera TOKENS
        self.user1 = ctx.author.id
        self.user1_name = ctx.author.display_name

        embed = discord.Embed(
            description=f'''
            **JOGO CRIADO**\n
            COD da partida: {self.token}
            <@{self.user1}>
            ''',
            color=discord.Color.darker_grey(),  # Cor do embed
            )
        await ctx.send(embed=embed, delete_after=110)

    @commands.command(name='entrar_xadrez')
    async def EntrarXadrez(self, ctx, arg):
        """
        EntrarXadrez

        Args:
        arg (str): Uma string que contém o TOKEN;
        Comando onde valida o token é seta o usuario2 porem não é aqui que é
        feita a conexao com o 'back' ela chama o metodo iniciar().

        Tags: </comando> </envia> </validacao>
        """

        arg.strip()
        if arg == self.token:
            self.user2 = ctx.author.id
            self.user2_name = ctx.author.display_name

            embed = discord.Embed(
                description=f'''
                **<@{self.user2}>* entrou na partida de <@{self.user1}>**
                ''',
                color=discord.Color.fuchsia(),  # Cor do embed
            )

            await ctx.send(embed=embed)
            await self.iniciar(ctx)
            return
        else:
            embedcon = discord.Embed(
                description='''**Token invalido**''',
                color=discord.Color.red(),  # Cor do embed
            )
            await ctx.send(embed=embedcon)
            return

    async def iniciar(self, ctx):
        """
        Iniciar

        Args:
        É chamada pelo comando EntrarXadrez() aqui é onde acontece
        realmente a conexao com o 'back' é começa a partida faz a validação
        se contém dois player é depois seta as cores aleratoriamente de
        cada um dos player é gera a primeria imagem.

        Tags: </validacao> </metodo> </envia> </conexao> </instancias>
        """

        if self.user1 and self.user2:
            seq = ['preto', 'branca']

            # Seleciona aleratoriamente um valor da lista seq e depois para
            # para o user1.
            resp = random.choice(seq=seq)

            self.user1_color = resp

            # Seta o valor contrario do user1 no user2
            self.user2_color = 'branca' if resp == 'preto' else 'preto'
            self.chess = Xadrez()
            embedconclusao = discord.Embed(
                description=f'''
                **INICIADO!**
                BRANCAS - <@{self.user2 if self.user1_color == 'preto' else self.user1 }>\
                \nPRETAS - <@{self.user2 if self.user1_color != 'preto' else self.user1 }>\
                \n**As brancas começam!**''',  # noqa: E501
                color=discord.Color.fuchsia(),  # Cor do embed  # type: ignore
            )

            await ctx.send(embed=embedconclusao)
            image_bytes = self.chess.gerarImagem()
            image_bytes.seek(0)

            # Gera a imagem em bytes é envia para o discord.
            await ctx.send(
                file=discord.File(
                    image_bytes, filename='tabuleiro_xadrez.png'
                )
            )
            return
        return

    @commands.command(name='mover')
    async def mover(self, ctx, arg=None):
        """
        MOVER
        O comando mais complexo com varias validaçoes. contendo 6 validações
        sendo elas:

        1 - Verifica se não contém argumentos se contém ele ativa o resto das
        validações se não retorna uma mensagem ao user;
        2- Verificação se é uma partida nova ou não para setar o jogador atual;
        3- Verifica se existem os dois jogadores;
        4- Verificação de posição válida;
        5- Verifica se o jogador está na sua vez;
        6 - Verifica se o jogo acabou;
        7 - Verifica se o jogo esta em check.

        Tags: </validacao> </comando> </envia> </imagem>
        """

        if arg != None:  # noqa: E711
            con = 0
            arg.strip()
            arg.lower()

            # Validação 1
            if con < 1:
                jogador_atual = self.user1 if self.user1_color == 'branca' else self.user2  # noqa: E501

            # Validação 2
            if self.user1 and self.user2:
                # Validação 3
                if self.chess.movimento_legal(arg):  # type: ignore
                    # Validação 4
                    if ctx.author.id == jogador_atual:  # type: ignore
                        con = 3
                        self.chess.movimentar(arg)  # type: ignore
                        self.user1, self.user2 = self.user2, self.user1

                        image_bytes = self.chess.gerarImagem()  # type: ignore
                        image_bytes.seek(0)

                        await ctx.send(file=discord.File(
                                image_bytes, filename='tabuleiro_xadrez.png'
                            ))

                        # Validação 5
                        if self.chess.is_game_over():  # type: ignore
                            embedcon = discord.Embed(
                                description=f'''
                                **JOGO FINALIZADO!**
                                RESULTADO: {self.chess.is_game_over()}''',  # type: ignore  # noqa: E501
                                color=discord.Color.blue(),  # Cor do embed
                            )

                            await ctx.send(embed=embedcon)
                            image_bytes = self.chess.gerarImagem()  # type: ignore  # noqa: E501
                            image_bytes.seek(0)

                            await ctx.send(file=discord.File(
                                image_bytes, filename='tabuleiro_xadrez.png'
                            ))

                            await self.finalizar(ctx)
                            return

                        # Validação 6
                        if self.chess.check():  # type: ignore
                            embedcon = discord.Embed(
                                description=f'''
                                **O JOGADOR <@{self.user1 if self.chess.turn == self.chess.WHITE else self.user2}> Esta em cheque**''',  # type: ignore  # noqa: E501
                                color=discord.Color.red(),  # Cor do embed
                            )

                            await ctx.send(embed=embedcon)
                            image_bytes = self.chess.gerarImagem()  # type: ignore  # noqa: E501
                            image_bytes.seek(0)

                            await ctx.send(file=discord.File(
                                image_bytes, filename='tabuleiro_xadrez.png'
                            ))
                    else:
                        embedcon = discord.Embed(
                            description=f'''
                            **NÃO ESTÁ NA SUA VEZ!! <@{ctx.author.id}>**
                            ''',
                            color=discord.Color.red(),  # Cor do embed
                        )

                        await ctx.send(embed=embedcon)
                        return
                else:
                    embedcon = discord.Embed(
                        description='''
                        **Movimento não permitido! Tente novamente.**
                        ''',
                        color=discord.Color.red(),  # Cor do embed
                    )

                    await ctx.send(embed=embedcon)
                    image_bytes = self.chess.gerarImagem()  # type: ignore  # noqa: E501
                    image_bytes.seek(0)

                    await ctx.send(file=discord.File(
                        image_bytes, filename='tabuleiro_xadrez.png'
                    ))
                    return

            else:
                embedcon = discord.Embed(
                    description=f'''
                    **CRIE UMA PARTIDA OU ENCONTRE UM PARCEIRO!! \
                    <@{ctx.author.id}>**
                    ''',
                    color=discord.Color.red(),  # Cor do embed
                )

                await ctx.send(embed=embedcon)
                return

        embedcon = discord.Embed(
            description=f'''
            **Digite um Codigo! <@{ctx.author.id}>**
            ''',
            color=discord.Color.red(),  # Cor do embed
        )
        await ctx.send(embed=embedcon)

    @commands.command(name='desistir')
    async def desistir(self, ctx):
        """
        DESISTIR

        Args:
            Comando para o usuario desistir da partida. Contém 3 validações:

            1 - Verifica se o jogo existe e está ativo (contém jogadores),
                apos isso ele cria uma mensagem com botoes que é instanciado
                com a classe botoes no back;
            2 - Verifica se nenhum botão foi clicado;
            3 - Verifica se retornou TRUE (o jogador desistiu);
            4 (else) - Se caso o jogador resolveu continuar.

            Tags: </validacao> </comando> </envia> </botoes> </conexao>
        """

        # Validação 1
        if self.user1 and self.user2:
            view = Desistir()
            embedcon = discord.Embed(
                description=f'''
                **TEM CERTEZA QUE DESEJA DESISTIR? <@{ctx.author.id}>**
                ''',
                color=discord.Color.red(),  # Cor do embed
            )

            await ctx.send(embed=embedcon, view=view, delete_after=10)
            await view.wait()

            # Validação 2
            if view.value is None:
                embedcon = discord.Embed(
                    description='''
                    **Tempo expirado... Continuando o jogo**
                    ''',
                    color=discord.Color.red(),  # Cor do embed
                )

                await ctx.send(embed=embedcon, delete_after=10)

            # Validação 3
            elif view.value:
                await self.finalizar(ctx)

            # Validação 4
            else:
                embedcon = discord.Embed(
                    description='''**Continuando o jogo!**''',
                    color=discord.Color.red(),  # Cor do embed
                )

                await ctx.send(embed=embedcon, delete_after=10)
                return
        else:
            embedcon = discord.Embed(
                description=f'''
                **Você não esta em um jogo ativo. <@{ctx.author.id}>**
                ''',
                color=discord.Color.red(),  # Cor do embed
            )

            await ctx.send(embed=embedcon, delete_after=10)

    async def finalizar(self, ctx):
        """
        FINALIZAR

        Args:
            Método que é chamado quando o jogo acaba ou o jogador resolveu
            desistir, ele limpa a classe do comando de xadrez.

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
