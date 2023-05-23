'''
Checker move generation program reworked to utilize numpy arrays
'''

from mcts import *
from copy import deepcopy
from index_dict import *
import numpy as np
dict = IndexDictionary()
from threading import Thread
from move_cache import *
BLACK  = 1
WHITE  = 2 
BLACK_KING =3
WHITE_KING =4
NA = -1000
STARTING_BOARD =  np.array( [1,1,1,1,     # 0  1  2  3
                             1,1,1,1,     # 4  5  6  7
                             1,1,1,1,     # 8  9  10 11
                             0,0,0,0,     # 12 13 14 15
                             0,0,0,0,     # 16 17 18 19
                             2,2,2,2,     # 20 21 22 23
                             2,2,2,2,     # 24 25 26 27
                             2,2,2,2])    # 28 29 30 31
class State:
    def __init__(self,current_player=1,board=STARTING_BOARD, which=BLACK):
        self.is_current_player = current_player
        self.board = board
        

    '''
    @return 1 for maximizer, -1 for minimizer
    required by mcts library
    '''
    def getCurrentPlayer(self):
        return self.is_current_player

    def generateActions(self):
        # first check if moved is stored in the cache
        # loop through every location on the board
        for location in range(32):
            piece = self.board[location]
            if(piece == 0 or (not self.is_controllable(piece))):
                continue # skip over
            else:

          
