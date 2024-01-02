import flappy
import numpy as np

def onGameover(gameInfo):
    print(gameInfo)

def shouldEmulateKeyPress(params):
    # print(params)
    return np.random.choice([False, True], p=[0.9, 0.1])

flappy.main(shouldEmulateKeyPress, onGameover)