from konane import *

# float("inf") or -float("inf") indicate no more moves
class MinimaxPlayer(Konane, Player):    
    
    def __init__(self, size, depthLimit):
        Konane.__init__(self, size)
        self.limit = depthLimit
        self.name = "Unique team name"

    # The initial call will be for the maximizing player
    # Node is a board
    def minimax(node, depth, alpha, beta, isMaximizingPlayer):
        allValidMoves = self.generateMoves(node, self.side)
        # If depth is zero or we are the deepest in the tree
        if depth == 0 || allValidMoves.len() == 0:
            # return the heuristic of this node
            return eval(node)
        if isMaximizingPlayer:
            value = -float("inf")
            # get possible moves for the node and FOR EACH
            #   Value = the max b/w value and a recursive call to the alpha beta:
            #   alphabeta(child, depth - 1, alpha, beta, false)
            #    alpha = max(alpha, value)
            #    This is inside of the loop
            for move in allValidMoves:
                value = max(value, alphabeta(self.nextBoard(node, self.side, move), depth - 1, alpha, beta, False))
                if value >= beta:
                    break # beta cutoff
                alpha = max(alpha, value)
            return value
        # We are the minimizing player
        else:
            value = float("inf")
            # get possible moves for the node
            # Value = the min b/w value and a recursive call to the alpha beta:
            # alphabeta(child, depth - 1, alpha, beta, true)
            # beta = min(beta, value)
            for move in allValidMoves:
                value = min(value, alphabeta(self.nextBoard(node, self.opponent(self.side), move), depth - 1, alpha, beta, True))
                if value <= alpha:
                    break # alpha cutoff
                beta = min(alpha, value)
            return value
            

    def initialize(self, side):
        pass

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
        n = len(moves)
        if n == 0:
            return []
        else:
            bestMove = (-float("inf"), null)
            for move in moves:
                moveWeight = minimax(board, self.limit, -float("inf"), float("inf"), True)
                if (moveWeight >= bestMove[0])
                    bestMove[0] = moveWeight
                     bestMove[1] = move
            return bestMove[1]
                
    # 
    def eval(self, board):
        pass

game = Konane(8)
game.playOneGame(RandomPlayer(8), RandomPlayer(8), 1)

# game.playNGames(2, MinimaxPlayer(8, 2), MinimaxPlayer(8, 1), 0)