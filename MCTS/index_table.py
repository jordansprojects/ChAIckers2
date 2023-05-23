
'''
Stores legal moves for each index on a checkerboard  following the ID implementation
TO-DO : rework this to remove addiction computed 

'''
BLACK  = 1
WHITE  = 2 
BLACK_KING =3
WHITE_KING =4

class IndexTable:
  def __init__(self):
    #
    self.black_steps=[ [] for _ in range(32)]
    self.white_steps=[]
    self.king_steps=[]
    # hops is a dictionary of tuples. The first element in the tuple is the index of the 
    # checker that is being taken. The second index is the landing location of the checker doing the hop
    self.black_hops =[ [] for _ in range(32)]
    self.white_hops = []
    self.king_hops =[]

    #initialize entries for black pieces
    self.init_black()

    #TO-DO purify lists of invalid entries

  '''
  Retrieves desired move list from the index dictionary.
  '''
  def get_steps(self,value,index):
      if( value == BLACK):
          return self.black_steps[index]
      elif(value == WHITE):
          return self.white_steps[index]
      else:
        return self.king_steps[index]

  def get_hops(self,value,index):
      if( value == BLACK):
          return self.black_hops[index]
      elif(value == WHITE):
          return self.white_hops[index]
      else:
          return self.king_hops[index]
   


  def init_black(self):
      location = 0
      for row in range(8): 
          for col in range(4): 
              self.black_steps[location].append(location+4)
              if row % 2 == 0: # even row
                  if col < 3: # can move to the right
                      self.black_steps[location].append(location+5)
                      self.black_hops[location].append( (location+5,location+9))
                  if col > 0: # can move to the left
                      self.black_hops[location].append( (location+4, location+7))
              else: # odd row
                  if col < 3 : # can move right
                      self.black_hops[location].append( (location+4, location+9))
                  if col > 0: # can move to the left
                      self.black_steps[location].append(location+3)
                      self.black_hops[location].append( (location+3, location+7) )
              location = location+1 #increment location value
