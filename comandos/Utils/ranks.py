from PDO import PDO
import json
from datetime import datetime

class Rank:
    def __init__(self, id: str):
        self.user_id = id
        self.rank_id_registro = None
        self.ranks = None
        self.primerio = None
        self.erros = None
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
            a  = self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            b = self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                    int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            if a is None or b is None:
                self.setErro('NÃO É POSSIVEL DESCER MAIS RANKS. rank setado foi 1')
                return False
            return True
        

    def consultarRank(self,registro:bool = False):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()


        if registro:

            resp = self.conx.query('''SELECT rr.data_hora , r1.rank_name as de, r2.rank_name as qual
                                FROM registro_ranks rr 
                                JOIN ranks_nomes r1 ON r1.id = rr.de 
                                JOIN ranks_nomes r2 ON r2.id = rr.qual
                                WHERE user_id = ?''', self.user_id)
            
            json_resultante = json.dumps(resp, default=lambda o: o.isoformat() if isinstance(o, datetime) else None)
            return json_resultante 
        else:
            resp = self.conx.query('''SELECT ranks_nomes.rank_name 
                                   FROM rank 
                                   JOIN ranks_nomes ON ranks_nomes.id = rank.rank_id 
                                   WHERE user_id = ?''', self.user_id)
            json_resultante = json.dumps(resp)
            return json_resultante
        
    def inserirPonts(self,qnt:int=0):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()
        if qnt > 0:
            self.conx.insertUpdate('''UPDATE rank SET ponts = ? WHERE user_id = ?''',  qnt, self.user_id)
            return True
        if qnt <0 :
            self.setErro('O NUMERO NAO DEVE SER MENOR QUE ZERO!!em inserirPonts()')
            return False

    def removerPonts(self,qnt:int=0):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        if qnt > 0:
            
            res = self.conx.query('''SELECT ponts FROM rank WHERE user_id = ?''',  self.user_id)
            res = int(res[0]['ponts'])
            if res > 0 :
                valor = res - qnt
                self.conx.insertUpdate('''UPDATE rank SET ponts = ? WHERE user_id = ?''',  valor, self.user_id)
                if qnt < 0 :
                    self.setErro('O USUARIO FICOU COM SALDO NEGATIVO!!')
                    return True
                return True
            else:
                self.setErro('Usuario tem 0 pontos. nao é possivel a remoção em removerPonts()')
                return False
        if qnt <0 :
            self.setErro('O NUMERO NAO DEVE SER MAIOR QUE ZERO!!em inserirPonts()')
            return False
        
    def consultarPonts(self):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        resp = self.conx.query('''SELECT ponts FROM rank  WHERE user_id = ? ''', self.user_id )
        return resp[0]['ponts']
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
            self.primerio = 1
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
        




    def setErro(self,erro:str='Ocorreu um Erro na classe Ranks.'):
        self.erros = '<br>'+ erro + '<br>'
        with open("errosClasse.txt", "a") as arquivo:
            arquivo.write("\n")
            arquivo.write(self.erros + "\n")
        return self.erros
    
    def getErros(self):
        return self.erros
    
    def get_erroSql(self):
        return self.conx.get_errors()


# Adicione o ponto de interrupção no final do arquivo para depuração

sql = Rank('6666666')
resul = sql.consultarPonts()
print(resul)
print(sql.get_erroSql())
#print(sql.get_erro())
