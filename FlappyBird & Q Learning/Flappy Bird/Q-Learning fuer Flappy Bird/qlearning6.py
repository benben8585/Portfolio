import flappy
import numpy as np
import sys
from collections import defaultdict

rewardAlive = 1
rewardKill = -10000
alpha = 0.2
gamma = 0.9

# Q[state] = (Nicht springen, springen)
Q = defaultdict(lambda: [0, 0])


def paramsToState(params):
    playerVelY = params['playerVelY']
    playery = round(params["playery"] / 10) * 10

    if int(params["upperPipes"][0]['x']) < 56:
        index = 1
    else: 
        index = 0

    upperPipeX = round(int(params["upperPipes"][index]['x']) / 10) * 10
    upperPipeY = round(int(params["upperPipes"][index]['y']) / 10) * 10

    return str(playerVelY) + "_" + str(playery) + "_" + str(upperPipeX) + "_" + str(upperPipeY)

oldState = None
oldAction = None

def onGameover(gameInfo):
    global oldState
    global oldAction

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

    print(Q)


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