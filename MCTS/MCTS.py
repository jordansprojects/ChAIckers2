#from mcts_lib import *
from mcts import *
from copy import deepcopy
from index_dict import *
dict = IndexDictionary()
from threading import Thread
from move_cache import *
BLACK  = 1
WHITE  = 2 
BLACK_KING =3
WHITE_KING =4
NA = -1000
STARTING_BOARD =    [1,1,1,1,     # 0  1  2  3
                      1,1,1,1,    # 4  5  6  7
                      1,1,1,1,    # 8  9  10 11
                      0,0,0,0,    # 12 13 14 15
                      0,0,0,0,    # 16 17 18 19
                      2,2,2,2,    # 20 21 22 23
                      2,2,2,2,    # 24 25 26 27
                      2,2,2,2]   # 28 29 30 31
 
class State:
  '''
  Initializes state object
  '''
  def __init__(self,current_player=1, board=STARTING_BOARD, which=BLACK):
    # open debugger log
    # variable to indicate whether we are the current player
    self.is_current_player = current_player
    self.board = board
    self.which_player = which 
    self.no_more_moves = True
    self.over = False
    self.cache = MoveCache()
    self.possible_actions  = []
    self.feasible_list = []
    self.feasible_count = -1
    self.generateActions()
    
  '''
  Returns 1 for maximizer, -1 for minimizer
  Required by mcts library
  '''
  def getCurrentPlayer(self):
    return self.is_current_player

  def generateActions(self):
    # first check if this state is already in the cache
    stored_moves = self.cache.retrieve_moves(self.which_player, self.board)
    if stored_moves != -1:
        print("mcts.py: cached collection of moves identified")
        # update feasible count so terminal state can be identified
        self.feasible_count = len(stored_moves)
        self.possible_actions = stored_moves
        print_board_nicely(self.board)
        print(stored_moves)
        # exit before calculating, we already have moves calculated
        return 

    self.feasible_count = 0 # determine whether the player could actually move
    # iterate through every location in the board
    for i in range(len(self.board)):
        piece = self.board[i]
        # if the location is uninhabited, or not controlled by current player
        if(piece == 0 or (not self.is_controllable(piece))): 
          # skip over
          continue
        # if the loctation can be controlled by player, find all potential movesets
        else:
          # get moves for every piece
          if(self.does_legal_move_exist(i)):
            self.init_moves(i,piece)
            self.feasible_list.append(i)
    #update feasible_count here so that isTerminal knows whether to actually end or not 
    self.feasible_count = len(self.feasible_list)


  '''
  Returns an iterable of all actions which can be taken from this state
  Required by mcts library
  '''
  def getPossibleActions(self):
    #write possible actions to cache before returning, if entry does not exist
    if self.cache.retrieve_moves(self.which_player,self.board) == -1:
        self.cache.write_moves(self.which_player,self.board, self.possible_actions)
    return self.possible_actions


  def does_legal_move_exist(self, i):
      val = self.board[i]
      if(val == 0):
        return False
      moves = dict.get(i,val)
      if(self.is_viable_dest(i+moves[0]) or self.is_viable_dest(i+moves[1]) or self.is_viable_dest(i+moves[4]) or self.is_viable_dest(i+moves[5])):
        return True
      if self.is_viable_hop(i,i+moves[0],i+moves[2]) or self.is_viable_hop(i,i+moves[1],i+moves[3]) or self.is_viable_hop(i,i+moves[5],i+moves[7]) or self.is_viable_hop(i,i+moves[4], i+moves[6]):
        return True
      return False # no legal move was found so no legal move exists
     
  
  # thread wrapper function to remove overhead from lambda expresion
  def perform_hop_wrapper(self,index,a,b):
    self.perform_hop(index, a,b,self.board)

  # thread wrapper function to remove overhead from lambda expresion
  def perform_placement_wrapper(self,index,a):
    self.perform_placement(index, a)


  def init_moves(self,index,piece_val):
    moveset = dict.get(index,piece_val)
    # create threads for each hop
    hop_threads = []

    hop_threads.append(Thread(target=self.perform_hop_wrapper, args=(index,index+moveset[0],index+moveset[2])))
    hop_threads.append(Thread(target=self.perform_hop_wrapper, args=(index,index+moveset[1],index+moveset[3])))
    hop_threads.append(Thread(target=self.perform_hop_wrapper, args=(index,index+moveset[4],index+moveset[6])))
    hop_threads.append(Thread(target=self.perform_hop_wrapper, args=(index,index+moveset[5],index+moveset[7])))

    # first run hop threads 
    for thread in hop_threads:
      thread.start()
    for thread in hop_threads:
      thread.join()

    # check if the list is nonempty before initiating placement threads, so that only taking moves are considered 
    if (len(self.getPossibleActions()) != 0):
        return

    placement_threads =[]
    for i in [0,1,4,5]:
        placement_threads.append(Thread(target=self.perform_placement_wrapper(index,index+moveset[i])))
   
   # now run placement threads 
    for thread in placement_threads:
      thread.start()
    for thread in placement_threads:
      thread.join()


  '''
  Returns the state which results from taking action action
  Required by mcts library
  '''  
  def takeAction(self,action):
        new_state = deepcopy(self)
        new_state.board = action.board
        # clear lists for next state
        new_state.possible_actions.clear() 
        new_state.feasible_list.clear()
        new_state.is_current_player = self.is_current_player * -1
        # alternate between whether it is black or white 
        new_state.which_player = BLACK if (self.which_player == WHITE) else WHITE
        new_state.generateActions()
        
        return new_state

  '''
  to string for state object
  '''
  def __str__(self):
    
    str_board = "\n"
    for i in range(len(self.board)):
        str_board = str_board + " " +  str(self.board[i]) 
        if ((i+1) % 4 == 0): # new line 
          str_board = str_board + " : "
          for j in range(i-3,i+1):
            str_board = str_board + " " + str(j)
          str_board = str_board + "\n"
    str_board = str_board + "Pieces left with possible moves:\n"
    for i in range(len(self.board)):
        val = self.board[i]
        if(val != 0):
          moves = dict.get(i,val)
          str_board = str_board + str(i) + " :"
          for j in range(len(moves)):
            if(moves[j] != NA):
              str_board = str_board + " "+ str(i + moves[j]) + " , "
          str_board = str_board + '\n'
    any_legal = False
    count = 0
    for i in range(len(self.board)):
       if(self.does_legal_move_exist(i)):
          str_board = str_board + "Legal moves exist for " + str(i) +" val(" +str(self.board[i]) + ") \n"
          str_board = str_board + "Dictionary entry for "+str(i) + " : " + str(dict.get(i,self.board[i])) + '\n'
          count+=1
          any_legal = True
    if(any_legal == True):
        str_board+=("Therefore legal moves exist for this state.\n")
        str_board+=("Legal move count: " + str(count) +'\n')
    else:
        str_board+=("There are no legal moves for this state\n")
    str_board+=("len(possible_actions) = " + str(len(self.possible_actions)) + '\n')
    str_board+=("feasible_count = " + str(self.feasible_count) + '\n')
    str_board+=("feasible list = " + str(self.feasible_list))
    return str_board

  '''
  Gives information on the board state in the form of a numpy array
  Inspired by this article : 
  https://blog.paperspace.com/building-a-checkers-gaming-agent-using-neural-networks-   and-reinforcement-learning/
  '''
  def get_metrics():
    pass
  '''
  Determines whether the game is over. 
  Required by mcts library
  '''
  def isTerminal(self):
    # current player has no legal moves
    if(self.feasible_count == 0 ):
      return True
    # black has no checkers left
    if( (1 not in self.board) and (3 not in self.board) ):
      return True
    # white has no checkers left
    elif( (2 not in self.board) and (4 not in self.board) ):
      return True
    #if all previous conditions are false, the game is still on! 
    else:
      return False

  '''
  Returns the reward for this state. Only needed for terminal states.
  Required by mcts library
  '''
  def getReward(self):
    sum_b = self.board.count(BLACK) + (self.board.count(BLACK_KING)) 
    sum_w = self.board.count(WHITE) + (self.board.count(WHITE_KING) )
    if(self.which_player == BLACK and sum_w == 0):
        return 1
    elif(self.which_player == WHITE and sum_b == 0):
        return 1
    else: #no reward unless game is won
      return 0

    

  '''
  Returns whether a checker piece has reached a kinging zone 
  '''
  def is_in_the_king_zone(self, index):
    if(self.which_player == WHITE):
        if(index < 4):
          return True
    elif(self.which_player == BLACK):
        if(index > 27):
          return True
    return False

    '''
    Determines whether a piece can be moved by the current player or not. 
    '''
  def is_controllable(self,piece):
      if(piece == self.which_player):
        return True
      elif(self.which_player == BLACK and piece ==BLACK_KING ):
        return True
      elif(self.which_player == WHITE and piece == WHITE_KING):
        return True
      else:
        return False

  '''
  Modfies array to represent piece taking,
1  is called recursively until no hops are left
  
  '''
  def perform_hop(self,start,middle,end,board):
    new_board = deepcopy(board)
    if(self.is_viable_hop(start,middle,end)):
      val = new_board[start]
      if(self.is_in_the_king_zone(end)):
        val = BLACK_KING if val == BLACK else WHITE_KING
      new_board[start] = 0
      new_board[middle] =0
      new_board[end] = val # put the piece back
      start = end
      moveset = dict.get(index=start,piece_value=val)
      # hops in the positive direction
      #start, #left, #lefthop
      if(moveset[0]!= NA and moveset[2] != NA):
        return self.perform_hop(start,start+moveset[0],start+moveset[2],new_board)
                  #start, right, righthop
      if(moveset[1]!= NA and moveset[3] != NA):
        return self.perform_hop(start,start+moveset[1],start+moveset[3],new_board)

      # hops in negative direction
                  #start,left,lefthop
      if(moveset[4]!= NA and moveset[6] != NA):
        return self.perform_hop(start,start+moveset[4], start+moveset[6],new_board)
                  #start, right, righthop
     
      if(moveset[4]!= NA and moveset[6] != NA):
        return self.perform_hop(start,start+moveset[5], start+moveset[7],new_board)

      self.possible_actions.append(Action(player=self.getCurrentPlayer(),board_state=board))
    else:
      # base case, recursion ends
      # if the board has changed, add it to the action list
        if(self.board != new_board):
            self.add_action(new_board)
  '''
  Modifies array to represent piece movement 
  Takes board state, starting index and ending index
  '''
  def perform_placement(self,start,end):
    if self.is_viable_dest(end) and self.index_in_range(start):
      new_board = deepcopy(self.board)
      if(self.is_in_the_king_zone(end)):
        piece = BLACK_KING if (self.which_player == BLACK) else WHITE_KING
      else:
        piece = new_board[start] # grab moving piece's value   
      new_board[start] = 0     # leave previous space empty 
      new_board[end] = piece   # place piece in new location
      self.add_action(new_board)
  '''
  Determines whether a hop is possible or not.
  Can be called multiple times for checking validity of multiple hops
  Accepts three indicies, the starting index of the piece
  The index of the piece they are hopping over, and the
  target destination
  '''
  def is_viable_hop(self,start,middle,end):
    # If all needed conditions are met, return true
    # 0 ) Must be a piece
    #  1 ) All indicies must be in range, 
    #  2 ) The destination location must be a 0,
    # 3  ) The taken piece and the taker piece must be on different teams
    if(self.board[start] < 1):
      return False
    if(self.index_in_range(start) and self.index_in_range(middle) and self.index_in_range(end)):
      taker = self.board[start]
      taken = self.board[middle]
      dest = self.board[end]
      if( dest == 0):
        if((taker == WHITE or taker == WHITE_KING) and (taken == BLACK or taken == BLACK_KING) ):
          return True
        elif((taker == BLACK or taker == BLACK_KING) and (taken == WHITE or taken == WHITE_KING)):
          return True
    #One of these conditions was not met if this code is reached. Return False.
    return False

  '''
  Appends action object to list, used for collecting all possible moves
  Accepts old index and new index
  '''
  def add_action(self,board):
      # only add an action if its unique from current board; this shouldnt be possible 
      if(board != self.board):
          self.possible_actions.append(Action(player=self.getCurrentPlayer(),board_state=board))
      return self.possible_actions
      
  '''
  Returns whether an index is in range
  '''
  def index_in_range(self,index):
      return (index >= 0 and index <= 31)

  '''
  Returns whether a location is a viable destination
  '''
  def is_viable_dest(self,index):
    if(not self.index_in_range(index)):
      return False
    elif(self.board[index] == 0):
      return True
    else:
      return False
 
'''
  Action class. Contains board array. 
'''
class Action():
    def __init__(self, player,board_state):
        self.player = player
        self.board = board_state

    def __str__(self):
      str_board = "\n"
      for i in range(len(self.board)):
          str_board = str_board + " " +  str(self.board[i])
          if ((i+1) % 4 == 0): # new line 
            str_board = str_board + "\n"
      return str_board

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        for i in range(len(self.board)):
          if (self.board[i] != other.board[i]):
            return False
        return True

    def __hash__(self):
        return hash((tuple(self.board), self.player))

def print_board_nicely(board: list[int]):
  str_board = "\n"
  for i in range(len(board)):
      str_board = str_board + " " +  str(board[i]) 
      if ((i+1) % 4 == 0): # new line 
        str_board = str_board + " : "
        for j in range(i-3,i+1):
          str_board = str_board + " " + str(j)
        str_board = str_board + "\n"
  print(str_board)


