
import discord
from discord.ext import commands
from comandos.Utils.interatividade.botoes import Desistir
from comandos.Utils.xadrez import Xadrez
from comandos.Utils.ronda import Ronda
from comandos.Utils.interatividade.botoes import EntrarRonda
from comandos.Utils.interatividade.botoes import CartasRonda
from comandos.Utils.interatividade.botoes import ContinuarRound
from comandos.Utils.interatividade.embeds import embeds_ronda

class RondaJogo(commands.Cog):
    def __init__(self, bot):
        """
onexao com o 'back', instancia da classe Xadrez.
        """

        self.bot = bot
        self.mao = []
        self.jogo = None

    @commands.group(name='ronda', invoke_without_command=True)
    async def ronda_grupo(self, ctx):
        await ctx.send("Bem vindo ao ronda!")
        await ctx.send(embed=embeds_ronda.embedRonda())



    async def callback_destruir(destruir):
        print("A partida foi destruída:", destruir)

    @ronda_grupo.command()
    async def ronda(self, ctx, aposta=None):
        embed_message = await ctx.send(embed=embeds_ronda.embedRondaJogar(ctx, '50'))
        botcarta = None
        # Em seguida, associe a view à mensagem
        async def callback_destruir(destruir):
          await embed_message.edit(embed=embeds_ronda.embedRondaAbortar(ctx), view=None)
          return
            
        view = EntrarRonda(embed_message, ctx.author.id, callback_destruir)
        await embed_message.edit(view=view)
        await view.wait()
        self.jogo = Ronda()
        await self.jogo.adicionarJogadores(view.value)
        cartas = await self.jogo.distruibuirCartas()
        if len(cartas)==2:
            botcarta = cartas[1]
        resp = True
        while resp:
            msg = await ctx.send(embed=embeds_ronda.embedRondaJogarBotoes(ctx,0))
            if botcarta != None:
                viewRond = CartasRonda(msg,cartas, ctx.author.id,botcarta)
            else:
                viewRond = CartasRonda(msg,cartas, ctx.author.id)

            await msg.edit(view=viewRond)
            await viewRond.wait()
            resp = await self.roundRonda(ctx,viewRond.value,viewRond.valor, ctx.author.id)
        
        #await ctx.send()
    async def roundRonda(self,ctx,users,valor, dono):
        #if len(users) == 1:
         #  users.append()
        result = await self.jogo.jogarSimples(users)
        if result is not None:

            if result['resultado']:
                msg = await ctx.send(embed=embeds_ronda.embedRondaVencedor(valor=valor, dic=users, venc=result['jogador']))
                return False

        else: 
            msg = await ctx.send(f'O jogador <@{result["jogador"]}> nao tem saldo suficiente. A partida foi finalizada...')
            return False
        

                    

            

