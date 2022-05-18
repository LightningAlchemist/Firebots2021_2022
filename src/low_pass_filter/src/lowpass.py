#!/usr/bin/env python 
#from geometry_msgs import msg
import numpy
import rospy
import roslib
import math

from cv2 import sqrt
#mport tf2_py
from geometry_msgs.msg import Vector3
#from nav_msgs.msg import Odometry, OccupancyGrid
from std_msgs.msg import Bool, Float32, String, Float32MultiArray, Int16
#from nav_msgs.msg import Odometry
from localizer_dwm1001.msg import Tag
from math import pow, acos
#import tf2_geometry_msgs
#mport tf2_msgs
#import tf2_ros
#from tf import transformations

class LowPassFilter:

    #def current_milli_time():
    #    return round(time.time() * 1000)

    #Odometry coordinates are commented out
    #getting positions from decawave
    def getPosition(self, data):
        #print("\ndatax is: ")
		#print(data.x)
		#print("\ndatay is: ")
		#print(data.y)
        self.pose.x = data.x
        self.pose.y = data.y
    
    def __init__(self):        
        self.pose = Tag() # dwm1001/tag1
        rospy.init_node('lowpass_listener', anonymous=False)
        rospy.Subscriber('/dwm1001/tag', Tag, self.getPosition) # subscribe tag message
        self.pub_filtered_position = rospy.Publisher('filtered_pos', Vector3, queue_size=1)
        self.pub_initial_position = rospy.Publisher('initial_position', Vector3, queue_size=1)
        self.pub_rob_index = rospy.Publisher('rob_index', Int16, queue_size=1)

        # Filter coefficients 
        self.low_pass_filter = [-0.0053,-0.0028,0.0435,0.1695,0.2951,0.2951,0.1695,0.0435,-0.0028,-0.0053]; # low pass filter to time domain

        self.prev_pose_x = [0,0,0,0,0,0,0,0,0,0]; # ten previous x coodinates
        #self.prev_deriv_x = [0,0,0,0,0,0,0,0,0,0]; # ten x derivatives
        
        self.prev_pose_y = [0,0,0,0,0,0,0,0,0,0]; # ten previous y coodinates
        #self.prev_deriv_y = [0,0,0,0,0,0,0,0,0,0]; # ten y derivatives
        
        self.filtered_pose = Vector3() # difference between current and last position
        self.initial_pose = Vector3()

        self.filtered_pose.x = 0
        self.filtered_pose.y = 0
        self.filtered_pose.z = 1

        # slice_size = index size
        self.slice_size = 150
        self.led_length = 5.00
        self.index_distance = self.led_length / self.slice_size
        self.rob_index = 0
        self.count = 0

        self.initial_pose.x = self.filtered_pose.x
        self.initial_pose.y = self.filtered_pose.y
        self.initial_pose.z = self.filtered_pose.z

        self.pub_initial_position.publish(self.initial_pose)

    def main(self):
        # Shift sensor measurement array and add new value 
        # void *memcpy(void *dest, const void * src, size_t n)
        # copy prevDistVals[1] to prevDistVals[0]
        # memcpy(prevDistVals, &prevDistVals[1], sizeof(prevDistVals) - sizeof(float));
        self.count = self.count + 1

        if self.count == 20:
            self.initial_pose.x = self.filtered_pose.x
            self.initial_pose.y = self.filtered_pose.y
            self.initial_pose.z = self.filtered_pose.z

        self.prev_pose_x = self.prev_pose_x[1:] # remove the first element or del a[0], pop is not inefficient as it returns the item
        self.prev_pose_x.append(self.pose.x)

        self.prev_pose_y = self.prev_pose_y[1:]
        self.prev_pose_y.append(self.pose.y)
        
        # Multiply by filter coefficients to calculate filtered motor position 
        
        filtered_pose_x = 0
        filtered_pose_y = 0
        
        for i in range(10):
            filtered_pose_x += self.prev_pose_x[i] * self.low_pass_filter[i]
            filtered_pose_y += self.prev_pose_y[i] * self.low_pass_filter[i]

        self.filtered_pose.x = filtered_pose_x
        self.filtered_pose.y = filtered_pose_y
        
        self.rob_index = int(min(math.floor((self.filtered_pose.x - self.initial_pose.x) / self.index_distance), 149))

        self.pub_filtered_position.publish(self.filtered_pose)
        self.pub_rob_index.publish(self.rob_index)

if __name__ == "__main__":
    lowpassfilter = LowPassFilter()
    while not rospy.is_shutdown():
        #print('filtered: ', lowpassfilter.filtered_pose)
        print("current position x,y: {}, {}".format(lowpassfilter.filtered_pose.x, lowpassfilter.filtered_pose.y))
        print("initial position x,y: {}, {}".format(lowpassfilter.initial_pose.x, lowpassfilter.initial_pose.y))
        print("robot current index: ", lowpassfilter.rob_index)
        lowpassfilter.main()
        rospy.sleep(0.1)
