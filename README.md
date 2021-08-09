# Mancala Game

Implementation of 3 different heuristics for the functions: evaluation of game board states and decision making:
- Monte Carlo
Before starting the evaluation of the game board states, extract and evaluate the board squares that will be used in the analysis. Then making a decision to choose the most promising moves. The selection starts from the root of the tree. Then the method creates descendant nodes in a loop until it reaches a value which symbolises a leaf of the tree. 
The method plays out simulations based on the selected nodes, up to the final depth of the tree. During this process, the program saves the node with which the simulation went best.  Through back propagation, the information in the nodes is updated.

-Monte Carlo - informed
evaluates the state of the board and makes a decision to select the most promising moves. The selection starts with determining the number of iterations of the observed nodes. The program proceeds to analyse the fields of the game board and the possible points, stored in the moveScore table. Points are counted based on the player's selected moves from the availableMoves array, which is a decision to select the most promising moves.
 
-Monte Carlo - random
Evaluation of the state of the board is undertaken randomly.

Comparison of the number of moves AI winning vs AI with algorithm 
min-max vs alpha-beta for different tree depths:
- tree depth = 2,
- tree depth = 4,
- tree depth = 5,
- tree depth = 6,
- tree depth = 7,

...

Visualization of game board state


...
