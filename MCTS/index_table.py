`
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

    # list of lists, stores viable one-step
    # movements for each index 
    # each piece value has its own list 
    self.black_steps=[ [] for _ in range(32)]
    self.white_steps=[ [] for _ in range(32) ]
    self.king_steps=[  [] for _ in range (32) ]
    

    # List of tuples. First index is the index being
    # hoped over, the second index is the landing 
    # index of the piece doing the taking
    # each piece value has its own list 
    self.black_hops =[ [] for _ in range(32)]
    self.white_hops = [[] for _ in range(32) ]
    self.king_hops =[ [] for _ in range(32) ]

    # compute list entrites to fill list with
    # valid indicies from a given location 
    self.init_entries()

    # Scan through list to remove all invalid entries 
    self.purify()

  '''
  Retrieves list of moves for a provided piece value and index
  @return a list of integers, each a potential valid move index 
  '''
  def get_steps(self,value,index):
      if( value == BLACK):
          return self.black_steps[index]
      elif(value == WHITE):
          return self.white_steps[index]
      else:
        return self.king_steps[index]

  '''
  Retrieves hop list for a provided piece value and index 
  @return a list of tuples in the format (hopped_over, hopped_to)
  '''
  def get_hops(self,value,index):
      if( value == BLACK):
          return self.black_hops[index]
      elif(value == WHITE):
          return self.white_hops[index]
      else:
          return self.king_hops[index]
   
  '''
  Utiilizes mathematical patterns found in the checkerboard to init a list of lists for each piece.
  The index in the list corresponds to the index location in the board, providing a list of all
  viable moves or jump-tuple pairs. 
  '''
  def init_entries(self):
      location = 0
      for row in range(8): 
          for col in range(4): 
              self.black_steps[location].append(location+4)
              self.white_steps[location].append(location-4)
              if row % 2 == 0: # even row
                  if col < 3: # can move to the right
                      self.black_steps[location].append(location+5)
                      self.black_hops[location].append( (location+5,location+9))
                      self.white_steps[location].append(location -3)
                      self.white_hops[location].append( (location-3, location-7))
                  if col > 0: # can move to the left
                      self.black_hops[location].append( (location+4, location+7))
              else: # odd row
                  if col < 3 : # can move right
                      self.black_hops[location].append( (location+4, location+9))
                      self.white_hops[location].append( (location-4,location-7)) 
                  if col > 0: # can move to the left
                      self.black_steps[location].append(location+3)
                      self.black_hops[location].append( (location+3, location+7) )
                      self.white_steps[location].append(location-5)
                      self.white_hops[location].append( (location-5,location-9)) 
              location = location+1 #increment location value

  '''
  Removes entries that are out of range
  '''
  def purify(self):
      for i in range(32):
          # remove invalid location indicies for steps
          self.black_steps[i] = [number for number in self.black_steps[i] if number < 31 and number > -1]
          self.white_steps[i] = [number for number in self.white_steps[i] if number < 31 and number > -1]

          # remove any invalid hop tuple that contains an invalid index
          self.black_hops[i] = [ tpl for tpl in self.black_hops[i] if tpl[0] < 31 and tpl[0] > -1 and  tpl[1] < 31 and tpl[1] > -1]
          self.white_hops[i] = [ tpl for tpl in self.white_hops[i] if tpl[0] < 31 and tpl[0] > -1 and  tpl[1] < 31 and tpl[1] > -1]
   
          # join lists for king movements, since a king can move in the directions of a white piece and a black piece
          self.king_steps[i] = self.black_steps[i] + self.white_steps[i]
          self.king_hops[i] = self.black_hops[i] + self.white_hops[i]
