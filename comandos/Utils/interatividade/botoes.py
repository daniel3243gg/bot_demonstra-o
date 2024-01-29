# from discord.ext import commands

import discord


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
