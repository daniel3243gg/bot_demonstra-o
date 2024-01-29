from PDO import PDO

class Coins :
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.registro_rank = None
        self.registro_coin = None
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


    def erro(self):
        return self.conx.get_errors()



in_class = Coins()
in_class.start("799432942006304788")
in_class.inserirCoins(200)
print(in_class.erro())
