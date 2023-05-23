
'''
Stores legal moves for each index on a checkerboard  following the ID implementation
TO-DO : rework this to remove addiction computed 

'''

# "ODD" vs "EVEN" row indicies are relevant as they determine  rules in terms of movement 
ODD_ROW_INDICIES = [0, 1 , 2 , 3, 8 ,9, 10, 11, 16,17, 18, 19, 24,25,26,27]
EVEN_ROW_INDICIES = [4,5,6,7,12,13,14,15,20,21,22,23,28,29,30,31] 

# Constant to represent invalid movements from a particular position
# NA aka Non-Applicable
NA = -1000
class IndexDictionary:
  '''
  The IndexDictionary structure is as follows:
  index : list of lists for each piece. 
  
  The internal lists use the following structure : 
  
    [+left move, +right move, +left hop, +right hop, -left move, -right move, -left hop, -right hop]
    The constant NA, set to -1, represents a movement that is not legal to that piece.
    For example, a black piece at index zero can only go to 4, 5, and 9. It cannot go to 7 so the right hop entry must be NA 
  '''
  
  def __init__(self):
    self.step_catalogue ={}
    self.hop_catalogue ={}

  '''
  Retrieves desired move list from the index dictionary.
  For example, in the State class call
  index_dict.get(0,BLACK),
  this function returns the list from the 0 entry at index 0. (Since constant BLACK == 1)
  
  '''
  def get(self,index):
    return self.catalogue.get(index)



  def init_entries():
      location = 0
      for i in range(8): # rows
          for j in range(4): #co
              if (i % 2 == 0): # even row
                  self.catalogue[location] = [location + 4, location + 5]
