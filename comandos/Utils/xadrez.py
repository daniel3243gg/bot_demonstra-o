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
        

        def check(self,cor:str):
            if cor == 'preta':

                is_black_in_check = self.board.is_check(chess.BLACK)
                return is_black_in_check
            
            is_white_in_check = self.board.is_check(chess.WHITE)
            return is_white_in_check
        
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

            

        def is_game_over(self):
            return self.board.is_game_over()

        def get_result(self):
            return self.board.result()

        def get_turn(self):
            return self.board.turn



