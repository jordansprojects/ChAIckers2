# mcts_test.py - tester file for mcts 
import os, sys
import unittest
sys.path.append(os.getcwd() + '/..')
from checker_mcts import *
from debugger_board import *

'''
 @board : 1D array of len 32 representing checker board
 @param whos_turn : 1 for BLACK (Player 1) or 2 for WHITE (Player 2)
        Using WHITE default
 @param current_player: max or minimizing. 1 for maximizing player, -1 for min. 
       Using max default
 @return array that was considered the best action or -1 if terminal state reached
'''
def run_mcts(board , whos_turn = WHITE ,current_player=1,limit=2500):
  searcher = mcts(timeLimit=limit)
  s = State(which =whos_turn,current_player=current_player,board=board )
  if(s.isTerminal()):
    print("Terminal state reached.")
    return -1
  action = searcher.search(initialState=s)
  return action.board

'''
 creates pyqt window of mcts 
'''
def create_debugger():
    app = QApplication(sys.argv)
    board_widget = CheckerBoardWidget() 
    board_widget.show()
    board_widget.get_piece_sprites()
    board_widget.draw_pieces_on_board(STARTING_BOARD)
    sys.exit(app.exec_())


'''
    Alternates between black and white,
    finds best move for each player. That
    becomes the new state to find the best move from 
'''
def play_against_self():
    app = QApplication(sys.argv)
    board_widget = CheckerBoardWidget() 
    board_widget.show()
    board_widget.get_piece_sprites()
    board_widget.draw_pieces_on_board(STARTING_BOARD)
    b= STARTING_BOARD
    who = BLACK
    i = 0
    while( True and isinstance(b, np.ndarray )):
        print("turn #" , i)
        board_widget.draw_pieces_on_board(b)
        board_widget.repaint()
        app.processEvents()
        #print_board_nicely(b)
        b = run_mcts(board=b, whos_turn=who)
        who = BLACK if who == WHITE else WHITE
        i = i +0.5
    sys.exit(app.exec_())



'''
    Alternates between black and white,
    finds best move for each player. That
    becomes the new state to find the best move from 
'''
def play_against_self_console():
    b= STARTING_BOARD
    who = BLACK
    while( True ):
        print_board_nicely(b)
        b = run_mcts(board=b, whos_turn=who)
        who = BLACK if who == WHITE else WHITE


if __name__ == '__main__':
    play_against_self()
