from typing import Optional
import json
from datetime import datetime
from PDO import PDO

class Rank:
    def __init__(self, id: str):
        self.user_id = id
        self.rank_id_registro = None
        self.ranks = None
        self.primerio = None
        self.erros = None
        self.conx = None

    async def init(self):
        self.conx = await PDO.create()

    async def carregaRanks(self):
        if self.conx is None:
            await self.init()
        self.ranks = await self.conx.query("SELECT * FROM ranks_nomes")
        return self.ranks

    async def subirRank(self, qnt: int = None):
        if self.ranks is None:
            await self.carregaRanks()

        self.user_id = await self.cadastrar_user()
        await self.obterRankIdRegistro()

        if qnt is None:
            resp = await self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            valor = int(resp[0]['rank_id']) + 1
        
            await self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            await self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True
        else:
            resp = await self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            qnt = qnt - 1 if self.primerio == 1 else qnt
            valor = int(resp[0]['rank_id']) + qnt
            await self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            await self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True

    async def descerRank(self, qnt: int = None):
        if self.ranks is None:
            await self.carregaRanks()
        self.user_id = await self.cadastrar_user()
        await self.obterRankIdRegistro()

        if qnt is None:
            resp = await self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            valor = int(resp[0]['rank_id']) - 1
            await self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            await self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True
        else:
            resp = await self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            qnt = qnt - 1 if self.primerio == 1 else qnt
            valor = int(resp[0]['rank_id']) - qnt
            a = await self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            b = await self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                    int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            if a is None or b is None:
                self.setErro('NÃO É POSSIVEL DESCER MAIS RANKS. rank setado foi 1')
                return False
            return True
        
    async def consultarRank(self, registro: bool = False) -> str:
        if self.ranks is None:
            await self.carregaRanks()

        self.user_id = await self.cadastrar_user()
        await self.obterRankIdRegistro()

        if registro:
            resp = await self.conx.query('''SELECT rr.data_hora , r1.rank_name as de, r2.rank_name as qual
                                FROM registro_ranks rr 
                                JOIN ranks_nomes r1 ON r1.id = rr.de 
                                JOIN ranks_nomes r2 ON r2.id = rr.qual
                                WHERE user_id = ?''', self.user_id)
            json_resultante = json.dumps(resp, default=lambda o: o.isoformat() if isinstance(o, datetime) else None)
            return json_resultante 
        else:
            resp = await self.conx.query('''SELECT ranks_nomes.rank_name 
                                   FROM rank 
                                   JOIN ranks_nomes ON ranks_nomes.id = rank.rank_id 
                                   WHERE user_id = ?''', self.user_id)
            json_resultante = json.dumps(resp)
            return json_resultante
    
    async def inserirPonts(self, qnt: int = 0) -> bool:
        if self.ranks is None:
            await self.carregaRanks()

        self.user_id = await self.cadastrar_user()
        await self.obterRankIdRegistro()

        if qnt > 0:
            await self.conx.insertUpdate('UPDATE rank SET ponts = ? WHERE user_id = ?',  qnt, self.user_id)
            return True
        if qnt < 0 :
            self.setErro('O NUMERO NAO DEVE SER MENOR QUE ZERO!!em inserirPonts()')
            return False

    async def removerPonts(self, qnt: int = 0) -> bool:
        if self.ranks is None:
            await self.carregaRanks()

        self.user_id = await self.cadastrar_user()
        await self.obterRankIdRegistro()

        if qnt > 0:
            res = await self.conx.query('''SELECT ponts FROM rank WHERE user_id = ?''',  self.user_id)
            res = int(res[0]['ponts'])
            if res > 0 :
                valor = res - qnt
                await self.conx.insertUpdate('''UPDATE rank SET ponts = ? WHERE user_id = ?''',  valor, self.user_id)
                if qnt < 0 :
                    self.setErro('O USUARIO FICOU COM SALDO NEGATIVO!!')
                    return True
                return True
            else:
                self.setErro('Usuario tem 0 pontos. nao é possivel a remoção em removerPonts()')
                return False
        if qnt < 0 :
            self.setErro('O NUMERO NAO DEVE SER MAIOR QUE ZERO!!em inserirPonts()')
            return False
        
    async def consultarPonts(self) -> Optional[int]:
        if self.ranks is None:
            await self.carregaRanks()

        self.user_id = await self.cadastrar_user()
        await self.obterRankIdRegistro()

        resp = await self.conx.query('''SELECT ponts FROM rank  WHERE user_id = ? ''', self.user_id )
        return resp[0]['ponts'] if resp else None

    async def cadastrar_user(self) -> int:
        resul = await self.conx.query("SELECT * FROM users WHERE id_discord = ? ", self.user_id)
        if resul is None:
            a = await self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", self.user_id)
            resp = await self.conx.query("SELECT id FROM users WHERE id_discord = ?", self.user_id)
            return resp[0]['id']
        else:
            return resul[0]['id']

    async def obterRankIdRegistro(self):
        resul = await self.conx.query('SELECT * FROM rank WHERE user_id = ? ', self.user_id)
        if resul is None:
            self.primerio = 1
            await self.conx.insertUpdate('INSERT INTO rank (rank_id, ponts, user_id) VALUES (?, ?, ?)',
                                   self.ranks[0]['id'], 0, self.user_id)

            res = await self.conx.query('SELECT id FROM rank WHERE user_id = ?', self.user_id)
            self.rank_id_registro = int(res[0]['id'])
            return
        else:
            self.user_id = resul[0]['user_id']
            res = await self.conx.query('SELECT id FROM rank WHERE user_id = ?', self.user_id)
            self.rank_id_registro = int(res[0]['id'])
            return

    def setErro(self, erro: str = 'Ocorreu um Erro na classe Ranks.'):
        self.erros = '<br>'+ erro + '<br>'
        with open("errosClasse.txt", "a") as arquivo:
            arquivo.write("\n")
            arquivo.write(self.erros + "\n")
        return self.erros

    def getErros(self):
        return self.erros

    def get_erroSql(self):
        return self.conx.get_errors()
