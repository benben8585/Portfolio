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
    return str(params['playerVelY']) + "_" + str(params["playery"]) + "_" + \
        str(int(params["upperPipes"][0]['x'])) + "_" + str(int(params["upperPipes"][0]['y'])) + "_" + \
        str(int(params["upperPipes"][1]['x'])) + "_" + str(int(params["upperPipes"][1]['y']))


def onGameover(gameInfo):
    print(gameInfo)

oldState = None
oldAction = None

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