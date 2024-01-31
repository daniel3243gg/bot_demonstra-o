from PDO import PDO
import pdb  # Adicione esta linha para importar o módulo pdb
from datetime import datetime

class Rank:
    def __init__(self, id: str):
        self.user_id = id
        self.rank_id_registro = None
        self.ranks = None
        self.primerio = None
        self.conx = PDO().create()

    def carregaRanks(self):
        self.ranks = self.conx.query("SELECT * FROM ranks_nomes")
        return self.ranks

    def subirRank(self, qnt: int = None):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        if qnt is None:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            valor = int(resp[0]['rank_id']) + 1
            self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True
        else:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            qnt = qnt - 1 if self.primerio == 1 else qnt
            valor = int(resp[0]['rank_id']) + qnt
            self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True

    def descerRank(self, qnt: int = None):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        if qnt is None:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            valor = int(resp[0]['rank_id']) - 1
            self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True
        else:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            qnt = qnt - 1 if self.primerio == 1 else qnt
            valor = int(resp[0]['rank_id']) - qnt
            self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True

    def cadastrar_user(self):
        resul = self.conx.query("SELECT * FROM users WHERE id_discord = ? ", self.user_id)
        if resul is None:
            a = self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", self.user_id)
            resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", self.user_id)
            return resp[0]['id']
        else:
            return resul[0]['id']

    def obterRankIdRegistro(self):
        resul = self.conx.query('SELECT * FROM rank WHERE user_id = ? ', self.user_id)
        if resul is None:
            pdb.set_trace()
            self.primeiro = 1
            self.conx.insertUpdate('INSERT INTO rank (rank_id, ponts, user_id) VALUES (?, ?, ?)',
                                   self.ranks[0]['id'], 0, self.user_id)

            res = self.conx.query('SELECT id FROM rank WHERE user_id = ?', self.user_id)
            self.rank_id_registro = int(res[0]['id'])
            return
        else:
            self.user_id = resul[0]['user_id']
            res = self.conx.query('SELECT id FROM rank WHERE user_id = ?', self.user_id)
            self.rank_id_registro = int(res[0]['id'])
            return

    def get_erro(self):
        return self.conx.get_errors()


# Adicione o ponto de interrupção no final do arquivo para depuração
pdb.set_trace()

sql = Rank('799432942006304788')
resul = sql.descerRank(1)
print(resul)
print(sql.get_erro())
