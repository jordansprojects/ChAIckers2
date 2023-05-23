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

