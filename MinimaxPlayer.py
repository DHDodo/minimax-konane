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

    # "Jumpable neighbors" heuristic
    # Aim is to have more pieces that can jump in the future than opponent
    # Does not ignore walls, ignores pieces in the way and multi jumps
    # Positive score = more jumps than opponent. Negative = less (losing).
    def eval(self, board):
        count = 0
        # Loop through the valid range within the grid (so we don't hit edges)
        for row in range(self.size):
            for col in range(self.size):
                # Get current piece to check its opponent for viability
                currentPiece = board[row][col]
                # Only affect heuristic count if there's a valid piece
                if currentPiece != ".":
                    # North jump check--must be row 2 or higher, must have a piece to jump
                    northIsViable = False
                    if row >= 2:
                        northPiece = board[row - 1][col]
                        northIsViable = northPiece == self.opponent(currentPiece)

                    # East jump check--must be col 5 or lower, must have a piece to jump
                    eastIsViable = False
                    if col <= 5:
                        eastPiece = board[row][col + 1]
                        eastIsViable = eastPiece == self.opponent(currentPiece)

                    # South jump check--must be row 5 or lower, must have a piece to jump
                    southIsViable = False 
                    if row <= 5:
                        southPiece = board[row + 1][col]
                        southIsViable = southPiece == self.opponent(currentPiece)

                    # West jump check--must be col 2 or higher, must have a piece to jump
                    westIsViable = False 
                    if col >= 2:
                        westPiece = board[row][col - 1]
                        westIsViable = westPiece == self.opponent(currentPiece)

                    # Add if it's our piece, subtract if it isn't
                    if currentPiece == self.side:
                        count += 1 if northIsViable else 0
                        count += 1 if eastIsViable else 0
                        count += 1 if southIsViable else 0
                        count += 1 if westIsViable else 0
                    else:
                        count -= 1 if northIsViable else 0
                        count -= 1 if eastIsViable else 0
                        count -= 1 if southIsViable else 0
                        count -= 1 if westIsViable else 0
        # Return heuristic stored in count
        return count

# game = Konane(8) 
# game.playOneGame(RandomPlayer(8), RandomPlayer(8), 1)
game.playNGames(10, MinimaxPlayer(8, 4), RandomPlayer(8), 0)
