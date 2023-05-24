'''
Checker move generation program reworked to utilize numpy arrays
'''

from mcts import *
from copy import deepcopy
from index_table import *
import numpy as np
from move_cache import *

STARTING_BOARD = np.array ( [1 ,1 , 1, 1,
                             1, 1, 1, 1,
                             1, 1, 1, 1,
                             0, 0, 0, 0,
                             0, 0, 0, 0,
                             2, 2, 2, 2,
                             2, 2, 2, 2,
                             2, 2, 2, 2])

class State:
    def __init__(self,current_player=1,board=STARTING_BOARD, which=BLACK):
        self.table = IndexTable()
        self.is_current_player = current_player
        self.board = board
        self.possible_actions = []

    '''
    @return 1 for maximizer, -1 for minimizer
    required by mcts library
    '''
    def getCurrentPlayer(self):
        return self.is_current_player

    '''
    @ return void
    generates possible moves for a piece
    '''
    def generate_actions(self):
        # first check if moved is stored in the cache
        # loop through every location on the board
        for location in range(32):
            piece = self.board[location]
            if(self.is_controllable(piece)):
                continue # skip over
            else:
                # get moves for piece
                self.init_moves(location, piece)


    '''
    @ param index : index of element in numpy array representing the board state
    @ param value: the value of the piece
    '''
    def init_moves(self, index, value):
        pass

    '''
    @param  value: the value of the piece
    @return if the piece type corresponds to who the player is 
    '''
    def is_controllable(self,value):
        if self.which == BLACK:
            return value == BLACK or value == BLACK_KING
        else:
            return value == WHITE or value == WHITE_KING


    '''
    @return an iteratable of all actions which can be taken from this state
    required by mcts library
    '''
    def getPossibleActions(self):
        return self.possible_actions


    '''
    @param end: location to move piece  
    @return true or false, indicating whether a piece can be placed at the location
    '''
    def can_place(self, end):
        return (self.board[end] == 0)

    '''
    @param start : index of the piece to move
    @param end: index of the location to move the piece
    '''
    def perform_placement(self, start,end):
        new_board = deepcopy(self.board)
        # store piece value 
        value = new_board[start]
        # pick up piece, leaving old location empty
        new_board[start] = 0
        # place in new location
        new_board[end] = value


   

