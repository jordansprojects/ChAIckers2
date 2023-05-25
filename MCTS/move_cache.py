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
        index = hash(given.tobytes())
        if who == 1:
           self.black[index] = moves
        else:
            self.white[index]= moves

    def retrieve_moves(self,who,given):
        index = hash(given.tobytes())
        if who ==1:
            moves = self.black.get(index,-1)
        else:
           moves = self.white.get(index,-1)
        return moves

