import flappy
import numpy as np
import sys
from collections import defaultdict
import pickle

rewardAlive = 1
rewardKill = -10000
alpha = 0.1
gamma = 1

# Q[state] = (Nicht springen, springen)
Q = None # defaultdict(lambda: [0, 0])

with open("Q.pickle", "rb") as file:
    Q = defaultdict(lambda: [0, 0], pickle.load(file))

def paramsToState(params):
    playerVelY = params['playerVelY']
    playery = params["playery"]

    if int(params["upperPipes"][0]['x']) < 40:
        index = 1
    else: 
        index = 0

    upperPipeX = round(int(params["upperPipes"][index]['x']) / 3) * 3
    upperPipeY = int(params["upperPipes"][index]['y'])

    yDiff = round((playery - upperPipeY) / 3) * 3

    return str(playerVelY) + "_" + str(yDiff) + "_" + str(upperPipeX)

oldState = None
oldAction = None
gameCounter = 0
gameScores = []

def onGameover(gameInfo):
    global oldState
    global oldAction
    global gameCounter
    global gameScores

    gameScores.append(gameInfo['score'])

    if gameCounter % 100 == 0:
        print(str(gameCounter) + ": " + str(np.mean(gameScores[-100:])))

    # Q updaten für die vorherige Aktion
    #  -> Die vorherige Aktion war nicht erfolgreich!
    prevReward = Q[oldState]
    index = None
    if oldAction == False:
        index = 0
    else: 
        index = 1
    
    prevReward[index] = (1 - alpha) * prevReward[index] + \
        alpha * rewardKill
    Q[oldState] = prevReward

    oldState = None
    oldAction = None

    #if gameCounter % 10000 == 0:
    #    with open("Q/qlearning10_" + str(gameCounter) + ".pickle", "wb") as file:
    #        pickle.dump(dict(Q), file)

    gameCounter+=1


def shouldEmulateKeyPress(params):
    global oldState
    global oldAction

    state = paramsToState(params)
    estReward = Q[state]


    # Q updaten für die vorherige Aktion
    #  -> Die vorherige Aktion war erfolgreich!
    prevReward = Q[oldState]
    index = None
    if oldAction == False:
        index = 0
    else: 
        index = 1
    
    prevReward[index] = (1 - alpha) * prevReward[index] + \
        alpha * (rewardAlive + gamma * max(estReward))
    Q[oldState] = prevReward
    
    oldState = state
    if estReward[0] >= estReward[1]:
        oldAction = False
        return False
    else:
        oldAction = True
        return True


flappy.main(shouldEmulateKeyPress, onGameover)