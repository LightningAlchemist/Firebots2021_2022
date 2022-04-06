#!/usr/bin/env python

import numpy

distanceThreshold = 10
redThreshold = 0.03
FPR = 0.1
FNR = 0.1

estimated_state = [0.5] * 100  # list of 100 locations with initial probability of 0.5

index_position = 0
current_position = 0
last_position = 0


# TODO add subscriber code and rout to redscore
# TODO add subscriber code and rout to getPosition()

def getPosition():
    return current_position + 1 # TODO this is a stub


while True:
    # check if robot has moved to the next grid
    last_position = current_position
    current_position = getPosition()
    dif = current_position - last_position
    if abs(dif) > distanceThreshold:
        if numpy.sign(dif) == -1:
            index_position -= 1
        else:
            index_position += 1

    if redscore > redThreshold:
        estimated_state[index_position] = ((1 - FNR) * estimated_state[index_position]) / \
                                    ((1 - FNR) * estimated_state[index_position] + FPR * (1 - estimated_state[index_position]))
    else:
        estimated_state[index_position] = (FNR * estimated_state[index_position]) / \
                                    ((1 - FPR) * (1-estimated_state[index_position]) + FPR * (estimated_state[index_position]))

    for belief in estimated_state:
        if belief > 0.5:
            belief = 0.998 * belief
        else:
            belief = max(0.01, 1.01 * belief)