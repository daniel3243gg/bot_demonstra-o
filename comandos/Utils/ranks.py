from PDO import PDO
import json
from datetime import datetime


'''Classe para manipular os ranks do usuarios
    DEVE SER INSTANCIADO o ID do usuario no contrustor em formato string.

'''
class Rank:
    def __init__(self, id: str):
        self.user_id = id
        self.rank_id_registro = None
        self.ranks = None
        self.primerio = None
        self.erros = None
        self.conx = PDO().create()#instancia a conexao com banco de dados


        """FUNÇÃO INTERNA PARA CARREGAR OS RANKS DO BANCO EM UMA LISTA DE DICIONARIOS
        """
    def carregaRanks(self):
        self.ranks = self.conx.query("SELECT * FROM ranks_nomes")
        return self.ranks


        """_Função responavel para subir ranks

            Si for chamada sem passar parametros vai subir um nivel do usuario, si passar parametros 
            deve ser passado a quantidade de niveis que deseja subir do usuario
            @param int qtde : Quantidade de níveis que quer subir

        """
    def subirRank(self, qnt: int = None):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        if qnt is None:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            valor = int(resp[0]['rank_id']) + 1 #transforma  o retorno da query em inteiro e adiciona mais um, a query retorna uma lista de dics
        
            self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True
        else:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            qnt = qnt - 1 if self.primerio == 1 else qnt
            valor = int(resp[0]['rank_id']) + qnt # pega o rank atual da query é soma com a quantidade que deseja upar, é depois da UPDATE no banco
            self.conx.insertUpdate('UPDATE rank SET rank_id = ? WHERE user_id = ?', valor, self.user_id)
            self.conx.insertUpdate('INSERT INTO registro_ranks(de, qual, user_id, user_rank) VALUES (?, ?, ?, ?)',
                                   int(resp[0]['rank_id']), valor, self.user_id, self.rank_id_registro)
            return True


        """Responsavel por abaixar o nivel  do Rank do jogador
        Se não tiver informado a quantidade de vezes que ele vai baixar somente 1 nivel
        @param int qtde : Quantidade de vezes que você quer abaixar o rank
        @return : retorna um bool False si ocorrer algum erro, vai salvar no metodo getErros() True si tudo ocorrer certo.
        """
    def descerRank(self, qnt: int = None):
        if self.ranks is None:
            self.carregaRanks()
        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        if qnt is None:
            resp = self.conx.query('SELECT rank_id FROM rank WHERE id = ?', self.rank_id_registro)
            valor = int(resp[0]['rank_id']) - 1 # coleta o resultado da query transforma em um inteiro o rank atual do user é depois abaixa 1 nivel
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
        
        """"Metodo responsavel para retornar o rank do usuario.
        @param registro:boll : fica como padrao False para retornar somente o rank do usuario porem
        si quiser o historico de rank dele so passar True cque vai retornar um json com  todas suas movimentaçoes
        """
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
            #acima  pega todos os dados dos registros de mudanca de rank do usuario porem existe um objeto datatime
            #e preciso passar aquela funçao lambda la para converter o objeto datatime em string 
            return json_resultante 
        else:
            resp = self.conx.query('''SELECT ranks_nomes.rank_name 
                                   FROM rank 
                                   JOIN ranks_nomes ON ranks_nomes.id = rank.rank_id 
                                   WHERE user_id = ?''', self.user_id)
            json_resultante = json.dumps(resp)
            return json_resultante
        
        """_Metodo Responsavel para inserir ponts no usuario 
            @param  qnt:int : quantidade de Pontos que serao adicionados ao usuario caso nao for passado nada
            sera adicionado 0 pontos

            @returns:  bool : True si tudo ocorrer certo, si caso de algum erro interno sera setado em getErros()
        """
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

        """Metodo responsavel por remover os pontos do usuario.
            @param  qnt: int : Quantidade de Pontos a ser removidos si passado nada sera removido 0 pontos.

            @returns  bool : Se retornou true foi bem sucedido  e se false houve algum erro. ele fica salvo em getErros()
        """
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
        
        """ Metodo Responsavel para consultar os pontos.

            Nao espera nenhum @param retorna a quantidade pontos do usuario
        """
    def consultarPonts(self):
        if self.ranks is None:
            self.carregaRanks()

        self.user_id = self.cadastrar_user()
        self.obterRankIdRegistro()

        resp = self.conx.query('''SELECT ponts FROM rank  WHERE user_id = ? ''', self.user_id )
        return resp[0]['ponts']
    


        """Metodo INTERNO responsavel para cadastrar usuario ou COLETAR SEU ID.
            Ele dever usado toda que vez for criado um novo metodo para classe Rank
        """
    def cadastrar_user(self):

        resul = self.conx.query("SELECT * FROM users WHERE id_discord = ? ", self.user_id)
        if resul is None:
            a = self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", self.user_id)
            resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", self.user_id)
            return resp[0]['id']
        else:
            return resul[0]['id']


        """Metodo responsavel para criar o usuario na tabela rank é coletar seu id da tabela
            METODO INTERNO!! nao dever ser chamado fora da classe. 
        """
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
        



        """Metodo interno responsavel para setar os erros da classe.
        @param  msg : mensagem do erro padrao caso nao for passado uma.
        """
    def setErro(self,erro:str='Ocorreu um Erro na classe Ranks.'):
        self.erros = '<br>'+ erro + '<br>'
        with open("errosClasse.txt", "a") as arquivo:
            arquivo.write("\n")
            arquivo.write(self.erros + "\n")
        return self.erros
    
        """Metodo responsavel por retornar os erros que ocorreu na classe Ranks
        """
    def getErros(self):
        return self.erros
    
        """_Metodo resposanvel por retornar os ERROS no sql, OS ERROS SQL tambem sao salvos em um arquivo
        chamado errosClasse.txt .
        """
    def get_erroSql(self):
        return self.conx.get_errors()


# Adicione o ponto de interrupção no final do arquivo para depuração

sql = Rank('010101017')
resul = sql.inserirPonts(200)
print(resul)
print(sql.get_erroSql())
#print(sql.get_erro())
