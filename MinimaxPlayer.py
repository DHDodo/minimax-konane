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

    # Performs alpha-beta pruning to determine the most optimal board for a given player.
    # Node refers to a board
    def minimax(self, node, side, depth, alpha, beta, isMaximizingPlayer):
        allValidMoves = self.generateMoves(node, side)
        # When we reach a point with no more valid moves,
        # don't return heuristic, instead indicate win/loss
        if len(allValidMoves) == 0:
            return float("-inf") if isMaximizingPlayer else float("inf")
        # Get heuristic once we are at our depth
        if depth == 0:
            return self.eval(node)

        # Alpha-beta pruning algorithm (fail-hard)
        if isMaximizingPlayer:
            value = float("-inf")
            # Get possible moves for the node 
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
            # Get possible moves for the node
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
                if moveWeight > bestMove[0]:
                    bestMove[0] = moveWeight
                    bestMove[1] = move
            # Defeat conditional: select the first move if we have no winning options
            if bestMove[1] == None:
                return moves[0]
            # Otherwise, return the best move that we found
            return bestMove[1]

    # My possible moves - enemy's possible moves heuristic
    # Considers the # of moves the board affords to the player - the # of moves it affords to the enemy
    def eval(self, board):
        return len(self.generateMoves(board, self.side)) - len(self.generateMoves(board, self.opponent(self.side)))
