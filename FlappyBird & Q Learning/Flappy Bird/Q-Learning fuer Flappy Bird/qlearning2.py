import flappy
import numpy as np
import sys

rewardAlive = 1
rewardKill = -10000
alpha = 0.2
gamma = 0.9

Q = {}

def paramsToState(params):
    return str(params['playerVelY']) + "_" + str(params["playery"]) + "_" + \
        str(int(params["upperPipes"][0]['x'])) + "_" + str(int(params["upperPipes"][0]['y'])) + "_" + \
        str(int(params["upperPipes"][1]['x'])) + "_" + str(int(params["upperPipes"][1]['y']))

print(paramsToState({'playerVelY': 0, 'playery': 156, 'upperPipes': [{'x': 400, 'y': -189}, {'x': 544.0, 'y': -147}], 'lowerPipes': [{'x': 400, 'y': 231}, {'x': 544.0, 'y': 273}]}))
sys.exit()


def onGameover(gameInfo):
    print(gameInfo)

def shouldEmulateKeyPress(params):
    print(params)
    return np.random.choice([False, True], p=[0.9, 0.1])

flappy.main(shouldEmulateKeyPress, onGameover)