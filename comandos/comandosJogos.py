from discord.ext import commands


class Xadrez(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='criar')
    async def criar(self, ctx):