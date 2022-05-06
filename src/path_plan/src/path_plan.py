#!/usr/bin/env python 
import numpy
import rospy
import roslib
import math

from cv2 import sqrt
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool, Float32, String, Float32MultiArray
#from nav_msgs.msg import Odometry
#from localizer_dwm1001.msg import Tag

class PathPlan:      
    
    def __init__(self):
        self.pose = Vector3() #filltered position 
        rospy.init_node('GoToPos', anonymous=True)
        self.rate = rospy.Rate(10) # 10hz  slows this down
        #rospy.Subscriber('odom', Odometry, self.getPosition)
        rospy.Subscriber('estimated_state', Float32MultiArray, self.getState) # subscribe tag message
        rospy.Subscriber('filtered_pos', Vector3, self.getPosition) # subscribe estimator message

        self.pub = rospy.Publisher('desired_position', Vector3, queue_size=10)
        
        self.des_pos = Vector3()
        self.offset = 0
        self.slice_size = 150
        self.led_length = 4.9022
        self.index_distance = self.led_length / self.slice_size
        self.entropy = [0] * self.slice_size
        self.desired_index = 0
        self.estate = Float32MultiArray()
        self.rob_index = min(math.floor(self.pose.x / self.index_distance), 149) #prevent out of bound
		
        #initialize desired postion = current position
        self.des_pos.z = self.pose.z
        self.des_pos.x = self.pose.x
        self.des_pos.y = self.pose.y

    def getState(self, data):
        #print("\ndatax is: ")
	#print(data.x)
	#print("\ndatay is: ")
	#print(data.y)
        self.estate.data = data.data 

    def getPosition(self, data):
        #print("\ndatax is: ")
	#print(data.x)
	#print("\ndatay is: ")
	#print(data.y)
        self.pose.x = data.x
        self.pose.y = data.y  

    def main(self):
        #Binary entropy calculation
        #rob_index is pose.x 
        #N = 150 <= index size
        
        #entropy = -est_state.*log2(est_state)-(1-est_state).*log2(1-est_state); 
        #for i in range(0, 149):
        for i in range(0, len(self.entropy)):
            print(len(self.estate.data))
            self.entropy[i] = -self.estate.data[i]*math.log2(self.estate.data[i])-(1-self.estate.data[i])*math.log2(1-self.estate.data[i])

        #Robot motion based on entropy - look 30 steps away (1 meter) 
        
        #ind1 = max(1,rob_index-30);
        ind1 = max(0,self.rob_index-30)
        #ind2 = min(N,rob_index+30);
        ind2 = min(self.slice_size-1,self.rob_index+30)
        entropy_left = 0
        entropy_right = 0
        #entropy_left = sum(entropy(ind1:(rob_index-1)));
        for i in range(ind1, self.rob_index-1):
            entropy_left = entropy_left + self.entropy[i]
        #entropy_right = sum(entropy((rob_index+1):ind2)); 
        for i in range(self.rob_index+1, ind2):
            entropy_right = entropy_right + self.entropy[i]
        
        #Note: Added bias to move towards center of map (this takes effect 
        #when entropy values are similar)      
        
        if self.rob_index > self.slice_size/2:
            if (entropy_left+3)>entropy_right:
                self.desired_index = max(0,self.rob_index-1)
            else:
                self.desired_index = min(self.slice_size-1,self.rob_index+1) 
        else:
            if entropy_left>(entropy_right+1.5): 
                self.desired_index = max(0,self.rob_index-1)
            else:
                self.desired_index = min(slice_size-1,rob_index+1) 
        
        self.des_pos.z = 0
        self.des_pos.x = self.desired_index * self.index_distance
        self.des_pos.y = self.pose.y
        
        #send position and print it
        rospy.loginfo(self.des_pos)
        pub.publish(self.des_pos)
        rate.sleep()        

if __name__ == "__main__":
    path_plan = PathPlan();
    while not rospy.is_shutdown():
        #print('desired position: ', pathplan.des_pos)
        path_plan.main()
        rospy.sleep(1)
