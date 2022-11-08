## Filename: MinimaxPlayer.py
## Authors: Briar Sauble and Robert Bunning

from konane import *

# float("inf") or -float("inf") indicate no more moves
class MinimaxPlayer(Konane, Player):    
    
    def __init__(self, size, depthLimit):
        Konane.__init__(self, size)
        self.limit = depthLimit

    def initialize(self, side):
        self.side = side
        self.name = "Super Minimax Deluxe"

    # The initial call will be for the maximizing player
    # Node is a board
    def minimax(self, node, side, depth, alpha, beta, isMaximizingPlayer):
        allValidMoves = self.generateMoves(node, side)
        # If depth is zero or we are the deepest in the tree, get heuristic
        if depth == 0:
            # return the heuristic of this node
            return self.eval(node)
        if len(allValidMoves) == 0:
            return float("-inf") if isMaximizingPlayer else float("inf")
        if isMaximizingPlayer:
            value = float("-inf")
            # get possible moves for the node 
            # Value = the max b/w value and a recursive call to the alpha beta:
            for move in allValidMoves:
                value = max(value, self.minimax(self.nextBoard(node, side, move), self.opponent(self.side), depth - 1, alpha, beta, False))
                if value >= beta:
                    break # beta cutoff
                alpha = max(alpha, value)
            return value
        # We are the minimizing player
        else:
            value = float("inf")
            # get possible moves for the node
            # Value = the min b/w value and a recursive call to the alpha beta:
            for move in allValidMoves:
                value = min(value, self.minimax(self.nextBoard(node, side, move), self.side, depth - 1, alpha, beta, True))
                if value <= alpha:
                    break # alpha cutoff
                beta = min(beta, value)
            return value

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
        n = len(moves)
        # If there's no moves, don't bother
        if n == 0:
            return []
        else:
            # We want to find the best next move
            bestMove = [float("-inf"), None]
            # Loop through all possible moves for our maximizer
            for move in moves:
                # Calculate the weight of the move based on what our minimizing opponent will do
                moveWeight = self.minimax(self.nextBoard(board, self.side, move), self.opponent(self.side), self.limit - 1, bestMove[0], float("inf"), False)
                # Replace the best move if it obtains a higher score
                if (moveWeight > bestMove[0]):
                    bestMove[0] = moveWeight
                    bestMove[1] = move
            return bestMove[1]
                
    # 
    def eval(self, board):
        count = 0
        for row in range(self.size):
            for col in range(self.size):
                # Check left (Can we go left?)
                if row > 2 and board[row - 1][col] != '.' and board[row - 1][col] == self.opponent(self.side):
                    count += 1
                # Check right
                    
        # We don't care what this does yet, just make it eval something as a test
        # Having pieces on the board that still have valid moves
        return random.randint(0, 9)

# game = Konane(8) 
# game.playOneGame(RandomPlayer(8), RandomPlayer(8), 1)
# game.playNGames(2, MinimaxPlayer(8, 2), MinimaxPlayer(8, 1), 0)