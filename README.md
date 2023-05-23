# ChAIckers2
Checker Playing AI using Deep Learning
------------------------------------------

### Notable changes made since CS478 Project :
## MTCS:
  * Checker states are represented with Numpy Array (as opposed to int lists) for better time and space complexity
  * Caching system to save time re-computing possible moves for a given state
  * GUI debugger for easier error checking  
   ![myboard_checkers (4)](https://github.com/jordansprojects/ChAIckers2/assets/54329371/8512ecb7-2138-4754-a607-bc324759b6d7)
   
  * Index system is reworked so that valid checker indicies from a given position are computed beforehand, so that minimal computations are done during the move generation phase.
