from PDO import PDO
import json
from datetime import datetime

class Coins :
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.registro_coin = None
        self.erro = None
        self.conx = PDO.create()

    def start(self, id:str, name:str = None):
        resul = self.conx.query("SELECT *FROM users WHERE id_discord = ? " , [id])
        
        if resul == None :
            if  name != None : 
                self.conx.insertUpdate("INSERT INTO users (id_discord, user_name) VALUES (?)", [id, name])
                self.user_name = name
                resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", [id])
                self.user_id = resp[0]['id']
            else:
                 self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", [id])
                 resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", [id])
                 self.user_id = resp[0]['id']
            return True 
        else:
            resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", [id])
            self.user_id = resp[0]['id']
            return True
    

    def inserirCoins(self,qnt:int=0):
            
            
        
        resul = self.conx.query("SELECT *FROM coins WHERE user_id = ? " , self.user_id)
        if resul == None:
            self.conx.insertUpdate('INSERT INTO coins (coins, user_id) VALUES(?,?)',[qnt , self.user_id])
            resp = self.conx.query("SELECT id FROM coins WHERE user_id = ?",self.user_id)
            self.registro_coin = resp[0]['id']
                
        
        else:
            self.conx.insertUpdate('UPDATE coins SET coins = ? WHERE user_id = ?',[ qnt, self.user_id])
            resp = self.conx.query("SELECT id FROM coins WHERE user_id = ?", [self.user_id])
            self.registro_coin = resp[0]['id']

            # Verifique se o registro_coin não é None antes de executar o segundo insertUpdate
            if self.registro_coin is not None:
                self.conx.insertUpdate("INSERT INTO registro_coins (movement, coins_id, user_id) VALUES (?, ?, ?)", [qnt, self.registro_coin, self.user_id])
                return True
    def removerCoins(self, qnt:int=1):
        resul = self.conx.query("SELECT *FROM coins WHERE user_id = ? " , self.user_id)
        if resul == None:
            msg = 'Não é Possivel remover coins de um usuario sem nada.'
            self.setErros(msg)
            return False
        else:
            resp = self.conx.query("SELECT coins FROM coins WHERE user_id = ?",self.user_id)
            coins = int(resp[0]['coins'])
            resul = coins - qnt 
            self.conx.insertUpdate('UPDATE coins SET coins = ? WHERE user_id = ?',[resul,self.user_id])
            resp = self.conx.query("SELECT id FROM coins WHERE user_id = ?", [self.user_id])
            self.registro_coin = resp[0]['id']
            self.conx.insertUpdate("INSERT INTO registro_coins (movement, coins_id, user_id) VALUES (?, ?, ?)", [-qnt, self.registro_coin, self.user_id])
            return True
        
    def consultarCoins(self,registro:bool = False):

        if(registro):

            resp = self.conx.query("SELECT data_hora, movement FROM registro_coins WHERE user_id = ?", [self.user_id])
            json_resultante = json.dumps(resp, default=lambda o: o.isoformat() if isinstance(o, datetime) else None)

            return json_resultante
        else:
            resp = self.conx.query("SELECT coins FROM coins WHERE user_id = ?", [self.user_id])
            resp = resp[0]['coins']
            return resp
        
    def setErros(self,erro:str = 'ocorreu um erro na classe.'):
        self.erro += '<br>'+ erro + '<br>'
        return True
    def getErroSql(self):
        return self.conx.get_errors()
    
    def getErroCoins(self):
        return self.erro
    
sql = Coins()
sql.start('799432942006304788')
resul = sql.consultarCoins()
print(resul)





