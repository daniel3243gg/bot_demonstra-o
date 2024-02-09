from comandos.Utils.PDO import PDO
import json
from datetime import datetime

class Coins:
    def __init__(self):
        self.user_id = None
        self.registro_coin = None
        self.erro = None
        self.conx =  None

    async def initialize(self):
        self.conx = await PDO().create()

    async def start(self, id: int, name: str = None):
        if self.conx is None:
            await self.initialize()
        resul = await self.conx.query("SELECT * FROM users WHERE id_discord = ?", id)
        if resul is False:
            if name is not None:
                await self.conx.insertUpdate("INSERT INTO users (id_discord, user_name) VALUES (?, ?)", id, name)
                self.user_name = name
                resp = await self.conx.query("SELECT id FROM users WHERE id_discord = ?", id)
                self.user_id = resp[0]['id']
            else:
                await self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", id)
                resp = await self.conx.query("SELECT id FROM users WHERE id_discord = ?", id)
                self.user_id = resp[0]['id']
            return True
        else:
            self.user_id = resul[0]['id']
            return True

    async def inserirCoins(self, qnt: int = 0):
        if self.conx is None:
            await self.initialize()       
        resul = await self.conx.query("SELECT * FROM coins WHERE user_id = ?", self.user_id)
        if resul is False:
            await self.conx.insertUpdate('INSERT INTO coins (coins, user_id) VALUES(?,?)', qnt, self.user_id)
            resp = await self.conx.query("SELECT id FROM coins WHERE user_id = ?", self.user_id)

            self.registro_coin = resp[0]['id']
        else:
            resp = await self.conx.query("SELECT coins FROM coins WHERE user_id = ?", self.user_id)
            coins = int(resp[0]['coins'])
            resul = coins + qnt
            await self.conx.insertUpdate('UPDATE coins SET coins = ? WHERE user_id = ?', resul, self.user_id)
            resp = await self.conx.query("SELECT id FROM coins WHERE user_id = ?", self.user_id)
            self.registro_coin = resp[0]['id']

            if self.registro_coin is not False:
                await self.conx.insertUpdate("INSERT INTO registro_coins (movement, coins_id, user_id) VALUES (?, ?, ?)", qnt, self.registro_coin, self.user_id)

                return True

    async def removerCoins(self, qnt: int = 1):
        if self.conx is None:
            await self.initialize()

        resul = await self.conx.query("SELECT * FROM coins WHERE user_id = ?", self.user_id)
        if resul is False:
            msg = 'Não é Possivel remover coins de um usuario sem nada.'
            self.setErros(msg)
            return False
        else:
            resp = await self.conx.query("SELECT coins FROM coins WHERE user_id = ?", self.user_id)
            coins = int(resp[0]['coins'])
            resul = coins - qnt
            await self.conx.insertUpdate('UPDATE coins SET coins = ? WHERE user_id = ?', resul, self.user_id)
            resp = await self.conx.query("SELECT id FROM coins WHERE user_id = ?", self.user_id)
            self.registro_coin = resp[0]['id']
            await self.conx.insertUpdate("INSERT INTO registro_coins (movement, coins_id, user_id) VALUES (?, ?, ?)", -qnt, self.registro_coin, self.user_id)
            return True

    async def consultarCoins(self, registro: bool = False):
        if self.conx is None:
            await self.initialize()
        if registro:
            resp = await self.conx.query("SELECT data_hora, movement FROM registro_coins WHERE user_id = ?", self.user_id)
            json_resultante = json.dumps(resp, default=lambda o: o.isoformat() if isinstance(o, datetime) else False)
            return json_resultante
        else:
            resp = await self.conx.query("SELECT coins FROM coins WHERE user_id = ?", self.user_id)
            resp = resp[0]['coins']
            return resp

    async def setErros(self, erro: str = 'ocorreu um erro na classe.'):
        if self.conx is None:
            await self.initialize()
        self.erro = '<br> ocorreu um erro na classe. <br>'
        self.erro += '<br>' + erro + '<br>'
        return True

    async def getErroSql(self):
        return await self.conx.get_errors()

    async def getErroCoins(self):
        return self.erro
