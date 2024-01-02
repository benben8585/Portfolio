import flappy
import numpy as np
import sys
from collections import defaultdict

rewardAlive = 1
rewardKill = -10000
alpha = 0.2
gamma = 0.9

Q = defaultdict(lambda: (0, 0))


def paramsToState(params):
    return str(params['playerVelY']) + "_" + str(params["playery"]) + "_" + \
        str(int(params["upperPipes"][0]['x'])) + "_" + str(int(params["upperPipes"][0]['y'])) + "_" + \
        str(int(params["upperPipes"][1]['x'])) + "_" + str(int(params["upperPipes"][1]['y']))


def onGameover(gameInfo):
    print(gameInfo)

def shouldEmulateKeyPress(params):
    state = paramsToState(params)

    estReward = Q[state]
    
    if estReward[0] >= estReward[1]:
        return False
    else:
        return True


flappy.main(shouldEmulateKeyPress, onGameover)