import chess
import chess.svg
from wand.image import Image
from io import BytesIO
from PIL import Image, ImageDraw
from wand.image import Image as WandImage
class Xadrez ():
        
        def __init__(self):
            self.brancas = None
            self.pretas = None
            self.board = chess.Board()
    

        def movimentar(self,mov:str):

            move = chess.Move.from_uci(mov)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            return False
        
        def check(self, cor: str):  
            if cor == 'preto':
                is_in_check = self.board.is_check(chess.BLACK)
                return is_in_check

            is_in_check = self.board.is_check(chess.WHITE)
            return is_in_check
        def gerarImagem(self):
            board_svg = chess.svg.board(board=self.board)

            # Certifique-se de que board_svg seja bytes
            board_svg_bytes = board_svg.encode('utf-8')

            # Converter o SVG para uma imagem usando a biblioteca Wand
            with WandImage(blob=board_svg_bytes, format="svg") as image:
                image.format = 'png'
                png_bytes = image.make_blob()

            # Salvar a imagem como bytes em vez de no disco
            image_bytes = BytesIO(png_bytes)

            return image_bytes

            
        def movimento_legal(self, movimento):
            try:
                move = chess.Move.from_uci(movimento)
                return move in self.board.legal_moves
            except ValueError:
                return False
        
        def is_game_over(self):
            if self.board.is_game_over():
                result = self.get_result()
                if result == "1-0":
                    return "As brancas venceram!"
                elif result == "0-1":
                    return "As pretas venceram!"
                elif result == "1/2-1/2":
                    return "O jogo terminou em empate."
            
            return False
            

        def get_result(self):
            return self.board.result()

        def get_turn(self):
            cor = ''
            if self.board.turn == chess.WHITE:
                cor = 'branca'
            else:
                cor = 'preto'
            return cor



