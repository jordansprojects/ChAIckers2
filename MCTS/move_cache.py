'''
Stores possible moves from a state

'''
class MoveCache:
    def __init__(self):
        # stored moves for black
        self.black = {}
        self.best_for_black ={}
        # stored moves for white
        self.white = {}
        self.best_for_white ={}

    def write_moves(self, who,given,moves):
        if who == 1:
           self.black[tuple(given)] = (tuple(moves))
        else:
            self.white[tuple(given)]= (tuple(moves))

    def retrieve_moves(self,who,given):
        if who ==1:
            moves = self.black.get(tuple(given),-1)
        else:
           moves = self.white.get(tuple(given),-1)
        if( moves != -1):
            moves = list(moves)
        return moves

