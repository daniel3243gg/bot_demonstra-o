import asyncio 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup


class EmailsFacil():
    smtpToken = ''
    message = MIMEMultipart()
    smtpUseremail = ''
    smtpPort = 0
    smtpServer = ''        
    template = """ """
    string = ''
    destinatarios = []  

    @classmethod
    async def setInfoLogin(cls, smtpServer='smtp.gmail.com', smtpPort=587, smtpUseremail='email@gmail.com', smtpSenha='sndmsjdsds'):
        cls.smtpServer = smtpServer
        cls.smtpPort = smtpPort
        cls.smtpUseremail = smtpUseremail
        cls.smtpToken = smtpSenha

    @classmethod
    async def setInfoDest(cls, destinatarios, assunto):
        cls.destinatarios = destinatarios
        cls.message['From'] = cls.smtpUseremail
        cls.message['To'] = ', '.join(destinatarios)
        cls.message['Subject'] = assunto

    @classmethod
    async def setTemplate(cls, template=""" """):
        try:
            soup = BeautifulSoup(template, 'html.parser')
            cls.message.attach(MIMEText(template, 'html'))
            return True
        except Exception as e:
            await cls.setErros('<br>Erro ao processar o template HTML<br>')
            return False

    @classmethod
    async def setErros(cls, erros):
        cls.string += '<br>ERROS DA CLASSE<br>'
        cls.string += erros
        with open("errosClasse.txt", "a") as arquivo:

            arquivo.write("ERROS DA CLASSE:\n")
            arquivo.write(erros + "\n")


    @classmethod
    async def getErros(cls):
        return cls.string

    @classmethod
    async def enviar(cls, qnt=1):
        try:
            server = smtplib.SMTP(cls.smtpServer, cls.smtpPort)
            server.starttls() 
            server.login(cls.smtpUseremail, cls.smtpToken)
            for desti in cls.destinatarios:
                for _ in range(qnt):
                    await asyncio.sleep(2)
                    cls.message.replace_header('To', desti)
                    server.sendmail(cls.smtpUseremail, desti, cls.message.as_string())
            server.quit()
        except smtplib.SMTPException as smtp_error:
            await cls.setErros(f'<br>Erro ao enviar e-mail: {smtp_error}<br>')
        except Exception as e:
           await  cls.setErros(f'<br>Erro inesperado: {e}<br>')



#para testes       
'''
async def main():
    email = EmailsFacil
    await email.setInfoLogin('smtp.gmail.com',587,'daniew600brandao@gmail.com','baxv ejvg rqsw cosi' )
    await email.setInfoDest(['daniew600@gmail.com', 'juninho642.cp@gmail.com'],'OLA MUNDO')
    await email.setTemplate(""" <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Boas-Vindas!</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }

            .container {
                max-width: 600px;
                margin: 20px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            h1 {
                color: #333;
            }

            p {
                color: #666;
            }

            .cta-button {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                background-color: #007BFF;
                color: #fff;
                text-decoration: none;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bem-vindo(a) à nossa comunidade!</h1>
            <p>Olá [Nome],</p>
            <p>Estamos muito felizes em tê-lo(a) conosco. Esperamos que você desfrute da sua experiência e encontre valor em nossa plataforma.</p>
            <p>Fique à vontade para explorar e descobrir todas as funcionalidades que oferecemos.</p>
            <p>Se tiver alguma dúvida ou precisar de ajuda, não hesite em entrar em contato conosco.</p>
            <a href="#" class="cta-button">Começar Agora</a>
            <p>Obrigado mais uma vez e aproveite!</p>
            <p>Atenciosamente,<br>Equipe [Nome da Sua Empresa]</p>
        </div>
    </body>
    </html>""")
    await email.enviar(5)
    
asyncio.run(main())
'''