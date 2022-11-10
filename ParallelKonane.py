from konane import *
from MinimaxPlayer import *
from multiprocessing import Pool
import time

def playKonaneGame(player1, player2, boardSize, gameNumber):
    konaneGame = Konane(8)
    winner = konaneGame.playOneGame(player1, player2, False)
    result = "Game " + str(gameNumber) + " (" + player1.name + " vs " + player2.name + "): "
    if winner == 'B':
        result += player1.name + " wins"
    else:
        result += player2.name + " wins"
    return result

def playNGamesParallel(n, player1Func, player2Func, boardSize):
    pool = Pool(processes=n)
    resultBuffer = []
    for i in range(n):
        firstPlayer = player1Func() if i % 2 == 0 else player2Func()
        secondPlayer = player2Func() if i % 2 == 0 else player1Func()
        resultBuffer.append(pool.apply_async(playKonaneGame, [firstPlayer, secondPlayer, boardSize, i]))
    startTime = time.time()
    pool.close()
    pool.join()
    resultBuffer = [r.get() for r in resultBuffer]
    endTime = time.time()
    print()
    for i in range(len(resultBuffer)):
        print(resultBuffer[i])
    print("\nRun Time:", (endTime - startTime))
    
def createMinimaxPlayer(boardSize, depthCutoff):
    return lambda: MinimaxPlayer(boardSize, depthCutoff)

def createRandomPlayer(boardSize):
    return lambda: RandomPlayer(boardSize)

if __name__ == "__main__":
    playNGamesParallel(6, createMinimaxPlayer(8, 4), createRandomPlayer(8), 8)