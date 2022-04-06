from geometry_msgs import msg
import roslib
import math
import tf2_py

from geometry_msgs.msg import PoseStamped, Twist, Vector3, TransformStamped
from nav_msgs.msg import Odometry, OccupancyGrid
from std_msgs.msg import Bool, Float64, Float32

import tf2_geometry_msgs
import tf2_msgs
import tf2_ros
from tf import transformations


import numpy
import rospy


distanceThreshold = 10
redThreshold = 0.001
FPR = 0.1
FNR = 0.1

estimated_state = [0.5] * 100  # list of 100 locations with initial probability of 0.5

index_position = 0
current_position = 0
last_position = 0

startX = 0;
startY = 0;

end_x = 0;
end__y = 0;

current_redscore = 0;


def getPosition(location): #get position from DecaWave topic Distance from starting position
    coordinates = location.data
    position = ((coordinates[0]-startX)^2 + (coordinates[1] - startY)^2)**(0.5);
    return position; 


def getRedScore(redScore):
    return redScore.data

def decayBeleif():
    for belief in estimated_state:
        if belief > 0.5:
            belief = 0.998 * belief
        else:
            belief = max(0.01, 1.01 * belief)

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
    rospy.init_node('Estimator Listener', anonymous=False)
    odom_pos = {};
    rospy.init_node('img_print', anonymous=True)
    rospy.Subscriber('img_rec_line', Float32, getRedScore);
    rospy.init_node('/nav_msgs/Odometry', anonymous=True)
    rospy.Subscriber('odom_position_labled', odom_pos, getPosition);
    current_redscore = getRedScore()
    last_position = current_position
    current_position = getPosition()
    dif = current_position - last_position
    if abs(dif) >= distanceThreshold:
        last_position = current_position - (dif - distanceThreshold)
        if numpy.sign(dif) == -1:
            index_position -= 1
        else:
            index_position += 1
    
    if current_redscore > redThreshold:
        estimated_state[index_position] = ((1 - FNR) * estimated_state[index_position]) / \
                                    ((1 - FNR) * estimated_state[index_position] + FPR * (1 - estimated_state[index_position]))
    else:
        estimated_state[index_position] = (FNR * estimated_state[index_position]) / \
                                    ((1 - FPR) * (1-estimated_state[index_position]) + FPR * (estimated_state[index_position]))
    decayBeleif();
    print(estimated_state);
    rospy.spin();


if __name__ == "__main__":
    estimator();