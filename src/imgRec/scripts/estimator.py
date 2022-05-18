#!/usr/bin/env python 
#from geometry_msgs import msg
import numpy
import rospy
import roslib
import math
import rosbag

from cv2 import sqrt
#mport tf2_py
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool, Float32, String, Float32MultiArray
from localizer_dwm1001.msg import Tag
from math import floor, pow, acos

class Estimator:
    def getRedScore(self, data):
        self.redScore = data.data

    def getPosition(self, data):
        self.index_position = data.data

    def __init__(self):
        rospy.init_node('estimator_listener', anonymous=False)
        rospy.Subscriber('img_rec_line', Float32, self.getRedScore)
        rospy.Subscriber('rob_index', int, self.getPosition) # subscribe tag message

        self.pub = rospy.Publisher('estimated_state', Float32MultiArray, queue_size=5)

        self.distanceThreshold = 4.9022/150  # The linear travel distance that constitutes a move to another grid
        self.redThreshold = 0.0005  # the threshold to determine if the grid is on fire
        self.FPR = 0.1  # false positive rate
        self.FNR = 0.1  # false negative rate
        self.num_locations = 150
        self.estimated_state = [0.5] * self.num_locations  # list of 100 locations with initial probability of 0.5

        self.index_position = 0  # linear index position to left end of strip
        self.view_width = 5 # the number of indexes to the left and right of the position that are updated
        self.redScore = 0
        self.decayRate = 0.99

        # spinlock to block until the position is updated once through subscriber
        while not self.index_position:
            continue


    def decayBelief(self):
        # Decays the belief P(Fire_i(time=t)) based on current belief, the average belief of the the neighboring locations, and a decay rate.
        #  Equation is: P(F_i(t+1)) = decayRate*P(F_i(t)) + (1-decayRate)*(.5*P(F_i-1(t)) + .5*P(F_i+1(t)))

        previous_belief = self.estimated_state.copy()   # deep copy of current belief at time = t
        for idx, belief in enumerate(self.estimated_state):
            if(idx == 0):   # edge case: at left boundary
                self.estimated_state[idx] = self.decayRate*previous_belief[idx] + (1-self.decayRate)*( previous_belief[idx+1])
            elif(idx == self.num_locations-1):  # edge case: at right boundary
                self.estimated_state[idx] = self.decayRate*previous_belief[idx] + (1-self.decayRate)*( previous_belief[idx-1])
            else:
                self.estimated_state[idx] = self.decayRate*previous_belief[idx] + (1-self.decayRate)*(.5*(previous_belief[idx-1] + previous_belief[idx+1]))


    def main(self):
        # check if robot has moved to the next grid
        # get the position of the robot. if the difference between the new and old positions exceed
        #  the distance threshold, update the old position to the current position and update the
        #  linear index for the belief matrix

        # force the index to be bounded between 0 and num_locations to prevent out-of-bounds errors.
        #   preemptively raise an exception if something fuckity happens to help with back-tracing.
        if(self.index_position < 0):
            self.index_position = 0;
        elif(self.index_position > self.num_locations):
            self.index_position = self.num_locations-1
        # print('index_pos: ', self.index_position)
        if self.index_position<0 or self.index_position > self.num_locations:
            raise IndexError('Robot out of bounds!')

        # set dynamic bounds to the left and right of the central position based on the view_width parameter
        #   ie., ensure that the "view width" doesn't cause an out-of-bounds error.
        leftBound = self.index_position - self.view_width
        if leftBound < 0:
            leftBound = 0
        rightBound = self.index_position + self.view_width
        if rightBound > (self.num_locations - 1):
            rightBound = self.num_locations - 1
        viewArea = range(leftBound, rightBound + 1)

        # get the redscore and check against the threshold. If above threshold, update belief that there is
        #  a fire at the current location in the belief matrix. Otherwise, update that there is no fire.
        #  do this for all locations within the view area bounds itteratively.
        for index in viewArea:
            e_state = self.estimated_state[index]
            if self.redScore > self.redThreshold:
                self.estimated_state[index] = ((1 - self.FNR) * e_state) / ((1 - self.FNR) * e_state + self.FPR * (1 - e_state))
            else:
                self.estimated_state[index] = (self.FNR * e_state) / ((1 - self.FPR) * (1 - e_state) + self.FPR * e_state)

        # the belief at each index in the belief matrix tends towards 0.5 (maximum uncertainty)
        self.decayBelief()
        pubdata = Float32MultiArray()
        pubdata.data = self.estimated_state
        self.pub.publish(pubdata)
        #self.bag.write('state', pubdata)
        #print(self.estimated_state).


if __name__ == "__main__":
    estimator = Estimator();
    while not rospy.is_shutdown():
        print('est state: ', estimator.estimated_state)
        #print("last position x,y: {}, {}".format(estimator.last_pose.x, estimator.last_pose.y))
        print("current position x,y: {}, {}".format(estimator.pose.x, estimator.pose.y))
        estimator.main()
        rospy.sleep(1)
