# ChAIckers2: Checker Playing AI using Deep Learning

## Notable changes made since CS478 Project :
### MTCS:
  * Checker states are represented with Numpy Array (as opposed to int lists) for better time and space complexity
  * Caching system to save time re-computing possible moves for a given state
  * GUI debugger for easier error checking  
![checkerboard](https://github.com/jordansprojects/ChAIckers2/assets/54329371/565c8e92-5ce8-4488-8ee8-73ecf4c38b68)

  * Index system reworked so that valid checker indicies from a given position are computed beforehand, so that minimal computations are done during the move generation phase.
