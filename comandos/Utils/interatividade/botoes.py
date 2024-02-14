# from discord.ext import commands
from comandos.Utils.interatividade.embeds import embeds_ronda
import discord
import io
import aiohttp

class Desistir(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their
    # choice.
    @discord.ui.button(label='Desistir', style=discord.ButtonStyle.red)
    async def desistir(
        self, interaction: discord.Interaction, button: discord.ui.Button
            ):
        await interaction.response.send_message(
            'Desistindo...', ephemeral=True, delete_after=2
        )
        self.value = True
        self.stop()

    @discord.ui.button(label='Continuar', style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):

        await interaction.response.send_message(
            'Continuando...', ephemeral=True, delete_after=2
        )
        self.value = False
        self.stop()


class EntrarRonda(discord.ui.View):
    def __init__(self, embedm, autor, callback=None):
        super().__init__()
        self.value = []
        self.autor = autor
        self.users = []
        self.cont = 0
        self.destruir = False
        self.callback = callback
        self.embed_message = embedm
    @discord.ui.button(label='Entrar', style=discord.ButtonStyle.green)
    async def entrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.value:
         await interaction.response.send_message(content='Voce ja esta na partida', ephemeral=True, delete_after=5)
        else: 
            await interaction.response.send_message(content='Você entrou!', ephemeral=True, delete_after=5)
            
            self.value.append(interaction.user.id)
            self.users.append(interaction.user)
            # Atualiza a embed com a nova lista de usuários
            await self.update_embed()
            self.cont += 1
            if self.cont >= 10:
                await interaction.response.send_message(content='Partida iniciada! Numero de jogadores Maximo atingido')          
                self.stop()
            
    @discord.ui.button(label='Iniciar', style=discord.ButtonStyle.blurple)
    async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.autor:
            await interaction.response.send_message(content='Você nao é o dono!', ephemeral=True, delete_after=5)
        else:
            if len(self.value) > 0:
                await interaction.response.send_message(content='Partida iniciada!')
                if len(self.value) == 1:
                   # dic = {}
                    self.value.append(666)   
   
                self.stop()
            else:
                await interaction.response.send_message(content='Não tem jogadores!!', ephemeral=True, delete_after=5)

        
    async def call_callback(self):

        if self.callback:
            await self.callback(self.destruir)
   
    @discord.ui.button(label='Destruir a partida!', style=discord.ButtonStyle.red)
    async def destruir_partida(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.autor:
            await interaction.response.send_message(content='Você acabou com a partida!', ephemeral=True, delete_after=5)
            self.destruir = True
            await self.call_callback()
        else:
            await interaction.response.send_message(content='Você não é o dono da partida!', ephemeral=True, delete_after=5)

    async def update_embed(self):
        # Obtém a mensagem original
        message = await self.embed_message.channel.fetch_message(self.embed_message.id)

        # Cria uma nova embed com a lista atualizada de usuários
        embed = embeds_ronda.embedRondaJogar(message, '50', self.users, self.autor)

        # Edita a mensagem original para refletir a nova embed
        await message.edit(embed=embed)


class CartasRonda(discord.ui.View):
    def __init__(self, embedm,maos=None, autor=None, maobot=None):
        super().__init__()
        self.maos = maos
        self.value = []
        self.url = None
        self.maobot = maobot
        self.autor = autor
        self.valor= 0 
        self.saldo = None
        self.embed_message = embedm


    @discord.ui.button(label='Participar', style=discord.ButtonStyle.green)
    async def participar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.value:
            await interaction.response.send_message(content='Voce ja esta no round', ephemeral=True, delete_after=5)
        else: 
            await interaction.response.send_message(content='Você Escolheu jogar!', ephemeral=True, delete_after=5)
            for mao in self.maos:
                if int(mao['jogador']) == interaction.user.id:
                    self.value.append(mao)

            await self.update_embed()

    @discord.ui.button(label='Iniciar mesa', style=discord.ButtonStyle.red)
    async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.autor:
            await interaction.response.send_message(content='Você nao é o dono!', ephemeral=True, delete_after=5)
        else:
            if len(self.value) > 0:
                await interaction.response.send_message(content='Round Iniciado')
                if self.maobot != None:
                    self.value.append(self.maobot)
                self.stop()
            else:
                await interaction.response.send_message(content='Não tem jogadores!!', ephemeral=True, delete_after=5)

    @discord.ui.button(label='Vizualizar Carta', style=discord.ButtonStyle.blurple)
    async def vizualizar(self, interaction: discord.Interaction, button: discord.ui.Button):

        for mao in self.maos:
            if int(interaction.user.id) == int(mao['jogador']):
                self.url = mao['carta']
                self.saldo = mao['saldo']

        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    image_bytes = await response.read()
                    image_buffer = io.BytesIO(image_bytes)
                    await interaction.response.send_message(content=f'Seu saldo é: {self.saldo}',file=discord.File(image_buffer, filename="imagem.jpg"), ephemeral= True)
                else:
                    await interaction.response.send_message("Não foi possível obter a imagem.", ephemeral=True)
    async def update_embed(self):
        
        # Obtém a mensagem original
        message = await self.embed_message.channel.fetch_message(self.embed_message.id)

        self.valor = 50*len(self.value)
        # Cria uma nova embed com a lista atualizada de usuários
        embed = embeds_ronda.embedRondaJogarBotoes(message, self.valor , self.autor, self.value)

        # Edita a mensagem original para refletir a nova embed
        await message.edit(embed=embed)

class ContinuarRound(discord.ui.View):
    def __init__(self, dono):
        super().__init__()
        self.value = None
        self.dono = dono
  


    @discord.ui.button(label='Continuar', style=discord.ButtonStyle.green)
    async def continuar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.dono:
            await interaction.response.send_message('A partida continua...')
            self.value = True
            self.stop()

    @discord.ui.button(label='Parar', style=discord.ButtonStyle.red)
    async def parar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.dono:
            await interaction.response.send_message('A partida foi finalizada!...')
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('Você não é o dono!', ephemeral=True)