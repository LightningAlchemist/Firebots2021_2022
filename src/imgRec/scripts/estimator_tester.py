#!/usr/bin/env python 
import math
from std_msgs.msg import Bool, Float64, Float32
import numpy
import rospy


distanceThreshold = 10
redThreshold = 0.001
FPR = 0.1
FNR = 0.1

estimated_state = [0.5] * 2 # list of 100 locations with initial probability of 0.5
estimated_state[0] = 0.1
estimated_state[1] = 0.9
index_position = 0
position = 0
redscore1 = 0
current_redscore = 0;





def getRedScore(data):
    redscore1 = data.data

def decayBeleif():
    for idx, belief in enumerate(estimated_state):
        if belief > 0.5:
            estimated_state[idx] = 0.998 * belief
        else:
            estimated_state[idx] = max(0.01, 1.01 * belief)

def getNumberOfLeds(redScore):
    leds = (1009.615*redScore).asType(int)
    if leds > 23:
        led = 23
    return leds.asType(int)

def setIndexAblaze(i): #Register certain locations as on fire as long as within the index
    if i < 100 and i >= 0: 
        estimated_state[index_position] = ((1 - FNR) * estimated_state[index_position]) / \
                                    ((1 - FNR) * estimated_state[index_position] + FPR * (1 - estimated_state[index_position]))

def setIndexNotAblaze(i): #Register certain locations as not on fire as long as within the index
    if i < 100 and i >= 0:
        estimated_state[index_position] = (FNR * estimated_state[index_position]) / \
                                    ((1 - FPR) * (1-estimated_state[index_position]) + FPR * (estimated_state[index_position]))


def estimator():
    rospy.init_node('estimator_listener', anonymous=False)
    rospy.Subscriber('img_rec_line', Float32, getRedScore)
    
    current_redscore = redscore1
    if current_redscore > redThreshold:
        estimated_state[index_position] = ((1 - FNR) * estimated_state[index_position]) / \
                                    ((1 - FNR) * estimated_state[index_position] + FPR * (1 - estimated_state[index_position]))
    else:
        estimated_state[index_position] = (FNR * estimated_state[index_position]) / \
                                    ((1 - FPR) * (1-estimated_state[index_position]) + FPR * (estimated_state[index_position]))
    decayBeleif();
    print(estimated_state);
    



if __name__ == "__main__":
    while not rospy.is_shutdown():
        estimator();
        rospy.sleep(1)