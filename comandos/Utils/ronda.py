from PDO import PDO
from coins import Coins
import json 
import random
import requests
class Ronda:

    def __init__(self):
        self.jogadores= []
        self.erros = None
        self.conx = PDO().create()
        self.url = 'https://cartas-d2746-default-rtdb.firebaseio.com/.json'
        self.cartas = self.defCartas()
        self.maosC = []

    def defCartas(self):

        
        response = requests.get(self.url)

        # Verifica se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Converte o conteúdo JSON da resposta para um objeto Python
            cartas = response.json()

            # Você pode manipulá-lo conforme necessário

            return cartas
        else:
            self.setErros(f"A requisição falhou com o código  status: {response.status_code}")
            return False

    def cadastrar_user(self, jogador:str ):

        resul = self.conx.query("SELECT * FROM users WHERE id_discord = ? ", jogador)
        if resul is None:
            a = self.conx.insertUpdate("INSERT INTO users (id_discord) VALUES (?)", jogador)
            resp = self.conx.query("SELECT id FROM users WHERE id_discord = ?", jogador)
            return resp[0]['id']
        else:
            return resul[0]['id']
        
        

    def setErros(self,erro:str = 'Ocorreu um erro.'):
        self.erros = '<br>'+ erro + '<br>'

    def getErros(self):
        return self.erros
    
    def adicionarJogadores(self,*jogadoress):

        for jogador in jogadoress:
            id = self.cadastrar_user(jogador)
            self.jogadores.append({'jogador':jogador})



    def distruibuirCartas(self):
        maos = []
        n = 0
        for jogador in self.jogadores:
            naipe_aleatorio = random.choice(list(self.cartas.keys()))

            # Escolher uma carta aleatoriamente dentro do naipe escolhido
            carta_aleatoria = random.choice(list(self.cartas[naipe_aleatorio].keys()))
            coins = Coins()
            coins.start(jogador['jogador'])
            saldo = coins.consultarCoins()
            self.maosC.append( {'carta':self.cartas[naipe_aleatorio][carta_aleatoria], 'jogador':jogador['jogador'], 'saldo': saldo} )
            n += 1
        return self.maosC
    

    def jogarSimples(self):
        mesa = None
        result = {'mesa': None, 'resultado': None, 'jogador': None}
        naipe_aleatorio = random.choice(list(self.cartas.keys()))

        # Escolher uma carta aleatoriamente dentro do naipe escolhido
        carta_aleatoria = random.choice(list(self.cartas[naipe_aleatorio].keys()))
        mesa = self.cartas[naipe_aleatorio][carta_aleatoria]
        n = 0

        for mao in self.maosC:
            if mao['saldo'] < 50:
                result = {'resultado': None , "jogador" : mao['jogador']}
                return result
            else:
                if mao['carta'] == mesa:

                    result = {'mesa': mesa, 'resultado': True, 'jogador': mao['jogador']}
                    coins = Coins()
                    coins.start(str(mao['jogador']))
                    calc = 50 * len(self.maosC)
                    coins.inserirCoins(calc)
                    for jogador in self.jogadores:
                        if jogador['jogador'] == mao['jogador']:
                            # Faça algo com o jogador encontrado
                            # Se necessário, adicione lógica aqui
                            pass
                        else:
                            coins2 = Coins()
                            coins2.start(str(jogador['jogador']))
                            coins2.removerCoins(50)
                    # Se encontrar uma correspondência, interromper o loop
                    break

        # Correção: Definir o resultado como True apenas se nenhuma correspondência for encontrada
        if result['resultado'] is None:
            result = {'mesa': mesa, 'resultado': False}


        return result

    def jogarApostaFixa(self,qnt:int=0):

            
        mesa = None
        result = {'mesa': None, 'resultado': None, 'jogador': None}
        naipe_aleatorio = random.choice(list(self.cartas.keys()))

        # Escolher uma carta aleatoriamente dentro do naipe escolhido
        carta_aleatoria = random.choice(list(self.cartas[naipe_aleatorio].keys()))
        mesa = self.cartas[naipe_aleatorio][carta_aleatoria]
        n = 0

        for mao in self.maosC:


            if mao['saldo'] < qnt:
                result = {'resultado': None , "jogador" : mao['jogador']}
                return result
            else:
                if mao['carta'] == mesa:
                    coins = Coins()
                    coins.start(str(mao['jogador']))
                    calc = qnt * len(self.maosC)
                    result = {'mesa': mesa, 'resultado': True, 'jogador': mao['jogador'] , 'vitoria':calc , 'derrota': qnt}
                    coins.inserirCoins(calc)
                    for jogador in self.jogadores:
                        if jogador['jogador'] == mao['jogador']:
                            # Faça algo com o jogador encontrado
                            # Se necessário, adicione lógica aqui
                            pass
                        else:
                            coins2 = Coins()
                            coins2.start(str(jogador['jogador']))
                            coins2.removerCoins(qnt)
                    # Se encontrar uma correspondência, interromper o loop
                    break        
        # Correção: Definir o resultado como True apenas se nenhuma correspondência for encontrada
            if result['resultado'] is None:
                result = {'mesa': mesa, 'resultado': False}


        return result

    def apostaLivre(self,apostas:dict):

        mesa = None
        result = {'mesa': None, 'resultado': None, 'jogador': None}

        naipe_aleatorio = random.choice(list(self.cartas.keys()))

        # Escolher uma carta aleatoriamente dentro do naipe escolhido
        carta_aleatoria = random.choice(list(self.cartas[naipe_aleatorio].keys()))
        mesa = self.cartas[naipe_aleatorio][carta_aleatoria]

        for mao in self.maosC:
            mesa = mao['carta']
            if mao['carta'] == mesa:
                jogador_id = mao['jogador']
                coins = Coins()
                coins.start(str(jogador_id))
                calc = sum(aposta['valor'] for aposta in apostas)
                result = {'mesa': mesa, 'resultado': True, 'jogador': jogador_id, 'vitoria': calc}
                coins.inserirCoins(calc)

                for jogador in self.jogadores:
                    if jogador['jogador'] == jogador_id:
                        # Faça algo com o jogador encontrado, se necessário
                        ...
                    else:
                        for aposta in apostas:
                            print(aposta)
                            print(jogador['jogador'])
                            if aposta['id'] == jogador['jogador']:
                                coins2 = Coins()
                                coins2.start(str(jogador['jogador']))
                                coins2.removerCoins(aposta['valor'])

                # Se encontrar uma correspondência, interromper o loop
                break
            # Correção: Definir o resultado como True apenas se nenhuma correspondência for encontrada
            if result['resultado'] is None:
                result = {'mesa': mesa, 'resultado': False}

        return result
    
