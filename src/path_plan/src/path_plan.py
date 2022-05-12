#!/usr/bin/env python 
import numpy as np
import rospy
import roslib
import math

from cv2 import sqrt
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool, Float32, String, Float32MultiArray


# from nav_msgs.msg import Odometry
# from localizer_dwm1001.msg import Tag

class PathPlan:

    def __init__(self):
        self.pose = Vector3()  # filltered position
        rospy.init_node('GoToPos', anonymous=True)
        # rospy.Subscriber('odom', Odometry, self.getPosition)
        rospy.Subscriber('estimated_state', Float32MultiArray, self.getState)  # subscribe tag message
        rospy.Subscriber('filtered_pos', Vector3, self.getPosition)  # subscribe estimator message

        self.pub_desired_position = rospy.Publisher('c', Vector3, queue_size=1)
        self.pub_entropy = rospy.Publisher('entropy', Float32MultiArray, queue_size=1)

        self.des_pos = Vector3()
        self.offset = 0.71
        self.slice_size = 150
        self.led_length = 4.9022
        self.index_distance = self.led_length / self.slice_size
        # self.entropy = [0] * self.slice_size
        self.entropy = np.zeros((self.slice_size))
        self.desired_index = 0
        self.estate = Float32MultiArray()
        self.rob_index = 0

        # initialize desired postion = current position
        self.des_pos.z = self.pose.z
        self.des_pos.x = self.pose.x
        while(not self.pose.y):
            continue
        self.des_pos.y = self.pose.y

    def getState(self, data):
        self.estate.data = data.data

    def getPosition(self, data):
        self.pose.x = data.x
        self.pose.y = data.y

    def main(self):
        # Binary entropy calculation
        # entropy = -est_state.*log2(est_state)-(1-est_state).*log2(1-est_state); <= matlab code
        # entropy is max at 1 when estate is 0.5 => rate of decrement increases as estate decrease

        self.rob_index = int(
            min(math.floor((self.pose.x - self.offset) / self.index_distance), 149))  # prevent out of bound, rob_index is pose.x
        for i in range(0, self.slice_size):
            if (len(self.estate.data) != 0):  # take some time to sync
                est_state = self.estate.data[i]
                est_state_not = 1 - est_state
                self.entropy[i] = -est_state * math.log(est_state, 2.0) - (est_state_not) * math.log(est_state_not, 2.0)

        # Robot motion based on entropy - look 30 steps away (1 meter)
        # ind1 = max(1,self.rob_index-30);
        ind1 = max(0, self.rob_index - 30)
        # ind2 = min(self.slice_size,self.rob_index+30);
        ind2 = min(self.slice_size - 1, self.rob_index + 30)
        entropy_left = 0
        entropy_right = 0
        # entropy_left = sum(self.entropy(ind1:self.rob_index-1));
        # get the sum of entropy between the indices
        entropy_left = np.sum(self.entropy[int(ind1):int(self.rob_index - 1)])
        print('left total',entropy_left, ind1, self.rob_index)
        # entropy_right = sum(entropy((rob_index+1):ind2));
        # get the sum of entropy between the indices
        entropy_right = np.sum(self.entropy[int(self.rob_index + 1):int(ind2)])
        print('right total',entropy_right, self.rob_index, ind2)

        # Note: Added bias to move towards center of map (this takes effect
        # when entropy values are similar)

        if self.rob_index > self.slice_size / 2:
            if (entropy_left + 3) > entropy_right:
            #if entropy_left > entropy_right:
                #self.desired_index = max(0, self.rob_index - 1)
                self.desired_index = 0
            else:
                #self.desired_index = min(self.slice_size - 1, self.rob_index + 1)
                self.desired_index = 149
        else:
            if entropy_left > (entropy_right + 1.5):
            #if entropy_left > entropy_right:
                #self.desired_index = max(0, self.rob_index - 1)
                self.desired_index = 0
            else:
                #self.desired_index = min(self.slice_size - 1, self.rob_index + 1)
                self.desired_index = 149

        #print('entropy: ', self.rob_index)

        self.des_pos.z = 0
        self.des_pos.x = float(self.desired_index * self.index_distance + self.offset)
        #self.des_pos.y = self.pose.y
        
        #send position and print it
	    #rospy.loginfo(self.pose)        
	    #rospy.loginfo(self.des_pos)
        #pub_entropy = Float32MultiArray()
        #pub_entropy = self.entropy

        self.pub_desired_position.publish(self.des_pos)    
        #self.pub_entropy.publish(pub_entropy) 

if __name__ == "__main__":
    path_plan = PathPlan();
    while not rospy.is_shutdown():
        #print('current position: ', path_plan.pose)
        #print('desired position: ', path_plan.des_pos)
        # print('subscribed state: ', path_plan.estate.data)
        print('entropy: ', path_plan.entropy)
        path_plan.main()
        rospy.sleep(2)  # 10Hz
