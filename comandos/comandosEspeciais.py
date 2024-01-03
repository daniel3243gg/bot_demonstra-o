from discord.ext import commands
import asyncio
import bleach
import discord 
from comandos.funcoesUteis.classeEmail import EmailsFacil
class ComandosEspeciais(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name='email')
    async def email(self, ctx):
        info_login = []
        info_envio = []
        info_destinos = []
        mensagem_topo = await ctx.send('POR FAVOR INSIRA SUAS INFORMAÇOES DE LOGIN NO SEGUINTE FORMATO ')
        embed = discord.Embed(
            description='''
            **<smtpServer> <smtpPort> <smtpUseremail> <smtpSenha>**\n
            <smtpServer> sendo seu servidor SMTP o padrão é smtp.gmail.com\n
            <smtpPort> sendo sua porta o padrão é 587\n
            <smtpUseremail> sendo seu email de envio \n
            <smtpSenha> sendo seu token que você ganha quando ativa verificação de duas etapas da conta email
            ''',
            color=discord.Color.blue(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
       
            mensagem_usuario_login = await self.bot.wait_for('message', timeout=60, check=check)

        
        except asyncio.TimeoutError:
            await mensagem_usuario_destinatarios.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')

        info_login = mensagem_usuario_login.content.split(' ')
        if  len(info_login) != 3:
            await ctx.send(len(info_login))
            await ctx.send('FALTO UM ARGUMENTO')
            return
        if '@' not in info_login[0]:
            await ctx.send('smtpServer NAO É VALIDO')
        if not info_login[1].isdigit():
            await ctx.send('smtpPort esta incorreto')
        if '@' not in info_login[2]:
            await ctx.send('SMTPUSEREMAIL nao é um email valido')

        await mensagem_usuario_login.delete()
        await mensagem_embed.delete()
        await mensagem_topo.delete()


#destinos
        
        mensagem_topo = await ctx.send('POR FAVOR INFORME PARA QUEM ENVIAR NO SEGUINTE FORMATO')
        embed = discord.Embed(
            description='''
            **<destinatario> <destinatario> <destinatario> **\n
            ''',
            color=discord.Color.red(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
            mensagem_usuario_destinatarios = await self.bot.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            await mensagem_usuario_destinatarios.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')

        
        await mensagem_usuario_destinatarios.delete()
        await mensagem_embed.delete()
        await mensagem_topo.delete()
        info_destinos = mensagem_usuario_destinatarios.content.split()
        for destinatario in info_destinos:
            if '@' not in destinatario:
                await ctx.send(f'{destinatario}, EMAIL INVALIDO')



#infor login
        
        mensagem_topo = await ctx.send('POR FAVOR INFORME INFORMARÇOES DE ENVIO')
        embed = discord.Embed(
            description='''
            **<assunto do email> <template do email>**\n
            <template do email> sendo a sua mensagem em formatado html
            ''',
            color=discord.Color.blue(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
       
            mensagem_usuario_envio = await self.bot.wait_for('message', timeout=60, check=check)

            
        except asyncio.TimeoutError:
            await mensagem_usuario_destinatarios.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')


        await mensagem_usuario_envio.delete()
        await mensagem_embed.delete()  
        await mensagem_topo.delete()
        info_envio = mensagem_usuario_envio.content.split()
        if  len(info_envio) != 1 :
            await ctx.send('FALTA ARGUMENTO')
        try:
        
            cleaned_html = bleach.clean(info_envio[1], tags=[], attributes={})
        except bleach.exceptions.ValidationError:
            await ctx.send('TEMPLATE HTML INVALIDO')


#usando as informaçoes

        Email = EmailsFacil()
        await Email.setInfoLogin(info_login[0],info_login[1],info_login[2],info_login[3])       
        await Email.setInfoDest(info_destinos,mensagem_usuario_envio[0])
        await Email.setTemplate(mensagem_usuario_envio[1])
        await Email.enviar()

