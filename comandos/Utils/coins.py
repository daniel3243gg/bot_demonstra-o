from PDO import PDO
import json
from datetime import datetime

"""Classe Coins

    Returns:
        classe que DEVE ser usado para manipular coins do usuario nela contem todos os metodos necessarios 
        para consultar,debitar é creditar coins, TODA VEZ QUE INSTANCIA A CLASSE DEVE SER CHAMADO O METODO start
        nele que cria o usuario no banco ou instancia ele com a classe. 

        Metodos:
        - __init__(self, user_id) : Construtor da Classe Coins, aqui ocorre a instancia com o banco.

        
        start: Metodo que sempre deve ser chamado juntamente com a classe, ele recebe o ID o usuario 
        é verifica si ele ja existe na base de dados caso existir so coleta o ID dele no banco caso nao existir
        ele cria o usuario é coleta o seu ID.

        inserirCoins:  Metodo responsavel por adicionar as moedas ao usuario, recebe como parameto
        a quantidade de moedas que vai ser inserido no banco, é tambem registra a movimentação na tabela registro_coins.

        
        removerCoins:    Metodo responsavel por remover as moedas do usuario,  recebe como parametro
                         quantidade de moedas a ser removida é salva a movimentação negativada(EX: -10) indicando que foi 
                         uma retirada na tabela registro_coins.

                         
        consultarCoins:    Metodo responsavel por retornar a quantidade de moedas do usuario ou o registro de 
                           coins (caso passar True de parametro), ele retorna um INT da moedas do usuario ou uma lista
                           de dicionarios contendo todas a movimentação do usuario caso for passado True de parametro.

    
"""
class Coins :
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.registro_coin = None
        self.erro = None
        self.conx = PDO.create()

    def start(self, id:str, name:str = False):
        resul = self.conx.query("SELECT *FROM users WHERE id_discord = ? " , id)
        
        if resul == False :
            if  name != False : 
                self.conx.insertUpdate("INSERT INTO users (id_discord, user_name) VALUES (?)", id, name)
                self.user_name = name
                resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", id)
                self.user_id = resp[0]['id']
            else:
                 self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", id)
                 resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", id)
                 self.user_id = resp[0]['id']
            return True 
        else:
            resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", id)
            self.user_id = resp[0]['id']
            return True
    

    def inserirCoins(self,qnt:int=0):
            
            
        
        resul = self.conx.query("SELECT *FROM coins WHERE user_id = ? " , self.user_id)
        if resul == False:
            self.conx.insertUpdate('INSERT INTO coins (coins, user_id) VALUES(?,?)',qnt , self.user_id)
            resp = self.conx.query("SELECT id FROM coins WHERE user_id = ?",self.user_id)

            self.registro_coin = resp[0]['id']
                
        
        else:
            resp = self.conx.query("SELECT coins FROM coins WHERE user_id = ?",self.user_id)
            coins = int(resp[0]['coins'])
            resul = coins + qnt 
            self.conx.insertUpdate('UPDATE coins SET coins = ? WHERE user_id = ?', resul, self.user_id)
            resp = self.conx.query("SELECT id FROM coins WHERE user_id = ?", self.user_id)
            self.registro_coin = resp[0]['id']

            # Verifique se o registro_coin não é False antes de executar o segundo insertUpdate
            if self.registro_coin is not False:
                self.conx.insertUpdate("INSERT INTO registro_coins (movement, coins_id, user_id) VALUES (?, ?, ?)", qnt, self.registro_coin, self.user_id)
               
                return True
    def removerCoins(self, qnt:int=1):
        resul = self.conx.query("SELECT *FROM coins WHERE user_id = ? " , self.user_id)
        if resul == False:
            msg = 'Não é Possivel remover coins de um usuario sem nada.'
            self.setErros(msg)
            return False
        else:
            resp = self.conx.query("SELECT coins FROM coins WHERE user_id = ?",self.user_id)
            coins = int(resp[0]['coins'])
            resul = coins - qnt 
            self.conx.insertUpdate('UPDATE coins SET coins = ? WHERE user_id = ?',resul,self.user_id)
            resp = self.conx.query("SELECT id FROM coins WHERE user_id = ?", self.user_id)
            self.registro_coin = resp[0]['id']
            self.conx.insertUpdate("INSERT INTO registro_coins (movement, coins_id, user_id) VALUES (?, ?, ?)", -qnt, self.registro_coin, self.user_id)
            return True
        
    def consultarCoins(self,registro:bool = False):

        if(registro):

            resp = self.conx.query("SELECT data_hora, movement FROM registro_coins WHERE user_id = ?", self.user_id)
            json_resultante = json.dumps(resp, default=lambda o: o.isoformat() if isinstance(o, datetime) else False)
            #acima estou transformando a data-hora do banco de dados em formato dicionario 
            #o banco de dados envia um objeto datatime
            return json_resultante
        else:
            resp = self.conx.query("SELECT coins FROM coins WHERE user_id = ?", self.user_id)
            resp = resp[0]['coins']
            return resp


    #ABAIXO ESTA AS FUNÇOES PARA RETORNAR ERROS sendo getErroSql() erros da consulta ou do banco 
    #getErroCoins() erro da classe.  
    #setErros() usada para setar erros da classe si caso nao passsar o erro ele vai escrever uma mensagem simples de erro.
    def setErros(self,erro:str = 'ocorreu um erro na classe.'):
        self.erro = '<br> ocorreu um erro na classe. <br>'
        self.erro += '<br>'+ erro + '<br>'
        return True
    def getErroSql(self):
        return self.conx.get_errors()
    
    def getErroCoins(self):
        return self.erro






