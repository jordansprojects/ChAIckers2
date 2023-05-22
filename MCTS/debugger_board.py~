# Simple GUI for displaying checker board when debugging MCTS

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap,QImage
from PyQt5.QtCore import Qt
import sys

class CheckerBoardWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        canvas = QPixmap(400,400)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_checkerboard()
        self.init_boardinates()



    '''  generates the coordinates for
        each checker location on the GUI
    '''
    def init_boardinates(self):
        self.boardinates =[]
        even_x = 60
        odd_x = y = 10
        new_row = 50
        new_col = 100

        for row in range(8):
            if (row % 2 == 0):
                # even row
                x = even_x
            else:
                #odd row
                x = odd_x
            for j in range(4):
                 # append coordinate to array of tuples
                 self.boardinates.append((x,y))
                 x = x + new_col
            # increase y after row is finished
            y = y + new_row

    ''' draws the checkerboard pattern
        onto the screen
    '''
    def draw_checkerboard(self):
        qp = QPainter(self.label.pixmap())
        square_size = 50
        num_squares = 8
        # loop through each square and draw it
        for row in range(num_squares):
            for col in range(num_squares):
                x = col * square_size
                y = row * square_size

                #Set square color based on positon
                color = QColor(255,255,255) if (row + col) % 2 == 0 else QColor(159,43,104);
                qp.fillRect(x,y,square_size,square_size,color)
        qp.end()


    '''images from OpenGameArt.org
    Title: "BoardGame Tiles"
    Author: Sharm
    link: https://opengameart.org/content/boardgame-tiles
    '''
    def get_piece_sprites(self):
        self.pieces = []
        path = "images/c"
        for i in range(1,5):
            image = QImage()
            img_path = path + str(i) + ".png"
            if image.load(img_path):
                self.pieces.append(image)
            else:
                print("debugger_board.py: Image failed to load.")
        print("sprites loaded")

    def draw_pieces_on_board(self,board_state: list[int]):
        # first paint over previous board
        self.draw_checkerboard()
        qp = QPainter(self.label.pixmap())
        # then draw checkers based on board state provided
        for location in range(len(board_state)):
            piece_val = board_state[location] -1
            # retrieve GUI coordinates for the location
            x = self.boardinates[location][0]
            y = self.boardinates[location][1]

            if ( piece_val != -1):
                qp.drawImage(x,y, self.pieces[piece_val])
        qp.end()


