from konane import *
from MinimaxPlayer import *
from vvvPlayer import *
from hhhPlayer import *
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
    
def createvvvPlayer(boardSize, depthCutoff):
    return lambda: vvvPlayer(boardSize, depthCutoff)
    
def createhhhPlayer(boardSize, depthCutoff):
    return lambda: hhhPlayer(boardSize, depthCutoff)

def createRandomPlayer(boardSize):
    return lambda: RandomPlayer(boardSize)

if __name__ == "__main__":
    # All of these tests take about 4 minutes on my computer
    # Serially, 10 games of hhh vs vvv takes about 3.33 minutes on my computer
    startTime = time.time()
    playNGamesParallel(10, createMinimaxPlayer(8, 4), createhhhPlayer(8, 4), 8)
    playNGamesParallel(10, createMinimaxPlayer(8, 4), createvvvPlayer(8, 4), 8)
    playNGamesParallel(10, createMinimaxPlayer(8, 4), createRandomPlayer(8), 8)

    playNGamesParallel(10, createvvvPlayer(8, 4), createhhhPlayer(8, 4), 8)
    playNGamesParallel(10, createvvvPlayer(8, 4), createRandomPlayer(8), 8)

    playNGamesParallel(10, createhhhPlayer(8, 4), createRandomPlayer(8), 8)
    print("All tests took", (time.time() - startTime), "second(s)")