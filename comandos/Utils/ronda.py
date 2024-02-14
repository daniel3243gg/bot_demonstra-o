from comandos.Utils.PDO import PDO
from comandos.Utils.coins import Coins
import asyncio
import json 
import random
import aiohttp

class Ronda:
    def __init__(self):
        self.jogadores = []
        self.erros = None
        self.conx = None
        self.url ='https://cartas2-default-rtdb.firebaseio.com/.json'
        self.cartas = None
        self.maosC = []

    async def initialize(self):
        self.conx = await PDO().create()

    async def defCartas(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    self.cartas = await response.json()
                else:
                    self.setErros(f"A requisição falhou com o código de status: {response.status}")
                    return False

    async def setErros(self, erro: str = 'Ocorreu um erro.'):
        self.erros = f"<br>{erro}<br>"

    def getErros(self):
        return self.erros
    
    async def adicionarJogadores(self, *jogadores):
        #if len(jogadores == 1):
            jogadores_for = jogadores[0]
            for jogador in jogadores_for:
                jogador = str(jogador)
                self.jogadores.append({'jogador': jogador})

    async def distruibuirCartas(self):
        if self.cartas is None:
            await self.defCartas()

        maos = []
        n = 0
        for jogador in self.jogadores:
            naipe_aleatorio = random.choice(list(self.cartas.keys()))

            # Escolher uma carta aleatoriamente dentro do naipe escolhido
            carta_aleatoria = random.choice(list(self.cartas[naipe_aleatorio].keys()))
            coins = Coins()
            await coins.start(jogador['jogador'])
            saldo = await coins.consultarCoins()
            self.maosC.append({'carta': self.cartas[naipe_aleatorio][carta_aleatoria], 'jogador': jogador['jogador'], 'saldo': saldo, 'n': carta_aleatoria})
            n += 1
        return self.maosC
    
    async def jogarSimples(self,players):
        if self.cartas is None:
            await self.defCartas()
        jogo = True
        mesa = {}
        cartas_usadas = []
        result = {'mesa': None, 'resultado': None, 'jogador': None}

        while jogo:
            naipe_aleatorio = random.choice(list(self.cartas.keys()))
            # Escolher uma carta aleatoriamente dentro do naipe escolhido
            carta_aleatoria = random.choice(list(self.cartas[naipe_aleatorio].keys()))
            mesa = {'carta':self.cartas[naipe_aleatorio][carta_aleatoria],'n':carta_aleatoria}
            n = 0
            if cartas_usadas.count(mesa['carta']) >= 4:
                continue

            for player in players:
                if player['saldo'] < 50:
                    result = {'resultado': None , "jogador" : player['jogador']}
                    return result
                else:
                    if player['n'] == mesa['n']:
                        result = {'mesa': mesa['carta'], 'resultado': True, 'jogador': player['jogador']}
                        coins = Coins()
                        print('houve um vencedor')
                        await coins.start(str(player['jogador']))
                        calc = 50 * len(players)
                        await coins.inserirCoins(calc)
                        jogo = False
                        for jogador in players:
                            if jogador['jogador'] == player['jogador']:
                                pass
                            else:
                                coins2 = Coins()
                                await coins2.start(str(jogador['jogador']))
                                await coins2.removerCoins(50)
                            
                        break
                    

        return result

    async def jogarApostaFixa(self, qnt: int = 0):
        if self.cartas is None:
            await self.defCartas()

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
                    await coins.start(str(mao['jogador']))
                    calc = qnt * len(self.maosC)
                    result = {'mesa': mesa, 'resultado': True, 'jogador': mao['jogador'] , 'vitoria': calc , 'derrota': qnt}
                    await coins.inserirCoins(calc)
                    for jogador in self.jogadores:
                        if jogador['jogador'] == mao['jogador']:
                            pass
                        else:
                            coins2 = Coins()
                            await coins2.start(str(jogador['jogador']))
                            await coins2.removerCoins(qnt)
                    break        

            if result['resultado'] is None:
                result = {'mesa': mesa, 'resultado': False}

        return result

    async def apostaLivre(self, apostas: dict):
        if self.cartas is None:
            await self.defCartas()

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
                await coins.start(str(jogador_id))
                calc = sum(aposta['valor'] for aposta in apostas)
                result = {'mesa': mesa, 'resultado': True, 'jogador': jogador_id, 'vitoria': calc}
                await coins.inserirCoins(calc)

                for jogador in self.jogadores:
                    if jogador['jogador'] == jogador_id:
                        ...
                    else:
                        for aposta in apostas:
                            if aposta['id'] == jogador['jogador']:
                                coins2 = Coins()
                                await coins2.start(str(jogador['jogador']))
                                await coins2.removerCoins(aposta['valor'])

                break

            if result['resultado'] is None:
                result = {'mesa': mesa, 'resultado': False}

        return result


