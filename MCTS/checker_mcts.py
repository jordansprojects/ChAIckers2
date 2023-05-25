'''
checker_mcts.py -  Checker move generation program.
'''

from mcts import *              # Monte Carlo Tree Search library
from copy import deepcopy       # To copy states 
from index_table import *       # To pull viable index information for each piece and location
import numpy as np              # Numpy arrays
from move_cache import *        # To cache moves so that repeated states are not re-computed 

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
        self.which = which
        self.cache = MoveCache()
        self.generateActions()
    '''
    @return 1 for maximizer, -1 for minimizer
    required by mcts library
    '''
    def getCurrentPlayer(self):
        return self.is_current_player

    '''
    Determines whether a terminal state has been reached
    Required by the mcts library
    '''
    def isTerminal(self):
        # current player has no legal moves
        if len(self.possible_actions) == 0:
            return True
        # black has no checkers left
        if  not np.any( (self.board ==  BLACK) | (self.board == BLACK_KING) ) :
            return True
        # white has no checkers left
        elif not np.any( (self.board == WHITE) | (self.board == WHITE_KING) ) :
            return True
        else: # if all other conditions arent met, the game is still on!
            return False


    '''
    Returns the reward for a terminal state
    Required by mcts library
    '''
    def getReward(self):
        # variables to give penalty if losing 
        is_white = 1 if self.which == WHITE else -1 
        is_black = 1 if self.which == BLACK else -1
        if not np.any( (self.board == WHITE ) | (self.board == WHITE_KING )):
            return 1 * is_black
        elif not np.any( (self.board == BLACK) | (self.board == BLACK_KING ) ):
            return 1 * is_white
        else: # no reward unless game is won
            return 0 
    '''
    generates possible moves for a piece
    '''
    def generateActions(self):
        # first check if an entry exists yet
        actions = self.cache.retrieve_moves( self.which, self.board)

        # if an entry already exists, set it and exit
        if actions != -1:
            print("cache entry found for\n " + str(self.board))
            self.possible_actions = actions
            return
        # first check if moved is stored in the cache
        # loop through every location on the board
        for location in range(32):
            piece = self.board[location]
            if(self.is_controllable(piece)):
                # get moves for each piece 
                self.init_moves(location, piece)


    '''
    @ param index : index of element in numpy array representing the board state
    @ param value: the value of the piece
    '''
    def init_moves(self, index, value):
        # perform hops first 
        if (self.init_hops(index,value)):
            # if the checker can hop, exit
            return 
        else:
            # otherwise perform checker steps 
            self.init_steps(index, value)

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
    @return true if a checker is in the king zone and not yet a king
    '''
    def is_in_the_king_zone(self, index):
        if self.which == WHITE:
            if  index < 4  :
                return True
        elif (self.which == BLACK):
            if index > 27:
                return True
        else:
            return False

    '''
    @return an iteratable of all actions which can be taken from this state
    required by mcts library
    '''
    def getPossibleActions(self):
        return self.possible_actions


    '''
    Returns the state which results from taking action
    Required by mcts library
    '''
    def takeAction(self, action):
        # check if there is a cache entry for the current state
        if self.cache.retrieve_moves(self.which, self.board) == -1:
            # write to cache if no entry exists yet
            self.cache.write_moves(self.which, self.board,self.possible_actions)
        new_state = deepcopy(self)
        new_state.board = action.board
        # clear list for next state
        new_state.possible_actions.clear()
        # alternate between minimizer and maximizer
        new_state.is_current_player = self.is_current_player *-1
        # alternate whether player is black or white
        new_state.which = BLACK if self.which == WHITE else WHITE
        new_state.generateActions()
        
        
        return new_state

    '''
    @param end: location to move piece  
    @return true or false, indicating whether a piece can be placed at the location
    '''
    def can_place(self, end):
        return (self.board[end] == 0)

    
    '''
    @param index of the piece 
    @ return true if enemy/opposing piece, false if ally piece.
    '''
    def is_enemy(self, index):
        value = self.board[index]
        if self.which == WHITE:
            return value == BLACK or value == BLACK_KING
        else:
            return value == WHITE or value == WHITE_KING


    '''
    @param start : beginning index of piece
    @param hop_tuple : tuple possessing the piece being hopped over and the desired location
    '''
    def can_hop(self, hop_tuple):
        # unpack tuple
        piece_to_take = hop_tuple[0]
        destination = hop_tuple[1]
        
        # check if the piece in between is an enemy piece and whether there is a 
        # free space after them
        if  self.is_enemy(piece_to_take) and self.can_place(destination) :
            return True
        else:
            return False


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
        new_board[end] = value+2 if self.is_in_the_king_zone(end) and value < 3 else value

        # finish and add board to the list
        self.add_action(new_board)



    '''
    @param index: index of current piece
    @param value: value of current piece
    '''
    def init_steps(self, index, value):
        steps = self.table.get_steps(index, value)
        for step in steps:
            if self.can_place(step):
                self.perform_placement(index, step)



    '''
    @param index: location of the checker in the board array
    @param value: piece value of the checker: WHITE,BLACK, WHITE_KING or BLACK_KING
    @return boolean: true if there exists a successful hop, false if no successful hops
    '''
    def init_hops(self,index,value):
        has_hopped = False 
        hops = self.table.get_hops(index,value)
        for hop in hops:
            if self.can_hop( hop):
                has_hopped = True
                self.perform_hop(index, hop)
        return has_hopped

    '''
    @ param start: starting index of the hop
    @ param hop_tuple: tuple of indicies, in the form (hopped_over, landed) 
    '''
    def perform_hop(self,start,hop_tuple):
        new_board = deepcopy(self.board)
        # store piece value
        value = new_board[start]

        # unpack tuple
        hopped_over = hop_tuple[0]
        destination = hop_tuple[1]
        
        # begin hop, leaving old spot empty
        new_board[start] = 0

        # hop over piece, taking it
        new_board[hopped_over] =  0
        
        # place piece in new spot
        new_board[destination] = value+2 if self.is_in_the_king_zone(destination) and value <3 else value

        '''
        TO-DO: FIX THIS 
        # must participate in continous hops if they exist
        # while this code may seem redundant, it is necessary to differentiate between a 
        # continuous hop and the initialization of a singular hop
        
        # destination becomes start

        # grab hop list
        hops = self.table.get_hops(destination, new_board[destination])

        # make recursive call for continiuous hop
        for hop in hops:
            if self.can_hop(hop):
                self.perform_hop(destination, hop)
        '''
        # finish and add board to the list
        self.add_action(new_board)

    '''
    Adds a board state to the possible actions list
    @ param board: numpy array representing the board state 
    '''
    def add_action (self, board):
        # only add an action if it is unique from the current board
        self.possible_actions.append(Action(player=self.getCurrentPlayer(), board_state=board))


''' 
 Action class, encapsulates state data needed for MCTS 
'''

class Action():
    '''
    @param board_state : numpy array representing the board
    @param player: 1 or -1 indicating whether it is a maximizing or minimizing state
    '''
    def __init__(self, player, board_state):
        self.player = player
        self.board = board_state

    def __str__(self):
        str_board = '\n'
        for number in self.board:
            str_board = str_board +  " "+ str(number)
            if ( i + 1 ) % 4 == 0: # new line
                str_board = str_board + '\n'
        return str_board

    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        return self.player == other.player and np.array_equal( self.board, other.board)

    def __hash__(self):
        return hash( (self.board.tobytes(), self.player))



