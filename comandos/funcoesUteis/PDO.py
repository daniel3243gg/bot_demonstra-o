from funcoesUteisR import carregar_configuracoes
import pyodbc
import asyncio 

class PDO:
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
    async def create(cls):
        instance = cls()
        await instance.init()
        return instance

    async def init(self):
        await self.carregar_configuracoes()

        self.connection_string = f"DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

    async def carregar_configuracoes(self):
        # Chama a função para carregar as configurações
        self.config = await carregar_configuracoes()
        self.server = self.config['database']['host']
        self.database = self.config['database']['database']
        self.username = self.config['database']['username']
        self.password = self.config['database']['password']

    async def query(self, query: str, *args):
        try:
            # Executa a consulta
            self.cursor.execute(query, args)
            
            columns = [column[0] for column in self.cursor.description]
            rows = self.cursor.fetchall()

            result_dicts = [dict(zip(columns, row)) for row in rows]

            return result_dicts
        except pyodbc.Error as e:
            await self.set_errors(f"Erro ao executar a query: {e}")
            return None

    async def insert(self, insert: str, *args):
        try:
            self.cursor.execute(insert, args)
            await self.executar_commit()

        except pyodbc.Error as e:
            await self.set_errors(f"Erro ao executar o insert: {e}")

    async def executar_commit(self):
        # Executa o commit para aplicar alterações no banco de dados
        self.conn.commit()

    async def fechar_conexao(self):
        # Fecha o cursor e a conexão ao final
        self.cursor.close()
        self.conn.close()

    #função para setar os erros da conexao
    async def set_errors(self, erro: str):
        self.error += '<br> ' + erro + '<br>'

    #função para retornar os erros da conexao
    async def get_errors(self):
        return self.error


async def princp():
    conex = await PDO.create()
    resul = await conex.query("SELECT *FROM users")
    print(resul)
    print(await conex.get_errors())

asyncio.run(princp())
