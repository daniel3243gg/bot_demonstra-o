from discord.ext import commands
import asyncio
import bleach
import discord 
from comandos.Utils.classeEmail import EmailsFacil
class ComandosEspeciais(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name='email')
    async def email(self, ctx):
        user_id = ctx.author.id
        info_login = []
        info_envio = []
        info_destinos = []
        mensagem_topo = await ctx.send('POR FAVOR INSIRA SUAS INFORMAÇOES DE LOGIN NO SEGUINTE FORMATO ')
        embed = discord.Embed(
            description='''
            **<smtpServer> <smtpPort> <smtpUseremail>**\n
            <smtpServer> sendo seu servidor SMTP o padrão é smtp.gmail.com\n
            <smtpPort> sendo sua porta o padrão é 587\n
            <smtpUseremail> sendo seu email de envio \n
            
            ''',
            color=discord.Color.blue(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
       
            mensagem_usuario_login = await self.bot.wait_for('message', timeout=60, check=check)

        
        except asyncio.TimeoutError:
            await mensagem_usuario_login.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')

        info_login = mensagem_usuario_login.content.split(' ')
        if  len(info_login) != 3:
            await ctx.send(f'FALTA ARGUMENTOS')
            return
        if '.' not in info_login[0]:
            await ctx.send(f'{info_login[0]} smtpServer NAO É VALIDO')
            return
        if not info_login[1].isdigit():
            await ctx.send(f'{info_login[1]} smtpPort esta incorreto')
            return   
        if '@' not in info_login[2].strip():
            await ctx.send(f'{info_login[2]} SMTPUSEREMAIL nao é um email valido')
            return
        await mensagem_usuario_login.delete()
        await mensagem_embed.delete()
        await mensagem_topo.delete()


#destinos
        
        mensagem_topo = await ctx.send('POR FAVOR INFORME PARA QUEM ENVIAR NO SEGUINTE FORMATO')
        embed = discord.Embed(
            description='''
            **<destinatario> <destinatario> <destinatario> **\n
            ''',
            color=discord.Color.blue(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
            mensagem_usuario_destinatarios = await self.bot.wait_for('message', timeout=60, check=check)
            info_destinos = mensagem_usuario_destinatarios.content.split()

        except asyncio.TimeoutError:
            await mensagem_usuario_destinatarios.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')

        
        await mensagem_usuario_destinatarios.delete()
        await mensagem_embed.delete()
        await mensagem_topo.delete()
        for destinatario in info_destinos:
            if '@' not in destinatario:
                await ctx.send(f'{destinatario}, EMAIL INVALIDO')



#infor envio
        mensagem_usuario_envio = None
        mensagem_topo = await ctx.send('POR FAVOR INFORME INFORMARÇOES DE ENVIO')
        embed = discord.Embed(
            description='''
            **<assunto do email>,<quantidades de envio>**\n
            **\n
            USE AS VIRGULAS PARA SEPARAR 
            ''',
            color=discord.Color.blue(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
       
            mensagem_usuario_envio = await self.bot.wait_for('message', timeout=60, check=check)
            info_envio = mensagem_usuario_envio.content.split(',')

            
        except asyncio.TimeoutError:
            await mensagem_usuario_envio.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')


        await mensagem_usuario_envio.delete()
        await mensagem_embed.delete()  
        await mensagem_topo.delete()
        qnt = int(info_envio[1])
        if len(info_envio) < 1:
            await ctx.send('FALTA ARGUMENTO')


#info template
        mensagem_usuario_template = ''''''
        mensagem_topo = await ctx.send('POR FAVOR INFORME O TEMPLATE')
        embed = discord.Embed(
            description='''
            **<TEMPLATE HTML>**\n
                seu template deve ser um html.**\n
            
            ''',
            color=discord.Color.blue(),  # Cor do embed
        )
        mensagem_embed = await ctx.send(embed=embed)
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
       
            mensagem_usuario_template = await self.bot.wait_for('message', timeout=60, check=check)
            info_template = mensagem_usuario_template.content

            
        except asyncio.TimeoutError:
            await mensagem_usuario_template.delete()
            await mensagem_embed.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')

        await mensagem_usuario_template.delete()
        await mensagem_embed.delete()
        await mensagem_topo.delete()
        try:
        
            cleaned_html = bleach.clean(info_template, tags=[], attributes={})
        except bleach.exceptions.ValidationError:
            await ctx.send('TEMPLATE HTML INVALIDO')



#infor senha
        
        mensagem_topo = await ctx.send('POR FAVOR INFORME SEU TOKEN DE LOGIN')
       
        def check(mensagem):
            return mensagem.author == ctx.author and mensagem.channel == ctx.channel

        try:
       
            mensagem_usuario_senha = await self.bot.wait_for('message', timeout=60, check=check)
            info_senha = mensagem_usuario_senha.content

            
        except asyncio.TimeoutError:
            await mensagem_usuario_senha.delete()
            await mensagem_topo.delete()
            await ctx.send('Tempo limite excedido. Tente novamente.')


        await mensagem_usuario_senha.delete()
        await mensagem_topo.delete()
         


#usando as informaçoes

        Email = EmailsFacil()
        await Email.setInfoLogin(info_login[0],info_login[1],info_login[2],info_senha)       
        await Email.setInfoDest(info_destinos,info_envio[0])
        await Email.setTemplate(info_template)
        await Email.enviar(qnt)
        erros = await Email.getErros()
        if erros is not None:
            await ctx.send(f"Erros armazenados na classe:\n{erros}")
        await ctx.send(f"Enviado!! <@{user_id}>")
        


