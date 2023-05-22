
'''
Stores legal moves for each index on a checkerboard  following the ID implementation
  
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
    # Hardcoding some of the special cases to not only show the structure of the dictionary,
    # but also to avoid repeated branching-and-hard-to-identify bugs. 
    self.catalogue =  {0 :[[4,5,NA,9,NA,NA,NA,NA], # Black piece's potential movement index when starting from location 0 on checkerboard
                         [NA,NA,NA,NA,NA,NA,NA,NA],    # White piece's potential movement index when starting from location 0 on checkerboard
                         [4,5,NA,9,NA,NA,NA,NA,NA],    # Black king's piece  potential movement index when starting from location 0 on checkerboard
                         [4,5,NA,9,NA,NA,NA,NA,NA]],    # White King's piece potential movement index when starting from location 0 on checkerboard
                         
                      31: [[NA,NA,NA,NA,NA,NA,NA,NA], # No such thing as a black piece at index 31, just like no such thing as white piece at index 0 
                          [NA,NA,NA,NA,-5,-4,-9,NA],   # White piece's legal movements from index 31
                          [NA,NA,NA,NA,-5,-4,-9,NA],   # Black king's legal movements from index 31
                          [NA,NA,NA,NA,-5,-4,-9,NA]], # White king's legal movements from index 31
                       
                      28:[[NA,NA,NA,NA,NA,NA,NA,NA],  # No black piece at index 28 as it is a kinging zone 
                          [NA,NA,NA,NA,NA,-4,NA,-7],  # white piece legal movements from index 28... you get the idea
                          [NA,NA,NA,NA,NA,-4,NA,-7],
                          [NA,NA,NA,NA,NA,-4,NA,-7]],
                    3: [[4,NA,NA,7,NA,NA,NA,NA],  
                          [NA,NA,NA,NA,NA,NA,NA,NA],  
                          [4,NA,NA,7,NA,NA,NA,NA],
                          [4,NA,NA,7,NA,NA,NA,NA]],
                    1: [[4,5,7,9,NA,NA,NA,NA],  
                        [NA,NA,NA,NA,NA,NA,NA,NA],  
                        [4,5,7,9,NA,NA,NA,NA],
                        [4,5,7,9,NA,NA,NA,NA]],
                      2: [[4,5,7,9,NA,NA,NA,NA],  
                        [NA,NA,NA,NA,NA,NA,NA,NA],  
                        [4,5,7,9,NA,NA,NA,NA],
                        [4,5,7,9,NA,NA,NA,NA]],
                      25:[[4,5,NA,NA,NA,NA,NA,NA], 
                         [NA,NA,NA,NA, -4,-3,-9,-7],
                         [4,5,NA,NA, -4,-3,-9,-7], 
                         [4,5,NA,NA,  -4,-3,-9,-7],], 
                      30:[[4,5,NA,NA,NA,NA,NA,NA], 
                         [NA,NA,NA,NA, -4,-3,-9,-7],
                         [4,5,NA,NA, -4,-3,-9,-7], 
                         [4,5,NA,NA,  -4,-3,-9,-7],],  
                    
                      }
    self.add_left_edges()
    self.add_right_edges()
    self.add_restricted()
    self.add_common_cases()

  '''
  Adds left edge locations to the dictionary. Such as 4, 12 and 20.
  '''
  def add_left_edges(self):
    table = [[NA,4,NA,9,NA,NA,NA,NA],
            [NA,NA,NA,NA,NA,-4,NA,-7],
            [NA,4,NA,9,NA,-4,NA,-7],
            [NA,4,NA,9,NA,-4,NA,-7]]
    
    self.catalogue[12] = table
    self.catalogue[20] = table
    # slightly adjust table for index 4 to save branches later
    for i in range(4):
      table[i][7] = NA
    self.catalogue[4] = table

  '''
  Adds right edge locations to the dictionary. Such as 11,19,27
  '''
  def add_right_edges(self):
    table = [[4,NA,7,NA,NA,NA,NA,NA],
            [NA,NA,NA,NA,NA,-4,NA,-9],
            [4,NA,7,NA,NA,-4,NA,-9],
            [4,NA,7,NA,NA,-4,NA,-9]]
    
    self.catalogue[11] = table
    self.catalogue[19] = table
    # slightly adjust table for index 27 to save branches later
    for i in range(4):
      table[i][2] = NA
    self.catalogue[27] = table

  '''
  Adds all common case locations to dictionary. Such as 13,9,18 
  where from a kings perspective all potential moves are more or less legal
  '''
  def add_common_cases(self):
    for i in range(32):
      if i not in self.catalogue:
        if i in ODD_ROW_INDICIES:
          table =[[4,5,7,9,NA,NA,NA,NA], 
                [NA,NA,NA,NA, -4,-3,-9,-7],
                 [4,5,7,9, -4,-3,-9,-7], 
                 [4,5,7,9, -4,-3,-9,-7],]
        if i in EVEN_ROW_INDICIES:
          table =[[3,4,7,9,NA,NA,NA,NA], 
                [NA,NA,NA,NA, -5,-4,-9,-7],
                 [3,4,7,9, -5,-4,-9,-7], 
                 [3,4,7,9, -5,-4,-9,-7],]
        self.catalogue[i] = table # add entry to internal dictionary 
        

  '''
  Retrieves desired move list from the index dictionary.
  For example, in the State class call
  index_dict.get(0,BLACK),
  this function returns the list from the 0 entry at index 0. (Since constant BLACK == 1)
  
  '''
  def get(self,index,piece_value):
    return self.catalogue.get(index)[piece_value-1]


  '''
  For columns that only have 6 potential locations instead of 8
  Kind of hacky and ugly, but only runs once and gets the job done. *shrug* 
  '''
  def add_restricted(self):
    no_left_jumps = [8,16,24]
    no_right_jumps =[7,15,23]

    odd = [[4,5,7,9,NA,NA,NA,NA], 
                [NA,NA,NA,NA, -4,-3,-9,-7],
                 [4,5,7,9, -4,-3,-9,-7], 
                 [4,5,7,9, -4,-3,-9,-7],]
    even =[[3,4,7,9,NA,NA,NA,NA], 
                [NA,NA,NA,NA, -5,-4,-9,-7],
                 [3,4,7,9, -5,-4,-9,-7], 
                 [3,4,7,9, -5,-4,-9,-7],]
    for i in range(3):
      x = no_left_jumps[i]
      y = no_right_jumps[i]
      if(x in EVEN_ROW_INDICIES):
        tablex = list(even)
      elif(x in ODD_ROW_INDICIES):
        tablex= list(odd)
      if(y in EVEN_ROW_INDICIES):
        tabley = list(even)
      elif(y in ODD_ROW_INDICIES):
        tabley= list(odd)

      for i in range(4):
          tablex[i][2] = NA
          tablex[i][6] =NA
          tabley[i][3] = NA
          tabley[i][7] = NA
      #append entries to the dictionary 
      self.catalogue[x] = tablex
      self.catalogue[y] =tabley
    
      


