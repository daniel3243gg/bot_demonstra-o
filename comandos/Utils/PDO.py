# import io

import pyodbc
from funcoesUteisR import carregar_configuracoes


# classe de conexao com banco
class PDO:
    """
    Classe para ser usado para a conexao no banco. NAO USAR DIRETAMENTE EM
    CODIGOS COM O USUARIO, DEVE SER ADICIONADO VALIDAÇOES.

    CONTEM:
    delete
    insert/update (mesmo metodo)
    query(select)
    geterros(retorna erros)
    """
    def __init__(self):
        self.config = None
        self.server = None
        self.database = None
        self.username = None
        self.password = None
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.connection_string = None
        self.conn = None
        self.cursor = None
        self.error = ""

    @classmethod
    def create(self):
        """
        Funçao para instanciar a classe.

        Returns:
            [self]: [invoca a classe e ativa a conexao com o banco.]
        """
        instance = self()
        instance.init()
        return instance

    def init(self):
        
        """
        Instancia os metodos da classe pyodoc e realmente iniciar a conexao
        com o SQLSERVER
        """

        self.carregar_configuracoes()

        self.connection_string = f"DRIVER={self.driver}; SERVER={self.server};\
            DATABASE={self.database}; UID={self.username}; PWD={self.password}"
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

    def carregar_configuracoes(self):
        # Chama a função para carregar as configurações

        """
        Carrega as config
        """

        self.config = carregar_configuracoes()
        self.server = self.config['database']['host']
        self.database = self.config['database']['database']
        self.username = self.config['database']['username']
        self.password = self.config['database']['password']

    def query(self, query: str, *args):
        """
        Classe para pesquisas no banco

        Args:
            query (str): SELECT *FROM _tabela
            *args : Argumentos da pesquisa
        Returns:
            dic: Retorna um dicionario em python com o seguinte formato:
            coluna:valor
        """

        try:
            # Executa a consulta
            self.cursor.execute(query, args)  # type: ignore

            columns = [column[0] for column in self.cursor.description]  # type: ignore  # noqa: E501
            rows = self.cursor.fetchall()  # type: ignore

            result_dicts = [dict(zip(columns, row)) for row in rows]
            if result_dicts == []:
                return False
            else:
                return result_dicts

        except pyodbc.Error as e:
            self.set_errors(f"Erro ao executar a query: {e}")
            return False

    def insertUpdate(self, insert: str, *args):
        """
        Metodo para envio de valores para o banco

        Args:
            insert (str): Sua Query, condição etc
            *args : Os argumentos que você quer inserir ou atualizar

        Returns:
            True: Ocorreu tudo certo
            False: Ocorreu algum erro no banco, o erro fica salvo em getErros
        """
        try:
            self.cursor.execute(insert, args)  # type: ignore
            self.executar_commit()
            return True
        except pyodbc.Error as e:
            self.set_errors(f"Erro ao executar o insert: {e}")
            return False

    def getColunas(self, tabel: str):
        """
        Metodo de colunas

        Args:
            tabel (str): A tabela que deseja saber as colunas.

        Returns:
            List: Retorna uma lista com todas as colunas do banco
        """

        try:
            # Executa a consulta
            query = f"SELECT *FROM {tabel} "
            self.cursor.execute(query)  # type: ignore
            columns = [column[0] for column in self.cursor.description]  # type: ignore  # noqa: E501
            return columns

        except pyodbc.Error as e:
            self.set_errors(f"Erro ao executar a query: {e}")
            return False

        except TypeError as te:
            self.set_errors(f"Erro ao obter colunas: {te}")
            return False

    def delete(self, tabel: str, condicao: str):
        """
        Metodo Delete

        Args:
            tabel (str): [Sua tabela]
            condicao (str): [Sua condição de busca]

        Returns:
            [True]: [Si ocorreu tudo certo no delete]
            [False] : [Si ocorreu algum erro, ele guarda o erro no get_Erros]
        """

        try:
            query = f"DELETE FROM {tabel} WHERE {condicao}"
            self.cursor.execute(query)  # type: ignore
            self.executar_commit()
            return True

        except pyodbc.Error as e:
            self.set_errors(f"Erro ao executar o insert: {e}")
            return False

    def executar_commit(self):
        """
        NAO USAR
        """

        # Executa o commit para aplicar alterações no banco de dados
        self.conn.commit()  # type: ignore

    def fechar_conexao(self):
        """Usar sempre que terminar o uso do banco"""
        # Fecha o cursor e a conexão ao final
        self.cursor.close()  # type: ignore
        self.conn.close()  # type: ignore

    # Função para setar os erros da conexao
    def set_errors(self, erro: str):
        self.error += '<br> ' + erro + '<br>'
        with open("errosClasse.txt", "a") as arquivo:
            arquivo.write("\n")
            arquivo.write(self.error + "\n")

    # Função para retornar os erros da conexao
    def get_errors(self):
        """
        _summary_

        Returns:
            String: Retorna os erros que ocorreu no banco
        """
        return self.error


